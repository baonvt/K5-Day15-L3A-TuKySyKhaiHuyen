# Tứ kỵ sỹ khải huyền — Review này có đáng tin không, và mình có nên mua không?

**Lớp:** L3A · **Track:** D — Thương mại điện tử.

**Repo:** [K5-Day15-L3A-TuKySyKhaiHuyen](https://github.com/baonvt/K5-Day15-L3A-TuKySyKhaiHuyen).

**Thành viên và mã học viên:** [TEAMS.md](TEAMS.md). Đội trưởng: **Nguyễn Võ Thái Bảo — 2A202603638**; dùng cùng mã này khi nộp các checkpoint.

## CP1 — Nội dung chuẩn bị nộp

**Bài toán:** Khi mua đồ công nghệ online, người mua mất thời gian đọc review mà vẫn khó biết đâu là trải nghiệm thật, đâu là lời quảng cáo. Họ có thể chọn nhầm sản phẩm rồi phải đổi trả.

**Lát cắt dự kiến:** Với một sản phẩm công nghệ người mua đang cân nhắc, hệ thống gắn nhãn dự đoán cho từng review, giải thích lý do rồi dùng các review được giữ lại để tóm tắt ưu nhược điểm và tính lại điểm sao.

**Canvas 7 dòng:** [canvas.md](canvas.md).

Ba chức năng MVP theo ý tưởng nhóm:

1. Đánh giá độ tin cậy từng review, kèm lý do ngắn gọn.
2. Tóm tắt ưu điểm, nhược điểm và vấn đề thường gặp từ tập review được giữ sau lọc.
3. So sánh điểm sao ban đầu với điểm sao tính lại sau lọc.

Nhóm chọn ngách sản phẩm công nghệ. Ba nhãn “Độ tin cậy cao”, “Chưa rõ độ tin cậy” và “Độ tin cậy thấp” thể hiện dự đoán của hệ thống. Người mua xem lý do rồi tự quyết định. Nhóm sẽ chốt chuẩn đạt bằng số ở CP2.

| Yêu cầu CP1 | Tình trạng |
|---|---|
| Thông tin nhóm, mã học viên, đội trưởng ở dòng 1 | Đã điền trong `TEAMS.md` |
| Track + bài toán 1–2 câu | Đã có ở trên |
| Lát cắt dự kiến một câu | Đã có ở trên, khớp `canvas.md` |
| Canvas đủ 7 dòng | Đã điền đủ 7 dòng, gồm phân công theo tên nhóm đã xác nhận |
| Repo GitHub công khai, người không đăng nhập đọc được | Đã kiểm bằng GitHub API không dùng xác thực ngày 27/11/2026; repo có `README.md`, `TEAMS.md`, `canvas.md`, `run.py` ở gốc |
| Nộp form CP1 | Chưa xác nhận đã nộp; bộ đề đang để trống URL form, đội trưởng dùng link BTC cung cấp |

**Trạng thái:** Nội dung hồ sơ CP1 đã hoàn thiện. Đội trưởng dùng thông tin ở trên để nộp form CP1 do BTC cung cấp.

## Nhóm làm gì, khung làm gì

Nhóm xác định bài toán, nguồn bằng chứng, thiết kế, bộ câu thử và tiêu chí đánh giá. Repo giữ bộ khung BTC cấp để chạy bản thử, ghi trace, đánh giá và mô phỏng chi phí ở các checkpoint sau.

Phần đã làm: điền thông tin nhóm, viết hồ sơ CP1 và nghiên cứu nguồn công khai. Phần từ CP2 trở đi vẫn là mẫu hoặc đang chờ nhóm chốt; chưa có kết quả đánh giá mô hình hay mô phỏng chi phí.

## Chạy trong 3 phút

Cần Python 3.10 trở lên; bộ khung chưa cần cài thư viện ngoài. Mở terminal tại thư mục có `run.py`, rồi chạy:

```powershell
python run.py
python run.py check
```

`python run.py` hiện chạy **workflow ví dụ của starter-repo với AI giả**, chưa phải luồng review của nhóm. Lệnh `check` kiểm cả phần bộ câu thử và metric dành cho CP2/CP3, nên các phần mẫu đó còn cảnh báo ở giai đoạn CP1.

## Lệnh

| Lệnh | Mục đích |
|---|---|
| `python run.py` | Chạy bản thử dòng lệnh; hiện là ví dụ với AI giả |
| `python run.py check` | Kiểm định dạng `TEAMS.md`, bộ câu thử và metric |
| `python run.py eval --try` | Thử nối model khi triển khai CP2/CP3 |
| `python run.py eval` | Chạy bộ câu thử; AI giả không được tính là một lượt đánh giá thật |
| `python run.py score eval/run-N.csv` | Tính tỷ lệ đạt sau khi nhóm chấm cột `pass` |
| `python run.py simulate --try` | Thử mô phỏng chi phí ở giai đoạn sau |
| `python run.py simulate` | Chạy mô phỏng chi phí ở giai đoạn sau |

## Bản chạy thử — viết ở đâu

| File | Nội dung |
|---|---|
| `codebase/agent.py` | Luồng chính của lát cắt; hiện giữ ví dụ của khung |
| `codebase/tools.py` | Công cụ lấy dữ liệu của bài toán; hiện giữ ví dụ của khung |
| `codebase/ai.py` | Chỗ gọi model; hiện dùng chế độ giả mặc định |
| `run.py`, `codebase/tracing.py`, `eval/run_eval.py`, `cost/simulate.py` | Giữ nguyên bộ khung BTC cấp |

Nối model thật ở checkpoint sau theo [docs/connect-model.md](docs/connect-model.md). Không đưa API key vào repo.

## Phần nào thật, phần nào giả

| Thành phần | Tình trạng |
|---|---|
| Tên, mã học viên, lớp, track, đội trưởng | Thông tin do nhóm cung cấp |
| Tài liệu công khai và 5 trích dẫn | Đã tìm và ghi nguồn tại [evidence/public-sources.md](evidence/public-sources.md) |
| Phỏng vấn, khảo sát, mẫu review nhóm tự thu | Chưa có |
| Giải pháp review chạy được | Chưa triển khai; đang ở CP1 |
| Model trong bộ khung | AI giả; chưa gọi model thật |
| Số liệu hiệu quả, điểm sao điều chỉnh và precision/recall/F1 của nhóm | Chưa đo; không có kết quả để báo cáo |

## Dùng AI vào việc gì

Codex hỗ trợ đọc đề, chuẩn bị cấu trúc repo, ghi hồ sơ từ thông tin nhóm cung cấp và tìm nguồn công khai. Chưa có xác nhận kiểm tay của thành viên đối với tài liệu; chưa dùng kết quả AI làm lời phỏng vấn hoặc số liệu khảo sát. Chi tiết ở [docs/ai-usage.md](docs/ai-usage.md); quy ước cho coding agent ở [AGENTS.md](AGENTS.md).

## File mẫu — điền ở bước nào

| File | Mốc |
|---|---|
| [TEAMS.md](TEAMS.md), [canvas.md](canvas.md), README này | Hồ sơ CP1 đã hoàn thiện; phân công đã được nhóm xác nhận |
| [evidence/hypothesis.md](evidence/hypothesis.md), [evidence/summary.md](evidence/summary.md) | Bằng chứng đang phát triển, đủ ngưỡng trước CP3 |
| [spec.md](spec.md) | Thiết kế và chuẩn đạt ở CP2; các mục còn lại theo checkpoint |
| [data/DATA_CARD.md](data/DATA_CARD.md), [eval/benchmark.csv](eval/benchmark.csv), [eval/metric_spec.yaml](eval/metric_spec.yaml) | Bản đầu CP2; hiện còn là mẫu |
| [eval/README.md](eval/README.md), [eval/report.md](eval/report.md) | Hồ sơ và kết quả đánh giá ở giai đoạn sau |
| [cost/personas.yaml](cost/personas.yaml), [cost/cost-estimate.md](cost/cost-estimate.md) | Mô phỏng chi phí ở giai đoạn sau |
| [slides/outline.md](slides/outline.md), [reflection/TEMPLATE.md](reflection/TEMPLATE.md) | Slide và reflection ở giai đoạn sau |

## Bảy hạng mục bắt buộc — nằm ở file nào

| Hạng mục | Nơi lưu | Tiến độ |
|---|---|---|
| Bằng chứng pain | `evidence/` | Có tài liệu công khai; chưa có phép đếm pain của nhóm |
| Impact có số | `spec.md` §2 | Chưa làm |
| Thiết kế giải pháp | `spec.md` §4 | Chưa chốt |
| Bản chạy thử làm trọn lát cắt | `codebase/` | Chưa triển khai |
| Bộ câu thử, metric và đánh giá | `data/`, `eval/` | Còn mẫu |
| Mô phỏng chi phí | `cost/` | Chưa làm |
| Slide, demo, video | `slides/`, PDF và link video khi có | Chưa làm |
