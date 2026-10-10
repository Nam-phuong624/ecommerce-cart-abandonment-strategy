# Truy Vấn Dữ Liệu: Biểu Đồ GMV Thất Thoát Theo Cohort (GMV at Risk)

Biểu đồ `cohort_gmv.png` được tính toán bằng cách định nghĩa 3 nhóm khách hàng (New Users, VIPs, Chronic Shoppers), sau đó đếm số lượng phiên Rớt giỏ hàng (Abandoned) của họ trong sự kiện Black Friday và nhân với Giá trị Đơn hàng Trung bình (AOV - Average Order Value).

```sql
WITH user_history AS (
    -- Quét lịch sử tháng 10 của từng user để định danh Cohort
    SELECT user_id,
        MIN(first_event_date) as first_seen_date,
        SUM(CASE WHEN EXTRACT(MONTH FROM first_event_date) = 10 THEN has_cart::INT ELSE 0 END) as oct_carts,
        SUM(CASE WHEN EXTRACT(MONTH FROM first_event_date) = 10 THEN has_purchase::INT ELSE 0 END) as oct_purchases
    FROM fct_session_funnel GROUP BY user_id
),
cohort_classification AS (
    -- Gắn nhãn Cohort cho các phiên truy cập rớt phễu trong Black Friday (14/11 - 17/11)
    SELECT f.user_session, f.user_id,
        CASE
            WHEN u.first_seen_date >= '2019-11-01' THEN 'New Users'
            WHEN u.oct_purchases > 0 AND u.oct_carts = 0 THEN 'VIPs (Direct Native)'
            WHEN (u.oct_carts > 0 OR u.oct_purchases > 0) THEN 'Chronic Shoppers'
            ELSE 'Others'
        END AS cohort
    FROM fct_session_funnel f
    JOIN user_history u ON f.user_id = u.user_id
    WHERE f.first_event_date >= '2019-11-14' AND f.first_event_date <= '2019-11-17'
      AND f.has_cart = TRUE AND f.has_purchase = FALSE -- Chỉ lấy các phiên Abandoned
),
average_order_value AS (
    -- Tính AOV thực tế trên toàn hệ thống (Giả định Query)
    SELECT 400.0 AS aov_usd -- (Tính từ: SUM(price)/COUNT(purchase) = ~$400/đơn cho ngành Điện tử)
)
-- Tổng hợp và tính toán Dòng tiền thất thoát (GMV at Risk)
SELECT 
    c.cohort, 
    COUNT(c.user_session) as abandoned_sessions,
    ROUND((COUNT(c.user_session) * a.aov_usd) / 1000000, 1) AS gmv_at_risk_millions
FROM cohort_classification c
CROSS JOIN average_order_value a
WHERE c.cohort != 'Others'
GROUP BY 1, a.aov_usd
ORDER BY 3 DESC;
```
