# Truy Vấn Dữ Liệu: Quy Mô Rớt Phễu Theo Cohort

Truy vấn này phân loại toàn bộ các phiên truy cập bị rớt phễu trong Black Friday (Từ 11/11 trở đi) thành 3 nhóm khách hàng cốt lõi dựa trên lịch sử hành vi của họ trước đó.

```sql
WITH user_history AS (
    SELECT user_id, 
        MIN(first_event_date) as first_seen_date,
        SUM(CASE WHEN first_event_date < '2019-11-11' THEN has_cart::INT ELSE 0 END) as hist_carts,
        SUM(CASE WHEN first_event_date < '2019-11-11' THEN has_purchase::INT ELSE 0 END) as hist_purchases
    FROM fct_session_funnel GROUP BY user_id
),
cohort_classification AS (
    SELECT f.user_session,
        CASE
            WHEN u.hist_purchases > 0 AND u.hist_carts = 0 THEN '3. VIPs (Direct Native)'
            WHEN (u.hist_carts > 0 OR u.hist_purchases > 0) THEN '2. Chronic Shoppers'
            WHEN u.first_seen_date >= '2019-11-11' THEN '1. New Users'
        END AS cohort
    FROM fct_session_funnel f JOIN user_history u ON f.user_id = u.user_id
    WHERE f.first_event_date >= '2019-11-11'
      AND f.has_cart = TRUE AND f.has_purchase = FALSE -- Lọc các ca rớt phễu
)
SELECT cohort, COUNT(user_session) as volume
FROM cohort_classification 
WHERE cohort IS NOT NULL 
GROUP BY 1 ORDER BY 1 ASC;
```
