import duckdb
import matplotlib.pyplot as plt
import numpy as np
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, '../../../data/processed/ecommerce.duckdb')
output_path = os.path.join(current_dir, '../images/direct_collapse_proof.png')

query = """
WITH successful_orders AS (
    SELECT CASE WHEN EXTRACT(MONTH FROM first_event_date) = 10 THEN 'Tháng 10' ELSE 'Tháng 11' END AS period,
           CASE WHEN has_cart::INT = 0 THEN 'Direct' ELSE 'Cart' END AS flow,
           COUNT(user_session) as total_purchases
    FROM fct_session_funnel WHERE has_purchase = TRUE AND EXTRACT(MONTH FROM first_event_date) IN (10, 11) GROUP BY 1, 2
),
abandonments AS (
    SELECT CASE WHEN EXTRACT(MONTH FROM first_event_date) = 10 THEN 'Tháng 10' ELSE 'Tháng 11' END AS period,
           COUNT(user_session) as total_abandoned
    FROM fct_session_funnel WHERE has_purchase = FALSE AND has_cart = TRUE AND EXTRACT(MONTH FROM first_event_date) IN (10, 11) GROUP BY 1
)
SELECT s.period, s.flow, s.total_purchases, 
       ROUND(s.total_purchases * 100.0 / SUM(s.total_purchases) OVER(PARTITION BY s.period), 1) AS pct, a.total_abandoned
FROM successful_orders s JOIN abandonments a ON s.period = a.period ORDER BY s.period, s.flow DESC;
"""

con = duckdb.connect(db_path, read_only=True)
df = con.execute(query).df()
con.close()

# Extract Panel 1 data
oct_dir = df[(df['period']=='Tháng 10') & (df['flow']=='Direct')]['total_purchases'].sum()
nov_dir = df[(df['period']=='Tháng 11') & (df['flow']=='Direct')]['total_purchases'].sum()
oct_cart = df[(df['period']=='Tháng 10') & (df['flow']=='Cart')]['total_purchases'].sum()
nov_cart = df[(df['period']=='Tháng 11') & (df['flow']=='Cart')]['total_purchases'].sum()
oct_dir_pct = df[(df['period']=='Tháng 10') & (df['flow']=='Direct')]['pct'].sum()
nov_dir_pct = df[(df['period']=='Tháng 11') & (df['flow']=='Direct')]['pct'].sum()

# Extract Panel 2 data
oct_abnd = df[df['period']=='Tháng 10']['total_abandoned'].iloc[0]
nov_abnd = df[df['period']=='Tháng 11']['total_abandoned'].iloc[0]

labels = ['Tháng 10', 'Tháng 11 (BF)']
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))

# PANEL 1
ax1.bar(labels, [oct_dir, nov_dir], 0.5, label='Mua Ngay', color='#2ca02c')
ax1.bar(labels, [oct_cart, nov_cart], 0.5, bottom=[oct_dir, nov_dir], label='Mua qua Giỏ', color='#1f77b4')
ax1.set_title('Sự Sụp Đổ Của "Mua Ngay"', fontweight='bold', pad=15)
ax1.legend(loc='upper right')
ax1.text(0, oct_dir/2, f"{oct_dir_pct}%\n({oct_dir:,})", ha='center', va='center', color='white', fontweight='bold')
ax1.text(1, nov_dir/2, f"{nov_dir_pct}%\n({nov_dir:,})", ha='center', va='center', color='white', fontweight='bold')

# PANEL 2
x = np.arange(len(labels))
rects = ax2.bar(x, [oct_abnd, nov_abnd], 0.4, color='#d62728', label='Bỏ giỏ hàng')
ax2.set_title('Hệ Quả: Rớt Phễu', fontweight='bold', pad=15)
ax2.set_xticks(x); ax2.set_xticklabels(labels)

for rect in rects:
    height = rect.get_height()
    label = f"{height/1000000:.2f}M" if height >= 1000000 else f"{height/1000:.0f}K"
    ax2.annotate(label, xy=(rect.get_x() + rect.get_width() / 2, height), xytext=(0, 3), textcoords="offset points", ha='center', fontweight='bold')

def fmt(v, t): return f'{v/1000000:.1f}M' if v>=1000000 else f'{v/1000:.0f}K' if v>=1000 else str(v)
ax1.yaxis.set_major_formatter(plt.FuncFormatter(fmt))
ax2.yaxis.set_major_formatter(plt.FuncFormatter(fmt))
ax1.spines['top'].set_visible(False); ax1.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False); ax2.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(output_path, dpi=300)
print(f"Lưu thành công (Live Data): {output_path}")
