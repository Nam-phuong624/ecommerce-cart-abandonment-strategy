# Báo Cáo Phân Tích Thất Thoát Doanh Thu Mùa Black Friday

---

## 1. Vấn Đề 

Black Friday lẽ ra là thời điểm hái ra tiền, nhưng dữ liệu hệ thống lại chỉ ra một nghịch lý: **Lượng truy cập tăng vọt, nhưng tỷ lệ khách bỏ ngang giỏ hàng cũng cao chưa từng có.**

Khi phân tích dữ liệu hành vi của người dùng trong 4 ngày cao điểm (14/11 - 17/11), chúng tôi phát hiện ra có **~8.02 Triệu USD** đã bị khách hàng đưa vào giỏ rồi bỏ lại.

Sự rò rỉ này đến từ một nguyên nhân đứt gãy của 3 nhóm khách hàng với 3 hành vi hoàn toàn khác biệt.

---

## 2. Phân Rã 3 Nhóm Khách Hàng


| Nhóm | Đặc Điểm | Số Người Bỏ Giỏ Hàng | Doanh Thu Bị Rớt | Tỷ Lệ Tự Quay Lại Mua |
| :--- | :--- | :--- | :--- | :--- |
| **Khách Ngủ Đông** | Lướt xem rất nhiều ở tháng trước nhưng không mua, đợi Sale mới vào xem lại, đây là nhóm có sự suy nghĩ rất kỹ. | **150,802** | **$4.04M** |  20.0% |
| **Khách Hàng Mới** | Lần đầu tiên tải app và lướt web nhờ chiến dịch Quảng cáo Black Friday. Bỏ đi rất nhanh. | **93,059** | **$2.49M** |  7.2% |
| **Khách VIP** | Từng mua hàng rất nhiều trước đây bằng "Nút Mua Ngay", nhưng đợt Sale bị ảnh hưởng bởi UI khuyến mãi nên gây khó chịu cho hành vị của hàng nhanh chóng của nhóm này (Nhóm này dù có Black Friday hay không vẫn mua hàng) | **55,711** | **$1.49M** |  18.2% |
| **TỔNG CỘNG** | | | **~$8.02M** | |

---

## 3. Hướng Giải Quyết Đề Xuất 


### Giải Pháp 1: Hướng đến tập khách hàng ngủ đông (target $4.04M)
- **Hành động:** Gửi thông báo Giảm giá nhanh cho chính xác các món đồ họ đã ngắm nghía từ tháng trước (dựa trên thông báo khi họ mới đăng nhập)
- **Mục tiêu (Giả định):** Nâng tỷ lệ phục hồi lên 22.5%.

### Giải Pháp 2: Giữ Chân Khách Mới (target $2.49M)
- **Hành động:** Bật Cửa sổ  Popup tặng mã giảm giá nhỏ hoặc Freeship ngay giây phút họ định vuốt màn hình để thoát app.
- **Mục tiêu (Giả định):** Nâng tỷ lệ phục hồi lên 16.2%.

### Giải Pháp 3: Giải Cứu Khách VIP (target $1.49M)
- **Hành động:** Tối ưu trải nghiệm mua ngay của nhóm này, họ cần cảm giác quen thuộc và nhanh chóng, không quan tâm quá nhiều vào việc giảm giá.
- **Mục tiêu (Giả định):** Nâng tỷ lệ phục hồi lên 30.0%.
