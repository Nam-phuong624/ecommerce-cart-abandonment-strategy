import duckdb
import os
import psutil
import glob

def check_memory():
    # Kiểm tra RAM Python process (<3GB)
    process = psutil.Process(os.getpid())
    mem_usage_gb = process.memory_info().rss / (1024 ** 3)
    if mem_usage_gb > 3.0:
        raise MemoryError(f"FAIL-FAST: Python RAM vượt quá 3GB ({mem_usage_gb:.2f}GB)")
        
    # Kiểm tra kích thước temp_directory (<20GB)
    temp_dir = '/tmp/duckdb_spill'
    if os.path.exists(temp_dir):
        total_size = sum(os.path.getsize(os.path.join(dirpath, f)) for dirpath, _, filenames in os.walk(temp_dir) for f in filenames)
        total_size_gb = total_size / (1024 ** 3)
        if total_size_gb > 20.0:
            raise MemoryError(f"FAIL-FAST: DuckDB Temp Dir vượt quá 20GB ({total_size_gb:.2f}GB)")

def main():
    # Khởi tạo thư mục spill
    os.makedirs('/tmp/duckdb_spill', exist_ok=True)
    
    # Path setup
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    db_path = os.path.join(base_dir, 'data', 'processed', 'ecommerce.duckdb')
    raw_data_dir = os.path.join(base_dir, 'data', 'raw')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Kết nối DuckDB
    con = duckdb.connect(db_path)
    
    # 1. Cấu hình NGHIÊM NGẶT
    print("Thiết lập cấu hình DuckDB Memory-Safe...")
    con.execute("PRAGMA memory_limit='2GB';")
    con.execute("PRAGMA threads=4;")
    con.execute("PRAGMA temp_directory='/tmp/duckdb_spill';")
    con.execute("PRAGMA preserve_insertion_order=false;")
    
    con.execute("DROP TABLE IF EXISTS events;")
    con.execute("""
        CREATE TABLE events (
            event_time TIMESTAMP,
            event_type VARCHAR,
            product_id BIGINT,
            category_id BIGINT,
            category_code VARCHAR,
            brand VARCHAR,
            price DOUBLE,
            user_id BIGINT,
            user_session VARCHAR
        )
    """)
    
    # Lấy danh sách các file CSV theo tháng
    csv_files = sorted(glob.glob(os.path.join(raw_data_dir, '20*.csv')))
    if not csv_files:
        print("Không tìm thấy file CSV nào khớp mẫu 20*.csv")
        return

    # 3. Transform có checkpoint (partition theo tháng)
    print(f"Bắt đầu Ingest {len(csv_files)} tháng dữ liệu...")
    total_rows = 0
    
    for file_path in csv_files:
        month_name = os.path.basename(file_path)
        print(f"Đang xử lý tháng: {month_name}")
        
        # Ingest file hiện tại theo pattern streaming
        con.execute(f"""
            INSERT INTO events
            SELECT * FROM read_csv_auto('{file_path}', header=True)
        """)
        
        # Lấy số rows vừa ingest
        res = con.execute("SELECT count(*) FROM events").fetchone()[0]
        added = res - total_rows
        total_rows = res
        print(f"  -> Ingested {added:,} rows. Tổng cộng: {total_rows:,} rows.")
        
        # Flush WAL sau mỗi tháng
        con.execute("CHECKPOINT;")
        print("  -> CHECKPOINT hoàn tất.")
        
        # Dự phòng fail-fast
        check_memory()

    print("\nQuá trình Ingestion Hoàn Tất!")
    print(f"Tổng số bản ghi trong bảng events: {total_rows:,}")

if __name__ == "__main__":
    main()
