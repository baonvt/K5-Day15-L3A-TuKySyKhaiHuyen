# Canvas — Tứ kỵ sỹ khải huyền · Track D

CP2 · Lớp L3A · 27/11/2026

| # | Nội dung | Nhóm điền |
|---|---|---|
| 1 | Track và hướng làm | **D — Thương mại điện tử.** Giúp người mua cân nhắc sản phẩm công nghệ qua review. |
| 2 | Người dùng chính | Người mua ở Việt Nam đang đọc review để chọn đồ công nghệ trên sàn thương mại điện tử. |
| 3 | Bài toán | Khi mua đồ công nghệ online, người mua mất thời gian đọc review mà vẫn khó biết đâu là trải nghiệm thật, đâu là lời quảng cáo. Họ có thể chọn nhầm sản phẩm rồi phải đổi trả. |
| 4 | Bằng chứng đầu | Trong 6.032 review sản phẩm công nghệ thuộc ViSpamReviews v2, tác giả bộ dữ liệu gắn nhãn spam cho 1.152 review (19,1%). Con số này mô tả tập nghiên cứu. Về khó khăn của người mua, Ủy ban Cạnh tranh Quốc gia nhận xét về đánh giá có trả phí: “các đánh giá này dễ khiến người tiêu dùng tin tưởng và khó nhận ra là giả.” [Data Card](data/DATA_CARD.md) · [Nguồn S01](evidence/public-sources.md#s01) |
| 5 | Lát cắt đã chốt | Với một sản phẩm công nghệ người mua đang cân nhắc, hệ thống gắn nhãn dự đoán cho từng review, giải thích lý do rồi dùng các review được giữ lại để tóm tắt ưu nhược điểm và tính lại điểm sao. |
| 6 | Mức tự động và lý do | Ba nhãn “Độ tin cậy cao”, “Chưa rõ độ tin cậy” và “Độ tin cậy thấp” thể hiện dự đoán dựa trên dấu hiệu trong review. Người mua xem lý do rồi tự quyết định, vì gắn nhãn sai có thể ảnh hưởng cả người mua và người bán. |
| 7 | Phân công | **Nguyễn Võ Thái Bảo:** đội trưởng, tổng hợp hồ sơ và nộp bài; **Võ Sỹ Thái Sơn:** thu thập và kiểm tra bằng chứng; **Trần Nguyễn Anh Phong:** thiết kế và code; **Đoàn Văn Hiệp:** bộ câu thử và đánh giá. |

**Thay đổi so với CP1**

Nhóm đã triển khai luồng dán review của một sản phẩm, dẫn mã nguồn cho từng ý và tính sao trước/sau lọc bằng code.
Bộ đánh giá có 14 câu và 4 metric với chuẩn đạt ghi ở §7. Hiệp và Sơn đồng thuận 5/5 khi chấm thử.
