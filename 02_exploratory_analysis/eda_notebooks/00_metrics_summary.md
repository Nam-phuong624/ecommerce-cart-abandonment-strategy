# Phân Tích Dữ Liệu: Tóm Tắt Metrics

## XÁC MINH NGUỒN DỮ LIỆU
- **Tổng Events (raw):** 109,950,743
- **Tổng Unique Sessions:** 23,017,590 (Trong fct_session_funnel, mỗi session là 1 dòng, 23M là số lượng sessions hợp lý cho 110M events, trung bình ~4.8 events/session).

## H1: Funnel & Engagement
### Phân Tích Event Counts
| event_type   |     count |
|:-------------|----------:|
| view         | 104335509 |
| cart         |   3955446 |
| purchase     |   1659788 |

### Event Counts theo Tháng
| month               | event_type   |    count |
|:--------------------|:-------------|---------:|
| 2019-10-01 00:00:00 | cart         |   926516 |
| 2019-10-01 00:00:00 | purchase     |   742849 |
| 2019-10-01 00:00:00 | view         | 40779399 |
| 2019-11-01 00:00:00 | cart         |  3028930 |
| 2019-11-01 00:00:00 | purchase     |   916939 |
| 2019-11-01 00:00:00 | view         | 63556110 |

### Unique Sessions theo Bước Funnel
|   total_sessions |   sessions_with_view |   sessions_with_cart |   sessions_with_purchase |
|-----------------:|---------------------:|---------------------:|-------------------------:|
|         23017590 |             23006536 |              2316434 |                  1402758 |

### Conversion theo Top 20 Category Code
| category_code                    |   unique_sessions |   purchase_sessions |   conversion_rate_pct |
|:---------------------------------|------------------:|--------------------:|----------------------:|
| electronics.smartphone           |           7307576 |              609168 |                  8.34 |
| electronics.audio.headphone      |            976759 |               63825 |                  6.53 |
| electronics.clocks               |            928014 |               37093 |                  4    |
| electronics.video.tv             |            789982 |               46381 |                  5.87 |
| computers.notebook               |            700548 |               30086 |                  4.29 |
| apparel.shoes                    |            601816 |               12904 |                  2.14 |
| appliances.kitchen.washer        |            523077 |               32288 |                  6.17 |
| appliances.kitchen.refrigerators |            518012 |               22108 |                  4.27 |
| appliances.environment.vacuum    |            500863 |               28708 |                  5.73 |
| computers.desktop                |            283451 |                6409 |                  2.26 |
| apparel.shoes.keds               |            274170 |                4628 |                  1.69 |
| furniture.bedroom.bed            |            272561 |                4731 |                  1.74 |
| auto.accessories.player          |            245460 |                7826 |                  3.19 |
| electronics.tablet               |            235659 |               10549 |                  4.48 |
| furniture.living_room.cabinet    |            226483 |                4119 |                  1.82 |
| furniture.living_room.sofa       |            181106 |                2457 |                  1.36 |
| apparel.costume                  |            171533 |                1288 |                  0.75 |
| electronics.telephone            |            166098 |                7533 |                  4.54 |
| kids.carriage                    |            160361 |                4557 |                  2.84 |
| electronics.audio.subwoofer      |            160092 |                5773 |                  3.61 |

### Conversion theo Top 20 Brand
| brand    |   unique_sessions |   purchase_sessions |   conversion_rate_pct |
|:---------|------------------:|--------------------:|----------------------:|
| samsung  |           4277366 |              323051 |                  7.55 |
| apple    |           3615477 |              263763 |                  7.3  |
| xiaomi   |           2388345 |              111828 |                  4.68 |
| huawei   |            886330 |               42120 |                  4.75 |
| lucente  |            617716 |               23510 |                  3.81 |
| lg       |            578207 |               19566 |                  3.38 |
| bosch    |            532230 |               12708 |                  2.39 |
| sony     |            483825 |               15385 |                  3.18 |
| cordiant |            478066 |               25420 |                  5.32 |
| oppo     |            462393 |               23190 |                  5.02 |
| acer     |            380109 |               11948 |                  3.14 |
| artel    |            359501 |               14159 |                  3.94 |
| respect  |            354264 |                6092 |                  1.72 |
| lenovo   |            335873 |               10146 |                  3.02 |
| philips  |            300425 |                9517 |                  3.17 |
| dauscher |            290860 |                7223 |                  2.48 |
| hp       |            289097 |                7120 |                  2.46 |
| redmond  |            265637 |                8675 |                  3.27 |
| vitek    |            255957 |                9152 |                  3.58 |
| indesit  |            246056 |                9348 |                  3.8  |

## H2: Abandonment
### Phân Phối Giá
|   min |   p25 |    p50 |    p75 |     p95 |     max |     avg |
|------:|------:|-------:|-------:|--------:|--------:|--------:|
|     0 | 67.96 | 164.93 | 360.11 | 1003.85 | 2574.07 | 291.635 |

### Full Clear vs True Abandoned
|   sessions_full_clear |   sessions_true_abandoned |
|----------------------:|--------------------------:|
|                     0 |                   1376216 |

