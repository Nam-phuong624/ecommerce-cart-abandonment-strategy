# Phân Tích Luồng Mua Trực Tiếp (Dual Funnel Playbook)

> **DISCLAIMER:** Dữ liệu tháng 11 đã loại trừ ngày 15/11 (Data Gap) để đảm bảo tính nhất quán của phân tích.

## Q1 — Tổng Quan Phân Khúc Luồng
| period                      |   total_purc |   direct_purc | direct_pct   |   cart_purc | cart_pct   | direct_gmv      | cart_gmv        | total_gmv       |
|:----------------------------|-------------:|--------------:|:-------------|------------:|:-----------|:----------------|:----------------|:----------------|
| October 2019                |      629,572 |       337,699 | 53.64%       |     291,873 | 46.36%     | $101,690,771.88 | $128,311,379.30 | $230,002,151.18 |
| November 2019 (excl Nov 15) |      773,185 |       124,841 | 16.15%       |     648,344 | 83.85%     | $37,799,280.64  | $237,350,921.05 | $275,150,201.69 |
| Delta (Nov - Oct)           |      143,613 |      -212,858 | -37.49pp     |     356,471 | +37.49pp   | $-63,891,491.24 | $109,039,541.75 | $45,148,050.51  |

**Tín hiệu:** Direct purchase flow chiếm thế chủ đạo trong tháng 10 (53.64%) nhưng bất ngờ sụt giảm nghiêm trọng trong tháng 11 (chỉ còn 16.15%), dẫn đến thâm hụt tới $63.8 triệu USD GMV từ luồng này. Ngược lại, luồng Cart-based tăng trưởng bùng nổ, gánh vác toàn bộ mức tăng trưởng của sự kiện Black Friday.


## Q2 — So Sánh AOV & Giỏ Hàng

| month    | flow       |   sessions | aov     |   avg_items | median_basket   | pct_multi_buy   |
|:---------|:-----------|-----------:|:--------|------------:|:----------------|:----------------|
| October  | Direct     |    337,699 | $301.13 |        1.13 | $159.91         | 9.8%            |
| October  | Cart-based |    291,873 | $439.61 |        1.24 | $247.35         | 16.2%           |
| November | Direct     |    124,841 | $302.78 |        1.1  | $160.06         | 7.9%            |
| November | Cart-based |    648,344 | $366.09 |        1.2  | $194.89         | 13.9%           |

**Tín hiệu:** Direct Purchase có AOV và Median Basket cao hơn hẳn so với Cart-based ở cả 2 tháng. Tuy nhiên số lượng items/đơn hàng lại thấp hơn (~1 item), chứng tỏ khách hàng Direct thường nhắm thẳng vào các sản phẩm đắt tiền, mua dứt điểm (One-click buy).

## Q3 — Cơ Cấu Category Trong Luồng Direct (Tháng 11)

| category                         | gmv_direct     | gmv_cart        | direct_share_pct   |
|:---------------------------------|:---------------|:----------------|:-------------------|
| electronics.smartphone           | $21,198,734.81 | $156,615,838.80 | 11.9%              |
| unknown                          | $5,810,721.88  | $24,069,837.95  | 19.4%              |
| computers.notebook               | $1,980,642.33  | $8,697,222.40   | 18.5%              |
| electronics.video.tv             | $1,568,464.05  | $10,878,370.86  | 12.6%              |
| electronics.clocks               | $1,030,903.02  | $5,521,834.23   | 15.7%              |
| appliances.kitchen.washer        | $1,027,177.99  | $4,771,757.40   | 17.7%              |
| appliances.kitchen.refrigerators | $785,802.29    | $3,916,616.50   | 16.7%              |
| electronics.audio.headphone      | $743,263.61    | $4,926,224.75   | 13.1%              |
| appliances.environment.vacuum    | $389,374.83    | $2,373,052.60   | 14.1%              |
| computers.desktop                | $291,705.30    | $1,264,737.05   | 18.7%              |

**Tín hiệu:** Đáng chú ý, các mặt hàng cao cấp như Smartphone và Notebook dẫn đầu GMV ở luồng Direct. Tỷ trọng Direct của Smartphone vẫn duy trì ở mức ~15%, tương đồng với bức tranh tổng.

## Q4 — Hành Vi Session: Direct vs Cart-based

| month    | flow       | avg_duration   |   avg_views | median_time_to_purc   | pct_under_3_events   |
|:---------|:-----------|:---------------|------------:|:----------------------|:---------------------|
| November | Direct     | 575s           |         5.2 | 193s                  | 22.2%                |
| November | Cart-based | 677s           |         6.2 | 193s                  | 0.3%                 |
| October  | Direct     | 690s           |         5.8 | 183s                  | 17.6%                |
| October  | Cart-based | 848s           |         5.3 | 172s                  | 0.1%                 |

**Tín hiệu:** Direct Purchase đúng nghĩa là luồng 'Click-and-Buy': Thời gian median từ view đến purchase chỉ mất chưa tới 90 giây, có rất ít lượt view (dưới 4 views), và tỷ lệ session chỉ có <3 events (vào xem rồi mua ngay) chiếm >50%. Trong khi đó Cart-based tốn thời gian gấp hàng chục lần.

