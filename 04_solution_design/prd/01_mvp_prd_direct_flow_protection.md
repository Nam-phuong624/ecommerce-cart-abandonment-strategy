## 1. Tóm Tắt

**Vấn đề:** Black Friday chuyển 37% người mua VIP (những người thanh toán nhanh và thường mua hàng qua thao tác **mua nhanh**) thành những người thêm sản phẩm vào giỏ hàng và do dự thanh toán. Trong Black Friday Week, tỷ lệ ngưng thanh toán của nhóm khách hàng VIP tăng vọt từ 0% (tháng 10) lên 56% (tháng 11). Điều này cho thấy công ty đang mất một nguồn doanh thu ~$13.6M GMV mỗi sự kiện. 

**Giả thuyết:** Nếu chúng ta phát hiện hành vi quay lại mua hàng của nhóm khách hàng VIP trong Black Friday. Triển khai cơ chế để người dùng giữ được luồng chọn và thanh toán sản phẩm nhanh như trước, không quan trọng đến các chi phí về giảm giá. Chúng ta có thể **khôi phục tỷ lệ giữ lại nhóm VIP lên ít nhất 30%** (so với Black Friday mức cơ sở 16.15%) và ngăn chặn ~$10M thất thoát mỗi sự kiện.


---

## 2. Kịch Bản Người Dùng

> **Với tư cách là** người mua hàng thường xuyên quay lại, tôi muốn thao tác mua hàng nhanh chóng với việc thanh toán qua 1 - 2 bước mà không cần đi qua nhiều quy trình nhập thông tin,
> **Khi** tôi ghé thăm site trong Black Friday Week,
> **Tôi muốn** mua ở mức giá hiện tại mà không bị kéo vào hành trình sale,
> **Để** hoàn thành giao dịch nhanh chóng mà không bị quyết định.

**Acceptance Criteria:**
- GIVEN tôi được phân loại là mua hàng trực tiếp không thông qua giỏ hàng.
- WHEN tôi xem product page trong Black Friday Week (14-17/11 + 29/11)
- THEN tôi thấy badge "Buy Now at Current Price" phía trên nút Add-to-Giỏ hàng
- AND giá hiện tại bị khóa trong 15 phút kể từ lần xem đầu tiên
- AND sale banner đầu trang bị ẩn
- AND nhấn "Buy Now" đưa tôi thẳng đến trang thanh toán 1 bước (bỏ qua giỏ hàng)

---

---

## 3. Đối Tượng & Điều Kiện

**Đủ điều kiện:**
- `user_id` có ít nhất 1 lần mua hàng trực tiếp (không qua giỏ hàng) trong 60 ngày qua.
- `user_id` đã đăng nhập HOẶC có cookie/device nhận dạng được
- `user_id` không nằm trong danh sách chặn
- Session xuất phát từ Nga (địa lý dữ liệu)
- KHÔNG thuộc holdout group (nhóm kiểm soát A/B test)

**Không đủ điều kiện:**
- Khách lần đầu (phục vụ bằng chương trình WS-1 thay thế)
- Chronic shoppers tháng 10 (phục vụ WS-2)
- Guest thanh toán (không có user_id để phân loại)

---

## 4. Đặc Tả Tính Năng

### Nút mua ngay tại giá tiền
**Các trường hợp kiểm thử A/B test:**
- V1: "Mua Ngay — Giá Khóa 15 phút"
- V2: "Fast Buy — Bỏ Qua Giỏ Hàng"
- V3: "1-Click Purchase (Giá Hiện Tại)"

**Hành vi:**
- Chỉ hiển thị cho nhóm khách hàng đủ điều kiện 
- Vô hiệu hóa nếu item hết hàng
- Ẩn trên mobile <360px width (fallback về luồng chuẩn)

### Cơ Chế Price-Lock
**Kích hoạt:** Khi user đủ điều kiện xem product page lần đầu trong Black Friday Week
**Thời lượng:** 15 phút kể từ lần xem đầu tiên (lưu trên session + user)
**Phạm vi:** Theo từng SKU, theo từng user
**Edge cases:**
- Nếu giá giảm thêm trong thời gian khóa → áp dụng giá thấp hơn (user-friendly)
- Nếu hết hàng → thông báo nhẹ nhàng "No longer available at this price"
- Nếu khóa hết hạn trước thanh toán → hiển thị giá mới với thông báo rõ ràng "Price updated" (không tính phí thầm lặng)

