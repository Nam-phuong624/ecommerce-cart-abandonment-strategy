# Truy Vấn Dữ Liệu: Hành vi của Persona A (New User)

Truy vấn này trích xuất hành vi thực tế của nhóm Khách hàng mới (Lần đầu truy cập vào đợt Black Friday) để vẽ chân dung (Profiling) chính xác cho báo cáo PRD.

```sql
WITH new_users AS (
    -- Lấy tất cả user lần đầu xuất hiện từ 11/11 trở đi
    SELECT user_id, 
           COUNT(DISTINCT user_session) as total_sessions,
           SUM(view_count) as total_views,
           SUM(cart_count) as total_carts
    FROM fct_session_funnel
    WHERE first_event_date >= '2019-11-11'
    GROUP BY user_id
)
SELECT 
    ROUND(AVG(total_sessions), 1) as avg_sessions, 
    ROUND(AVG(total_views), 1) as avg_views, 
    ROUND(AVG(total_carts), 1) as avg_carts
FROM new_users;
```
