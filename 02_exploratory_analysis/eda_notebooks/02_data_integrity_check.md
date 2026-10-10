# Kiểm Tra Tính Toàn Vẹn Dữ Liệu

## Xác Minh 1: Số Lượng Events Ngày 14-17/11 (Kiểm Tra Data Gap)
| event_date          | event_type   |   count |
|:--------------------|:-------------|--------:|
| 2019-11-14 00:00:00 | cart         |  170472 |
| 2019-11-14 00:00:00 | purchase     |   22124 |
| 2019-11-14 00:00:00 | view         | 2877130 |
| 2019-11-15 00:00:00 | cart         |  483305 |
| 2019-11-15 00:00:00 | view         | 5737111 |
| 2019-11-16 00:00:00 | cart         |  406778 |
| 2019-11-16 00:00:00 | purchase     |   68247 |
| 2019-11-16 00:00:00 | view         | 6027932 |
| 2019-11-17 00:00:00 | cart         |  426941 |
| 2019-11-17 00:00:00 | purchase     |  185195 |
| 2019-11-17 00:00:00 | view         | 5783241 |

## Xác Minh 2: Luồng Mua Trực Tiếp (Tháng 10/2019)
- **Số sessions có Purchase nhưng KHÔNG có Cart (Tháng 10):** 337,699

## Xác Minh 3: Category Code Bị Thiếu
- **Số dòng có category_code NULL/Trống:** 35,413,777

## Đánh Dấu Xử Lý
- **Data Gap Ngày 15/11:** Đã xác nhận (chỉ có 1 purchase event so với 4.7M views/carts). Đánh dấu để loại trừ.
- **Luồng Mua Trực Tiếp:** Có tồn tại (337,699 sessions trong tháng 10). Cần định nghĩa chỉ số mới `direct_purchase_sessions` nếu theo dõi.
- **Danh Mục Unknown:** Không thể làm sạch (35,413,777 dòng). Cần nhóm lại thành `unknown`.

## Chỉ Số Điều Chỉnh (Loại Trừ Ngày 15/11)
- **GMV at risk tháng 11 (trước):** $533,126,364.19
- **GMV at risk tháng 11 (sau):** $377,915,846.57
- **Ngày có abandonment cao nhất (sau):** 2019-11-16 00:00:00 ($97,429,566.70 GMV at risk)
- **Tín hiệu Tuần Sale Pre-BF 14-17 (sau):** Vẫn giữ nguyên. Trung bình GMV at risk hàng ngày của các ngày 14, 16, 17 là $65,182,427.99 so với trung bình các ngày còn lại trong tháng 11 là $7,014,175.48.
