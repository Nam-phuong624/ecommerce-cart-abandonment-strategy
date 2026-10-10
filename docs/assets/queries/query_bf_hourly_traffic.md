# Truy Vấn Dữ Liệu: Lưu lượng truy cập theo giờ (Hourly Traffic Volume)

Truy vấn này chứng minh cơ sở khoa học của quyết định thiết lập "Guardrail 3 giờ". Bằng cách đo lường lượng Session đổ vào hệ thống trong những giờ cao điểm của Black Friday (14/11 - 17/11), chúng ta xác nhận được liệu 3 giờ có đủ lượng mẫu (Sample Size) để tính toán A/B Testing hay không.

```sql
-- 1. Xem 10 khung giờ bận rộn nhất trong 4 ngày đỉnh điểm
SELECT 
    CAST(session_start AS DATE) as event_date,
    EXTRACT(HOUR FROM session_start) as hour_of_day,
    COUNT(DISTINCT user_session) as session_count
FROM fct_session_funnel
WHERE session_start >= '2019-11-14 00:00:00' 
  AND session_start < '2019-11-18 00:00:00'
GROUP BY 1, 2
ORDER BY session_count DESC
LIMIT 10;

-- 2. Tính trung bình lượng Session trong 1 giờ và 3 giờ
SELECT 
    ROUND(COUNT(DISTINCT user_session) / (4.0 * 24.0), 0) as avg_sessions_per_hour,
    ROUND((COUNT(DISTINCT user_session) / (4.0 * 24.0)) * 3, 0) as avg_sessions_per_3_hours
FROM fct_session_funnel
WHERE session_start >= '2019-11-14 00:00:00' 
  AND session_start < '2019-11-18 00:00:00';
```
