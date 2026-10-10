# Truy Vấn Dữ Liệu: Biến động Lượng truy cập và Doanh thu theo giờ (Hourly Traffic vs GMV)

Truy vấn này được sử dụng để xuất dữ liệu vẽ biểu đồ `hourly_traffic_gmv.png`. Nó kết hợp đồng thời cả Lượng truy cập (Traffic) và Doanh thu (GMV) để tìm ra "Giờ Vàng" (Golden Hours) và những khoảng thời gian bất thường (Traffic cao nhưng GMV = 0).

```sql
SELECT 
    CAST(session_start AS DATE) as event_date,
    EXTRACT(HOUR FROM session_start) as hour_of_day,
    COUNT(DISTINCT user_session) as total_sessions,
    ROUND(SUM(COALESCE(purchase_value, 0)), 2) as hourly_gmv_usd
FROM fct_session_funnel
WHERE session_start >= '2019-11-16 00:00:00' 
  AND session_start < '2019-11-18 00:00:00'
GROUP BY 1, 2
ORDER BY event_date ASC, hour_of_day ASC;
```

**Mục đích sử dụng:**
- **`total_sessions`**: Định lượng mẫu (Sample Size) để chứng minh tính khả thi của Guardrail 1 giờ.
- **`hourly_gmv_usd`**: Tính toán vận tốc dòng tiền (GMV Velocity) để xác định ngưỡng Giờ Vàng (>$3M/giờ).
- Hàm `COALESCE(purchase_value, 0)` đảm bảo các giỏ hàng bị bỏ rơi (không có giá trị thanh toán) được tính là 0 USD thay vì báo lỗi NULL.
