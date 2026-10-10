# Talk Track Phỏng Vấn — Case Study BF Triple-Leak

**Mục đích:** Câu trả lời chuẩn bị sẵn cho phần thuyết trình portfolio + phỏng vấn hành vi.

---

## Pitch 30 Giây (Elevator)

> *"Tôi đã phân tích 110 triệu events từ clickstream của một sàn thương mại điện tử Nga trong dịp Black Friday và phát hiện ra 'hiệu ứng cannibalization' trị giá $23M, trong đó các sự kiện sale biến những người mua VIP 1-click quen thuộc thành những người đắn đo bỏ giỏ hàng — tỷ lệ abandon của họ nhảy từ 0% lên 56%. Tôi đã thiết kế Triple-Leak Protection Playbook với 3 chương trình phục hồi theo cohort, dự kiến $46M+ doanh thu tăng thêm mỗi sự kiện BF với ROI 17× năm 1. Dự án thể hiện full-stack analytics: data engineering, 6 giai đoạn phân tích dữ liệu, framing business, và product management."*

---

## Pitch 90 Giây (Trình Bày Portfolio)

> *"Dự án bắt đầu là phân tích cart abandonment sử dụng dataset REES46 e-commerce. Pivot đầu tiên: dataset cosmetics ban đầu có AOV $0.52 — quá nhỏ để tạo ra câu chuyện đáng tin cậy. Tôi chuyển sang multi-category electronics (AOV $360, 110M events).*
>
> *Pivot thứ hai đến từ chiều sâu phân tích. Framing chuẩn là 'cart abandonment lớn.' Tôi đào sâu hơn: so sánh baseline tháng 10 với Black Friday tháng 11, phát hiện tháng 11 có $533M at risk — gần 3× tháng 10. Sau đó phân tích Giai đoạn 3 cho thấy 53% lượt mua trong tháng 10 là 'direct purchase' hoàn toàn bypass cart. Giai đoạn 4 theo dõi những user VIP đó vào hành vi tháng 11 và thấy 37% di chuyển sang cart flow trong BF — abandon tăng từ 0% lên 56%, thời gian quyết định tăng từ 90 giây lên 613 giây. BF đang phá vỡ những khách hàng tốt nhất của chúng ta.*
>
> *Giai đoạn 5 xác minh đã phơi bày overclaim của chính tôi: cannibalization thực ra là $23M (strict cohort), không phải $42M (inclusive). Giai đoạn 6 sau đó cho thấy 3 cohort riêng biệt với 3 intent và recovery rate khác nhau — $154M new users, $160M chronic shoppers, $23M cannibalized VIPs. Một playbook không thể giải quyết cả ba.*
>
> *Vì vậy tôi đã thiết kế Triple-Leak Protection Playbook: phục hồi theo cohort với hạ tầng dùng chung (classifier + event pipeline + experiment platform), 3 workstream, 9 A/B test trong 90 ngày. MVP ship với cohort nhỏ nhất có độ tin cậy cao nhất (VIPs), mở rộng sang cơ hội lớn hơn ($154M new users). Dự kiến $46M mỗi sự kiện BF, ROI 17× năm 1.*
>
> *End-to-end: tôi xây dựng DE pipeline trong DuckDB xử lý 110M dòng với memory-safe streaming, chạy 6 giai đoạn DA bao gồm lần xác minh để bulletproof các số, viết BA problem brief với 3 kịch bản và sensitivity analysis, và bàn giao PM artifacts gồm Master PRD, MVP PRD với full A/B spec, experiment roadmap, và 90-day rollout plan với Gantt và risk register."*

---

## Đào Sâu Kỹ Thuật 5 Phút (Cho Phỏng Vấn Kỹ Thuật)

### Bối Cảnh (30 giây)
*"E-commerce multi-category của Nga, 110M events trong tháng 10-11/2019. Stack: DuckDB xử lý 110M dòng, dbt cho tầng transformation, Python cho phân tích, xlsx cho sizing hướng đến stakeholders."*

### Thách Thức DE (60 giây)
*"Thách thức big-data: 110M dòng, CSV 10GB+, ngân sách RAM 4GB. Phương án: DuckDB `read_csv_auto` streaming (không dùng bộ nhớ Python), phân vùng theo `event_month`, dbt incremental materialization, memory_limit=3.5GB để force spill-to-disk duyên dáng. Xây dựng 3 tầng: raw → stg_events + stg_sessions → fct_session_funnel. Validation query chạy <2 giây trên 23M dòng. Peak RAM giữ ở <3.8GB."*