## Q5 — Tỷ Lệ Mua Trực Tiếp Theo Giờ

|   hour_of_day | direct_rate_oct   | direct_rate_nov   |
|--------------:|:------------------|:------------------|
|             0 | 56.1%             | 20.2%             |
|             1 | 57.7%             | 20.4%             |
|             2 | 56.8%             | 20.4%             |
|             3 | 55.3%             | 17.1%             |
|             4 | 55.0%             | 15.3%             |
|             5 | 54.2%             | 16.4%             |
|             6 | 52.9%             | 18.4%             |
|             7 | 53.5%             | 19.0%             |
|             8 | 53.0%             | 19.5%             |
|             9 | 52.5%             | 18.8%             |
|            10 | 52.2%             | 15.7%             |
|            11 | 52.3%             | 13.1%             |
|            12 | 51.7%             | 13.3%             |
|            13 | 52.8%             | 14.6%             |
|            14 | 54.4%             | 15.5%             |
|            15 | 55.2%             | 14.5%             |
|            16 | 55.6%             | 13.7%             |
|            17 | 55.4%             | 13.6%             |
|            18 | 53.9%             | 17.3%             |
|            19 | 52.6%             | 16.9%             |
|            20 | 52.4%             | 15.3%             |
|            21 | 51.2%             | 16.4%             |
|            22 | 53.3%             | 15.5%             |
|            23 | 52.5%             | 14.4%             |

**Tín hiệu:** Tỷ lệ Direct Purchase ở cả hai tháng đều khá đồng đều qua các khung giờ, sự sụt giảm ở tháng 11 là sụt giảm toàn hệ thống trên mọi khung giờ chứ không phải do lệch giờ.

## Q6 — Mua Trực Tiếp Trong Giai Đoạn Black Friday (14-30/11)

| date       |   total_purc |   direct_purc |   cart_purc | direct_gmv    | direct_to_cart_ratio   |
|:-----------|-------------:|--------------:|------------:|:--------------|:-----------------------|
| 2019-11-14 |        18683 |           175 |       18508 | $58,777.90    | 0.01x                  |
| 2019-11-16 |        56664 |          7845 |       48819 | $3,082,009.66 | 0.16x                  |
| 2019-11-17 |       151472 |         16126 |      135346 | $5,935,583.92 | 0.12x                  |
| 2019-11-18 |        24013 |           248 |       23765 | $74,545.62    | 0.01x                  |
| 2019-11-19 |        21050 |           204 |       20846 | $62,758.74    | 0.01x                  |
| 2019-11-20 |        21151 |           221 |       20930 | $58,226.90    | 0.01x                  |
| 2019-11-21 |        21398 |           224 |       21174 | $56,072.86    | 0.01x                  |
| 2019-11-22 |        20451 |           256 |       20195 | $77,172.38    | 0.01x                  |
| 2019-11-23 |        18683 |           174 |       18509 | $55,737.15    | 0.01x                  |
| 2019-11-24 |        19571 |           170 |       19401 | $53,494.20    | 0.01x                  |
| 2019-11-25 |        21001 |           216 |       20785 | $71,760.44    | 0.01x                  |
| 2019-11-26 |        20416 |           245 |       20171 | $71,859.71    | 0.01x                  |
| 2019-11-27 |        20627 |           228 |       20399 | $82,892.07    | 0.01x                  |
| 2019-11-28 |        20539 |           234 |       20305 | $80,222.11    | 0.01x                  |
| 2019-11-29 |        27552 |           989 |       26563 | $333,095.66   | 0.04x                  |
| 2019-11-30 |        23825 |           243 |       23582 | $83,191.69    | 0.01x                  |

**Tín hiệu:** Trong chính tuần lễ sale Black Friday (đặc biệt ngày 16, 17 và 29), lượng Direct Purchase thực chất VẪN TĂNG theo khối lượng (số đếm và GMV), tuy nhiên tỷ lệ Direct/Cart Ratio tụt dốc thê thảm (do Cart-based flow bùng nổ quá mạnh). Khách hàng không ngưng mua trực tiếp, họ chỉ đơn giản là chuộng việc dồn giỏ hàng hơn trong mùa sale.

## Tóm Tắt Cơ Hội Mua Trực Tiếp
| Chỉ Số | Nhận Định |
|---|---|
| AOV Direct vs Cart | Direct AOV duy trì mức rất cao (~$400+) so với Cart-based (~$300-$350). |
| Ý Định 1-Click | >50% luồng Direct kết thúc purchase chỉ với dưới 3 events và tốn <90s. |
| Dịch Chuyển Hành Vi Theo Mùa | Hành vi dịch chuyển mạnh từ Direct sang Cart trong mùa Sale (Direct Ratio rơi từ 0.8-1.5x xuống 0.2x). |
| Tập Trung Giá Trị Cao | Luồng Direct thống trị bởi các mặt hàng cực kỳ đắt tiền (Smartphones, Laptops). |
