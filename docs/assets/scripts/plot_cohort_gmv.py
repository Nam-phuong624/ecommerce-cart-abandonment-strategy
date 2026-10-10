import duckdb
import matplotlib.pyplot as plt
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, '../../../data/processed/ecommerce.duckdb')
output_path = os.path.join(current_dir, '../images/cohort_gmv.png')

query = """
WITH user_history AS (
    SELECT user_id, MIN(first_event_date) as first_seen_date,
        SUM(CASE WHEN EXTRACT(MONTH FROM first_event_date) = 10 THEN has_cart::INT ELSE 0 END) as oct_carts,
        SUM(CASE WHEN EXTRACT(MONTH FROM first_event_date) = 10 THEN has_purchase::INT ELSE 0 END) as oct_purchases
    FROM fct_session_funnel GROUP BY user_id
),
cohort_classification AS (
    SELECT f.user_session, 
        CASE
            WHEN u.first_seen_date >= '2019-11-01' THEN 'New Users'
            WHEN u.oct_purchases > 0 AND u.oct_carts = 0 THEN 'VIPs (Direct Native)'
            WHEN (u.oct_carts > 0 OR u.oct_purchases > 0) THEN 'Chronic Shoppers'
        END AS cohort
    FROM fct_session_funnel f JOIN user_history u ON f.user_id = u.user_id
    WHERE f.first_event_date >= '2019-11-14' AND f.first_event_date <= '2019-11-17'
      AND f.has_cart = TRUE AND f.has_purchase = FALSE
)
SELECT cohort, ROUND((COUNT(user_session) * (SELECT AVG(purchase_value) FROM fct_session_funnel WHERE has_purchase = TRUE)) / 1000000, 1) AS gmv_millions
FROM cohort_classification WHERE cohort IS NOT NULL GROUP BY 1 ORDER BY 2 ASC;
"""

con = duckdb.connect(db_path, read_only=True)
df = con.execute(query).df()
con.close()

fig, ax = plt.subplots(figsize=(9, 5))
# Use dynamic data from DataFrame
cohorts = df['cohort'].tolist()
gmv = df['gmv_millions'].tolist()
colors = ['#d62728' if 'VIP' in c else '#ff7f0e' if 'Chronic' else '#1f77b4' for c in cohorts]

bars = ax.barh(cohorts, gmv, color=colors)
ax.set_title('Quy Mô Thất Thoát Doanh Thu đạt đỉnh tại 4 ngày (14-17/11)', fontweight='bold', pad=20)

for bar in bars:
    width = bar.get_width()
    ax.text(width + 1, bar.get_y() + bar.get_height()/2, f'${width}M', ha='left', va='center', fontweight='bold', fontsize=11)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.xaxis.set_ticks([])
plt.tight_layout()
plt.savefig(output_path, dpi=300)
print(f"Lưu thành công (Live Data): {output_path}")