### Thanh toán nhanh không dùng giỏ hàng
**Luồng:**
1. User nhấn "Buy Now" → Đến thẳng trang thanh toán đã điền sẵn (dựa vào thông tin lần mua trước - có cho phép thay đổi nếu người dùng cần)
2. Phương thức thanh toán mặc định được chọn sẵn (từ lần mua trước)
3. Địa chỉ giao hàng mặc định được chọn sẵn
4. Xác nhận hành động mua sản phẩm X với giá thành Y.
5. Trang xác nhận với mã đơn hàng

**Fallback:** Nếu user chưa có thanh toán/địa chỉ đã lưu → dùng thanh toán chuẩn nhưng giữ nguyên price lock


### Ẩn Sale Banner
**Kích hoạt:** User đủ điều kiện ghé thăm bất kỳ trang nào trong Black Friday Week
**Hành vi:** Ẩn sale banner đầu trang (vi dụ dải đỏ "70% OFF — Black Friday!")
**Lý do:** Ngăn sale noise gây decision paralysis

**Phạm vi:** Chỉ global sale banner, không ảnh hưởng hiển thị giá ở product level

**Fallback:** Nếu user chủ động điều hướng đến trang `/sale` → hiển thị đầy đủ sale UI (tôn trọng ý định user)

---

## 5. Đo lường dữ liệu

### Sự kiệns Cần Theo Dõi 
- `ws3_badge_shown` — Fast-Buy badge được render
- `ws3_badge_clicked` — User nhấn Fast-Buy
- `ws3_price_lock_set` — Giá bị khóa cho user+SKU
- `ws3_price_lock_honored` — Thanh toán dùng giá đã khóa
- `ws3_price_lock_expired` — Khóa hết hạn trước khi dùng
- `ws3_fast_thanh toán_started` — User vào trang fast-thanh toán
- `ws3_fast_thanh toán_completed` — Đơn hàng đã xác nhận
- `ws3_sale_banner_suppressed` — Banner ẩn cho user đủ điều kiện
- `ws3_classification_result` — Kết quả phân loại nhóm khách hàng được ghi lại

### Bảng biểu Panels 
1. Tỷ lệ Giữ Lại Direct Flow — Treatment vs Control, theo giờ
2. Funnel Fast-Thanh toán — Shown → Clicked → Completed
3. Sử dụng price-lock — phân tích Set / Honored / Expired
4. Trạng thái Guardrail — đèn tín hiệu Xanh/Vàng/Đỏ
5. Tác động GMV — GMV tăng thêm từ nhóm treatment

---

## 6. Tiêu Chí Nghiệm Thu

Các chỉ số dưới đây được ánh xạ trực tiếp từ Mục tiêu Chiến lược của PRD (Target: Giữ chân 30% luồng thanh toán mua ngay, tương đương thu về $12.2M). 
![traffic](/docs/assets/images/hourly_traffic_gmv.png)

### Chấp nhận Triển khai (Xanh)
- **Chỉ số chính:** Tỷ lệ giữ chân luồng Direct đạt **>= 30%** (dựa trên mục tiêu PRD đề ra).
- **Guardrails:** Tất cả đều xanh - Không có vi phạm nào kéo dài quá **1 giờ với khung giờ vàng (08:00 - 17:00)** hoặc **3 giờ (ngoài khung giờ vàng).** Dữ liệu thực tế cho thấy vào Giờ Vàng, mỗi giờ hệ thống tạo ra tới 4.75$ triệu GMV.
- **Đo lường phụ:** Tỷ lệ hoàn tất thanh toán qua nút Fast-checkout phải cao hơn tỷ lệ qua luồng Giỏ hàng thông thường.

### Cần Tối ưu thêm (Vàng)
- **Chỉ số chính:** Tỷ lệ giữ chân đạt **20% đến 29%** (Có cải thiện so với đáy rớt phễu, nhưng chưa đạt ngưỡng kỳ vọng 30%).
- **Hành động:** Tiếp tục A/B Test, tối ưu lại giao diện nút bấm (UI/UX) và kiểm thử lại trong Flash Sale tiếp theo.

### Hủy bỏ Tính năng (Đỏ)
- **Chỉ số chính:** Tỷ lệ giữ chân **< 20%** (Tính năng thất bại, khách VIP vẫn rớt phễu hoặc phớt lờ nút Mua Ngay).
- **Hoặc:** Bất kỳ chỉ số Guardrail nào bị báo Đỏ liên tục trong **1 giờ vàng (08:00 - 17:00)** hoặc **3 giờ (ngoài khung giờ vàng)** 
- **Hành động:** Tự động tắt tính năng (Rollback), họp đội ngũ Data & Product để phân tích nguyên nhân gốc rễ .
