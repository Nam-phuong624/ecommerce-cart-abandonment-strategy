"""
Ingest REES46 CSV files into DuckDB.
Usage:
    python ingest_rees46.py          # full run (all 5 files)
    python ingest_rees46.py --test   # dry-run on 2019-Dec.csv only
"""
import sys
import os
import time
import psutil
import duckdb

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
DB_PATH = os.path.join(BASE_DIR, "data", "processed", "ecommerce.duckdb")

ALL_FILES = [
    "2019-Oct.csv",
    "2019-Nov.csv",
    "2019-Dec.csv",
    "2020-Jan.csv",
    "2020-Feb.csv",
]
TEST_FILES = ["2019-Dec.csv"]  # smallest


def ram_mb():
    return psutil.Process().memory_info().rss / 1024 / 1024


def check_ram(label, limit_gb=4):
    mb = ram_mb()
    print(f"  RAM [{label}]: {mb:.0f} MB")
    if mb > limit_gb * 1024:
        raise MemoryError(f"RAM exceeded {limit_gb}GB at step: {label}")
    return mb


def source_row_count(csv_path):
    """Fast row count from CSV without loading into Python."""
    conn = duckdb.connect(":memory:")
    result = conn.execute(
        f"SELECT COUNT(*) FROM read_csv_auto('{csv_path}', HEADER=TRUE)"
    ).fetchone()[0]
    conn.close()
    return result


def ingest(files, db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = duckdb.connect(db_path)
    conn.execute("PRAGMA memory_limit='4GB'")
    conn.execute("PRAGMA threads=4")

    check_ram("startup")

    # Schema creation (empty table)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS raw_events (
            event_time      TIMESTAMPTZ,
            event_type      VARCHAR,
            product_id      INTEGER,
            category_id     BIGINT,
            category_code   VARCHAR,
            brand           VARCHAR,
            price           DOUBLE,
            user_id         BIGINT,
            user_session    VARCHAR,
            event_date      DATE,
            event_month     DATE,
            event_hour      TINYINT,
            day_of_week     TINYINT
        )
    """)

    total_loaded = 0
    for fname in files:
        fpath = os.path.join(RAW_DIR, fname)
        t0 = time.time()
        print(f"\n→ Ingesting {fname}...")

        src_count = source_row_count(fpath)
        print(f"  Source rows: {src_count:,}")

        conn.execute(f"""
            INSERT INTO raw_events
            SELECT
                CAST(event_time AS TIMESTAMPTZ)             AS event_time,
                event_type,
                CAST(product_id AS INTEGER)                 AS product_id,
                CAST(category_id AS BIGINT)                 AS category_id,
                category_code,
                brand,
                CAST(price AS DOUBLE)                       AS price,
                CAST(user_id AS BIGINT)                     AS user_id,
                user_session,
                CAST(event_time AS DATE)                    AS event_date,
                DATE_TRUNC('month', CAST(event_time AS TIMESTAMPTZ))::DATE AS event_month,
                CAST(EXTRACT(HOUR FROM CAST(event_time AS TIMESTAMPTZ)) AS TINYINT) AS event_hour,
                CAST(DAYOFWEEK(CAST(event_time AS TIMESTAMPTZ)) AS TINYINT) AS day_of_week
            FROM read_csv_auto('{fpath}', HEADER=TRUE, NULLSTR='')
        """)

        loaded = conn.execute(
            "SELECT COUNT(*) FROM raw_events"
        ).fetchone()[0] - total_loaded

        if loaded != src_count:
            conn.close()
            raise ValueError(
                f"Row count mismatch for {fname}: source={src_count:,}, loaded={loaded:,}"
            )

        total_loaded += loaded
        elapsed = time.time() - t0
        peak = check_ram(fname)
        print(f"  Loaded: {loaded:,} rows in {elapsed:.1f}s | RAM peak: {peak:.0f} MB")

    print(f"\n→ Creating indexes...")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_event_date    ON raw_events(event_date)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_user_session  ON raw_events(user_session)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_user_id       ON raw_events(user_id)")

    final_count = conn.execute("SELECT COUNT(*) FROM raw_events").fetchone()[0]
    db_size_mb = os.path.getsize(db_path) / 1024 / 1024

    print(f"\n{'='*50}")
    print(f"INGESTION COMPLETE")
    print(f"  Total rows: {final_count:,}")
    print(f"  DB size:    {db_size_mb:.0f} MB")
    print(f"  RAM peak:   {check_ram('final'):.0f} MB")
    print(f"{'='*50}")

    conn.close()
    return final_count


if __name__ == "__main__":
    test_mode = "--test" in sys.argv
    files = TEST_FILES if test_mode else ALL_FILES
    mode = "DRY-RUN (Dec only)" if test_mode else "FULL RUN (5 files)"
    print(f"REES46 Ingestion — {mode}")
    ingest(files, DB_PATH)
