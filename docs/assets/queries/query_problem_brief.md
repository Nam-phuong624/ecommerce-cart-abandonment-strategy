# Truy Vấn Dữ Liệu: Hồ sơ Vấn Đề (Problem Brief)

File này lưu trữ công thức truy vấn phân rã 3 nhóm khách hàng (Triple-Leak) gây ra thất thoát doanh thu trong dịp Black Friday.
AOV thực tế được áp dụng là $26.79.

### 1. Rớt phễu Nhóm Khách Mới
```sql
WITH new_users AS (
    SELECT user_id FROM fct_session_funnel GROUP BY user_id HAVING MIN(first_event_date) >= '2019-11-11'
)
SELECT 
    COUNT(DISTINCT CASE WHEN f.has_cart=True AND f.has_purchase=False THEN f.user_id END) as abandoners,
    ROUND(COUNT(DISTINCT CASE WHEN f.has_cart=True AND f.has_purchase=False THEN f.user_id END) * 26.79 / 1000000.0, 2) as gmv
FROM fct_session_funnel f JOIN new_users n ON f.user_id = n.user_id
WHERE f.first_event_date BETWEEN '2019-11-14' AND '2019-11-17'
```

### 2. Rớt phễu Nhóm Khách Ngủ Đông (Chronic)
```sql
WITH oct_users AS (
    SELECT user_id FROM fct_session_funnel 
    WHERE first_event_date >= '2019-10-01' AND first_event_date < '2019-11-01'
    GROUP BY user_id HAVING MAX(CAST(has_purchase AS INT)) = 0
)
SELECT 
    COUNT(DISTINCT CASE WHEN f.has_cart=True AND f.has_purchase=False THEN f.user_id END) as abandoners,
    ROUND(COUNT(DISTINCT CASE WHEN f.has_cart=True AND f.has_purchase=False THEN f.user_id END) * 26.79 / 1000000.0, 2) as gmv
FROM fct_session_funnel f JOIN oct_users o ON f.user_id = o.user_id
WHERE f.first_event_date BETWEEN '2019-11-14' AND '2019-11-17'
```

### 3. Rớt phễu Nhóm VIP (Direct Native)
```sql
WITH oct_buyers AS (
    SELECT user_id FROM fct_session_funnel 
    WHERE first_event_date >= '2019-10-01' AND first_event_date < '2019-11-01'
    GROUP BY user_id HAVING MAX(CAST(has_purchase AS INT)) = 1
)
SELECT 
    COUNT(DISTINCT CASE WHEN f.has_cart=True AND f.has_purchase=False THEN f.user_id END) as abandoners,
    ROUND(COUNT(DISTINCT CASE WHEN f.has_cart=True AND f.has_purchase=False THEN f.user_id END) * 26.79 / 1000000.0, 2) as gmv
FROM fct_session_funnel f JOIN oct_buyers o ON f.user_id = o.user_id
WHERE f.first_event_date BETWEEN '2019-11-14' AND '2019-11-17'
```
