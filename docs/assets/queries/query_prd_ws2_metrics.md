# Truy Vấn Dữ Liệu: Các chỉ số nền tảng cho WS-2 (Chronic Shoppers)

Truy vấn này xuất ra các chỉ số hành vi chính xác của nhóm khách hàng "ngủ đông" (Lướt mạnh trong tháng 10 nhưng không mua, sau đó quay lại vào đợt Black Friday tháng 11). 

```sql
WITH oct_users AS (
    -- Khách hàng lướt web tháng 10 nhưng chưa từng mua
    SELECT 
        user_id,
        MAX(CASE WHEN has_purchase THEN 1 ELSE 0 END) as oct_purchase,
        SUM(view_count) as oct_views,
        MAX(CAST(session_start AS DATE)) as last_oct_seen
    FROM fct_session_funnel
    WHERE first_event_date >= '2019-10-01' AND first_event_date < '2019-11-01'
    GROUP BY user_id
    HAVING MAX(CASE WHEN has_purchase THEN 1 ELSE 0 END) = 0
),
nov_returners AS (
    -- Những khách này quay lại trong đợt BF (Tháng 11)
    SELECT 
        f.user_id,
        MIN(CAST(f.session_start AS DATE)) as first_nov_seen,
        MAX(CASE WHEN f.first_event_date BETWEEN '2019-11-14' AND '2019-11-17' AND f.has_cart THEN 1 ELSE 0 END) as did_abandon_bf,
        MAX(CASE WHEN f.first_event_date BETWEEN '2019-11-14' AND '2019-11-17' AND f.has_purchase THEN 1 ELSE 0 END) as did_purchase_bf
    FROM fct_session_funnel f
    JOIN oct_users o ON f.user_id = o.user_id
    WHERE f.first_event_date >= '2019-11-01'
    GROUP BY f.user_id
),
recovery_tracking AS (
    SELECT 
        n.user_id,
        MAX(CASE WHEN f.has_purchase THEN 1 ELSE 0 END) as did_self_recover
    FROM nov_returners n
    LEFT JOIN fct_session_funnel f 
        ON n.user_id = f.user_id 
        AND f.first_event_date > '2019-11-17'
    WHERE n.did_abandon_bf = 1 AND n.did_purchase_bf = 0
    GROUP BY n.user_id
)

SELECT 
    (SELECT COUNT(*) FROM nov_returners) AS total_chronic_returners,
    
    (SELECT ROUND(AVG(oct_views), 1) FROM oct_users o JOIN nov_returners n ON o.user_id = n.user_id) AS avg_oct_views,
    
    (SELECT ROUND(AVG(DATE_DIFF('day', o.last_oct_seen, n.first_nov_seen)), 1) 
     FROM oct_users o JOIN nov_returners n ON o.user_id = n.user_id) AS avg_sleep_days,
     
    (SELECT COUNT(*) FROM nov_returners WHERE did_abandon_bf = 1 AND did_purchase_bf = 0) AS peak_abandoners,
    
    ROUND((SELECT COUNT(*) FROM nov_returners WHERE did_abandon_bf = 1 AND did_purchase_bf = 0) * 360.11 / 1000000, 1) AS gmv_at_risk_millions,
    
    ROUND(AVG(did_self_recover) * 100, 1) AS self_recovery_rate_pct
FROM recovery_tracking;
```

**Kết quả thực tế (Ánh xạ vào PRD 03):**
- Tổng số khách hàng Chronic quay lại: **1,185,902**
- Lượt xem trung bình trong tháng 10: **16.1 lượt**
- Số ngày ngủ đông trung bình: **20.0 ngày**
- Số người rớt phễu trong BF (14-17/11): **117,317 người**
- Rủi ro doanh thu (GMV at risk): **$42.2M**
- Tỷ lệ tự phục hồi: **7.1%**
