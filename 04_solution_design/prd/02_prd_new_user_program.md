## 1. Tóm Tắt 

1.5 triệu khách lần đầu đến trong đợt marketing Black Friday thêm 27M GMV trong giỏ hàng rồi bỏ.  Trong tổng số 27M thì chỉ có 6,2% là doanh thu tự phục hồi. 93,8% còn lại (tương đương 25.3M) là cơ hội để công ty khai thác và tối đa hóa lợi nhuận của khách hàng.

**Giả thuyết:** Chương trình phục hồi 3 bước (hành vi định thoát trang + Push/Trong ứng dụng cadence + shipping nudge + first-order discount) có thể đẩy tỷ lệ phục hồi từ **6.2%** lên ≥ **16.2%**, mang về $7.8M mỗi sự kiện Black Friday.

---


## 2. Kịch Bản Người Dùng

> **Với tư cách là** khách lần đầu trong Black Friday đang tìm kiếm deal,
> **Khi** tôi thêm items vào giỏ nhưng do dự ở thanh toán,
> **Tôi muốn** có một ưu đãi rõ ràng để hoàn thành giao dịch,
> **Để** tôi không bỏ lỡ deal do suy nghĩ quá nhiều hoặc so sánh nơi khác.

**Acceptance Criteria:**
- GIVEN tôi được phân loại là nhóm khách hàng `new_user` (lần đầu xuất hiện trong tháng 11)
- WHEN tôi thể hiện exit intent trên trang giỏ hàng/thanh toán
- THEN tôi thấy hành vi định thoát trang popup với ưu đãi giảm giá có giới hạn thời gian
- AND nếu tôi vẫn bỏ, tôi nhận 3 Push/Trong ứng dụng Notification phục hồi lúc T+1h, T+24h, T+72h
- AND discount là một lần dùng, liên kết với user, không thể chia sẻ

---


## 3. Đối Tượng & Điều Kiện

**Đủ điều kiện:**
- `user_id` lần đầu thấy trong tháng hiện tại (new_user nhóm khách hàng từ C1 classifier)
- Session có ít nhất 1 giỏ hàng sự kiện (tín hiệu ý định)
- session nhận dạng được (cho hành vi định thoát trang)
- Không nằm trong danh sách chặn 
- Không nằm trong nhóm các user kiểm thử

**Không đủ điều kiện:**
- Khách hàng quay trở lại (dùng cho ws-2 và ws-3)
- Khách hàng tiến hành thanh toán không nhận thông báo
- Khách hàng không đồng ý với chính sách tiếp nhận thông tin (sự theo dõi hành vi thao tác của người dùng - xác định hành vi sắp thoát trang)


---

## 4. Đặc Tả Tính Năng

### Exit-Intent Popup (Thông báo khi khách hàng có dấu hiệu muốn thoát trang)
**Kích hoạt:** Chuột rời khỏi viewport về phía đầu trang trên giỏ hàng/thanh toán, HOẶC idle 15s trên trang giỏ hàng
**Hiển thị:** Modal overlay, có thể đóng, X rõ ràng
**Các trường hợp kiểm thử (A/B):**
- V1: "Chờ đã! Giảm 10% cho đơn đầu tiên — Mã Black Friday10FIRST"
- V2: "Free shipping cho đơn trên $50 — ưu đãi một lần"
- V3: "Giữ giỏ hàng trong 20 phút — không cần mã"
**Frequency cap:** 1 lần mỗi session, 2 lần mỗi user mỗi 7 ngày

### Push/Trong ứng dụng Recovery Flow
**Bước 1 (T+1h):** "Still thinking about [items]?" — nhắc nhẹ kèm link giỏ hàng
**Bước 2 (T+24h):** "Your Black Friday deal is almost gone" — thêm mã giảm 10%
**Bước 3 (T+72h):** "Last chance" — free shipping + discount kết hợp

**Quy tắc:**
- Tắt nếu user mua giữa các bước
- Tắt nếu user hủy đăng ký
- Một sequence mỗi user mỗi 14 ngày
- Tôn trọng send-time optimization (không gửi trong giờ quiet của user)

### Ngưỡng Free Shipping tùy biến
**Kích hoạt**: giá trị giỏ hàng trong khoảng $X so với ngưỡng free shipping.

**Hành vi:** hiển thị thông báo "Add $X more for FREE shpping" trên trang giỏ hàng.

**Cơ chế tùy biến**: ngưỡng tính dựa trên items trong giỏ.


### Tín hiệu tin tưởng cho người dùng mới 
**Vị trí:** Sidebar trang thanh toán
**Thành phần:** Badge số lượng đánh giá, đảm bảo hoàn tiền, icon thanh toán bảo mật, ước tính giao hàng
Chỉ cho new users (A/B test nếu existing users cũng hưởng lợi)

---

## 5. Đánh giá đo lường

### Sự kiện Cần Theo Dõi
- `ws1_exit_intent_shown` / `_dismissed` / `_converted`
- `ws1_noti_sent` / `_opened` / `_clicked` / `_converted`
- `ws1_shipping_nudge_shown` / `_converted`
- `ws1_discount_code_generated` / `_used`
- `ws1_recovery_attribution`

### Bảng biểu Panels
1. Tỷ lệ phục hồi theo biến thể (hàng ngày)
2. Notification funnel: Sent → Opened → Clicked → Converted
3. Tỷ lệ chi phí discount (discount $ / GMV phục hồi)
4. Trạng thái Guardrail


---

## 6. Tiêu Chí Nghiệm Thu

Các chỉ số dưới đây được ánh xạ trực tiếp từ Mục tiêu Chiến lược của Master PRD (Target: Nâng tỷ lệ phục hồi của Khách Hàng Mới lên 16.2%, tương đương mang về $2.7M). 
### Chấp nhận Triển khai (Xanh)
- **Chỉ số chính:** Tỷ lệ phục hồi đạt **>= 16.2%** (Đạt đúng mục tiêu PRD đề ra).
- **Guardrails:** Không có vi phạm nào kéo dài quá **1 giờ với khung giờ vàng (08:00 - 17:00)** hoặc **3 giờ (ngoài khung giờ vàng).** Dữ liệu thực tế cho thấy vào Giờ Vàng, mỗi giờ hệ thống tạo ra tới $4.75 Triệu GMV.
- **Đo lường phụ:** Chi phí khuyến mãi  phải nhỏ hơn 15% tổng GMV được phục hồi.

### Cần Tối ưu thêm (Vàng)
- **Chỉ số chính:** Tỷ lệ phục hồi đạt **10% đến 15%** (cải thiện so với mức cơ sở 6.2%, nhưng chưa đạt ngưỡng kỳ vọng 16.2%).
- **Hành động:** Tiếp tục A/B Test, điều chỉnh lại mức độ giảm giá hoặc thay đổi nội dung Push Notification, kiểm thử lại trong sự kiện Flash Sale tiếp theo.

### Hủy bỏ Tính năng (Đỏ)
- **Chỉ số chính:** Tỷ lệ phục hồi **< 10%**, hoặc tỷ lệ hủy đăng ký  vượt mốc 1%.
- **Hoặc:** Chi phí khuyến mãi vượt quá 20% tổng GMV phục hồi.
- **Hoặc:** Bất kỳ chỉ số Guardrail nào bị báo Đỏ liên tục trong **1 giờ vàng (08:00 - 17:00)** hoặc **3 giờ (ngoài khung giờ vàng)**.
- **Hành động:** Tự động tắt popup và chuỗi Push (Rollback), họp đội ngũ Data & Product để phân tích nguyên nhân gốc rễ .
