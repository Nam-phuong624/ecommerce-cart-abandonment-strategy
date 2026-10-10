# Truy Vấn Dữ Liệu: Giá Trị Đơn Hàng Trung Bình (AOV) Thực Tế

Truy vấn này loại bỏ việc "bốc thuốc" hay dùng số cố định (hardcode) bằng cách tính toán AOV thực tế trực tiếp từ toàn bộ các giao dịch thành công trên hệ thống.

```sql
SELECT 
    ROUND(AVG(purchase_value), 2) AS actual_aov_usd
FROM fct_session_funnel 
WHERE has_purchase = TRUE;
-- Kết quả trả về: $360.11
```
