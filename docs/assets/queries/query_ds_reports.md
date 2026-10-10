# Truy Vấn Dữ Liệu: Thống kê Tập dữ liệu Machine Learning

File này lưu trữ các truy vấn dùng để xác minh quy mô dữ liệu trước khi đưa vào huấn luyện mô hình (Model Training).

### 1. Tổng khối lượng dữ liệu (Volume & Class Balance)
```sql
SELECT 
    COUNT(*) as total_cart_sessions,
    ROUND(SUM(CASE WHEN has_purchase=False THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as abandon_rate
FROM fct_session_funnel
WHERE has_cart = True
```

### 2. Quy mô tập Kiểm thử (Test Set: 21/11 - 30/11)
```sql
SELECT 
    COUNT(*) as test_sessions,
    ROUND(SUM(CASE WHEN has_purchase=False THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as test_abandon_rate
FROM fct_session_funnel
WHERE has_cart = True AND first_event_date >= '2019-11-21'
```
