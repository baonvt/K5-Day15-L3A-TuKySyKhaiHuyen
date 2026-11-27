# Tứ kỵ sỹ khải huyền — Review này có đáng tin không, và mình có nên mua không?

**Lớp:** L3A · **Track:** D — Thương mại điện tử.

**Repo:** [K5-Day15-L3A-TuKySyKhaiHuyen](https://github.com/baonvt/K5-Day15-L3A-TuKySyKhaiHuyen).

**Thành viên và mã học viên:** [TEAMS.md](TEAMS.md). Đội trưởng: **Nguyễn Võ Thái Bảo — 2A202603638**; dùng cùng mã này khi nộp các checkpoint.

## CP3 — Nội dung nộp

| Mục trong form | Nội dung của nhóm |
|---|---|
| Bằng chứng | 6/8 bài đăng công khai kể rằng người mua gặp khó khi dùng review để chọn laptop hoặc tai nghe. Riêng phần tiếng Việt có 2/4 bài. Cả 8 bài đều có trích dẫn, đường dẫn và lý do xếp loại. [Tóm tắt](evidence/summary.md) · [Từng bài gốc](evidence/data-mining.md) |
| Bộ câu thử | 24 câu gồm 8 câu thường, 12 câu khó và 4 câu từ chối. 18 câu dùng review từ ViSpamReviews v2. [Benchmark](eval/benchmark.csv) · [Nguồn dữ liệu](data/DATA_CARD.md) |
| Demo | Video 30 giây ghi lại một lượt phân tích tai nghe bằng `openai/gpt-4o-mini` qua OpenRouter. Điểm gốc 3,7 từ ba review, còn 3,0 khi giữ lại hai review. Cuối video là kết quả chấm lượt 1. [Tải MP4](demo-cp3.mp4) |
| Kết quả lượt 1 | **8/24 câu đạt (33%)**. Câu thường 2/8, câu khó 3/12, câu từ chối 3/4. Run ID `run-1@20261127-192447`. Lượt 1 chưa đạt chuẩn §7. [CSV đã chấm](eval/run-1.csv) · [Trace](traces/run-1.jsonl) · [Báo cáo](eval/report.md) |
| Spec | §0–§7 ghi bằng chứng, so sánh ba hướng, kiến trúc, cách đọc đầu ra và chuẩn đạt đã chốt ở CP2. [Đọc spec](spec.md) |

**Trước khi gửi form.** Nhóm cần link video YouTube không công khai hoặc Google Drive cho phép bất kỳ ai có link xem được. Theo hồ sơ chấm, Hiệp còn cần xác nhận phần chấm tay M3 và M4. §2 đã ghi một trường hợp phải hỏi thêm, số phút người mua Việt Nam dành để đọc review mỗi tháng vẫn chưa đo.

**Chạy lại demo.** Điền `MODEL_PROVIDER=openrouter`, `MODEL_NAME=openai/gpt-4o-mini` và khóa riêng vào file `.env` cạnh `run.py`. Chạy `python run.py` rồi dán ví dụ tai nghe ở mục CP2. Có thể kiểm lại hồ sơ bằng `python run.py check` và `python run.py score eval/run-1.csv`.

## CP2 — Nội dung nộp form

**Thay đổi từ CP1.** Bản chạy thử nhận tối đa 30 review của một sản phẩm công nghệ, gắn ba nhãn độ tin cậy và nêu lý do. Mỗi ý tóm tắt dẫn mã review. Code tính điểm sao gốc và điểm sau khi loại các review có nhãn thấp. [Canvas](canvas.md) · [Sơ đồ kiến trúc trong §4](spec.md#kien-truc-cp2)

**Bằng chứng.** Nhóm đã đọc 5 tài liệu công khai về đánh giá ảo. Trong phần công nghệ của ViSpamReviews v2, 1.152/6.032 review mang nhãn spam do tác giả bộ dữ liệu gán (19,1%). Nhóm dùng các review này để dựng tình huống kiểm thử. Số người mua gặp khó khi đọc review, thời gian họ mất và số lần đổi trả vẫn cần đo. [Nguồn và tiến độ](evidence/summary.md) · [Data Card](data/DATA_CARD.md)

**Đánh giá.** 14 câu thử gồm 4 thường, 8 khó và 2 từ chối. Có 10 câu lấy từ dữ liệu thật. Hiệp và Sơn chấm cùng 5 đầu ra của bản giả, đồng thuận 5/5 ở kết luận từng câu. Trong mẫu đó chỉ B12 đạt. [Benchmark](eval/benchmark.csv) · [4 metric](eval/metric_spec.yaml) · [Chấm chéo](eval/cham-thu-cp2.md)

**Chuẩn đạt đã chốt (§7)**

> Đạt khi ≥ 70% câu qua (cột `pass`), và 100% câu `tu_choi` qua, không câu nào khẳng định một review là giả hoặc kết luận người bán lừa đảo

**Demo CP2.** Chạy `python run.py`, rồi dán dòng sau.

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

Cần Python 3.10 trở lên; bộ khung chưa cần cài thư viện ngoài. Mở terminal tại thư mục có `run.py`, rồi chạy:

```powershell
python run.py
python run.py check
```

`python run.py` chạy luồng phân tích review. Bộ câu thử CP3 có 24 câu và đã qua lệnh `check`.

## Lệnh

| Lệnh | Mục đích |
|---|---|
| `python run.py` | Chạy bản thử dòng lệnh; phân tích review bằng AI giả ở CP2 |
| `python run.py check` | Kiểm định dạng `TEAMS.md`, bộ câu thử và metric |
| `python run.py eval --try` | Thử nối model khi triển khai CP2/CP3 |
| `python run.py eval` | Chạy bộ câu thử; AI giả không được tính là một lượt đánh giá thật |
| `python run.py score eval/run-N.csv` | Tính tỷ lệ đạt sau khi nhóm chấm cột `pass` |
| `python run.py simulate --try` | Thử mô phỏng chi phí ở giai đoạn sau |
| `python run.py simulate` | Chạy mô phỏng chi phí ở giai đoạn sau |

## Bản chạy thử — viết ở đâu

| File | Nội dung |
|---|---|
| `codebase/agent.py` | Tách input, kiểm nhãn và nguồn, tổng hợp kết quả và tính sao |
| `codebase/tools.py` | Ví dụ của starter; luồng CP2 đọc trực tiếp các review trong input |
| `codebase/ai.py` | Chỗ gọi model; hiện dùng chế độ giả mặc định |
| `run.py`, `codebase/tracing.py`, `eval/run_eval.py`, `cost/simulate.py` | Giữ nguyên bộ khung BTC cấp |

Bản CP3 đã có code cho OpenRouter. Xem cấu hình thực tế ở mục CP3 phía trên. [Tài liệu tham khảo của khung](docs/connect-model.md).

## Phần nào thật, phần nào giả

| Thành phần | Tình trạng |
|---|---|
| Tên, mã học viên, lớp, track, đội trưởng | Thông tin do nhóm cung cấp |
| Tài liệu công khai và 5 trích dẫn | Đã tìm và ghi nguồn tại [evidence/public-sources.md](evidence/public-sources.md) |
| Phỏng vấn, khảo sát, mẫu review nhóm tự thu | Chưa có |
| Giải pháp review chạy được | Đã chạy cả demo giả CP2 và demo thật CP3 trên dòng lệnh |
| Model trong bộ khung | Dùng OpenRouter khi cấu hình khóa. Lượt 1 có trace với model và số token theo từng câu |
| Hiệu quả của model thật và precision/recall/F1 | Lượt 1 đạt 8/24 theo metric đã chốt. Chưa đo precision, recall và F1 |

## Dùng AI vào việc gì

Codex hỗ trợ đọc đề, chuẩn bị cấu trúc repo, ghi hồ sơ từ thông tin nhóm cung cấp và tìm nguồn công khai. Đến CP3, bảng bằng chứng đã có tám bài đăng kèm trích dẫn để kiểm lại. Chi tiết ở [docs/ai-usage.md](docs/ai-usage.md); quy ước cho coding agent ở [AGENTS.md](AGENTS.md).

## File mẫu — điền ở bước nào

| File | Mốc |
|---|---|
| [TEAMS.md](TEAMS.md), [canvas.md](canvas.md), README này | Hồ sơ CP1 đã hoàn thiện; phân công đã được nhóm xác nhận |
| [evidence/hypothesis.md](evidence/hypothesis.md), [evidence/summary.md](evidence/summary.md) | Bằng chứng đang phát triển, đủ ngưỡng trước CP3 |
| [spec.md](spec.md) | Thiết kế và chuẩn đạt ở CP2; các mục còn lại theo checkpoint |
| [data/DATA_CARD.md](data/DATA_CARD.md), [eval/benchmark.csv](eval/benchmark.csv), [eval/metric_spec.yaml](eval/metric_spec.yaml) | Bản CP3 có Data Card, 24 câu thử và 4 metric |
| [eval/README.md](eval/README.md), [eval/report.md](eval/report.md) | Hồ sơ và kết quả đánh giá lượt 1 |
| [cost/personas.yaml](cost/personas.yaml), [cost/cost-estimate.md](cost/cost-estimate.md) | Mô phỏng chi phí ở giai đoạn sau |
| [slides/outline.md](slides/outline.md), [reflection/TEMPLATE.md](reflection/TEMPLATE.md) | Slide và reflection ở giai đoạn sau |

## Bảy hạng mục bắt buộc — nằm ở file nào

| Hạng mục | Nơi lưu | Tiến độ |
|---|---|---|
| Bằng chứng pain | `evidence/` | 6/8 bài công khai nêu khó khăn, gồm 2/4 bài tiếng Việt |
| Impact có số | `spec.md` §2 | Đã so ba hướng và đếm một lần phải hỏi thêm ở trường hợp D01. Số phút mỗi tháng chưa đo |
| Thiết kế giải pháp | `spec.md` §4 | Có sơ đồ và mô tả luồng CP2 |
| Bản chạy thử làm trọn lát cắt | `codebase/` | Demo CP3 chạy thật bằng OpenRouter |
| Bộ câu thử, metric và đánh giá | `data/`, `eval/` | 24 câu ở CP3, lượt 1 đạt 8/24 |
| Mô phỏng chi phí | `cost/` | Chưa làm |
| Slide, demo, video | [Video CP3](demo-cp3.mp4) và `slides/` | Đã có MP4 cho CP3. Slide và PDF thuộc mốc sau |
