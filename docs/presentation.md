# Bài Thuyết Trình Ban Lãnh Đạo — BF Triple-Leak Playbook

**Định dạng:** Bullet points sẵn sàng cho slide. Mỗi `##` là một slide.
**Thời lượng:** 15 phút + Q&A
**Đối tượng:** CEO, CFO, CMO, VP Product, VP Eng

---

## Slide 1 — Tiêu Đề

### Bảo Vệ Doanh Thu Black Friday
**Chẩn đoán $377.9M rò rỉ, mở khóa $100M+ phục hồi hàng năm**

Analytics + Product Team
2026-10-08

---

## Slide 2 — Mở Đầu

> ### "Trong Black Friday 2019, chúng ta thu được $275M.
> ### Nhưng ĐỒNG THỜI cũng để rò $378M.
> ### Hôm nay tôi sẽ chỉ cho bạn cách lấy lại $100M+ trong năm tới."

---

## Slide 3 — Bức Tranh Tổng Thể

- **Tháng 11/2019 so với baseline tháng 10:**
  - Traffic: +49%
  - Carts: +204% [OK]
  - Purchases: +23% [Cảnh báo]
  - **GMV at risk: +286%** [Cao]

- **Conversion tăng KHÔNG TUYẾN TÍNH so với traffic.**
- **Chúng ta chuẩn bị hạ tầng cho traffic — nhưng không chuẩn bị cho conversion.**

---

## Slide 4 — Vượt Ra Ngoài Cart Abandonment

**Quan điểm thông thường:** "Cart abandonment lớn — hãy phục hồi nó."

**Phát hiện của chúng ta:** Đây KHÔNG phải một vấn đề. Đây là BA vấn đề.

```
+----------------------------------------------+
|  COHORT                 GMV AT RISK   SOLUTION|
+----------------------------------------------+
|  [Cao] New Users (sale) $154M (41%)   KHAC   |
|  [TB cao] Chronic       $160M (42%)   KHAC   |
|  [TB] Cannibalized VIPs  $23M (6%)    KHAC   |
+----------------------------------------------+
```

Cùng triệu chứng (bỏ giỏ hàng), **nguyên nhân và cách chữa hoàn toàn khác nhau**.

---

## Slide 5 — Insight Mới: Cannibalization

**Khách hàng VIP 1-click tốt nhất của chúng ta:**

- Tháng 10: **0% abandonment** · checkout 90 giây · 1 item/giỏ
- Tuần BF tháng 11: **56% abandonment** · quyết định 613 giây · 1.78 items/giỏ

**Black Friday đang PHÁ VỠ thói quen mua hàng của những khách hàng tốt nhất chúng ta.**

Và thiệt hại kéo dài: abandon rate 30%+ tiếp diễn vào các tuần non-BF.

---

## Slide 6 — Bằng Chứng: Direct Flow Sụp Đổ

**Luồng Mua Trực Tiếp Tháng 10 → Tháng 11:**

- Tháng 10: 337,699 sessions (53.64% số đơn hàng)
- Tháng 11: 124,841 sessions (16.15% số đơn hàng)
- **Sụt giảm: -$63.9M GMV biên lợi nhuận cao**

**Chính banner sale là tác nhân kích hoạt cannibalization.**

---

## Slide 7 — Giải Pháp: Triple Playbook

### 3 chương trình theo cohort, 1 hạ tầng dùng chung

```
+-------------------------------------------------+
|  DÙNG CHUNG: Classifier | Event Pipeline | A/B  |
+-------------------------------------------------+
|  WS-1   |  New User Discount Program           |
|         |  Exit-intent + email + shipping      |
|         |  $15M mỗi sự kiện BF                 |
+-------------------------------------------------+
|  WS-2   |  Chronic Re-engagement               |
|         |  Price-drop + bundles + FOMO         |
|         |  $13M mỗi sự kiện BF                 |
+-------------------------------------------------+
|  WS-3 * |  VIP Direct Flow Protection (MVP)   |
|         |  Price-lock + fast-checkout          |
|         |  $18M mỗi sự kiện BF                 |
+-------------------------------------------------+
```

**Tổng cộng: $46M mỗi sự kiện BF · $100M+ hàng năm · ROI 17×**

---

## Slide 8 — Tại Sao MVP Bắt Đầu Với VIPs (Không Phải $ Lớn Nhất)

| Workstream | Quy Mô | Độ Tin Cậy | Lý Do Thứ Tự? |
|---|---|---|---|
| WS-3 VIPs | 37K | **Cao nhất** | Cohort sạch, dữ liệu phong phú, ship nhanh nhất |
| WS-1 New Users | 245K | Trung bình | $ lớn nhất, nhưng intent nhiễu |
| WS-2 Chronic | 217K | Trung bình | Cần hạ tầng cá nhân hóa |

**Ra mắt với cohort nhỏ/sạch nhất → xác nhận phương pháp → nhân rộng learnings.**

---

## Slide 9 — Đầu Tư & ROI

