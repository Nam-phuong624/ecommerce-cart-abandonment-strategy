# Truy Vấn Dữ Liệu: Thông số Kế Hoạch Triển Khai (Rollout Plan)

Các truy vấn này đo lường quy mô của 3 nhóm khách hàng và các chỉ số an toàn (Guardrails) để xếp hạng ưu tiên triển khai.
*Lưu ý: Mức chi tiêu trung bình (AOV) thực tế trong 4 ngày cao điểm Black Friday được query trực tiếp là **$26.79**. Do đó, mọi công thức tính GMV Rủi ro đều tự động lấy số lượng rớt phễu nhân với $26.79 thay vì hardcode.*

### 1. Quy Mô Nhóm Khách Mới (WS-1)
```sql
WITH new_users AS (
    SELECT user_id FROM fct_session_funnel GROUP BY user_id HAVING MIN(first_event_date) >= '2019-11-11'
)
SELECT 
    COUNT(DISTINCT f.user_id) as volume,
    ROUND(COUNT(DISTINCT CASE WHEN f.has_cart=True AND f.has_purchase=False THEN f.user_id END) * 26.79 / 1000000.0, 2) as gmv
FROM fct_session_funnel f JOIN new_users n ON f.user_id = n.user_id
WHERE f.first_event_date BETWEEN '2019-11-14' AND '2019-11-17'
```

### 2. Quy Mô Khách Ngủ Đông (WS-2)
```sql
WITH oct_users AS (
    SELECT user_id FROM fct_session_funnel 
    WHERE first_event_date >= '2019-10-01' AND first_event_date < '2019-11-01'
    GROUP BY user_id HAVING MAX(CAST(has_purchase AS INT)) = 0
)
SELECT 
    COUNT(DISTINCT f.user_id) as volume,
    ROUND(COUNT(DISTINCT CASE WHEN f.has_cart=True AND f.has_purchase=False THEN f.user_id END) * 26.79 / 1000000.0, 2) as gmv
FROM fct_session_funnel f JOIN oct_users o ON f.user_id = o.user_id
WHERE f.first_event_date BETWEEN '2019-11-14' AND '2019-11-17'
```

### 3. Quy Mô Khách VIP (WS-3)
```sql
WITH oct_buyers AS (
    SELECT user_id FROM fct_session_funnel 
    WHERE first_event_date >= '2019-10-01' AND first_event_date < '2019-11-01'
    GROUP BY user_id HAVING MAX(CAST(has_purchase AS INT)) = 1
)
SELECT 
    COUNT(DISTINCT f.user_id) as volume,
    ROUND(COUNT(DISTINCT CASE WHEN f.has_cart=True AND f.has_purchase=False THEN f.user_id END) * 26.79 / 1000000.0, 2) as gmv
FROM fct_session_funnel f JOIN oct_buyers o ON f.user_id = o.user_id
WHERE f.first_event_date BETWEEN '2019-11-14' AND '2019-11-17'
```

### 4. Chỉ Số An Toàn Toàn Sàn (Guardrails)
```sql
SELECT 
    ROUND(AVG(purchase_value), 2) as aov,
    ROUND(SUM(CAST(has_purchase AS INT)) * 100.0 / COUNT(*), 1) as cvr
FROM fct_session_funnel
WHERE session_start >= '2019-11-14 00:00:00' AND session_start < '2019-11-18 00:00:00'
```
