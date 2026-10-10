# Cảnh Báo Rủi Ro & Giới Hạn Của Hệ Thống

##  Tính chất theo thời điểm
* **Vấn đề:** Con AI này chỉ mới được đi học bằng dữ liệu của tháng 10 và tháng 11 (Mùa Black Friday). Nó cực kỳ giỏi việc bắt bài khách săn Sale mùa đông.
* **Rủi ro:** Nếu bê nguyên con AI này sang dịp Valentine hoặc Mùa Hè, nó có thể đoán sai bét vì tâm lý khách hàng các mùa là khác nhau. 
* **Giải pháp:** Cứ đến mùa mới, phải nạp thêm dữ liệu để dạy lại AI (Retrain).

##  Lúng Túng Với Khách Hàng Mới Tinh (Cold-Start)
* **Vấn đề:** Rất nhiều khách hàng lần đầu tải App. Họ không có lịch sử mua sắm trong quá khứ.
* **Rủi ro:** AI không có thông tin về họ nên khả năng dự đoán sẽ bị giảm độ chính xác.
* **Giải pháp:** Cần phát triển thêm tính năng phân tích hành vi theo Thời gian thực (Ví dụ: khách đang bấm liên tục vào xem giá rồi thoát) để bù đắp.

##  Khoảng Cách Giữa Mô Phỏng Và Thực Tế
* **Vấn đề:** Các con số lợi nhuận hiện tại đều là **(Giả định Mô phỏng)** trên máy tính.
* **Giải pháp:** Bắt buộc phải chạy thử nghiệm thật (A/B Testing) với một tập khách hàng nhỏ trước khi mở rộng ra 100% người dùng.
