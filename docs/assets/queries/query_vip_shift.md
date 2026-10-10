# Truy Vấn Dữ Liệu: Biểu Đồ Sự Đứt Gãy Hành Vi Của Nhóm VIP (VIP Behavior Shift)

Biểu đồ Stacked Bar Chart `vip_shift.png` được vẽ bằng cách lấy Tỷ trọng (%) từ kết quả của truy vấn cô lập nhóm "Pure Direct VIPs" và đối chiếu hành vi trước/trong Black Friday.

```sql
WITH historical_lifetime AS (
    -- Quét lịch sử ngày thường
    SELECT user_id, SUM(has_cart::INT) AS lifetime_cart_count, SUM(has_purchase::INT) AS lifetime_purchase_count
    FROM fct_session_funnel WHERE first_event_date < '2019-11-11' GROUP BY user_id
),
pure_direct_vips AS (
    -- Lọc gắt gao nhóm thuần Mua Ngay
    SELECT user_id FROM historical_lifetime WHERE lifetime_purchase_count > 0 AND lifetime_cart_count = 0
),
period_sessions AS (
    -- Gắn nhãn hành vi
    SELECT user_session, user_id, 
        CASE 
            WHEN EXTRACT(MONTH FROM first_event_date) = 10 THEN '1. Tháng 10'
            WHEN first_event_date >= '2019-11-11' THEN '2. Tháng 11 (BF)'
        END AS period_label,
        CASE 
            WHEN has_cart::INT = 0 AND has_purchase::INT > 0 THEN 'Mua Ngay (Direct)'
            WHEN has_cart::INT > 0 AND has_purchase::INT > 0 THEN 'Mua qua Giỏ hàng (Cart)'
            WHEN has_cart::INT > 0 AND has_purchase::INT = 0 THEN 'Bỏ giỏ hàng (Rớt phễu)'
            ELSE 'Chỉ lướt xem'
        END AS behavior
    FROM fct_session_funnel 
)
SELECT 
    p.period_label,
    p.behavior,
    COUNT(p.user_session) AS total_sessions,
    -- Tính tỷ trọng phần trăm để vẽ Stacked Bar Chart (Chia cho tổng số phiên Có ý định mua)
    ROUND(COUNT(p.user_session) * 100.0 / SUM(COUNT(p.user_session)) OVER (PARTITION BY p.period_label), 1) AS pct_share
FROM period_sessions p 
JOIN pure_direct_vips v ON p.user_id = v.user_id 
WHERE p.period_label IS NOT NULL 
  AND p.behavior != 'Chỉ lướt xem' -- Loại bỏ lướt xem để tính tỷ trọng 100% trên các phiên Có Ý Định (Intent Sessions)
GROUP BY 1, 2 
ORDER BY 1 ASC, 3 DESC;
```
