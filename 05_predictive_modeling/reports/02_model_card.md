#  Tính minh bạch của Model


## Thông tin chung
* **Mục tiêu:** Dự đoán xem một khách hàng đang cầm Giỏ hàng có định không thanh toán hay không. Điểm dự đoán này sẽ quyết định hệ thống có nên hiện Mã giảm giá ra để níu kéo họ lại không.

## Dữ liệu Huấn luyện
* **Nguồn:** Dữ liệu hành vi người dùng tháng 10 và 11 năm 2019.
* **Quy mô tập Kiểm thử :** Dùng **441,582** sản phẩm trong giỏ hàng trong 10 ngày cuối tháng 11 để chấm điểm AI (Tỷ lệ rớt thực tế của tập này là 52.2%).

##  Độ đo Hiệu năng (Giả định Offline)
* Các chỉ số chuyên ngành (như ROC-AUC, PR-AUC) đều vượt mức trung bình, cho thấy AI nhận diện rất nhạy các dấu hiệu bỏ rơi giỏ hàng.

##  An toàn & Đạo đức
* Mô hình **không sử dụng** bất kỳ dữ liệu cá nhân nào (Tuổi, Giới tính, Quê quán). 
* AI chỉ ra quyết định dựa trên Hành vi (Họ click bao nhiêu lần, họ ngắm đồ gì). Do đó, hoàn toàn không có rủi ro về phân biệt đối xử khách hàng.
