import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import os

def main():
    # Kết nối DuckDB
    db_path = '../../data/processed/ecommerce.duckdb'
    
    # Check current directory to resolve correct relative path
    if os.path.exists('data/processed/ecommerce.duckdb'):
        db_path = 'data/processed/ecommerce.duckdb'
    elif os.path.exists('../../../data/processed/ecommerce.duckdb'):
        db_path = '../../../data/processed/ecommerce.duckdb'
        
    try:
        con = duckdb.connect(db_path, read_only=True)
    except Exception as e:
        print(f"Lỗi kết nối DB: {e}. Đảm bảo bạn đã tắt DuckDB CLI (nhả khóa PID).")
        return

    # Câu truy vấn GMV và Traffic trong 2 ngày đỉnh điểm (16-17 Nov)
    query = """
    SELECT 
        CAST(session_start AS DATE) as event_date,
        EXTRACT(HOUR FROM session_start) as hour_of_day,
        COUNT(DISTINCT user_session) as total_sessions,
        ROUND(SUM(COALESCE(purchase_value, 0)), 2) as hourly_gmv_usd
    FROM fct_session_funnel
    WHERE session_start >= '2019-11-16 00:00:00' 
      AND session_start < '2019-11-18 00:00:00'
    GROUP BY 1, 2
    ORDER BY event_date ASC, hour_of_day ASC;
    """

    df = con.execute(query).df()
    con.close()

    if df.empty:
        print("Không có dữ liệu trả về.")
        return

    # Tạo nhãn Trục X (Ví dụ: 16/0h, 17/12h)
    df['datetime_label'] = df['event_date'].astype(str).str[8:10] + '/' + df['hour_of_day'].astype(str) + 'h'

    # Thiết lập biểu đồ 2 trục
    fig, ax1 = plt.subplots(figsize=(14, 6))

    color1 = '#3498db' # Xanh dương
    # ax1.set_xlabel('Ngày & Giờ (16 - 17 Tháng 11)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Lượng Truy Cập (Sessions)', color=color1, fontsize=11, fontweight='bold')
    ax1.bar(df['datetime_label'], df['total_sessions'], color=color1, alpha=0.7, label='Lượng truy cập')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.tick_params(axis='x', rotation=45)

    ax2 = ax1.twinx()
    color2 = '#e74c3c' # Đỏ
    ax2.set_ylabel('Doanh Thu (GMV - USD)', color=color2, fontsize=11, fontweight='bold')
    ax2.plot(df['datetime_label'], df['hourly_gmv_usd'], color=color2, marker='o', linewidth=2.5, label='GMV Thực tế')
    ax2.tick_params(axis='y', labelcolor=color2)

    plt.title('Lượng truy cập và doanh thu trong giai đoạn Black Friday (14-17/11)', fontsize=14, fontweight='bold', pad=20)
    fig.tight_layout()

    # Đường dẫn lưu file
    out_dir = 'docs/assets/images'
    if not os.path.exists(out_dir):
        if os.path.exists('../../docs/assets/images'):
            out_dir = '../../docs/assets/images'
    
    out_path = os.path.join(out_dir, 'hourly_traffic_gmv.png')
    plt.savefig(out_path, dpi=300)
    print(f"✅ Đã tạo thành công biểu đồ và lưu tại: {out_path}")

if __name__ == "__main__":
    main()
