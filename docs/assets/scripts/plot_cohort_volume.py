import duckdb
import matplotlib.pyplot as plt
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, '../../../data/processed/ecommerce.duckdb')
output_path = os.path.join(current_dir, '../images/cohort_volume.png')

query = """
WITH user_history AS (
    SELECT user_id, MIN(first_event_date) as first_seen_date,
        SUM(CASE WHEN first_event_date < '2019-11-11' THEN has_cart::INT ELSE 0 END) as hist_carts,
        SUM(CASE WHEN first_event_date < '2019-11-11' THEN has_purchase::INT ELSE 0 END) as hist_purchases
    FROM fct_session_funnel GROUP BY user_id
),
cohort_classification AS (
    SELECT CASE
            WHEN u.hist_purchases > 0 AND u.hist_carts = 0 THEN 'VIPs\n(Direct Native)'
            WHEN (u.hist_carts > 0 OR u.hist_purchases > 0) THEN 'Chronic Shoppers'
            WHEN u.first_seen_date >= '2019-11-11' THEN 'New Users'
        END AS cohort
    FROM fct_session_funnel f JOIN user_history u ON f.user_id = u.user_id
    WHERE f.first_event_date >= '2019-11-11' AND f.has_cart = TRUE AND f.has_purchase = FALSE
)
SELECT cohort, COUNT(*) as volume FROM cohort_classification WHERE cohort IS NOT NULL GROUP BY 1 ORDER BY 1;
"""

con = duckdb.connect(db_path, read_only=True)
df = con.execute(query).df()
con.close()

# Dữ liệu vẽ biểu đồ
cohorts = df["cohort"].tolist()
volumes = df["volume"].tolist()
colors = ["#ff7f0e", "#1f77b4", "#d62728"]

fig, ax = plt.subplots(figsize=(8, 6))

# Vẽ Pie Chart (đã bỏ width=0.4 và thêm pctdistance để căn chỉnh nhãn đẹp hơn)
wedges, texts, autotexts = ax.pie(
    volumes,
    labels=cohorts,
    autopct="",
    startangle=140,
    colors=colors,
    pctdistance=0.65,  # Đưa text vào khoảng 65% bán kính từ tâm
    wedgeprops=dict(edgecolor="w", linewidth=1.5),
    textprops={"fontsize": 12, "fontweight": "bold"},
)

# Tùy chỉnh text (Hiển thị % và K volume)
total = sum(volumes)
for i, a in enumerate(autotexts):
    a.set_text(f"{volumes[i]/1000:.1f}K\n({volumes[i]/total*100:.1f}%)")
    a.set_color("white")
    a.set_fontsize(11)

ax.set_title(
    "Tỷ lệ rớt phễu Black Friday theo từng nhóm", fontweight="bold", pad=20, fontsize=14
)
plt.tight_layout()
plt.savefig(output_path, dpi=300)
print(f"Lưu thành công biểu đồ Pie: {output_path}")
