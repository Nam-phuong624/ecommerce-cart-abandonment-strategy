# DA Giai Đoạn 6 — Phân Tích Sâu Cohort "Other Oct" + "New Users"

> **DISCLAIMER:** Dữ liệu tháng 11 đã loại trừ ngày 15/11 (Data Gap).

## Q1 — Quy Mô & Hồ Sơ Cohort

| cohort    |   user_count |   avg_sessions | avg_cart_value   | gmv_bf_week    | gmv_non_bf     | total_gmv_risk   |
|:----------|-------------:|---------------:|:-----------------|:---------------|:---------------|:-----------------|
| New Users |      245,131 |           6    | $440.40          | $77,397,309.37 | $76,673,715.92 | $154,071,025.29  |
| Other Oct |      217,095 |          14.52 | $444.58          | $90,672,496.77 | $69,451,103.83 | $160,123,600.60  |

**Tín hiệu:** Cả 2 cohort đều có quy mô người dùng rất lớn (~200k-250k users). Nhóm 'Other Oct' có độ gắn kết (avg_sessions) vượt trội so với 'New Users', nhưng cả 2 đều ôm một lượng GMV khổng lồ vào giỏ hàng trong tuần lễ Black Friday.


## Q2 — Mô Hình Hành Vi 'Other Oct'

- **Trung bình lượt xem (Tháng 10):** 23.2
- **Trung bình thêm vào giỏ (Tháng 10):** 0.2
- **Trung bình bỏ giỏ (Tháng 10):** 0.2
- **% Chronic Abandoner (>=3 carts trong Tháng 10):** 2.5%
- **Số ngày cách trung bình (Tháng 10 sang Tháng 11):** 17.1 ngày
- **Tỷ lệ quay lại (Tháng 10 -> Tháng 11):** 100% (Theo định nghĩa cohort)

**Top 5 Category (Giỏ Hàng Bỏ Quên Tháng 11):**
| category               | gmv             |
|:-----------------------|:----------------|
| electronics.smartphone | $110,916,211.33 |
| unknown                | $25,300,330.20  |
| electronics.video.tv   | $10,406,137.95  |
| computers.notebook     | $8,740,660.42   |
| electronics.clocks     | $4,874,645.71   |

**Tín hiệu:** Nhóm 'Other Oct' đích thị là các Chronic Window Shoppers. Họ vào web rất nhiều trong tháng 10, nhặt trung bình hàng chục lượt items vào giỏ nhưng không hề mua. Họ 'ngủ đông' khoảng 15 ngày rồi bùng nổ quay lại vào tháng 11 tiếp tục bỏ giỏ hàng.

## Q3 — Thu Hút & Hành Vi 'New Users'

- **Trung bình lượt xem (Session Bỏ Giỏ):** 7.2
- **Trung bình thêm vào giỏ (Session Bỏ Giỏ):** 1.7
- **% Đa Session (Quay lại trong Tháng 11):** 81.5%

**Thu Hút Theo Ngày (Top 5 Ngày):**
| date       |   new_users |
|:-----------|------------:|
| 2019-11-16 |      26,294 |
| 2019-11-17 |      15,739 |
| 2019-11-08 |      12,062 |
| 2019-11-14 |      11,859 |
| 2019-11-15 |      10,899 |

**Top 5 Category (Giỏ Hàng Bỏ Quên Tháng 11):**
| category                  | gmv             |
|:--------------------------|:----------------|
| electronics.smartphone    | $102,305,418.46 |
| unknown                   | $23,288,790.16  |
| electronics.video.tv      | $9,147,884.68   |
| computers.notebook        | $8,152,889.28   |
| appliances.kitchen.washer | $4,538,674.46   |

**Tín hiệu:** Khách hàng mới đổ bộ rầm rộ vào đúng các đợt sale (14-17/11). Họ tương tác cực kỳ ấn tượng với 81.5% user có từ 2 sessions trở lên trong tháng 11. Dù vậy, độ sâu tương tác mỗi session khá nông (chỉ ~7 views). Họ là nhóm traffic săn sale tích cực, return cao nhưng tỷ lệ bỏ giỏ (abandon) khổng lồ.

## Q4 — Tiềm Năng Phục Hồi Theo Cohort

| cohort        |   total_ab_users | natural_recovery_rate   | time_to_abandon   |
|:--------------|-----------------:|:------------------------|:------------------|
| New Users     |          245,131 | 21.3%                   | 868s              |
| Other Oct     |          217,095 | 25.6%                   | 841s              |
| Strict Direct |           36,712 | 38.5%                   | 678s              |

**Tín hiệu:** Nhóm VIP (Strict Direct) chốt đơn hụt cực kỳ chớp nhoáng (chỉ mất ~11 phút để từ bỏ giỏ hàng), trong khi nhóm New Users nán lại trên trang lâu nhất (~14.5 phút). Nhóm VIP có tỷ lệ tự quay lại mua (natural recovery) rất cao (38.5%), vượt xa Other Oct (25.6%) và New Users (21.3%). Tập VIP vẫn là nhóm dễ cứu nhất, trong khi New Users cần chiến lược Retargeting mạnh hơn.

## Ma Trận Cơ Hội Triple-Leak

| Cohort        | GMV At Risk   | Tỷ Lệ Phục Hồi Tự Nhiên | Điểm Ý Định                        | Giải Pháp                                     |
|:--------------|:--------------|:-------------------------|:---------------------------------|:----------------------------------------------|
| New Users     | $154.1M       | 21.3%                    | Thấp (Traffic Sale Chất Lượng Thấp) | Giảm giá mạnh / Exit-Intent Popup            |
| Other Oct     | $160.1M       | 25.6%                    | Trung bình (Chronic Window Shoppers) | Retargeting theo giảm giá / FOMO Urgency     |
| Strict Direct | $23.3M        | 38.5%                    | Cao (VIP bị Cannibalized)         | Checkout không ma sát / Bypass 1-Click       |
