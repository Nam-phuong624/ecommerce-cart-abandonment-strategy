## 1. Tóm Tắt

**Vấn đề:** **1,185,902** users duyệt web nhiều trong tháng 10 (trung bình **16.1** lượt xem/user) nhưng chưa bao giờ mua — họ là "chronic window shoppers." Họ quay lại tháng 11 sau khoảng ngủ đông **20.0** ngày và bỏ lại **$42.2M** giỏ hàng trong đợt cao điểm. Tỷ lệ tự phục hồi tự nhiên chỉ đạt **7.1%**.

**Giả định:** tâp trung vào những user đã thêm các sản nhận biết hoạt động tháng 10 (cảnh báo price-drop cho items đã xem + bundle cá nhân hóa + FOMO urgency) có thể đẩy tỷ lệ phục hồi từ 7.1% lên **≥22.5%**, mang về **$6.5M** cho sự kiện Black Friday.

**Lý do:** Đây là nhóm khách hàng có mức cơ sở ý định cao hơn khách mới, nhưng họ trì hoãn. Việc cá nhân hóa giá trị sẽ biến sự trì hoãn thành hành động chốt đơn.

---

## 2. Kịch Bản Người Dùng

> **Với tư cách là** người mua hàng quay lại, đã truy cập website và thêm sản phẩm vào giỏ hàng trước đó nhưng chưa thanh toán,
> **Khi** một sản phẩm tôi đã xem trong tháng 10 giảm giá trong Black Friday,
> **Tôi muốn** được thông báo để không bỏ lỡ deal,
> **Để** công sức nghiên cứu của tôi có giá trị thay vì bị lãng phí.

**Acceptance Criteria:**
- GIVEN tôi được phân loại là nhóm khách hàng `other_oct` (duyệt web tháng 10 không mua)
- WHEN một item tôi đã xem giảm xuống mức giá Black Friday mới
- THEN tôi nhận Thông báo Trong ứng dụng cảnh báo giá mới trong vòng 24h sau khi giảm
- AND thông báo hiển thị đúng item tôi đã xem + giá hiện tại + giá gốc tháng 10
- AND click vào dẫn đến lưu sản phẩm vào giỏ hàng.

---

## 3. Đối Tượng & Điều Kiện

**Đủ điều kiện:**
- `user_id` có hoạt động tháng 10 nhưng không có lần mua nào.
- Số lượt xem tháng 10 ≥3 
- App cài đặt + đã chấp nhân chính sách theo dõi hành vi trên website của người dùng
- Không nằm trong các user sử dụng trong quá trình kiểm thử

**Không đủ điều kiện:**
- Người mua tháng 10 (phục vụ WS-3 nếu là Direct, hoặc không treatment nếu là Giỏ hàng)
- Users chỉ có tháng 11 (phục vụ WS-1)

---

## 4. Đặc Tả Tính Năng

### Khung thông báo hiển thị giá mới của sản phẩm 
**Kích hoạt:** Sản phẩm user đã xem trong tháng 10 giảm ≥10% so với giá hiện tại
**Nội dung:**
- Hình ảnh hero của item đã xem
- "Bạn đã xem sản phẩm này tháng 10 — nay giảm X%"
- Giá tháng 10 (gạch ngang) → giá hiện tại
- CTA: "Add to Giỏ hàng" (1-click deep link)
- Scarcity: "N người đang xem sản phẩm này" (nếu stock thấp)

**Frequency cap:** 1 Push mỗi item mỗi user mỗi 14 ngày

### Gợi sản phẩm theo nhóm nhu cầu của khách hàng
**Kích hoạt:** User đã xem items từ ≥2 category trong tháng 10
**Cơ chế:** Gợi ý các sản phẩm tương ứng bổ sung theo nhóm sản phẩm user đã xem, có kèm combo giảm giá khi mua chung.
**Ví dụ:** Đã xem laptop + túi → "Bundle laptop + túi = giảm 5% khi mua cùng"
**Phân phối:** Trong ứng dụng Notification + on-site widget trên product page

