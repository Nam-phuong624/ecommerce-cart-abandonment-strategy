# Data Dictionary — BF Triple-Leak Analytics

**Mục đích:** Tài liệu tham khảo về schema, định nghĩa cohort, và các chỉ số tính toán. Dùng khi bảo trì pipeline hoặc diễn giải kết quả phân tích.
**Cập nhật lần cuối:** 2026-10-08

---

## 1. Nguồn Dữ Liệu Thô

### `data/raw/*.csv` — REES46 Multi-Category E-commerce Events

| Cột | Kiểu | Mô Tả | Ví Dụ |
|---|---|---|---|
| `event_time` | TIMESTAMP (UTC) | Thời điểm event xảy ra | `2019-10-01 00:00:00 UTC` |
| `event_type` | VARCHAR | Loại event | `view`, `cart`, `purchase` |
| `product_id` | BIGINT | Product ID duy nhất | `1004856` |
| `category_id` | BIGINT | Category ID duy nhất | `2053013555631882655` |
| `category_code` | VARCHAR | Đường dẫn category phân cấp bằng dấu chấm, có thể null | `electronics.smartphone` |
| `brand` | VARCHAR | Tên thương hiệu, có thể null | `samsung`, `apple` |
| `price` | DOUBLE | Giá sản phẩm tính bằng USD | `35.79` |
| `user_id` | BIGINT | Persistent user ID | `520088904` |
| `user_session` | VARCHAR | Session UUID | `4d3b30da-a5e4-...` |

**Lưu ý:**
- Không có event `remove_from_cart` trong dataset multi-category (khác với biến thể cosmetics)
- Đơn vị tiền tệ: USD (đã xác nhận)
- 32% `category_code` là NULL (gộp thành "unknown")
- Kích thước dataset: 110M dòng cho tháng 10 + 11/2019
- Data gap đã biết: Purchase events ngày 15/11 bị thiếu (đã xác nhận trong Giai đoạn 2.5)

---

## 2. Tầng Staging

### `stg_events`
Events thô đã được làm sạch với type casting và lọc bỏ dòng không hợp lệ.

| Cột | Kiểu | Biến Đổi |
|---|---|---|
| `event_id` | VARCHAR | Tạo tự động: hash của `(user_session, product_id, event_time, event_type)` |
| `event_time` | TIMESTAMP | Cast từ VARCHAR |
| `event_date` | DATE | DATE(event_time) |
| `event_month` | DATE | DATE_TRUNC('month', event_time) |
| `event_hour` | INT | EXTRACT(hour FROM event_time) |
| `day_of_week` | INT | 1=Thứ Hai, 7=Chủ Nhật |
| `event_type` | VARCHAR | Chuyển thành chữ thường |
| `product_id` | BIGINT | Pass-through |
| `category_code` | VARCHAR | COALESCE(category_code, 'unknown') |
| `brand` | VARCHAR | COALESCE(brand, 'unknown') |
| `price` | DOUBLE | Lọc: >0 |
| `user_id` | BIGINT | Pass-through |
| `user_session` | VARCHAR | Pass-through |

**Bộ lọc áp dụng:**
- `price > 0` (loại trừ giá $0 placeholder)
- `event_type IS NOT NULL`
- `user_session IS NOT NULL`

### `stg_sessions`
Tổng hợp ở mức session.

| Cột | Kiểu | Biến Đổi |
|---|---|---|
| `user_session` | VARCHAR | PK |
| `user_id` | BIGINT | MIN(user_id) |
| `first_event_time` | TIMESTAMP | MIN(event_time) |
| `last_event_time` | TIMESTAMP | MAX(event_time) |
| `session_duration_min` | DOUBLE | EXTRACT epoch diff / 60 |
| `event_count` | INT | COUNT(*) |

---

## 3. Tầng Mart

### `fct_session_funnel` — Bảng phân tích chính (1 dòng = 1 session)

Xem `docs/architecture.md` §4 để có danh sách cột đầy đủ.

