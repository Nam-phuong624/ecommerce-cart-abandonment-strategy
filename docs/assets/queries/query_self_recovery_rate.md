# Truy Vấn Dữ Liệu: Tỷ Lệ Tự Phục Hồi (Self-Recovery Rate) Theo Cohort

Thay vì giả định tỷ lệ khách hàng tự quay lại chốt đơn, truy vấn này theo dấu (track) chính xác những User đã rớt phễu trong tuần lễ Black Friday, và kiểm tra xem họ có sinh ra bất kỳ giao dịch thành công nào sau giai đoạn đó hay không.

```sql
WITH user_history AS (
    SELECT user_id, 
        MIN(first_event_date) as first_seen_date,
        SUM(CASE WHEN first_event_date < '2019-11-11' THEN has_cart::INT ELSE 0 END) as hist_carts,
        SUM(CASE WHEN first_event_date < '2019-11-11' THEN has_purchase::INT ELSE 0 END) as hist_purchases
    FROM fct_session_funnel GROUP BY user_id
),
bf_abandoners AS (
    -- Lấy danh sách những người rớt phễu trong tuần Black Friday
    SELECT f.user_id,
        CASE
            WHEN u.hist_purchases > 0 AND u.hist_carts = 0 THEN '3. VIPs (Direct Native)'
            WHEN (u.hist_carts > 0 OR u.hist_purchases > 0) THEN '2. Chronic Shoppers'
            WHEN u.first_seen_date >= '2019-11-11' THEN '1. New Users'
        END AS cohort
    FROM fct_session_funnel f JOIN user_history u ON f.user_id = u.user_id
    WHERE f.first_event_date BETWEEN '2019-11-11' AND '2019-11-17'
      AND f.has_cart = TRUE AND f.has_purchase = FALSE
),
recovery_status AS (
    -- Kiểm tra xem những user này có mua hàng THÀNH CÔNG ở các ngày SAU ĐÓ không
    SELECT b.user_id, b.cohort,
           MAX(CASE WHEN f.has_purchase = TRUE THEN 1 ELSE 0 END) as did_recover
    FROM bf_abandoners b
    LEFT JOIN fct_session_funnel f 
      ON b.user_id = f.user_id 
     AND f.first_event_date > '2019-11-17' -- Sau đỉnh điểm BF
    GROUP BY b.user_id, b.cohort
)
SELECT cohort, 
       COUNT(user_id) as total_abandoners, 
       ROUND(AVG(did_recover)*100, 1) AS self_recovery_pct
FROM recovery_status
WHERE cohort IS NOT NULL
GROUP BY cohort ORDER BY cohort;
```
