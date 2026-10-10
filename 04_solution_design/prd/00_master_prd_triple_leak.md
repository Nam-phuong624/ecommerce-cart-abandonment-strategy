# Product Requirement Document
---

## 1. Tóm Tắt Vấn Đề 

Giai đoạn đỉnh điểm 4 ngày Black Friday rò rỉ hơn ****$82.8M**** GMV từ 3 nhóm khách hàng khác biệt (New Users **$27.0M**, Chronic Shoppers **$42.2M**, Cannibalized VIPs $13.6M). Mỗi cohort có profile ý định và tỷ lệ tự phục hồi riêng (21% / 26% / 39%). Một playbook chung duy nhất phục vụ kém cả 3 phân khúc. Chương trình này xây dựng **cohort-aware recovery infrastructure** để thu về **$21.4M** mỗi sự kiện, mở rộng lên $100M+ hàng năm cho 7 flash sales.

**Định nghĩa thành công:** Đến cuối sự kiện Black Friday năm 1, chứng minh được ít nhất $30M GMV tăng thêm với ROI ít nhất 10×.

---

## 2. In Scope & Out of Scope

### In Scope
- Phân lọai user theo thời gian thực
- Xây dựng kết hợp 3 luồng trải nghiệm người dùng khác nhau
- Tiến hành kiểm thử A/B cho từng luồng trải nghiệm người dùng
- Xây dựng Dashboard thống kê và phân tích cho từng nhóm

### Out of Scope
- Tối ưu hóa infra/latency (đội CTO thực hiện song song)
- Cải tổ chiến lược giá
- Chương trình loyalty (sáng kiến tương lai)
- Mở rộng quốc tế
- Full post-purchase retention engine (phase 2+)

---

## 3. Users & Personas

### Persona A — New User
- Lần đầu ghé thăm trong đợt marketing Black Friday
- Hành động theo cảm xúc, nhạy cảm với giá, tập trung ngắn hạn
- Dành tới 3.4 sessions để lướt xem trung bình 16.0 sản phẩm, nhưng cực kỳ đắn đo và rớt phễu chỉ sau 0.9 lần thêm vào giỏ
- 7.2% tự phục hồi → để lại 92.**16.2%** cơ hội
- **Cần:** Discount rõ ràng, tạo urgency, tín hiệu tin tưởng, không ma sát

### Persona B — Chronic Shopper
- Người dùng cực kỳ tích cực trong tháng 10 (Đánh giá sản phẩm rất cẩn thận tới 39.9 lượt xem, nhưng quyết không chốt đơn)
- Quay lại sau đúng 23 ngày để săn Sale Black Friday với cùng pattern ngâm giỏ hàng
- 20.0% tự phục hồi nhưng cần kích hoạt
- **Cần:** Thông báo price-drop cho items đã xem, FOMO, cá nhân hóa

### Persona C — VIP
- Người mua habitual 1-click (Tháng 10: 100% mua trực tiếp, 0% rớt phễu)
- Bị phá vỡ bởi cơ chế khuyến mãi Black Friday: có thể đang bị ảnh hưởng bởi cập nhật UI dẫn đến 55.6% khách hàng rớt phễu.
- **Cần:** đánh giá lại thao tác người dùng dành cho tập khách hàng.

---

## 4. Kiến trúc đề xuất

### Luồng Tổng Quan
```
User đến → Cohort Classifier → Routing Engine → UX theo từng Cohort
     |                                                      |
Event stream <-- <-- <-- <-- <-- <-- <-- <-- <-- <-- Behavior tracker
     |
Recovery Trigger Service → [Email | Push | On-site] → Đo lường
```

### Kiến Trúc Hệ Thống (Các Khối Động Cơ Cốt Lõi)

Để 3 giải pháp (Workstreams) hoạt động tự động và chính xác ở quy mô hàng triệu users, Đội ngũ Kỹ thuật cần xây dựng 3 khối động cơ chạy ngầm phía sau:

**C1 — Bộ Phân Loại Khách Hàng Thời Gian Thực**
- **Mục đích:** Khi một User vừa truy cập vào app/web, hệ thống phải nhận diện ngay lập tức họ là ai (VIP, Thợ săn sale, hay Khách mới) để hiển thị giao diện phù hợp.
- **Cách hoạt động:** Quét mã `user_id` và lịch sử Tháng 10. Trả về nhãn (Output) chỉ định nhóm Cohort.
- **Yêu cầu:** Phải xử lý cực nhanh (Độ trễ mong muốn < 50ms) để kịp ẩn banner Sale hoặc hiển thị nút Fast-checkout cho VIP ngay khi trang web vừa tải xong.

