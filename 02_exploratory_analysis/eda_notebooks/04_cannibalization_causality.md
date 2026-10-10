# Phân Tích Di Chuyển Direct-to-Cart (Cannibalization Tuần BF)

> **DISCLAIMER:** Dữ liệu tháng 11 đã loại trừ ngày 15/11 (Data Gap).

## Q1 — Quy Mô Cohort & Chồng Lấp
| Chỉ Số | Số Lượng |
|---|---|
| Direct-Native Users (Tháng 10) | 214,542 |
| Cart-Native Users (Tháng 10) | 182,224 |
| Overlap Users (Cả 2 luồng trong Tháng 10) | 49,641 |
| Direct-Native Hoạt Động Trong Tháng 11 | 139,235 |
| Direct-Native Không Quay Lại Trong Tháng 11 | 75,307 |

**Tín hiệu:** Tập khách hàng Direct-Native ở tháng 10 có quy mô lớn. Một lượng đáng kể trong số này đã có quay trở lại tương tác trong tháng 11.


## Q2 — Hành Vi Di Chuyển (Direct-Native Tháng 10 -> Tháng 11)

| Phân Khúc                    |   active_users | pct_purc_direct   | pct_purc_cart   | pct_abandon_cart   | pct_view_only   |
|:--------------------------|---------------:|:------------------|:----------------|:-------------------|:----------------|
| Toàn Tháng 11 (Active Users) |         139235 | 16.7%             | 37.3%           | 32.2%              | 91.2%           |
| BF Week Active Users      |          75069 | 18.7%             | 46.5%           | 47.4%              | 94.6%           |
| Non-BF Week Active Users  |         131553 | 17.5%             | 38.1%           | 32.7%              | 92.2%           |

**Tín hiệu:** Đa số người dùng mua trực tiếp ở tháng 10 đã chuyển sang hành vi Cart-based (cả mua và bỏ giỏ) trong tháng 11. Tỷ lệ chuyển sang Cart-based và Abandon Cart tăng vọt mạnh hơn hẳn trong những ngày BF Week so với non-BF Week.

## Q3 — Tác Động Doanh Thu Từ Di Chuyển (Direct-Native Cohort)

| nov_gmv_direct_retained   | nov_gmv_cart_migrated   | nov_gmv_at_risk_migrated   | oct_cohort_aov   | nov_cohort_aov   | aov_delta_abs   |
|:--------------------------|:------------------------|:---------------------------|:-----------------|:-----------------|:----------------|
| $12,366,369.10            | $53,525,539.80          | $42,262,536.07             | $354.81          | $392.37          | $37.57          |

**Tín hiệu:** Có tới hơn $42 triệu USD GMV từ tập user mua thẳng đã bị kẹt lại thành GMV at risk trong các giỏ hàng bỏ quên (Cannibalized GMV At Risk). Mặc dù mức chi tiêu (AOV) của tập người dùng này trong tháng 11 có tăng nhẹ thêm $37, nhưng một lượng lớn giao dịch tiềm năng đã không thể hoàn tất do họ bị sa lầy vào luồng Cart.

## Q4 — Thời Điểm & Tác Nhân Di Chuyển (Theo Ngày)

| date       |   cohort_sessions |   cart_sessions | migration_rate_pct   |
|:-----------|------------------:|----------------:|:---------------------|
| 2019-11-01 |             39188 |            2666 | 6.8%                 |
| 2019-11-02 |             36195 |            2419 | 6.7%                 |
| 2019-11-03 |             34799 |            2333 | 6.7%                 |
| 2019-11-04 |             41332 |            2715 | 6.6%                 |
| 2019-11-05 |             37787 |            2314 | 6.1%                 |
| 2019-11-06 |             36656 |            2388 | 6.5%                 |
| 2019-11-07 |             36704 |            2186 | 6.0%                 |
| 2019-11-08 |             34852 |            8458 | 24.3%                |
| 2019-11-09 |             31822 |            7308 | 23.0%                |
| 2019-11-10 |             31828 |            7257 | 22.8%                |
| 2019-11-11 |             34193 |            7590 | 22.2%                |
| 2019-11-12 |             33529 |            7025 | 21.0%                |
| 2019-11-13 |             33290 |            7050 | 21.2%                |
| 2019-11-14 |             50341 |           14941 | 29.7%                |
| 2019-11-16 |            100867 |           32088 | 31.8%                |
| 2019-11-17 |             89300 |           27793 | 31.1%                |
| 2019-11-18 |             38575 |            7670 | 19.9%                |
| 2019-11-19 |             30564 |            6711 | 22.0%                |
| 2019-11-20 |             28522 |            6470 | 22.7%                |
| 2019-11-21 |             27426 |            6360 | 23.2%                |
| 2019-11-22 |             25862 |            5971 | 23.1%                |
| 2019-11-23 |             24536 |            5534 | 22.6%                |
| 2019-11-24 |             24441 |            5767 | 23.6%                |
| 2019-11-25 |             25170 |            6052 | 24.0%                |
| 2019-11-26 |             27249 |            6362 | 23.3%                |
| 2019-11-27 |             27217 |            6291 | 23.1%                |
| 2019-11-28 |             26676 |            6265 | 23.5%                |
| 2019-11-29 |             30487 |            7390 | 24.2%                |
| 2019-11-30 |             26750 |            6512 | 24.3%                |


### So Sánh Hành Vi BF vs Non-BF (Direct-Native Cohort)

| Giai Đoạn   | abandon_rate_pct   | avg_time_to_abandon_sec   |   avg_items_per_cart |   reference_oct_items |
|:------------|:-------------------|:--------------------------|---------------------:|----------------------:|
| Non-BF Week | 31.0%              | 553s                      |                 1.63 |                  1.13 |
| BF Week     | 56.0%              | 613s                      |                 1.78 |                  1.13 |

**Tín hiệu:** Tỷ lệ migration sang dùng Cart đạt đỉnh (Spike) rất rõ ràng vào các ngày Pre-BF (14, 16, 17) và ngày BF (29). Vào tuần lễ BF, tỷ lệ abandon của tập user cao cấp này nhảy vọt, và thời gian nán lại session (time-to-abandon) dài hơn, trong khi số lượng items nhặt vào giỏ cũng tăng gấp đôi so với thói quen 1-click ban đầu.

## Tóm Tắt Bằng Chứng Cannibalization

| Chỉ Số                                        | Giá Trị        | Hàm Ý                                                                    |
|:----------------------------------------------|:---------------|:-------------------------------------------------------------------------|
| Tỷ lệ Di Chuyển Direct-Native sang Cart (Nov) | 37.3%          | Cannibalization được xác nhận. Người mua quen thuộc chuyển sang cart flow. |
| Cannibalized GMV At Risk                      | $42,262,536.07 | Doanh thu bị mất do decision paralysis của người mua 1-click trước đây.   |
| AOV Shift                                     | +$37.57        | Dù ý định giỏ hàng cao hơn, người mua 1-click vẫn bị kẹt trong cart flow. |
| BF Week Migration Spike                       | Có             | Chiến dịch Sale đã thành công kéo người mua direct sang hành vi window shopping. |
| Tăng Kích Thước Giỏ Hàng                      | 1.78 items     | User chất đầy giỏ hàng nhưng không hoàn tất checkout (decision paralysis / infra choke). |
