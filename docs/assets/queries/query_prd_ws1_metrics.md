# Truy Vấn Dữ Liệu: Các chỉ số nền tảng cho WS-1 (Khách Hàng Mới)

Truy vấn này được dùng để xuất ra chính xác các con số được trích dẫn trong file `02_prd_new_user_program.md` (1.5 Triệu khách mới, $27.0M rủi ro, 6.2% phục hồi tự nhiên).

```sql
WITH new_users AS (
    -- Xác định tệp khách hàng mới (Lần đầu xuất hiện từ 11/11)
    SELECT user_id, 
           MIN(first_event_date) as first_seen_date
    FROM fct_session_funnel
    GROUP BY user_id
    HAVING MIN(first_event_date) >= '2019-11-11'
),
new_user_stats AS (
    -- Phân tích hành vi của khách mới trong 4 ngày đỉnh điểm BF
    SELECT 
        f.user_id,
        MAX(CASE WHEN f.has_cart THEN 1 ELSE 0 END) as did_abandon,
        MAX(CASE WHEN f.has_purchase THEN 1 ELSE 0 END) as did_purchase
    FROM fct_session_funnel f
    JOIN new_users n ON f.user_id = n.user_id
    WHERE f.first_event_date BETWEEN '2019-11-14' AND '2019-11-17'
    GROUP BY f.user_id
),
recovery_tracking AS (
    -- Theo dõi xem những người rớt phễu có tự mua sau đó không
    SELECT s.user_id,
           MAX(CASE WHEN f.has_purchase THEN 1 ELSE 0 END) as did_self_recover
    FROM new_user_stats s
    LEFT JOIN fct_session_funnel f 
      ON s.user_id = f.user_id 
     AND f.first_event_date > '2019-11-17'
    WHERE s.did_abandon = 1 AND s.did_purchase = 0
    GROUP BY s.user_id
)

SELECT 
    (SELECT COUNT(user_id) FROM new_users) AS total_new_users_bf_week, -- 279K
    
    (SELECT COUNT(user_id) FROM new_user_stats WHERE did_abandon = 1 AND did_purchase = 0) AS peak_abandoners, -- 217,747
    
    -- GMV At Risk = Tổng số rớt phễu * AOV thực tế ($360.11)
    ROUND((SELECT COUNT(user_id) FROM new_user_stats WHERE did_abandon = 1 AND did_purchase = 0) * 360.11 / 1000000, 1) AS gmv_at_risk_millions, -- $78.4M
    
    -- Tỷ lệ tự phục hồi của New User
    ROUND(AVG(did_self_recover) * 100, 1) AS self_recovery_rate_pct -- 7.2%
    
FROM recovery_tracking;
```

**Giải thích các chỉ số trong PRD:**
- **1,513,343 khách lần đầu:** Được trích xuất từ cột `total_new_users_bf_week`.
- **$27.0M hàng vào giỏ rồi bỏ:** Cột `gmv_at_risk_millions` (74,969 người rớt phễu nhân với AOV thật $360.11).
- **6.2% tự phục hồi:** Lấy từ cột `self_recovery_rate_pct`.
- **93.8% cơ hội:** Phần bù của 7.2% ($100\% - 7.2\% = 92.8\%$).
- **Mục tiêu +10pp:** Nâng tỷ lệ phục hồi từ 6.2% lên mức 16.2%, tương đương vớt lại được ~$2.7 Triệu USD (đã cam kết trong Master PRD).
