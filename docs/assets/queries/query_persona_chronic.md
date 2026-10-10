# Truy Vấn Dữ Liệu: Hành vi của Persona B (Chronic Shopper)

Truy vấn này theo dõi nhóm người dùng ngâm giỏ hàng từ Tháng 10, đo lường độ tích cực của họ (số lượt xem) và "Số ngày ngủ đông" trước khi bị chiến dịch marketing Black Friday đánh thức.

```sql
WITH oct_activity AS (
    -- Lọc những người ngâm giỏ hàng trong Tháng 10 (Có giỏ, không mua)
    SELECT user_id, 
           SUM(view_count) as oct_views,
           SUM(purchase_count) as oct_purchases,
           MAX(first_event_date) as last_oct_date
    FROM fct_session_funnel
    WHERE EXTRACT(MONTH FROM first_event_date) = 10
    GROUP BY user_id
    HAVING oct_purchases = 0 AND SUM(cart_count) > 0
),
bf_activity AS (
    -- Tìm ngày họ quay lại trong đợt Black Friday
    SELECT user_id, 
           MIN(first_event_date) as first_bf_date
    FROM fct_session_funnel
    WHERE first_event_date >= '2019-11-11'
    GROUP BY user_id
)
SELECT 
    ROUND(AVG(o.oct_views), 1) as avg_oct_views_before_hibernation,
    ROUND(AVG(DATE_DIFF('day', o.last_oct_date, b.first_bf_date)), 1) as avg_sleep_days
FROM oct_activity o
JOIN bf_activity b ON o.user_id = b.user_id;
```