**C2 — Pipeline Giám Sát Hành Vi**
- **Mục đích:** Là "camera giám sát" để phát hiện khoảnh khắc khách hàng định rời bỏ (Rớt phễu).
- **Cách hoạt động:** Thu thập liên tục thao tác (Xem, Thêm vào giỏ, Bắt đầu Checkout). Hệ thống sẽ làm giàu dữ liệu bằng cách tính tổng tiền trong giỏ (Cart value) và chấm điểm ý định mua (Intent Score).
- **Phân phối:** Bắn dữ liệu ngay lập tức về Động cơ C3 để kích hoạt chiến dịch cứu vớt, đồng thời lưu vào Database để Data Team làm Dashboard.

**C3 — Động Cơ Ra Quyết Định Cứu Vãn**
- **Mục đích:** Đóng vai trò là cơ chế trigger dựa trên thông tin kết hợp từ C1 và C2.
- **Quy tắc:** Nếu C1 báo "Thợ săn sale" + C2 báo "Ngâm giỏ hàng 3 tiếng" $\rightarrow$ C3 tự động bóp cò hiển thị 1 Hộp thông báo (Notification Box) cảnh báo giá giảm (Price-drop alert).
- **Điều phối Đa kênh:** Quyết định sẽ chặn người dùng lại bằng Popup ngay trên màn hình (On-site widget) hay để họ thoát ra rồi mới gửi Push Notification.
- Suppression logic: không gửi trùng trong 24h

**C4 — Hệ Thống Giao Diện Tương Tác**
- **Mục đích:** Triển khai phương thức tiếp cận trực tiếp trên giao diện.
- **Cách hoạt động:** Hiển thị Popup giảm giá cho Khách mới ngay khi họ định vuốt thoát App/Web (Exit-intent), hoặc đẩy một Notification Box (Hộp thông báo) nổi bật trên giao diện cho Thợ săn sale ngay khi họ vừa mở App trở lại.

**C5 — Nền Tảng Thử Nghiệm & Tự Bảo Vệ**
- **Mục đích:** Đảm bảo hệ thống không "phát nhầm" mã giảm giá hàng loạt gây thâm hụt lợi nhuận.
- **Cách hoạt động:** Mọi chiến dịch đều được chia tập khách hàng ra để Test (A/B Testing). Đặc biệt, hệ thống có cài sẵn cơ chế Guardrail. Nếu phát hiện lợi nhuận biên sụt giảm quá 2% trong 3 giờ liên tục, tính năng sẽ tự động vô hiệu hóa để bảo vệ dòng tiền.

**C6 — Dashboard**
- **Mục đích:** Cung cấp bức tranh toàn cảnh về tiến độ tối đa hóa dòng tiền cho công ty dành cho C-level.
- **Chỉ số theo dõi:** Cập nhật real-time số tiền GMV thất thoát đang được khôi phục. Hiển thị chi tiết tỷ lệ chuyển đổi của từng nhóm (VIP, New, Chronic). Kèm theo hệ thống đèn tín hiệu Xanh/Đỏ để cảnh báo sức khỏe toàn hệ thống.

---

## 5. Chi Tiết Các Giải Pháp (Workstreams)

### WS-1: Chương Trình Cứu Vãn Khách Mới (Quy mô rò rỉ: **$27.0M**)
- **Mục tiêu:** Chặn việc khách hàng lần đầu ghé thăm ứng dụng rời đi mà không mua hàng.
- **Giải pháp cốt lõi:**
  - **Popup cản đường (Exit-intent):** Hệ thống nhận diện khoảnh khắc khách định vuốt thoát App/Web để tung ngay mã giảm giá 10-15% chốt đơn tức thì.
  - **Nhắc nhở qua Push Notification:** Gửi thông báo đẩy liên hoàn vào các mốc 1 giờ, 24 giờ, và 72 giờ sau khi rớt phễu để hối thúc họ quay lại giỏ hàng.
  - **Mồi nhử Miễn phí vận chuyển:** Tự động thông báo "Chỉ mua thêm $X nữa để được Free Ship".
- **Chỉ số thành công:** Tỷ lệ vớt đơn đạt **16.2%** (Mục tiêu thu về: **$2.7M**).

### WS-2: Tái Kết Nối "Thợ Săn Sale" (Quy mô rò rỉ: **$42.2M**)
- **Mục tiêu:** Kích hoạt lại những người đã kiên nhẫn ngâm giỏ hàng suốt tháng 10 chỉ để chờ giá giảm chạm đáy vào đợt Black Friday.
- **Giải pháp cốt lõi:**
  - **Báo động giá giảm (Price-drop Alert):** Bắn thông báo (Push/In-app) ngay lập tức khi món đồ họ ngâm trong giỏ vừa được kích hoạt giá Flash Sale.
  - **Hộp nhắc nhở "Vẫn đang suy nghĩ?":** Hiển thị hộp thông báo cá nhân hóa ngay trên màn hình chính khi họ mở lại app.
  - **Tạo cảm giác khan hiếm (FOMO):** Cảnh báo "Sắp hết hàng" hoặc "Hết hạn giảm giá" để ép họ ra quyết định nhanh.
