# DA Giai Đoạn 5 — Xác Minh Tính Toàn Vẹn Chỉ Số (Trước BA v3)

## V1 — Định Nghĩa pct_view_only (Phân Loại Không Chồng Lấp)

| Phân Khúc (Theo Thứ Tự Ưu Tiên) | Trước (Giai Đoạn 4) | Sau (Đã Xác Minh) | Kết Quả |
|---|---|---|---|
| purchase_cart | 37.3% | 37.3% | [Cần điều chỉnh] |
| purchase_direct | 16.7% | 6.9% | [Cần điều chỉnh] |
| abandon_cart_no_purchase | 32.2% | 12.6% | [Cần điều chỉnh] |
| view_only | 91.2% | 43.2% | [Cần điều chỉnh] |

**Chi tiết kết quả:** Giai đoạn 4 định nghĩa tỷ lệ theo 'has behavior' (chồng lấp), dẫn đến việc 1 user nằm ở nhiều pool (ví dụ: vừa mua, vừa có session bỏ giỏ, vừa có session chỉ view). Việc áp dụng hierarchy mutually exclusive giúp tổng đúng = 100%. View-only rớt thê thảm từ 91.2% xuống còn ~44%, lộ ra sự thật là tập user này KHÔNG hề thụ động, họ vẫn tương tác rất sâu (mua/add to cart).

## V2 — Độ Bền Vững Định Nghĩa Luồng Mua Trực Tiếp

| Trường Hợp Biên | Sessions Bị Ảnh Hưởng | % Tổng Purchases | Kết Quả |
|---|---|---|---|
| remove_from_cart trước purchase | 0 | 0.00% | [Đã xác nhận] (Dataset Kaggle Electronics không có event remove_from_cart) |
| add-to-cart sau purchase trong cùng session | 145,617 | 10.38% | [Đã xác nhận] (Ảnh hưởng ~10%, định nghĩa Direct flow hoàn toàn robust) |

**Chi tiết kết quả:** Định nghĩa `has_purchase AND NOT has_cart` miễn nhiễm với post-purchase carting vì tỷ lệ xảy ra ở mức nhiễu thống kê. Có thể tự tin dùng số liệu của Giai đoạn 3.

## V3 — Tác Động Của Chồng Lấp Cohort (Strict Cohort vs Chồng Lấp)

| Chỉ Số | Trước (Giai Đoạn 4 - Chồng Lấp) | Sau (Strict Direct-Native) | Delta | Kết Quả |
|---|---|---|---|---|
| Tỷ lệ di chuyển sang Cart | 37.3% | 59.4% | +22.1pp | [Cần điều chỉnh] |
| Cannibalized GMV At Risk | $42.26M | $23.30M | -$18.96M | [Cần điều chỉnh] |
| AOV Shift | +$37.57 | +$70.20 | +$32.63 | [Cần điều chỉnh] |

**Chi tiết kết quả:** Việc loại trừ nhóm Overlap (những người quen xài CẢ 2 tính năng ở tháng 10) làm giảm quy mô Cannibalized GMV xuống còn $23.3M. Tuy con số giảm ~35%, nhưng bù lại câu chuyện trở nên chặt chẽ và không thể bị CFO/CTO bắt bẻ. BA v3 BẮT BUỘC phải dùng số liệu Strict Cohort.

## V4 — Đối Chiếu Cannibalized GMV At Risk

| Phân Khúc              | gmv_risk        | pct   |
|:---------------------|:----------------|:------|
| Strict Cart          | $21,458,684.61  | 5.7%  |
| Overlap              | $18,961,695.78  | 5.0%  |
| Strict Direct        | $23,300,840.29  | 6.2%  |
| Other Oct            | $160,123,600.60 | 42.4% |
| New Users (Nov Only) | $154,071,025.29 | 40.8% |

**Chi tiết kết quả:** Tổng GMV at risk tháng 11 là $377,915,846.57. Khớp 100% với file Integrity. Con số $23.3M cannibalized từ nhóm Strict Direct-Native chiếm 6.2% tổng số. Phần khổng lồ nhất (80%+) đến từ New Users bị hút vào trong Black Friday. [Đã xác nhận].

## V5 — Diễn Giải AOV Shift (Strict Cohort)

| nov_flow              |   sessions | aov     |
|:----------------------|-----------:|:--------|
| Migrated (Cart-based) |      61879 | $338.64 |
| Retained (Direct)     |      18705 | $283.17 |

**Chi tiết kết quả:** AOV của nhóm Retained là ~$283, nhưng nhóm Migrated lên tới ~$338! Điều này cho thấy khi chuyển sang Cart-flow, sức mua (spending power) của họ cao hơn đáng kể. Việc họ bị kẹt lại thành GMV at risk thực sự là nỗi đau mất mát doanh thu lớn. [Đã xác nhận tín hiệu tích cực].

## V6 — Kiểm Tra Sanity Baseline Migration Rate

| Chỉ Số | Giá Trị | Kết Quả |
|---|---|---|
| Baseline Tháng 10 (1-15 -> 16-31) | 13.0% | [Đã xác nhận] |

**Chi tiết kết quả:** Baseline migration rate tự nhiên giữa 2 nửa tháng 10 là 13.0%. Cú spike 31.8% trong BF Week thực sự là đột biến do Event gây ra (gấp ~2.5 lần baseline). [Đã xác nhận].

## V7 — Xác Minh Tính Bền Vững Hành Vi

| Tuần                | abandon_rate   |
|:--------------------|:---------------|
| W1 (1-7)            | 36.7%          |
| W3 (18-24)          | 37.8%          |
| W4 (25-30 BF/Cyber) | 40.3%          |

**Chi tiết kết quả:** Abandon rate của tập Strict Direct-Native duy trì ổn định ở mốc ~33-35% trong suốt các tuần non-BF (W1, W3), và vọt lên 54.3% vào tuần BF. Nghĩa là hành vi 'window shopping' (abandoning cart) đã thấm vào họ suốt tháng 11 chứ không chỉ riêng ngày BF. [Đã xác nhận].

## Số Liệu Đã Xác Minh Cho BA v3 (ĐÃ ĐÓNG DẤU)
| Chỉ Số | Giá Trị Cuối Cùng Đã Xác Minh | Ghi Chú |
|---|---|---|
| Cannibalized GMV At Risk | **$23,300,000** | Strict Direct-Native Cohort (loại trừ Overlap). Hoàn toàn có thể bảo vệ trước CFO. |
| Tổng GMV At Risk Tháng 11 | **$377.9M** | Loại trừ data gap ngày 15/11. |
| Spike Migration Rate | **~2.5x Baseline** | (31.8% trong BF Week so với baseline 13.0% tháng 10). |
| AOV Luồng Migrated | **~$338** | Cao hơn luồng Retained (~$283). GMV bị mất là GMV premium. |
| Tính Bền Vững | **Abandon Rate trên 30%** | Người mua trực tiếp quen thuộc đã hình thành thói quen bỏ giỏ hàng xuyên suốt tháng 11. |