**Các flag tính toán chính:**
- `has_view` = session có ≥1 view event
- `has_cart` = session có ≥1 cart event
- `has_purchase` = session có ≥1 purchase event
- `is_abandoned` = `has_cart AND NOT has_purchase`

**Các giá trị tính toán chính:**
- `cart_value` = SUM(price) WHERE event_type='cart'
- `purchase_value` = SUM(price) WHERE event_type='purchase'
- `minutes_cart_to_purchase` = EXTRACT epoch (first_purchase_time - first_cart_time) / 60

---

## 4. Định Nghĩa Cohort

### Strict Direct-Native (Mục tiêu WS-3)
```sql
WHERE user_id IN (
  SELECT user_id FROM fct_session_funnel
  WHERE session_month = '2019-10-01'
    AND has_purchase = TRUE
    AND has_cart = FALSE
  GROUP BY user_id
  HAVING SUM(CASE WHEN has_cart = TRUE AND has_purchase = TRUE THEN 1 ELSE 0 END) = 0
)
```
**Quy mô:** 36,712 users (người mua trực tiếp tháng 10, KHÔNG có lần mua nào qua cart trong tháng 10)

### Chronic Oct Shopper (Mục tiêu WS-2)
```sql
WHERE user_id IN (
  SELECT user_id FROM fct_session_funnel
  WHERE session_month = '2019-10-01'
    AND has_view = TRUE
    AND has_purchase = FALSE
)
AND user_id IN (
  SELECT user_id FROM fct_session_funnel
  WHERE session_month = '2019-11-01'
    AND is_abandoned = TRUE
)
```
**Quy mô:** 217,095 users

### New User (Mục tiêu WS-1)
```sql
WHERE user_id NOT IN (
  SELECT DISTINCT user_id FROM fct_session_funnel
  WHERE session_month = '2019-10-01'
)
AND user_id IN (
  SELECT user_id FROM fct_session_funnel
  WHERE session_month = '2019-11-01'
    AND is_abandoned = TRUE
)
```
**Quy mô:** 245,131 users (xuất hiện lần đầu trong tháng 11, đã bỏ giỏ hàng)

### Overlap Cohort (Loại trừ khỏi WS-3)
Users có CẢ direct-purchase VÀ cart-based purchase trong tháng 10.
**Quy mô:** 49,641 users

---

## 5. Công Thức Chỉ Số Chính

### Tỷ Lệ Chuyển Đổi Funnel
```
view_to_cart = sessions_with_cart / sessions_with_view
cart_to_purchase = sessions_with_purchase / sessions_with_cart
view_to_purchase = sessions_with_purchase / sessions_with_view
```

### Abandonment Rate (Thực)
```
true_abandonment_rate = (sessions_with_cart - sessions_with_purchase) / sessions_with_cart
```

### Natural Recovery Rate (Theo Cohort, Trong Tháng 11)
```
natural_recovery = users_who_abandoned_then_purchased_later / users_who_abandoned_initially
```
Đo trong cửa sổ 7 ngày sau khi bỏ giỏ.

### GMV at Risk
```
gmv_at_risk = SUM(cart_value) WHERE is_abandoned = TRUE
```

### Chỉ Số Cannibalization
```
migration_rate = direct_native_users_who_used_cart_in_nov / direct_native_users_active_in_nov
cannibalized_gmv_at_risk = SUM(cart_value) WHERE user IN direct_native AND is_abandoned
```

---

## 6. Số Liệu Đã Xác Minh (Từ DA Giai Đoạn 5 — KHÔNG TÍNH LẠI MÀ KHÔNG XÁC MINH)

