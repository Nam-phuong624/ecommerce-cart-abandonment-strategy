import duckdb
import time
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "processed", "ecommerce.duckdb")

con = duckdb.connect(DB_PATH, read_only=True)
print(f"Connected to {DB_PATH}")

t0 = time.time()
res = con.execute("SELECT COUNT(*), SUM(purchase_value) FROM fct_session_funnel").fetchone()
t1 = time.time()

print(f"Rows in fct_session_funnel: {res[0]:,}")
print(f"Total Purchase Value: ${res[1]:,.2f}")
print(f"Query Runtime: {t1 - t0:.4f} seconds")

# Lấy dung lượng DB
db_size = os.path.getsize(DB_PATH) / (1024**3)
print(f"Database file size: {db_size:.2f} GB")

