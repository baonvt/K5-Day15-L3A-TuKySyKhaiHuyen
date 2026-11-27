# Khai báo dùng AI

Nhóm sử dụng Codex để đọc bộ đề, đối chiếu yêu cầu CP1/CP2, sao chép khung nộp và ghi bản nháp từ thông tin nhóm cung cấp. Theo yêu cầu tiếp theo, Codex tìm tài liệu công khai và bổ sung 5 trích dẫn có nguồn. Nhóm đã xác nhận ngách sản phẩm công nghệ và ba nhãn review cho CP1. Chuẩn đạt còn chờ chốt ở CP2.

| Việc đã thực hiện | Công cụ AI | Phần AI làm | Người kiểm |
|---|---|---|---|
| Đọc yêu cầu và chuẩn bị thư mục | Codex | Đọc đề, guide, Track D và AGENTS.md; sao chép starter-repo | Chưa có xác nhận đã kiểm của nhóm |
| Điền thông tin nhóm | Codex | Ghi tên, mã học viên, lớp, track và đội trưởng từ thông tin nhóm | Chưa có xác nhận đã kiểm của nhóm |
| Nháp Canvas và trạng thái bằng chứng | Codex | Viết lại ý tưởng nhóm; ghi rõ giả thuyết chưa được kiểm chứng | Chưa có xác nhận đã kiểm của nhóm |
| Tìm tài liệu công khai | Codex và công cụ duyệt web | Đọc nguồn gốc, ghi URL/ngày/vị trí của 5 trích dẫn; phân biệt dữ liệu quốc tế, nhận định và ví dụ minh hoạ | Chưa có xác nhận đã kiểm của nhóm |
| Hoàn thiện hồ sơ CP1 | Codex | Điền repo công khai, viết bài toán và lát cắt, thống nhất README với Canvas và TEAMS; kiểm định dạng bằng bộ khung | Nhóm đã chốt phân công theo tên; chưa xác nhận đã kiểm tay toàn bộ nội dung |
| Định dạng input/output của `answer()` | Claude Code | Soạn nháp `docs/answer-format.md` theo yêu cầu của Hiệp: định dạng input, 3 loại output, nhãn review, cách tính điểm sao | Hiệp và Phong duyệt trước khi khoá metric CP2 |
| Bộ câu thử và metric CP2 | Claude Code | Tìm và tải bộ dữ liệu ViSpamReviews v2; viết `data/chon_review.py`, chọn 53 review đồ công nghệ thành 10 câu `data_that`; viết 4 câu `tu_viet`, `eval/metric_spec.yaml`, chuẩn đạt `spec.md` §7, `data/DATA_CARD.md`, `eval/README.md` mục 1–4. Nhãn spam là nhãn gốc của dataset, AI không tự gán | Hiệp kiểm trước khi khoá lúc 19:30; chưa có người thứ hai chấm thử |
| Phiếu chấm thử metric | Claude Code | Tạo `eval/cham-thu-cp2.md`: chép 5 output từ lượt chạy AI giả, hướng dẫn chấm và bảng so sánh | Sơn chấm tay độc lập |
| Phiếu chấm của người chấm 1 | Claude Code | Theo yêu cầu của Hiệp, soạn nháp phiếu chấm 5 câu (trước khi Sơn đẩy phiếu lên), điền bảng so sánh và `eval/README.md` mục 3 | Hiệp nhận làm phiếu của mình; khớp 5/5 với phiếu chấm tay của Sơn |

Đã nghiên cứu tài liệu công khai; chưa thu thập/gán nhãn bộ review sản phẩm, phỏng vấn, khảo sát, đánh giá mô hình hoặc mô phỏng chi phí. Không có kết quả kiểm tay của thành viên hay điểm số mô hình để khai báo.
