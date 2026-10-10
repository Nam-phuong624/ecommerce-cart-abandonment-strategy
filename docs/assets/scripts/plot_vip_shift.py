import duckdb
import matplotlib.pyplot as plt
import numpy as np
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, '../../../data/processed/ecommerce.duckdb')
output_path = os.path.join(current_dir, '../images/vip_shift.png')

query = """
WITH historical_lifetime AS (
    SELECT user_id, SUM(has_cart::INT) AS lifetime_cart_count, SUM(has_purchase::INT) AS lifetime_purchase_count
    FROM fct_session_funnel WHERE first_event_date < '2019-11-11' GROUP BY user_id
),
pure_direct_vips AS (
    SELECT user_id FROM historical_lifetime WHERE lifetime_purchase_count > 0 AND lifetime_cart_count = 0
),
period_sessions AS (
    SELECT user_session, user_id, 
        CASE WHEN EXTRACT(MONTH FROM first_event_date) = 10 THEN 'Tháng 10' ELSE 'Tháng 11' END AS period,
        CASE 
            WHEN has_cart::INT = 0 AND has_purchase::INT > 0 THEN 'Direct'
            WHEN has_cart::INT > 0 AND has_purchase::INT > 0 THEN 'Cart'
            WHEN has_cart::INT > 0 AND has_purchase::INT = 0 THEN 'Abandon'
        END AS behavior
    FROM fct_session_funnel 
)
SELECT p.period, p.behavior,
       ROUND(COUNT(p.user_session) * 100.0 / SUM(COUNT(p.user_session)) OVER (PARTITION BY p.period), 1) AS pct
FROM period_sessions p JOIN pure_direct_vips v ON p.user_id = v.user_id 
WHERE p.period IS NOT NULL AND p.behavior IS NOT NULL
GROUP BY 1, 2 ORDER BY 1 ASC;
"""

con = duckdb.connect(db_path, read_only=True)
df = con.execute(query).df()
con.close()

# Prepare matrix
oct_direct = df[(df['period']=='Tháng 10') & (df['behavior']=='Direct')]['pct'].sum()
nov_direct = df[(df['period']=='Tháng 11') & (df['behavior']=='Direct')]['pct'].sum()
nov_cart = df[(df['period']=='Tháng 11') & (df['behavior']=='Cart')]['pct'].sum()
nov_abandon = df[(df['period']=='Tháng 11') & (df['behavior']=='Abandon')]['pct'].sum()

months = ['Tháng 10', 'Tháng 11 (Black Friday)']
direct = [oct_direct, nov_direct]
cart = [0.0, nov_cart]
abandon = [0.0, nov_abandon]

fig, ax = plt.subplots(figsize=(8, 6))
b1 = ax.bar(months, abandon, label='Bỏ Giỏ', color='#d62728', bottom=np.array(cart)+np.array(direct))
b2 = ax.bar(months, cart, label='Mua qua Giỏ', color='#ff7f0e', bottom=direct)
b3 = ax.bar(months, direct, label='Mua Ngay', color='#2ca02c')

ax.set_ylabel('Tỷ trọng (%)')
ax.set_title('Sự Đứt Gãy Hành Vi Nhóm VIP', fontweight='bold', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1))

def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        if height > 5:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_y() + height/2, f'{height:.1f}%', ha='center', va='center', color='white', fontweight='bold')
add_labels(b1); add_labels(b2); add_labels(b3)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(output_path, dpi=300)
print(f"Lưu thành công (Live Data): {output_path}")
