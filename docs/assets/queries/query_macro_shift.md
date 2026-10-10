# Truy Vấn Dữ Liệu: Biểu Đồ Sự Sụp Đổ Của Luồng "Mua Ngay" (Macro Shift)

Biểu đồ `macro_shift.png` được vẽ dựa trên kết quả của truy vấn đếm khối lượng hành vi trên toàn bộ hệ thống trong Tháng 10 và Tháng 11 (General Population). Không sử dụng bất kỳ bộ lọc cách ly khách hàng nào.

```sql
WITH period_sessions AS (
    SELECT 
        user_session,
        CASE 
            WHEN EXTRACT(MONTH FROM first_event_date) = 10 THEN '1. Tháng 10 (Toàn hệ thống)'
            WHEN EXTRACT(MONTH FROM first_event_date) = 11 THEN '2. Tháng 11 (Toàn hệ thống)'
        END AS period_label,
        CASE 
            WHEN has_cart::INT = 0 AND has_purchase::INT > 0 THEN '4. Mua Ngay (Direct)'
            WHEN has_cart::INT > 0 AND has_purchase::INT > 0 THEN '3. Mua qua Giỏ hàng (Cart)'
            WHEN has_cart::INT > 0 AND has_purchase::INT = 0 THEN '2. Bỏ giỏ hàng (Rớt phễu)'
            ELSE '1. Chỉ lướt xem'
        END AS behavior
    FROM fct_session_funnel 
    WHERE EXTRACT(MONTH FROM first_event_date) IN (10, 11)
)
SELECT 
    period_label,
    behavior,
    COUNT(user_session) AS total_sessions
FROM period_sessions
WHERE behavior != '1. Chỉ lướt xem' -- Loại bỏ lướt xem để tập trung vẽ biểu đồ vào ý định mua
GROUP BY 1, 2
ORDER BY 1 ASC, 2 ASC;
```