### Độ Chặt Chẽ DA (90 giây)
*"6 giai đoạn với lần xác minh tường minh. Giai đoạn 1 metrics tổng thể, Giai đoạn 2 so sánh Oct-vs-Nov, Giai đoạn 2.5 integrity check phát hiện data gap ngày 15/11 và direct purchase flow. Giai đoạn 3 deep-dive direct flow. Giai đoạn 4 — bằng chứng rõ ràng — theo dõi cohort Direct-Native tháng 10 vào hành vi tháng 11, tìm thấy 37% di chuyển + 56% abandon BF Week so với 0% baseline tháng 10. Giai đoạn 5 xác minh phát hiện 3 red flag: bug logic pct_view_only (sửa thành mutually exclusive), overclaim overlap cohort ($42M → $23M strict), hạ cấp tỷ lệ baseline cherry-pick (5× → 2.5×). Giai đoạn 6 đối chiếu toàn bộ cohorts cộng đúng $377.9M. Mỗi con số được đóng dấu XÁC MINH trước khi BA sử dụng."*

### BA Framing (60 giây)
*"Hai lần reframe chứng minh sự trưởng thành phân tích. Đầu tiên: pivot dataset cosmetics → multi-category khi tôi nhận ra magnitude AOV. Thứ hai: pivot narrative từ cart abandonment → cannibalization khi Giai đoạn 4 tìm ra nhân quả hành vi. Narrative cuối cùng: Triple-Leak vì framing single-metric đã bỏ lỡ 94% cơ hội. Sizing model xây dựng trong xlsx với 3 kịch bản × bảng sensitivity — stakeholders có thể thay giả định và thấy tác động trực tiếp. Mỗi cohort có intent riêng biệt, natural recovery rate (21/26/39%), và solution bucket."*

### PM Execution (60 giây)
*"Master PRD định nghĩa shared infra (cohort classifier, event pipeline, trigger engine, A/B platform) + 3 workstream song song. MVP PRD cho Direct Flow Protection (cohort nhỏ nhất, độ tin cậy cao nhất — ra mắt Tuần 4) bao gồm user story, 4 tính năng (badge + price-lock + fast checkout + banner suppression), full A/B test spec với tính toán MDE (2,100 users/arm), guardrail metrics với auto-rollback. Lộ trình 90 ngày: 9 thử nghiệm trên 3 workstream, Gantt với critical path (0 buffer đã được gắn cờ), đỉnh 11 FTE, 4 phase gate với tiêu chí ship/kill. Risk register với 7 mục critical/high + biện pháp giảm thiểu."*

### Tóm Tắt Tác Động (20 giây)
*"$46M mỗi sự kiện BF base case, $100M+ hàng năm trên 7 flash sales. Setup $240K, annual opex $2.5M, hoàn vốn <1 sự kiện BF, ROI năm 1 là 17×."*

---

## Câu Hỏi Phỏng Vấn Thường Gặp + Câu Trả Lời

### H: "Hãy nói qua cách bạn tiếp cận phân tích dataset lớn."

**TL:** *"Tôi bắt đầu bằng xác định phạm vi trước khi chạm vào dữ liệu — định nghĩa câu hỏi business và hình dạng câu trả lời kỳ vọng. Sau đó tôi kiểm tra data integrity trước (tỷ lệ null, duplicate, khoảng timestamp, cardinality) trước bất kỳ phân tích nào. Với 110M dòng tôi dùng DuckDB với streaming ingest, phân vùng theo tháng, dbt staging để làm sạch types và lọc dòng không hợp lệ, rồi tầng mart với mỗi dòng = 1 session với pre-computed funnel flags. Điều này có nghĩa analytical queries trở thành GROUP BY đơn giản thay vì JOIN đắt tiền. Tôi luôn thêm lần xác minh trước khi tin vào số — trong dự án này nó đã phát hiện overclaim $19M và bug logic."*

### H: "Kể về một lần bạn phải thay đổi hướng giữa chừng."

**TL:** *"Hai lần trong dự án này. Đầu tiên là pivot dataset: AOV cosmetics ra $0.52 USD sau khi xác minh đơn vị tiền tệ — magnitude quá nhỏ để tạo case study có thể bảo vệ được. Tôi pivot sang multi-category electronics ($360 AOV, cùng schema nên pipeline tái sử dụng được). Thứ hai là pivot narrative: bắt đầu với framing 'cart abandonment recovery' nhưng phân tích Giai đoạn 4 cho thấy BF cannibalize khách hàng VIP — insight mới mẻ. Tôi reframe từ abandonment chung sang cannibalization cụ thể, điều này đã biến phản ứng của CEO từ 'phân tích hay' thành 'playbook có thể thực thi với ROI.'"*

### H: "Bạn quyết định việc gì cần làm tiếp theo như thế nào?"

**TL:** *"Tôi tính điểm theo (expected impact × độ tin cậy) / nỗ lực. Trong dự án này tôi có 9 thử nghiệm tiềm năng. Tôi chọn MVP là Workstream 3 (cohort $23M nhỏ nhất) vì nó có độ tin cậy cao nhất (baseline natural recovery 38.5%, tín hiệu rõ ràng nhất) và cohort nhỏ nhất (dễ pilot hơn). Mở rộng learnings sang các cohort $154M + $160M lớn hơn sau khi validate methodology."*