- **Chỉ số thành công:** Tỷ lệ quay lại chốt đơn đạt 6% (Mục tiêu thu về: $6.5M).

### WS-3: Bảo Vệ Dòng Tiền Nhóm VIP (Quy mô rò rỉ: $13.6M)
- **Mục tiêu:** Dỡ bỏ mọi rào cản thao tác phức tạp, trả lại luồng mua sắm "1 chạm" quen thuộc cho tệp khách VIP.
- **Giải pháp cốt lõi:**
  - **Trả lại nút Mua Ngay:** Đưa nút thanh toán trực tiếp hiển thị trở lại cho nhóm VIP, cho phép họ bỏ qua hoàn toàn bước vào Giỏ hàng rườm rà.
  - **Ẩn quảng cáo:** Xóa bỏ các popup sale không cần thiết để làm sạch giao diện cho những VIP đã có sẵn ý định mua.
  - **Cam kết giữ giá:** Khóa mức giá ưu đãi trong 15 phút để VIP an tâm chốt đơn ngay lập tức.
- **Chỉ số thành công:** Tỷ lệ giữ chân người mua trực tiếp đạt 30% (Mục tiêu thu về: $12.2M).

---

## 6. Hệ thống tự động bảo vệ (Guardrails)

Trong quá trình chạy A/B Testing cho 3 giải pháp trên, hệ thống được cài đặt các **Chỉ số an toàn**. Nếu bất kỳ chỉ số nào chạm ngưỡng vi phạm dưới đây trong 3 giờ liên tục (**Cơ sở logic:** 3 giờ trong BF sinh ra đủ Sample Size để đạt Stat Sig, giúp né nhiễu dữ liệu nhưng vẫn kịp cắt lỗ nhanh), hệ thống sẽ tự động vô hiệu hóa chiến dịch để bảo vệ nền tảng:

- **Tỷ lệ tắt Push Notification / Xóa App > 1%:** Bảo vệ trải nghiệm, tránh spam gây hiệu ứng ngược.
- **Giá trị đơn hàng trung bình (AOV) toàn sàn giảm > 5%:** Ngăn chặn tình trạng khách bòn mót mã giảm giá thay vì mua nguyên giá.
- **Chi phí phát mã Discount > 20% GMV khôi phục:** Bảo vệ biên lợi nhuận, không cứu vớt dòng tiền bằng mọi giá.
- **Độ trễ hệ thống (Latency P95) > 3s:** Tránh việc Model phân loại Cohort chạy quá nặng làm sập/lag trang web trong giờ cao điểm.

---

## 7. Đánh Giá Rủi Ro & Biện Pháp Giảm Thiểu

| Rủi ro Kỹ thuật & Vận hành | Mức độ | Biện pháp giảm thiểu (Mitigation) |
|---|---|---|
| Thuật toán phân loại Cohort nhận diện sai (False Positives) | <span style="color:#d62728; font-weight:bold">🔴 Cao</span> | Chạy mô hình ở chế độ "Shadow Mode" (chỉ ghi log, không hiển thị UI) trong 2 ngày đầu Black Friday để kiểm định độ chính xác của AI. |
| Khách hàng chia sẻ mã giảm giá Exit-intent ra các hội nhóm săn Sale | <span style="color:#ff7f0e; font-weight:bold">🟠 Trung bình - Cao</span> | Mã giảm giá được sinh ngẫu nhiên, khóa cứng theo định danh `user_id` và chỉ có hiệu lực đếm ngược trong 15 phút. |
| Tỷ lệ khách hàng tắt Push Notification tăng đột biến do bị làm phiền | <span style="color:#d62728; font-weight:bold">🔴 Cao</span> | Thiết lập giới hạn tần suất (Frequency cap) tối đa 1 Thông báo/User/Ngày. Kích hoạt ngay Guardrail nếu vi phạm. |
| Tính năng Fast-checkout làm giảm cơ hội Cross-sell (Bán chéo) | <span style="color:#2ca02c; font-weight:bold">🟢 Trung bình</span> | Chỉ mở khóa Bypass Giỏ hàng cho riêng tập VIPs (những người vốn dĩ đã có hành vi mua trực tiếp, không có thói quen mua chéo). |
