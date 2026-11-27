# Data card — dữ liệu bản chạy thử dùng

> Điền ở guide bước 2.4 (bản đầu ở CP2, đủ ở CP3). Ôn lại: ngày 6 · lab ngày 6. Chấm ở rubric R4.
> Một trang. Mỗi dataset một mục. Dữ liệu chạy thử (bài mẫu, thông báo mẫu, đoạn transcript…) để trong thư mục `data/` này.
> Không commit nguyên tài liệu khoá, dữ liệu cá nhân thật hay nguyên file data BTC cấp — chỉ đoạn trích ngắn, bản viết lại, hoặc số đã tổng hợp.

*Bản đầu CP2 · 27/11/2026 · người làm: Đoàn Văn Hiệp (trích và chọn review có AI hỗ trợ, xem `docs/ai-usage.md`).*

## Dataset 1 · ViSpamReviews v2: review sản phẩm trên sàn TMĐT Việt Nam, có nhãn spam

| | |
|---|---|
| Dùng để làm gì | Bộ câu thử: 18 câu `data_that` (B01–B10, B15–B22) và 4 review thật trong câu B12 của `eval/benchmark.csv`. Nhãn spam / không spam gốc là đáp án để chấm metric `nhan_khop_du_lieu`. |
| Từ đâu | Bộ dữ liệu nghiên cứu công khai của Co Van Dinh, Son T. Luu, Anh Gia-Tuan Nguyen: *Detecting Spam Reviews on Vietnamese E-commerce Websites* (ACIIDS 2022, [arXiv 2207.14636](https://arxiv.org/abs/2207.14636)); bản v2 có thêm thông tin sản phẩm ([arXiv 2405.13292](https://arxiv.org/abs/2405.13292)). File `dataset/vispamdetectionv2.zip` trong repo [sonlam1102/vispamdetection](https://github.com/sonlam1102/vispamdetection). Review lấy từ Tiki và Shopee. |
| Xử lý những bước gì | Lọc 3 nhóm hàng công nghệ (`Điện Tử`, `Điện Thoai - Máy Tính`, `Máy Ảnh`). Nhóm review theo link sản phẩm. Chọn tay 18 sản phẩm vừa có review spam vừa có review không spam, mỗi câu lấy 1–12 review của **một** sản phẩm. Bỏ qua review thật có lời kêu gọi mua rõ ("mn nên mua nha") để không mâu thuẫn với dấu hiệu nghi vấn trong `docs/answer-format.md`. Làm sạch: gộp về một dòng, che SĐT / link / email, bỏ ký tự `\|\|`, cắt review dài còn 250 ký tự (6 review bị cắt). B10 bỏ số sao của 1 review (ghi `[?]`) để thử trường hợp thiếu thông tin. Script: `data/chon_review.py` (mã dòng gốc `<split>:<số dòng>` ghi ở cột `source`). |
| Số dòng / số đoạn | Gốc 19.870 review. Nhóm hàng công nghệ: 6.032 review / 579 sản phẩm, trong đó 1.152 review gán spam (19,1%). Đưa vào bộ câu thử: **99 review thật** của 18 sản phẩm, 34 review spam (bản CP2: 53 review / 11 sản phẩm; thêm B15–B22 cho CP3). |
| Phiên bản / ngày lấy | v2, file trong zip ngày 06/04/2023. Tải ngày 27/11/2026. |
| Nhãn | **Thật**: nhãn do nhóm tác giả gán tay theo quy trình trong bài báo. `label` 0/1 (không spam / spam); `spam_label`: 1 = review giả, 2 = chỉ nói về shop / giao hàng, 3 = không liên quan / vô nghĩa. |
| Giới hạn | 93% review gốc là 5 sao, nên điểm sao gốc thường cao. Nhãn spam gộp cả review rác, quảng cáo, review chỉ nói về giao hàng, không chỉ review mua bán. Có chỗ nhãn không nhất quán (vd review rất ngắn "tốt" bị gán spam nhưng "hài lòng về chất lượng" thì không), nên metric chấp nhận nhãn `Chưa rõ độ tin cậy` ở cả hai phía. Dữ liệu cũ (bài báo 2022), chưa chắc giống review hiện nay. Thiếu thông tin người viết, nên không kiểm được tài khoản ảo. |
| Giấy phép | README của repo gốc ghi bộ dữ liệu dùng cho mục đích nghiên cứu và mời liên hệ tác giả khi sử dụng. Nhóm dùng cho bài hackathon học tập, không thương mại, có trích nguồn; **chưa liên hệ tác giả**. Không commit file dataset, chỉ commit 99 đoạn trích nằm trong bộ câu thử. |
| Dữ liệu cá nhân | Dataset không có tên hay tài khoản người viết. Script che SĐT, link, email. 99 review được chọn đã đọc lại: không thấy thông tin cá nhân (bỏ qua một review có nêu tên riêng). |

## Dataset 2 · Câu thử tự viết (`tu_viet`)

| | |
|---|---|
| Dùng để làm gì | 6 câu thử: B11 (hỏi mà không dán review), B12 (1 review tấn công chèn lệnh vào giữa 4 review thật), B13, B14, B23, B24 (`tu_choi`: nhờ viết review giả, đòi kết luận người bán lừa đảo, đòi lộ hướng dẫn hệ thống, đòi chọn hộ sản phẩm nên mua). |
| Từ đâu | Nhóm tự viết theo các kịch bản khó: lớp 2 (thiếu thông tin), lớp 3 (ngoài phạm vi, tấn công). |
| Nhãn | `synthetic`. **Không phải bằng chứng pain.** |
| Người kiểm | Hiệp (người viết). Chưa có người thứ hai kiểm. |
