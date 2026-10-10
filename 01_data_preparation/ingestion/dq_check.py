import os
import duckdb
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "data", "processed", "ecommerce.duckdb")
REPORT_PATH = os.path.join(os.path.dirname(__file__), "dq_report.md")

EXPECTED_COLS = [
    "event_time", "event_type", "product_id", "category_id",
    "category_code", "brand", "price", "user_id", "user_session",
]
VALID_EVENT_TYPES = {"view", "cart", "remove_from_cart", "purchase"}

def scalar(conn, sql):
    return conn.execute(sql).fetchone()[0]

def main():
    print("Khởi động dq_check.py với Memory Limit 2GB...")
    conn = duckdb.connect(DB_PATH, read_only=True)
    # Tối ưu RAM nghiêm ngặt cho DQ Check
    conn.execute("PRAGMA memory_limit='2GB'")
    conn.execute("PRAGMA threads=2")
    conn.execute("PRAGMA temp_directory='/tmp/duckdb_spill'")
    
    lines = [
        f"# Data Quality Report",
        f"**Generated:** {datetime.now().isoformat(timespec='seconds')}",
        f"**Source:** `{DB_PATH}`",
        "",
    ]

    print("1. Đang đếm Row Count...")
    total = scalar(conn, "SELECT COUNT(*) FROM events")
    lines += [
        "## 1. Row Count",
        f"| Metric | Value |",
        f"|---|---|",
        f"| Total rows | {total:,} |",
    ]
    for ev in VALID_EVENT_TYPES:
        n = scalar(conn, f"SELECT COUNT(*) FROM events WHERE event_type = '{ev}'")
        lines.append(f"| {ev} | {n:,} |")
    lines.append("")

    print("2. Đang kiểm tra Timestamp...")
    ts = conn.execute("SELECT MIN(event_time), MAX(event_time) FROM events").fetchone()
    lines += [
        "## 2. Timestamp Range",
        f"| | Value |",
        f"|---|---|",
        f"| Min event_time | {ts[0]} |",
        f"| Max event_time | {ts[1]} |",
        "",
    ]

    print("3. Đang tính Null Rates...")
    lines += ["## 3. Null Rates", "| Column | Null Count | Null % |", "|---|---|---|"]
    for col in EXPECTED_COLS:
        null_n = scalar(conn, f"SELECT COUNT(*) FROM events WHERE {col} IS NULL")
        pct = null_n / total * 100
        lines.append(f"| {col} | {null_n:,} | {pct:.2f}% |")
    lines.append("")

    print("4. Tính Duplicate Events (theo từng tháng để tránh OOM)...")
    # Tách chunk theo tháng để tính duplicate an toàn
    months = ['2019-10', '2019-11']
    total_dup = 0
    for m in months:
        dup = scalar(conn, f"""
            SELECT sum(n) FROM (
                SELECT COUNT(*) AS n
                FROM events
                WHERE event_time >= '{m}-01' AND event_time < '{m}-01'::DATE + INTERVAL 1 MONTH
                GROUP BY user_session, event_type, event_time
                HAVING n > 1
            )
        """)
        total_dup += (dup or 0)
        
    lines += [
        "## 4. Duplicate Events",
        f"| Metric | Value |",
        f"|---|---|",
        f"| Duplicate (session+type+time) groups | {total_dup:,} |",
        "",
    ]

    print("5. Phân tích Outliers của Price...")
    price_stats = conn.execute("""
        SELECT
            MIN(price)  AS min_price,
            MAX(price)  AS max_price,
            AVG(price)  AS avg_price,
            APPROX_QUANTILE(price, 0.5) AS median_price,
            COUNT(*) FILTER (WHERE price <= 0)  AS zero_or_neg,
            COUNT(*) FILTER (WHERE price > 5000) AS over_5000
        FROM events WHERE event_type IN ('cart','purchase')
    """).fetchone()
    lines += [
        "## 5. Price Outliers (cart + purchase events only)",
        f"| Metric | Value |",
        f"|---|---|",
        f"| Min price | {price_stats[0]:.2f} |",
        f"| Max price | {price_stats[1]:.2f} |",
        f"| Avg price | {price_stats[2]:.2f} |",
        f"| Median price | {price_stats[3]:.2f} |",
        f"| Zero or negative | {price_stats[4]:,} |",
        f"| Over $5000 | {price_stats[5]:,} |",
        "",
    ]

    print("6. Đếm Unique (Dùng APPROX_COUNT_DISTINCT)...")
    uniq = conn.execute("""
        SELECT
            APPROX_COUNT_DISTINCT(user_id)      AS users,
            APPROX_COUNT_DISTINCT(user_session) AS sessions,
            APPROX_COUNT_DISTINCT(product_id)   AS products,
            APPROX_COUNT_DISTINCT(brand)        AS brands,
            COUNT(DISTINCT date_trunc('month', event_time)) AS months
        FROM events
    """).fetchone()
    lines += [
        "## 6. Unique Counts (Approximate)",
        f"| Dimension | Count |",
        f"|---|---|",
        f"| Users (Approx) | {uniq[0]:,} |",
        f"| Sessions (Approx) | {uniq[1]:,} |",
        f"| Products (Approx)| {uniq[2]:,} |",
        f"| Brands (Approx)  | {uniq[3]:,} |",
        f"| Months | {uniq[4]} |",
        "",
    ]

    print("7. Đang kiểm tra Invalid Events...")
    invalid_ev = scalar(conn, f"""
        SELECT COUNT(*) FROM events
        WHERE event_type NOT IN ('view','cart','remove_from_cart','purchase')
    """)
    lines += [
        "## 7. Invalid Event Types",
        f"| Metric | Value |",
        f"|---|---|",
        f"| Invalid event_type rows | {invalid_ev:,} |",
        "",
    ]

    conn.close()
    report = "\n".join(lines)
    with open(REPORT_PATH, "w") as f:
        f.write(report)
    print(f"\n✅ Data Quality Report đã được lưu tại {REPORT_PATH}")

if __name__ == "__main__":
    main()
