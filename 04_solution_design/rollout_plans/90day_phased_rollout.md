# Kế Hoạch Triển Khai 90 Ngày 


## 1. Ưu Tiên Ra Mắt Dựa Trên Rủi Ro Doanh Thu

Thay vì ra mắt 3 tính năng cùng lúc, chúng ta xếp hạng ưu tiên dựa trên quy mô doanh thu đang bị rớt của từng tập khách hàng trong đúng 4 ngày cao điểm Black Friday (14/11 - 17/11).

| Giai Đoạn (Phase) | Nhóm Khách Hàng | Quy Mô Tập Khách | Doanh Thu Rớt (Đã xác thực) | Quyết Định & Lý Do |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1 (Tháng 1)** *(giả định)* | Khách Ngủ Đông (Chronic) | **489,016** | **$4.04M** | Ưu tiên Cao nhất: Doanh thu rớt lớn nhất, dễ tiếp cận qua Push Notification. |
| **Phase 2 (Tháng 2)** *(giả định)* | Khách Mới (New Users) | **376,362** | **$2.49M** | Ưu tiên Trung bình: Đông nhất nhưng rủi ro thập hơn. Cần cài đặt Popup chặn thoát trang cẩn thận. |
| **Phase 3 (Tháng 3)** *(giả định)* | Khách VIP (Direct Buyers) | **114,906** | **$1.49M** | Ưu tiên Thấp nhất: Lượng khách nhỏ. Thêm nữa, code Nút Mua Ngay rất rủi ro. |

---

## 2. Mục Tiêu Hoàn Vốn Từng Giai Đoạn (ROI)

Mục tiêu (KPI) thu hồi doanh thu được tính theo tỷ lệ phần trăm (giả định) nhân với tổng GMV rớt thực tế của từng nhóm.

| Giai Đoạn | Tính Năng Chạy Thử | Tỷ Lệ Phục Hồi Kỳ Vọng *(giả định)* | Doanh Thu Kỳ Vọng Lấy Lại *(giả định)* |
| :--- | :--- | :--- | :--- |
| **Phase 1** | Gửi thông báo giảm giá (Price-drop) | **22.5%** | **~$0.91M** |
| **Phase 2** | Cài đặt Popup chặn thoát trang | **16.2%** | **~$0.4M** |
| **Phase 3** | Mở nút Thanh toán nhanh (Fast-checkout) | **30.0%** | **~$0.45M** |
| **TỔNG** | | | **~$1.76M** |

---

## 3. Các Chỉ Số Guardrails

Trong suốt 90 ngày chạy thử nghiệm, nếu dữ liệu chung của cả sàn rớt xuống dưới các **Mức Cơ Sở** dưới đây, tính năng phải lập tức bị tắt (Rollback) trong vòng 1 Giờ Vàng.

| Tên Chỉ Số | Ngưỡng An Toàn (Đã xác thực) | Cách Xử Lý Nếu Bị Báo Đỏ |
| :--- | :--- | :--- |
| **Mức Chi Tiêu Trung Bình (AOV)** | Luôn duy trì >= **$26.79** | Tắt ngay luồng gửi Mã giảm giá/Bundle đang thử nghiệm. |
| **Tỷ Lệ Mua Hàng Chung (CVR)** | Luôn duy trì >= **6.9%** | Tắt ngay luồng Thanh toán nhanh (Fast-checkout) để tránh kẹt đơn. |
