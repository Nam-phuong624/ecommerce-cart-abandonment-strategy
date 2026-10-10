# Truy Vấn Dữ Liệu: Chứng Minh Sự Sụp Đổ Của Luồng "Mua Ngay"

Đoạn trích: *"Tháng 10, luồng Mua Ngay gánh tới 53.6% (337,699) tổng số đơn hàng thành công. Sang Black Friday, số đơn Mua Ngay rớt thê thảm xuống còn 124,841 đơn, nhường chỗ cho hơn 1 triệu ca rớt giỏ hàng."*

Để trả lời và chứng minh chính xác câu nói trên, truy vấn này sẽ làm 2 việc:
1. Tính **Tỷ trọng Đơn hàng thành công** (Chỉ xét các phiên có mua hàng) để chứng minh tỷ lệ 53.6%.
2. Đếm số lượng **Rớt giỏ hàng** (Phiên không mua hàng) để thấy con số 1 triệu.

```sql
WITH successful_orders AS (
    -- TÍNH TỶ TRỌNG CỦA CÁC ĐƠN HÀNG THÀNH CÔNG
    SELECT 
        CASE WHEN EXTRACT(MONTH FROM first_event_date) = 10 THEN 'Tháng 10' ELSE 'Tháng 11' END AS period,
        CASE WHEN has_cart::INT = 0 THEN 'Mua Ngay (Direct)' ELSE 'Mua qua Giỏ (Cart)' END AS checkout_flow,
        COUNT(user_session) as total_purchases
    FROM fct_session_funnel
    WHERE has_purchase = TRUE AND EXTRACT(MONTH FROM first_event_date) IN (10, 11)
    GROUP BY 1, 2
),
abandonments AS (
    -- TÍNH SỐ LƯỢNG RỚT PHỄU
    SELECT 
        CASE WHEN EXTRACT(MONTH FROM first_event_date) = 10 THEN 'Tháng 10' ELSE 'Tháng 11' END AS period,
        COUNT(user_session) as total_abandoned
    FROM fct_session_funnel
    WHERE has_purchase = FALSE AND has_cart = TRUE AND EXTRACT(MONTH FROM first_event_date) IN (10, 11)
    GROUP BY 1
)
SELECT 
    s.period, 
    s.checkout_flow, 
    s.total_purchases,
    -- Tính phần trăm tỷ trọng đơn Mua Ngay
    ROUND(s.total_purchases * 100.0 / SUM(s.total_purchases) OVER(PARTITION BY s.period), 1) AS pct_of_successful_orders,
    a.total_abandoned
FROM successful_orders s
JOIN abandonments a ON s.period = a.period
ORDER BY s.period, s.checkout_flow DESC;
```