### Thông báo tạo cảm giác cấp bách, nhằm buộc người dùng ra quyết định nhanh
**Vị trí:** Banner đầu site cho nhóm khách hàng đủ điều kiện trong Black Friday Week
**Các biến thể copy:**
- "Sale kết thúc trong [countdown] — items trong Oct giỏ hàng của bạn đang bán nhanh"
- "N items từ Oct wishlist của bạn sắp hết hàng"
- "Cảnh báo giảm giá: [tên item] vừa đạt giá thấp nhất 6 tháng"

**Quy tắc:**
- Chỉ hiển thị cho nhóm khách hàng trong Black Friday Week
- Có thể đóng, tôn trọng X của user
- Không ghép với promo khác

### Gợi nhắc những sản phẩm trong giỏ hàng chưa thanh toán
**Kích hoạt:** User quay lại tháng 11, có Oct giỏ hàng chưa hoàn thành
**Hành vi:** Hiển thị "Welcome back! Oct giỏ hàng của bạn vẫn còn đây" với items đã điền sẵn ở giá mới
**Minh bạch:** Thông báo rõ ràng về thay đổi giá nếu khác với lúc xem tháng 10

---

## 5. Đo lường dữ liệu

### Sự kiệns
- `ws2_price_drop_noti_sent` / `_opened` / `_clicked` / `_converted`
- `ws2_bundle_offer_shown` / `_added_to_giỏ hàng` / `_purchased`
- `ws2_fomo_banner_shown` / `_clicked` / `_dismissed`
- `ws2_oct_giỏ hàng_resurrect_shown` / `_restored` / `_purchased`

### Bảng biểu Panels
1. Tỷ lệ tái kết nối theo biến thể
2. Notification funnel theo kênh
3. Tỷ lệ bundle attach (% đơn hàng có bundle)
4. Theo dõi kích thước nhóm khách hàng (bao nhiêu "kích hoạt" từ chronic → buyer)


---

## 6. Tiêu Chí Nghiệm Thu

Các chỉ số dưới đây được ánh xạ trực tiếp từ mục tiêu trong PRD. Mục tiêu nâng tỷ lệ phục hồi của nhóm khách hàng đã thêm giỏ hàng nhưng chưa thanh toán trong tháng 10, đến tháng 11 mới thanh toán (nhóm Chronic Shoppers) lên 22.5%, tương đương mang về $6.5M.

### Chấp nhận Triển khai (Xanh)
- **Chỉ số chính:** Tỷ lệ phục hồi đạt **>= 22.5%**
- **Guardrails:** Tất cả đều xanh - Không có vi phạm nào kéo dài quá **1 giờ với khung giờ vàng (08:00 - 17:00)** hoặc **3 giờ (ngoài khung giờ vàng).**
- **Đo lường phụ:** Tỷ lệ khách hàng mua thêm sản phẩm kèm theo (dựa trên tính liên quan của sản phẩm đã mua) đạt > 10% tổng số đơn phục hồi.

### Cần Tối ưu thêm (Vàng)
- **Chỉ số chính:** Tỷ lệ phục hồi đạt **9.1% đến 22.5%**
- **Hành động:** Tiếp tục A/B Test, điều chỉnh lại Logic gợi ý Bundle hoặc thay đổi thuật toán Price-Drop, kiểm thử lại trong sự kiện Flash Sale tiếp theo.

### Hủy bỏ Tính năng (Đỏ)
- **Chỉ số chính:** Tỷ lệ phục hồi **< 9.1%**, hoặc tỷ lệ hủy đăng ký vượt mốc 1%.
- **Hoặc:** Lợi nhuận biên bị phá hủy do chiết khấu Price-drop chồng chéo lên nhau.
- **Hoặc:** Bất kỳ chỉ số Guardrail nào bị báo Đỏ liên tục trong **1 giờ vàng (08:00 - 17:00)** hoặc **3 giờ (ngoài khung giờ vàng)**.
- **Hành động:** Tự động tắt hệ thống Retargeting (Rollback) và tiến hành tìm ra nguyên nhân gốc rễ.
