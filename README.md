# Tứ kỵ sỹ khải huyền — Review này có đáng tin không, và mình có nên mua không?

**Lớp:** L3A · **Track:** D — Thương mại điện tử.

**Repo:** [K5-Day15-L3A-TuKySyKhaiHuyen](https://github.com/baonvt/K5-Day15-L3A-TuKySyKhaiHuyen).

**Thành viên và mã học viên:** [TEAMS.md](TEAMS.md). Đội trưởng: **Nguyễn Võ Thái Bảo — 2A202603638**; dùng cùng mã này khi nộp các checkpoint.

## CP2 — Nội dung nộp form

**Thay đổi từ CP1.** Bản chạy thử nhận tối đa 30 review của một sản phẩm công nghệ, gắn ba nhãn độ tin cậy và nêu lý do. Mỗi ý tóm tắt dẫn mã review. Code tính điểm sao gốc và điểm sau khi loại các review có nhãn thấp. [Canvas](canvas.md) · [Sơ đồ kiến trúc trong §4](spec.md#kien-truc-cp2)

**Bằng chứng.** Nhóm đã đọc 5 tài liệu công khai về đánh giá ảo. Trong phần công nghệ của ViSpamReviews v2, 1.152/6.032 review mang nhãn spam do tác giả bộ dữ liệu gán (19,1%). Nhóm dùng các review này để dựng tình huống kiểm thử. Số người mua gặp khó khi đọc review, thời gian họ mất và số lần đổi trả vẫn cần đo. [Nguồn và tiến độ](evidence/summary.md) · [Data Card](data/DATA_CARD.md)

**Đánh giá.** 14 câu thử gồm 4 thường, 8 khó và 2 từ chối. Có 10 câu lấy từ dữ liệu thật. Hiệp và Sơn chấm cùng 5 đầu ra của bản giả, đồng thuận 5/5 ở kết luận từng câu. Trong mẫu đó chỉ B12 đạt. [Benchmark](eval/benchmark.csv) · [4 metric](eval/metric_spec.yaml) · [Chấm chéo](eval/cham-thu-cp2.md)

**Chuẩn đạt đã chốt (§7)**

> Đạt khi ≥ 70% câu qua (cột `pass`), và 100% câu `tu_choi` qua, không câu nào khẳng định một review là giả hoặc kết luận người bán lừa đảo

**Ví dụ demo.** Chạy `python run.py`, mở địa chỉ web hiện trong terminal rồi dán dòng sau hoặc chọn **Dùng ví dụ**.

```text
Sản phẩm: Tai nghe X || [5] Pin dùng được 2 ngày || [5] Shop uy tín, mua ngay nhé || [1] Tai trái mất tiếng sau 3 ngày
```

Ở chế độ giả, kết quả giữ R1 và R3, ghi nguồn cho nhận xét về pin và tai trái, rồi tính lại điểm từ **3,7** (3 review) xuống **3,0** (2 review).

## CP1 — Nội dung chuẩn bị nộp

**Bài toán:** Khi mua đồ công nghệ online, người mua mất thời gian đọc review mà vẫn khó biết đâu là trải nghiệm thật, đâu là lời quảng cáo. Họ có thể chọn nhầm sản phẩm rồi phải đổi trả.

**Lát cắt dự kiến:** Với một sản phẩm công nghệ người mua đang cân nhắc, hệ thống gắn nhãn dự đoán cho từng review, giải thích lý do rồi dùng các review được giữ lại để tóm tắt ưu nhược điểm và tính lại điểm sao.

**Canvas 7 dòng:** [canvas.md](canvas.md).

Ba chức năng MVP theo ý tưởng nhóm:

1. Đánh giá độ tin cậy từng review, kèm lý do ngắn gọn.
2. Tóm tắt ưu điểm, nhược điểm và vấn đề thường gặp từ tập review được giữ sau lọc.
3. So sánh điểm sao ban đầu với điểm sao tính lại sau lọc.

Nhóm chọn ngách sản phẩm công nghệ. Ba nhãn “Độ tin cậy cao”, “Chưa rõ độ tin cậy” và “Độ tin cậy thấp” thể hiện dự đoán của hệ thống. Người mua xem lý do rồi tự quyết định. Chuẩn đạt CP2 đã ghi tại §7 của spec.

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

Phần đã làm đến CP2 gồm bản chạy thử với model giả, nghiên cứu nguồn công khai, bộ câu thử, metric và chấm chéo.

## Chạy trong 3 phút

Cần Python 3.10 trở lên. Mở terminal tại thư mục có `run.py`, rồi chạy:

```powershell
python run.py
```

Demo chạy tại [127.0.0.1:8765](http://127.0.0.1:8765). Nếu trình duyệt chưa tự mở, mở địa chỉ đó trong lúc terminal vẫn đang chạy. Nhấn **Ctrl+C** trong terminal để dừng.

Trong **Dán nội dung**, bấm **Phân tích review** để gửi ngay hoặc nhấn **Enter** để tách bộ review sang các ô riêng. Dùng **Shift+Enter** để xuống dòng. Trong **Nhập từng review**, nhập tên sản phẩm nếu có, nhập nội dung, chọn số sao và bấm **+ Thêm review** nếu cần.

Để thử bằng model thật, điền `MODEL_PROVIDER=openrouter`, `MODEL_NAME` và `API_KEY` trong `.env`. Khi dùng chế độ `fake`, giao diện vẫn hiển thị kết quả mô phỏng.

## Lệnh

| Lệnh | Mục đích |
|---|---|
| `python run.py` | Mở giao diện web local để phân tích review |
| `python run.py check` | Kiểm định dạng `TEAMS.md`, bộ câu thử và metric |
| `python run.py eval --try` | Thử nối model khi triển khai CP2/CP3 |
| `python run.py eval` | Chạy bộ câu thử; AI giả không được tính là một lượt đánh giá thật |
| `python run.py score eval/run-N.csv` | Tính tỷ lệ đạt sau khi nhóm chấm cột `pass` |
| `python run.py simulate --try` | Thử mô phỏng chi phí ở giai đoạn sau |
| `python run.py simulate` | Chạy mô phỏng chi phí ở giai đoạn sau |

## Bản chạy thử — viết ở đâu

| File | Nội dung |
|---|---|
| `codebase/app.py`, `codebase/web/` | Máy chủ local và giao diện demo gọi luồng phân tích review |
| `codebase/agent.py` | Tách input, kiểm nhãn và nguồn, tổng hợp kết quả và tính sao |
| `codebase/tools.py` | Ví dụ của starter; luồng CP2 đọc trực tiếp các review trong input |
| `codebase/ai.py` | Gọi OpenRouter theo cấu hình `.env` hoặc chạy chế độ giả |
| `run.py`, `codebase/tracing.py`, `eval/run_eval.py`, `cost/simulate.py` | Giữ nguyên bộ khung BTC cấp |

Hướng dẫn cấu hình model trong [docs/connect-model.md](docs/connect-model.md). Giữ API key ở `.env` trên máy.

## Phần nào thật, phần nào giả

| Thành phần | Tình trạng |
|---|---|
| Tên, mã học viên, lớp, track, đội trưởng | Thông tin do nhóm cung cấp |
| Tài liệu công khai và 5 trích dẫn | Đã tìm và ghi nguồn tại [evidence/public-sources.md](evidence/public-sources.md) |
| Phỏng vấn, khảo sát, mẫu review nhóm tự thu | Chưa có |
| Giải pháp review chạy được | Giao diện demo web trên máy local |
| Model trong bộ khung | OpenRouter khi có cấu hình, mô phỏng ở chế độ `fake` |
| Hiệu quả của model thật và precision/recall/F1 | Chưa đo; không có kết quả để báo cáo |

## Dùng AI vào việc gì

Codex hỗ trợ đọc đề, chuẩn bị cấu trúc repo, ghi hồ sơ từ thông tin nhóm cung cấp và tìm nguồn công khai. Chưa có xác nhận kiểm tay của thành viên đối với tài liệu; chưa dùng kết quả AI làm lời phỏng vấn hoặc số liệu khảo sát. Chi tiết ở [docs/ai-usage.md](docs/ai-usage.md); quy ước cho coding agent ở [AGENTS.md](AGENTS.md).

## File mẫu — điền ở bước nào

| File | Mốc |
|---|---|
| [TEAMS.md](TEAMS.md), [canvas.md](canvas.md), README này | Hồ sơ CP1 đã hoàn thiện; phân công đã được nhóm xác nhận |
| [evidence/hypothesis.md](evidence/hypothesis.md), [evidence/summary.md](evidence/summary.md) | Bằng chứng đang phát triển, đủ ngưỡng trước CP3 |
| [spec.md](spec.md) | Thiết kế và chuẩn đạt ở CP2; các mục còn lại theo checkpoint |
| [data/DATA_CARD.md](data/DATA_CARD.md), [eval/benchmark.csv](eval/benchmark.csv), [eval/metric_spec.yaml](eval/metric_spec.yaml) | Bản CP2 gồm Data Card, 14 câu thử và 4 metric |
| [eval/README.md](eval/README.md), [eval/report.md](eval/report.md) | Hồ sơ và kết quả đánh giá ở giai đoạn sau |
| [cost/personas.yaml](cost/personas.yaml), [cost/cost-estimate.md](cost/cost-estimate.md) | Mô phỏng chi phí ở giai đoạn sau |
| [slides/outline.md](slides/outline.md), [reflection/TEMPLATE.md](reflection/TEMPLATE.md) | Slide và reflection ở giai đoạn sau |

## Bảy hạng mục bắt buộc — nằm ở file nào

| Hạng mục | Nơi lưu | Tiến độ |
|---|---|---|
| Bằng chứng pain | `evidence/` | Có tài liệu công khai; chưa có phép đếm pain của nhóm |
| Impact có số | `spec.md` §2 | Chưa làm |
| Thiết kế giải pháp | `spec.md` §4 | Có sơ đồ và mô tả luồng CP2 |
| Bản chạy thử làm trọn lát cắt | `codebase/` | Demo web gọi cùng luồng `answer()` với bộ eval |
| Bộ câu thử, metric và đánh giá | `data/`, `eval/` | Đã có benchmark CP2 và chấm chéo |
| Mô phỏng chi phí | `cost/` | Chưa làm |
| Slide, demo, video | `slides/`, PDF và link video khi có | Chưa làm |
