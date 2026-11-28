# Khai báo dùng AI

Nhóm sử dụng Codex để đọc bộ đề, đối chiếu yêu cầu CP1/CP2, sao chép khung nộp và ghi bản nháp từ thông tin nhóm cung cấp. Theo yêu cầu tiếp theo, Codex tìm tài liệu công khai và bổ sung 5 trích dẫn có nguồn. Nhóm đã xác nhận ngách sản phẩm công nghệ và ba nhãn review cho CP1. Chuẩn đạt đã được ghi tại §7 ở bản CP2.

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
| Mở rộng bộ câu thử cho CP3 | Claude Code | Bỏ số câu viết cứng trong `metric_spec.yaml` (trước 19:30, giữ ngưỡng); chọn thêm 46 review thật của 7 sản phẩm thành B15–B22, viết B23–B24; cập nhật DATA_CARD, `eval/README.md`, `spec.md` §7, §10. Nhãn spam vẫn là nhãn gốc của dataset | Hiệp duyệt trước khi chạy lượt 1 |
| Lượt 1 (CP3) | Claude Code | Chạy `python run.py eval` trên máy Hiệp; viết `eval/cham_code.py` chấm 2 metric code; chấm nháp 2 metric người cho 24 câu, điền cột `pass`, `ghi_chu` của `eval/run-1.csv`; viết `eval/report.md` mục 1–2, đề xuất mục 3, `eval/README.md` mục 5–6, kết quả ở `spec.md` §7 | Hiệp đã kiểm tay M3, M4 và xác nhận lượt 1 đạt 8/24. |
| Chấm lượt 2 (CP4) | Claude Code | Chạy `eval/cham_code.py` cho M1, M2; chấm nháp M3, M4 cho 24 câu của `eval/run-2.csv`, điền `pass`, `ghi_chu`; điền số lượt 2 vào `eval/report.md` (mục 1, 3, 4), `eval/README.md` mục 5–6, `spec.md` §7 | Hiệp kiểm lại M3, M4 từng câu trước khi nộp |
| Phiếu chấm của người chấm 1 | Claude Code | Theo yêu cầu của Hiệp, soạn nháp phiếu chấm 5 câu (trước khi Sơn đẩy phiếu lên), điền bảng so sánh và `eval/README.md` mục 3 | Hiệp nhận làm phiếu của mình; khớp 5/5 với phiếu chấm tay của Sơn |

Ở CP3, nhóm dùng bài đăng công khai và nhãn có sẵn trong ViSpamReviews v2. Nhóm chưa phỏng vấn hoặc khảo sát. Bảng trên ghi cách chấm lượt 1 và việc Hiệp xác nhận kết quả.

CP2: Bảo dùng Codex để tổng hợp Canvas, mô tả luồng theo code, nối các kịch bản với benchmark và chuẩn bị nội dung nộp trong README.

CP3: Bảo dùng Codex đối chiếu các bài công khai, đếm lại bảng D01–D08, đọc mô tả Review Highlights của Amazon và tổng hợp §0–§7. Codex kiểm tra khung, đối chiếu trace và tính lại điểm trên file lượt 1 của Hiệp. Theo yêu cầu của Bảo, Codex thao tác trên giao diện web của nhóm, quay lượt gọi OpenRouter thật, xuất video 30 giây và kiểm tra file trên Drive khi không đăng nhập.
