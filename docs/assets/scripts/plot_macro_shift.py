import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, '../../../data/processed/ecommerce.duckdb')
output_path = os.path.join(current_dir, '../images/macro_shift.png')

query = """
WITH period_sessions AS (
    SELECT 
        CASE WHEN EXTRACT(MONTH FROM first_event_date) = 10 THEN 'Tháng 10'
             WHEN EXTRACT(MONTH FROM first_event_date) = 11 THEN 'Tháng 11' END AS period_label,
        CASE 
            WHEN has_cart::INT = 0 AND has_purchase::INT > 0 THEN 'Mua Ngay (Direct)'
            WHEN has_cart::INT > 0 AND has_purchase::INT > 0 THEN 'Mua qua Giỏ (Cart)'
            WHEN has_cart::INT > 0 AND has_purchase::INT = 0 THEN 'Bỏ giỏ hàng (Rớt phễu)'
        END AS behavior
    FROM fct_session_funnel 
    WHERE EXTRACT(MONTH FROM first_event_date) IN (10, 11)
)
SELECT period_label, behavior, COUNT(*) as total_sessions
FROM period_sessions 
WHERE behavior IS NOT NULL
GROUP BY 1, 2 ORDER BY 1, 2 DESC;
"""

con = duckdb.connect(db_path, read_only=True)
df = con.execute(query).df()
con.close()

# Prepare Data
oct_data = df[df['period_label'] == 'Tháng 10']['total_sessions'].tolist()
nov_data = df[df['period_label'] == 'Tháng 11']['total_sessions'].tolist()
labels = ['Mua Ngay (Direct)', 'Mua qua Giỏ (Cart)', 'Bỏ Giỏ Hàng (Abandon)']

x = np.arange(len(labels))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))
rects1 = ax.bar(x - width/2, oct_data, width, label='Tháng 10 (Baseline)', color='#2ca02c')
rects2 = ax.bar(x + width/2, nov_data, width, label='Tháng 11 (Black Friday)', color='#d62728')

ax.set_ylabel('Số lượng Phiên truy cập (Sessions)')
ax.set_title('Sự Sụp Đổ Của Luồng "Mua Ngay" Toàn Hệ Thống', fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

def format_func(value, tick_number):
    if value >= 1000000: return f'{value/1000000:.1f}M'
    elif value >= 1000: return f'{value/1000:.0f}K'
    return str(value)
ax.yaxis.set_major_formatter(plt.FuncFormatter(format_func))

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        label = format_func(height, 0)
        ax.annotate(label, xy=(rect.get_x() + rect.get_width() / 2, height), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontweight='bold')
autolabel(rects1)
autolabel(rects2)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(output_path, dpi=300)
print(f"Lưu thành công (Live Data): {output_path}")
