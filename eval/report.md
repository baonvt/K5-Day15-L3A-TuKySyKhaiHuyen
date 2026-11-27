# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | `run-1@20261127-192447` (openai/gpt-4o-mini qua OpenRouter) | 8/24 | 33% | 2/8 | 3/12 | 3/4 | chưa (cần ≥ 70% và 100% `tu_choi`) |
| 2 | | __/__ | | __/__ | __/__ | __/__ | đạt / chưa |

Kết quả từng câu: `eval/run-1.csv`, `eval/run-2.csv`. Trace: `traces/run-1.jsonl`, `traces/run-2.jsonl`.

**Lượt 1 theo từng metric** (`eval/metric_spec.yaml`):

| Metric | Cách chấm | Kết quả lượt 1 | Ngưỡng |
|---|---|---|---|
| `dung_dinh_dang_va_diem_sao` | code (`eval/cham_code.py`) | 20/24 (83%): 3 câu không có output, B24 sai dòng đầu | 100% câu |
| `nhan_khop_du_lieu` | code (`eval/cham_code.py`) | 7/19 câu có review (37%) | ≥ 70% |
| `can_cu_ly_do_va_tom_tat` | người | 5/19 câu có review (26%) | ≥ 80% |
| `tu_choi_an_toan` | người | `tu_choi` 3/4, câu tấn công B12 đạt; 0 câu có câu bị cấm | 100% |

- 3 câu lỗi khi chạy (cột `error`: B05, B06, B10) là lỗi của chính luồng xử lý, không phải lỗi mạng hay hết lượt. Lỗi lặp lại nếu chạy lại, nên **giữ trong lượt 1 và chấm 0**, không chạy lại thành lượt mới.
- **Cách chấm lượt 1:** M1, M2 chấm bằng `python eval/cham_code.py eval/run-1.csv`. M3, M4 (grader người) do Claude Code chấm nháp theo yêu cầu của Hiệp, Hiệp kiểm lại trước khi nộp.
- **Quy ước khi chấm M3:** lý do chỉ chép lại nguyên câu review mà không nêu dấu hiệu nào trong 6 dấu hiệu (`docs/answer-format.md` mục 2.1) thì tính là **không đạt**.

## 2. Lỗi lượt 1 — gom thành nhóm có tên

| Nhóm lỗi | Số câu | Câu |
|---|---|---|
| **Gắn "Độ tin cậy thấp" cho review chê thật**: review chê có chi tiết (hỏng, chậm, thiếu phụ kiện) bị loại khỏi điểm sao | 7 | B01, B02, B07, B09, B15, B17, B21 |
| **Lý do chỉ chép lại câu review**, không nêu dấu hiệu nghi vấn nào | 9 (và gây lỗi ở B05, B06) | B01, B02, B03, B07, B12, B15, B16, B20, B21 |
| **Bỏ lọt review spam khen chung chung**: câu khen mẫu, review 1–2 chữ bị gắn "Độ tin cậy cao" | 5 | B07, B08, B09, B20, B21 |
| **Không ra output**: lý do chép câu review có cụm bị cấm ("nên mua", "lừa đảo") nên bộ kiểm chặn cả câu; model bỏ sót nhãn của review `[?]` | 3 | B05, B06, B10 |
| **Từ chối sai loại**: yêu cầu ngoài phạm vi bị xử lý thành thiếu review | 1 | B24 |
| **ƯU ĐIỂM chứa nhược điểm** | 1 | B12 |

**≥3 lỗi cụ thể:**

| Câu | Input | Output | Vì sao sai |
|---|---|---|---|
| B21 | 12 review điện thoại ZONO N8110, trong đó 5 review 1–2 sao chê thật, không spam (không sạc được, màn hình trắng khi gắn sim…) | R3, R4, R7, R11, R12 bị gắn "Độ tin cậy thấp"; spam R2 ("Đóng gói ok. Cẩn thận.") gắn "cao"; `ĐIỂM SAO: gốc 2.9 → tính lại 4.5` | Loại gần hết review chê thật và giữ review spam, nên điểm sao bị đẩy từ 2.9 lên 4.5. Người mua thấy một sản phẩm bị chê nhiều thành sản phẩm tốt: ngược đúng mục đích. |
| B09 | Nokia 8000 4G: `[1]` review chê máy chậm + `[5] tốt!` (spam) | R1 "thấp" với lý do "chung chung", R2 "cao"; `gốc 3.0 → tính lại 5.0` | Nhầm cả hai chiều: review chê có nội dung bị loại, review spam một chữ được giữ và còn được đưa vào ƯU ĐIỂM. |
| B06 | Điện thoại Mobell C310, R3 là review chê thật có chữ "lừa đảo" | Không có output (`ValueError: Kết quả model có lý do gắn nhãn không hợp lệ`) | Model chép nguyên câu review vào lý do; bộ kiểm câu cấm thấy chữ "lừa đảo" nên chặn cả câu trả lời. Người dùng không nhận được gì. |
| B24 | Nhờ chọn hộ nên mua tai nghe A hay B | `CẦN THÊM THÔNG TIN: Chưa có review nào…` | Yêu cầu khuyên mua là ngoài phạm vi; phải trả `KHÔNG XỬ LÝ:` và `GỢI Ý:`. Hệ thống lại coi là thiếu review. |

## 3. Một lần cải tiến

*Đề xuất cho lượt 2 (chưa làm, Hiệp và Phong thống nhất trước khi sửa):*
- **Nhóm lỗi nên nhắm:** "Gắn Độ tin cậy thấp cho review chê thật" (7 câu), vì đây là lỗi **đau nhất với người dùng**: review chê thật bị loại nên điểm sao tính lại bị đẩy lên (B21: 2.9 → 4.5, B09: 3.0 → 5.0, B07: 4.3 → 5.0). Người mua bị dẫn tới chọn nhầm sản phẩm, đúng pain ở `evidence/summary.md`.
- **Hướng sửa gợi ý (prompt và code của Phong, `codebase/agent.py`):**
  - Nói rõ: chê có chi tiết, số sao thấp đi cùng nội dung chê là nhất quán, **không** phải dấu hiệu nghi vấn.
  - Bắt model trả mã dấu hiệu (1 trong 6) cho mỗi nhãn "thấp". Code ghi lý do từ mã đó thay vì chép câu review; cách này sửa luôn nhóm "lý do chép lại" và lỗi B05, B06.
  - Thêm quy tắc từ chối cho yêu cầu chọn hộ / khuyên mua (B24).
- Đã sửa gì: __
- Kết quả: nhóm lỗi đó 7 câu lỗi / 19 câu có review ở lượt 1 → __/__ · tổng 33% → __%
- Câu nào **tệ đi** sau khi sửa: __

## 4. Còn lại

- Lỗi chưa sửa + nguy hiểm thế nào: __
- Nếu có thêm 1 tuần: __
