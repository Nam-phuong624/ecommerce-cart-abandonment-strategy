# Decoding E-Commerce Cart Abandonment: Data-Driven Product Strategy

![DuckDB](https://img.shields.io/badge/DuckDB-OLAP_Engine-FFDE00?style=flat-square&logo=duckdb&logoColor=black)
![Python](https://img.shields.io/badge/Python-Data_Processing-3776AB?style=flat-square&logo=python&logoColor=white)
![Product Analytics](https://img.shields.io/badge/Product-Analytics-0052CC?style=flat-square)
![Data Driven](https://img.shields.io/badge/100%25-Data_Driven-2EA44F?style=flat-square)

> **Executive Summary:** 
> Dự án Phân tích Sản phẩm End-to-End. Xử lý tập dữ liệu **110 triệu sự kiện** thương mại điện tử để tìm ra nguyên nhân khiến **$7.04 Triệu USD** bị bỏ lại trong giỏ hàng mùa Sale. Bằng việc chuyển đổi từ tư duy "Phát mã giảm giá đại trà" sang "Can thiệp hành vi mục tiêu", dự án thiết kế 3 giải pháp Sản phẩm giúp khôi phục **~1.5 Triệu USD/đợt Sale** và bảo vệ biên lợi nhuận của công ty.

---

## 🎯 1. Bài toán Kinh doanh 
Black Friday là thời điểm bùng nổ traffic, nhưng dữ liệu hệ thống (truy vấn từ 14/11 - 17/11) phơi bày một lỗ hổng chí mạng: **Khách hàng đưa đồ vào giỏ rất nhiều, nhưng thoát trang (Abandon) cũng cao chưa từng có.**

Sự rò rỉ này không phải là một lỗi ngẫu nhiên, mà là sự đứt gãy từ 3 tập khách hàng riêng biệt (Hiện tượng **Triple-Leak**):

1. **Khách VIP (The Intent Shock) - Rủi ro $1.41M:** Đây là nhóm đắt giá nhất. Bình thường họ mua hàng bằng **"Nút Mua Ngay 1-chạm"**. Tuy nhiên, giao diện mùa Sale ép họ phải đi qua Giỏ hàng. Việc bẻ gãy hành vi này tạo ra "Cú sốc ý định", khiến **55.6% khách VIP tức giận thoát trang**.
2. **Khách Ngủ Đông (Chronic) - Rủi ro $3.14M:** Lướt ngắm đồ từ tháng trước nhưng lưỡng lự, chờ đợi một cú huých giá trị thực sự.
3. **Khách Mới (New Users) - Rủi ro $2.49M:** Vào app vì quảng cáo tò mò, thiếu động lực gắn kết sâu nên thoát trang cực nhanh.

---

## 💡 2. Giải pháp & Tác động Kinh tế 
Dự án áp dụng nguyên tắc **100% Data-Driven**, loại bỏ hoàn toàn các con số giả định. Giải pháp không nằm ở việc "đốt tiền" marketing, mà nằm ở việc cấu trúc lại Trải nghiệm Sản phẩm (Product Features):

*   **Tính năng 1:** Trả lại luồng Fast-Checkout (Mua Ngay) để giải cứu luồng chốt đơn của **Khách VIP**.
*   **Tính năng 2:** Gửi Push Notification báo giá giảm (Price-drop) đích danh món đồ đang nằm trong wishlist của **Khách Ngủ Đông**.
*   **Tính năng 3:** Bật Popup chặn thoát trang (Exit-intent) để níu chân **Khách Hàng Mới**.

👉 **Kỳ vọng Hoàn vốn (ROI):** Theo [Kế hoạch Triển khai (Rollout Plan)](04_solution_design/rollout_plans/90day_phased_rollout.md), chiến lược này mục tiêu khôi phục **~1.5 Triệu USD** lợi nhuận ròng, đồng thời thiết lập rơ-le an toàn (Guardrails) để tự động ngắt tính năng nếu Giá trị đơn hàng trung bình (AOV) rớt dưới mức nền `$26.79`.

---

## ⚙️ 3. Kiến trúc Hệ thống & Luồng Dữ liệu 

Làm thế nào để xử lý 110 triệu dòng dữ liệu (Big Data) trên một máy tính cá nhân mà không cần hệ thống Cloud đắt đỏ? 
Câu trả lời là **DuckDB** - Database OLAP In-process có tốc độ truy vấn hàng triệu rows chỉ tính bằng mili-giây.

Dự án được cấu trúc theo đúng vòng đời chuẩn của một Luồng Xử lý Dữ liệu (Data Lifecycle):

1. 📂 **`01_data_preparation/`**: Chuẩn bị, làm sạch và thiết kế schema từ dữ liệu thô (Kaggle REES46).
2. 🔍 **`02_exploratory_analysis/`**: Khám phá dữ liệu (EDA), phân tích phễu chuyển đổi (Funnel Analysis) bằng Python & SQL.
3. 📈 **`03_strategic_insights/`**: Đúc kết Tầm nhìn chiến lược. Cung cấp các báo cáo phân tích nguyên nhân gốc rễ (Root Cause) bằng dữ liệu đã xác thực.
4. 🛠️ **`04_solution_design/`**: Thiết kế Giải pháp. Chứa các tài liệu PRD (Product Requirements) và Kế hoạch Launch tính năng thực tế.
5. 🤖 **`05_predictive_modeling/`**: Đánh giá tính khả thi của Trí tuệ Nhân tạo (Machine Learning Feasibility). Chứng minh thuật toán XGBoost có thể phân loại người dùng bỏ giỏ hàng với độ chính xác cao.

---

## 🚀 4. Khám phá Dự án

*   **Bạn muốn xem kỹ năng viết SQL/Xử lý Data?** 
    $
ightarrow$ Mời xem folder [`docs/assets/queries/`](docs/assets/queries/) chứa toàn bộ mã nguồn truy vấn động chứng minh các số liệu trong dự án.
*   **Bạn muốn xem tư duy Business & Giải quyết vấn đề?** 
    $
ightarrow$ Mời xem báo cáo chuyên sâu [`Bằng chứng gãy phễu khách VIP`](03_strategic_insights/reports/02_vip_cohort_evidence.md).
*   **Bạn muốn xem kỹ năng Quản lý Sản phẩm (Product Management)?** 
    $
ightarrow$ Mời xem bản thiết kế giải pháp [`Master PRD`](04_solution_design/prd/00_master_prd_triple_leak.md) và [`Kế hoạch Rollout`](04_solution_design/rollout_plans/90day_phased_rollout.md).

---

## 💻 5. Khả năng Tái lập
Dự án đề cao tính minh bạch và khả năng tái lập toàn bộ kết quả.
1. Database cục bộ được lưu trữ tại `data/processed/ecommerce.duckdb`.
2. Truy vấn trực tiếp qua DuckDB CLI:
   ```bash
   duckdb data/processed/ecommerce.duckdb -c "SELECT * FROM fct_session_funnel LIMIT 5;"
   ```
3. Toàn bộ SQL Query được tối ưu hóa theo chuẩn phân tích OLAP (CTE, Window Functions, Aggregations).