### Tỷ Lệ Abandon theo Tier Giá Trị Giỏ Hàng (USD)
| cart_tier   |   total_carts |   abandoned_carts |   abandon_rate_pct |
|:------------|--------------:|------------------:|-------------------:|
| [$0-50]     |        282488 |            192715 |              68.22 |
| [$50-200]   |        721002 |            433647 |              60.15 |
| [$200-500]  |        643878 |            373297 |              57.98 |
| [$500-1000] |        374579 |            215183 |              57.45 |
| [$1000+]    |        294487 |            161374 |              54.8  |

### Tỷ Lệ Abandon theo Giờ
|   hour_of_day |   total_carts |   abandoned_carts |   abandon_rate_pct |
|--------------:|--------------:|------------------:|-------------------:|
|             0 |         13413 |             10397 |              77.51 |
|             1 |         27646 |             22163 |              80.17 |
|             2 |         57657 |             43500 |              75.45 |
|             3 |         93007 |             60121 |              64.64 |
|             4 |        125922 |             76225 |              60.53 |
|             5 |        140958 |             82929 |              58.83 |
|             6 |        146955 |             85789 |              58.38 |
|             7 |        151074 |             88796 |              58.78 |
|             8 |        153725 |             85794 |              55.81 |
|             9 |        151574 |             80799 |              53.31 |
|            10 |        148326 |             79102 |              53.33 |
|            11 |        142070 |             75751 |              53.32 |
|            12 |        131953 |             69927 |              52.99 |
|            13 |        129544 |             70393 |              54.34 |
|            14 |        128413 |             71567 |              55.73 |
|            15 |        125349 |             74160 |              59.16 |
|            16 |        117042 |             71357 |              60.97 |
|            17 |        106076 |             66026 |              62.24 |
|            18 |         85193 |             60785 |              71.35 |
|            19 |         59589 |             42939 |              72.06 |
|            20 |         37178 |             27126 |              72.96 |
|            21 |         21814 |             15494 |              71.03 |
|            22 |         12867 |              8899 |              69.16 |
|            23 |          9089 |              6177 |              67.96 |

### Tỷ Lệ Abandon theo Ngày trong Tuần (1=Thứ Hai, 7=Chủ Nhật)
|   day_of_week |   total_carts |   abandoned_carts |   abandon_rate_pct |
|--------------:|--------------:|------------------:|-------------------:|
|             1 |        227211 |            115978 |              51.04 |
|             2 |        230090 |            119958 |              52.14 |
|             3 |        227717 |            115423 |              50.69 |
|             4 |        271783 |            161550 |              59.44 |
|             5 |        499855 |            381817 |              76.39 |
|             6 |        451326 |            294760 |              65.31 |
|             7 |        408452 |            186730 |              45.72 |

### Tỷ Lệ Abandon: New vs Returning Users
| is_returning   |   total_carts |   abandoned_carts |   abandon_rate_pct |
|:---------------|--------------:|------------------:|-------------------:|
| False          |        341164 |            195622 |              57.34 |
| True           |       1975270 |           1180594 |              59.77 |

## H3: Time Analytics
### Thời Gian Đến Lúc Mua
| metric                       |   p25 |   p50 |   p75 |   p90 |   p95 |     avg |
|:-----------------------------|------:|------:|------:|------:|------:|--------:|
| First Cart to Purchase (sec) |    48 |    99 |   192 |   359 |   563 | 198.401 |

### Thời Lượng Session Abandon
| metric                                    |   p25 |   p50 |   p75 |   p90 |   p95 |     avg |
|:------------------------------------------|------:|------:|------:|------:|------:|--------:|
| Session Duration of Abandoned Carts (sec) |    71 |   232 |   660 |  1607 |  2734 | 866.064 |

### Avg Events mỗi Session
| segment    |   avg_events |
|:-----------|-------------:|
| Overall    |      4.77681 |
| Purchased  |      8.19085 |
| Abandoned  |      9.44299 |
| Full Clear |    nan       |

## Metrics Tổng Hợp theo Tháng
| month               |   total_sessions |   sessions_cart |   sessions_purchase |   sessions_abandoned |     AOV |     ACV |   GMV_purchased |   GMV_at_risk |
|:--------------------|-----------------:|----------------:|--------------------:|---------------------:|--------:|--------:|----------------:|--------------:|
| 2019-10-01 00:00:00 |          9244770 |          573129 |              629572 |               281256 | 365.331 | 539.745 |     2.30002e+08 |   1.37879e+08 |
| 2019-11-01 00:00:00 |         13772820 |         1743305 |              773186 |              1094960 | 355.866 | 503.791 |     2.7515e+08  |   5.33126e+08 |

### Tỷ Lệ Quay Lại Sau Abandon
| Metric | Giá trị | Tỷ lệ |
|---|---|---|
| Tổng Sessions Abandoned | 1,376,216 | 100% |
| Đã Quay Lại (Bất kỳ lúc) | 1,132,391 | 82.28% |
| Quay lại trong 1h | 415,978 | 30.23% |
| Quay lại trong 24h | 798,480 | 58.02% |
| Quay lại trong 72h | 951,397 | 69.13% |
| Quay lại trong 7d | 1,042,655 | 75.76% |