| Chỉ Số | Giá Trị | Nguồn Giai Đoạn |
|---|---|---|
| Tổng GMV at risk tháng 11 (loại trừ 15/11) | $377.9M | V4 đã đối chiếu |
| GMV at risk New Users | $154.1M | Giai đoạn 6 Q1 |
| GMV at risk Other Oct | $160.1M | Giai đoạn 6 Q1 |
| GMV at risk Strict Direct | $23.3M | Giai đoạn 5 V3 |
| GMV at risk Overlap | $19.0M | V4 |
| GMV at risk Strict Cart | $21.5M | V4 |
| Natural recovery New Users | 21.3% | Giai đoạn 6 Q4 |
| Natural recovery Other Oct | 25.6% | Giai đoạn 6 Q4 |
| Natural recovery Strict Direct | 38.5% | Giai đoạn 6 Q4 |
| Di chuyển Direct-Native Tháng 10→11 (strict) | 59.4% | Giai đoạn 5 V3 |
| Baseline migration rate tháng 10 | 13% | Giai đoạn 5 V6 |
| Migration rate BF Week | 31.8% | Giai đoạn 5 V6 |
| Hệ số spike | 2.5× | Giai đoạn 5 V6 |
| Abandon rate Direct-Native BF Week | 56% | Giai đoạn 5 V7 |
| Abandon rate Direct-Native Non-BF Week | 31% | Giai đoạn 5 V7 |
| Abandon rate baseline Direct-Native tháng 10 | 0% | Giai đoạn 5 V7 |

---

## 7. Vấn Đề Chất Lượng Dữ Liệu Đã Biết

| Vấn Đề | Phạm Vi | Xử Lý |
|---|---|---|
| Purchase events ngày 15/11 bị thiếu | Cả ngày | Loại trừ khỏi mọi phân tích tháng 11 |
| Tỷ lệ NULL `category_code` | 32% dòng | Gộp thành "unknown" |
| Tỷ lệ NULL `brand` | ~15% dòng | Gộp thành "unknown" |
| Event `remove_from_cart` vắng mặt | Toàn bộ dataset | Không thể phân biệt "full-clear" với "true abandon" |
| Add-to-cart sau purchase | 10.38% purchases | Nhiễu nhỏ, có thể chấp nhận |

---

## 8. Thư Viện SQL Snippet

### Đếm sessions theo cohort
```sql
SELECT
  COUNT(DISTINCT user_id) FILTER (WHERE cohort = 'strict_direct') AS n_strict_direct,
  COUNT(DISTINCT user_id) FILTER (WHERE cohort = 'other_oct') AS n_other_oct,
  COUNT(DISTINCT user_id) FILTER (WHERE cohort = 'new_user') AS n_new_user
FROM fct_session_funnel;
```

### GMV at risk theo ngày
```sql
SELECT
  session_date,
  SUM(cart_value) FILTER (WHERE is_abandoned) AS gmv_at_risk,
  SUM(purchase_value) AS gmv_purchased
FROM fct_session_funnel
WHERE session_month = '2019-11-01'
  AND session_date <> '2019-11-15'
GROUP BY 1
ORDER BY 1;
```

### Cohort migration tracker
```sql
WITH oct_direct AS (
  SELECT DISTINCT user_id FROM fct_session_funnel
  WHERE session_month = '2019-10-01'
    AND has_purchase AND NOT has_cart
)
SELECT
  COUNT(DISTINCT CASE WHEN has_purchase AND NOT has_cart THEN f.user_id END) AS retained_direct,
  COUNT(DISTINCT CASE WHEN has_purchase AND has_cart THEN f.user_id END) AS migrated_to_cart,
  COUNT(DISTINCT CASE WHEN is_abandoned THEN f.user_id END) AS migrated_abandoned
FROM fct_session_funnel f
JOIN oct_direct od ON f.user_id = od.user_id
WHERE f.session_month = '2019-11-01' AND f.session_date <> '2019-11-15';
```

---

## 9. Tài Liệu Liên Quan

- Kiến trúc: `docs/architecture.md`
- BA Brief: `03_strategic_insights/reports/01_problem_brief_v3.md`
- Lần xác minh: `02_exploratory_analysis/eda_notebooks/05_metric_verification.md`
- Phân tích cohort: `02_exploratory_analysis/eda_notebooks/06_triple_leak_profiling.md`