### H: "Phần khó nhất là gì?"

**TL:** *"Giai đoạn 5 xác minh — cụ thể là khoảnh khắc tôi phải gắn cờ overclaim của chính mình. Con số cannibalization ban đầu là $42M, nhưng định nghĩa strict cohort kéo xuống còn $23M. Hạ cấp 45% rất đau đớn. Nhưng $23M có thể bảo vệ trước CFO vẫn tốt hơn $42M đáng ngờ trong mọi trường hợp. Học cách tự phê bình trước khi CEO làm còn khó hơn nghe."*

### H: "Bạn xử lý bất đồng với stakeholder thế nào?"

**TL:** *"Với dữ liệu: khi một con số có vẻ quá tốt, tôi chủ động chạy verification queries và mang cả hai con số đến. Với narrative: khi một hypothesis có vẻ hiển nhiên, tôi ép ra 3 hypothesis cạnh tranh (infra choke / price shock / decision paralysis) và để dữ liệu chọn người thắng. Với sản phẩm: khi stakeholder muốn scope lớn hơn, tôi cho họ thấy opportunity sizing xlsx và để họ tự thấy trade-offs."*

### H: "Bạn sẽ làm khác gì?"

**TL:** *"Ba điều. Đầu tiên, tôi sẽ dành thời gian cho 'pre-mortem' trước Giai đoạn 1 — hỏi 'điều gì có thể phá hỏng phân tích này?' ngay từ đầu sẽ giúp phát hiện sớm hơn data gap ngày 15/11 và vấn đề đơn vị tiền tệ. Thứ hai, tôi sẽ build executive dashboard HTML sớm hơn — nó tổng hợp tất cả thành một visual và tôi sẽ dùng nó để kiểm tra câu chuyện trong suốt quá trình phân tích. Thứ ba, tôi sẽ cặp với một người có tư duy hoài nghi cho Giai đoạn 5 xác minh thay vì tự phê bình — một bộ não thứ hai phát hiện những điểm mù khác."*

---

## Artifacts Hỗ Trợ Để Trình Bày Trong Phỏng Vấn

1. **Dashboard HTML** → mở trực tiếp, trình bày 4 KPI + biểu đồ theo ngày + panel 3-leak
2. **Sizing xlsx** → thay đổi một ô giả định trực tiếp, thấy ROI cập nhật real-time
3. **BA Brief v3** → chỉ vào Decision Log ở phụ lục cho thấy hành trình
4. **MVP PRD** → chỉ phần thiết kế A/B test với tính toán MDE
5. **Rollout Plan** → chỉ Gantt + dependency map

---

## Các Con Số Cần Thuộc Lòng

| Chỉ Số | Con Số | Ngữ Cảnh |
|---|---|---|
| Events đã phân tích | 110M | Quy mô DE |
| GMV at risk tháng 11 | $377.9M | Tiêu đề chính |
| GMV Cannibalized | $23.3M | Strict, đã xác minh |
| Abandon rate direct shift | 0% → 56% | Bằng chứng rõ ràng |
| Thời gian quyết định shift | 90s → 613s | 6.8× |
| Cohort #1 (New Users) | $154.1M · 245K users | $ lớn nhất |
| Cohort #2 (Chronic) | $160.1M · 217K users | Cohort lớn nhất |
| Cohort #3 (VIPs) | $23.3M · 37K users | MVP |
| Phục hồi mỗi BF (base) | $46M | Tổng cộng |
| Phục hồi hàng năm (7 sự kiện) | $100M+ | Quy mô |
| Setup / annual opex | $240K / $2.5M | Đầu tư |
| ROI năm 1 | 17× | Hoàn vốn |

---

## Những Điều KHÔNG Nói

- "Tôi chỉ tải dataset từ Kaggle"
- "Phân tích khá là đơn giản"
- "Tôi dùng AI để tạo phần lớn nội dung"
- "Tôi không chắc tác động business là gì"
- "Các con số là ước tính"
- Các số cụ thể mà bạn không thể bảo vệ ($42M khi đã xác minh là $23M)

---

## Những Điều NÊN Nói

- "Tôi đã xác minh con số này bằng cách..." (thể hiện sự nghiêm túc)
- "Hypothesis tôi test là..." (thể hiện phương pháp khoa học)
- "Tôi loại trừ X vì dữ liệu cho thấy Y..." (thể hiện tư duy phản biện)
- "Điều này có thể bảo vệ được vì..." (thể hiện tư duy sẵn sàng cho CFO)
- "Trade-off là..." (thể hiện sự tinh tế)
- "Tôi pivot khi nhận ra..." (thể hiện khả năng thích nghi)