| | Trường Hợp Cơ Sở | Tích Cực |
|---|---|---|
| **Mỗi sự kiện BF** | | |
| GMV phục hồi | $46M | $82M |
| Lợi nhuận gộp (15%) | $6.9M | $12.3M |
| **Hàng năm (7 sự kiện)** | | |
| GMV phục hồi | $322M | $574M |
| Lợi nhuận gộp | $48M | $86M |
| **Đầu Tư** | | |
| Setup (một lần) | $240K | $240K |
| Annual opex | $2.5M | $2.5M |
| **Ròng Năm 1** | **$43M** | **$81M** |
| **ROI Năm 1** | **17×** | **30×** |

---

## Slide 10 — Timeline (90 Ngày)

```
W1-W4   Foundation + MVP build
W5-W8   WS-3 VIP test → ship/kill
W9-W12  WS-1 New User build & test
W11-W14 WS-2 Chronic build & test
W15-W16 Dry-run validation
→ BF Năm 2 SẴN SÀNG
```

4 phase gate với tiêu chí Go/Kill. CEO + CFO review tại W4, W8, W16.

---

## Slide 11 — Rủi Ro (Và Biện Pháp Giảm Thiểu)

| Rủi Ro | Biện Pháp Giảm Thiểu |
|---|---|
| Độ chính xác cohort classifier | Shadow mode 2 tuần + kiểm tra thủ công |
| Email deliverability khi BF đỉnh điểm | Pre-warm IP + đa dạng hóa ESP |
| Sự cố nền tảng | Widget dự phòng on-site + SLA |
| Chi phí discount leo thang | Guardrail: cost ≤15% phục hồi + auto-rollback |
| Pháp lý (price-lock, GDPR) | Review pháp lý Tuần 1 |

---

## Slide 12 — Những Gì Tôi Cần Từ Các Bạn

**CEO:**
- Phê duyệt $240K setup + $2.5M annual opex
- Phê duyệt phân bổ 11 FTE trong 16 tuần

**CFO:**
- Xác nhận giả định mô hình ROI (gross margin 15%)

**CMO:**
- Thống nhất mức trần discount an toàn với thương hiệu
- Quyền sở hữu kênh email

**CTO:**
- Phân bổ nhóm kỹ thuật (critical path)

**Quyết định yêu cầu:** Go/no-go MVP 90 ngày

---

## Slide 13 — Câu Kết Luận Duy Nhất

> ### "Black Friday không mở rộng quy mô kinh doanh của chúng ta.
> ### Nó đang cannibalize khách hàng tốt nhất của chúng ta.
> ### Triple-Leak Playbook mở khóa $100M+ bằng cách giải quyết đúng vấn đề cho đúng cohort."

---

## Slide 14 — Hỏi & Đáp

### Tài liệu hỗ trợ:
- BA Brief đầy đủ (12 phần)
- Sizing xlsx tương tác (thay đổi giả định trực tiếp)
- Live dashboard (HTML, mở trong trình duyệt)
- Master PRD + MVP PRD + Experiment Roadmap + Rollout Plan
- Kiến Trúc Kỹ Thuật (Mermaid diagrams)

**Tất cả trong thư mục dự án:** `/`

---

## Phụ Lục A — Nếu Hỏi "Bạn Tự Tin Đến Mức Nào Với $46M?"

- Các số liệu được xác minh qua 6 giai đoạn DA + lần xác minh tường minh (Giai đoạn 5)
- Tự phát hiện overclaim: cannibalization $42M → $23M (strict cohort)
- Đã đối chiếu: 3 cohort cộng lại $337.5M (89%) của tổng $377.9M
- Benchmarks ngành: 10% phục hồi là bảo thủ (các chương trình tốt nhất đạt 20-30%)
- Bảng sensitivity: ngay cả worst case (5% uplift, 25% discount) vẫn đạt $30M+ mỗi sự kiện BF

## Phụ Lục B — Nếu Hỏi "Tại Sao Không Dùng Công Cụ Abandonment Hiện Có?"

- Các công cụ hiện tại gửi cùng một email cho tất cả mọi người
- Dữ liệu của chúng ta cho thấy 3 cohort cần **3 thông điệp hoàn toàn khác nhau**:
  - New User: discount + tín hiệu tin tưởng
  - Chronic: price-drop trên các items cụ thể + FOMO
  - VIP: KHÔNG discount, chỉ loại bỏ ma sát (banner suppression, fast-checkout)
- Phương pháp đại trà nắm bắt ~10% cơ hội; phương pháp theo cohort nắm bắt ~30%+

## Phụ Lục C — Nếu Hỏi "Rủi Ro Lớn Nhất Là Gì?"

- Không phải kỹ thuật. Không phải ngân sách. **Mà là tổ chức.**
- Yêu cầu Marketing + Product + Eng + Data phối hợp trong timeline 90 ngày
- Biện pháp giảm thiểu: Phase gate với sự giám sát của CEO ngăn ngừa trượt tiến độ im lặng
- Kế hoạch dự phòng: Ngay cả khi chỉ ship WS-3 (nhỏ nhất) vẫn đem lại $18M mỗi sự kiện BF

---

## Phụ Lục D — Câu Tóm Tắt Portfolio

> *"Phát hiện Black Friday cannibalize $23M từ khách hàng VIP 1-click tại e-commerce Nga (abandonment 0% → 56%, thời gian quyết định tăng 6.8×). Thiết kế Triple-Leak Protection Playbook mở khóa $46M+ mỗi sự kiện BF với ROI 17× năm 1 trên 3 cohort khách hàng khác nhau."*
