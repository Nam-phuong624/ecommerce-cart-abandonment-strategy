# Báo Cáo Chất Lượng Dữ Liệu
**Tạo lúc:** 2026-10-08T20:03:09
**Nguồn:** `/home/namphuong/Documents/project_2/data/processed/ecommerce.duckdb`

## 1. Số Dòng
| Chỉ Số | Giá Trị |
|---|---|
| Tổng dòng | 109,950,743 |
| purchase | 1,659,788 |
| cart | 3,955,446 |
| view | 104,335,509 |
| remove_from_cart | 0 |

## 2. Khoảng Thời Gian Timestamp
| | Giá Trị |
|---|---|
| event_time nhỏ nhất | 2019-10-01 00:00:00 |
| event_time lớn nhất | 2019-11-30 23:59:59 |

## 3. Tỷ Lệ Null
| Cột | Số Null | % Null |
|---|---|---|
| event_time | 0 | 0.00% |
| event_type | 0 | 0.00% |
| product_id | 0 | 0.00% |
| category_id | 0 | 0.00% |
| category_code | 35,413,780 | 32.21% |
| brand | 15,331,243 | 13.94% |
| price | 0 | 0.00% |
| user_id | 0 | 0.00% |
| user_session | 12 | 0.00% |

## 4. Events Trùng Lặp
| Chỉ Số | Giá Trị |
|---|---|
| Nhóm trùng lặp (session+type+time) | 216,005 |

## 5. Ngoại Lệ Giá (Chỉ Cart + Purchase Events)
| Chỉ Số | Giá Trị |
|---|---|
| Giá nhỏ nhất | 0.00 |
| Giá lớn nhất | 2574.07 |
| Giá trung bình | 301.46 |
| Giá trung vị | 174.57 |
| Bằng 0 hoặc âm | 4,558 |
| Trên $5000 | 0 |

## 6. Số Lượng Duy Nhất (Xấp Xỉ)
| Chiều | Số Lượng |
|---|---|
| Users (Xấp xỉ) | 6,473,051 |
| Sessions (Xấp xỉ) | 25,929,449 |
| Products (Xấp xỉ) | 248,968 |
| Brands (Xấp xỉ) | 4,080 |
| Tháng | 2 |

## 7. Loại Event Không Hợp Lệ
| Chỉ Số | Giá Trị |
|---|---|
| Dòng event_type không hợp lệ | 0 |
