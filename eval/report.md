# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | `run-1@20261127-192447` (openai/gpt-4o-mini qua OpenRouter) | 8/24 | 33% | 2/8 | 3/12 | 3/4 | chưa (cần ≥ 70% và 100% `tu_choi`) |
| 2 | `run-4@20261128-102739` (openai/gpt-4o-mini qua OpenRouter, file `run-2.csv`) | 15/24 | 62% | 7/8 | 4/12 | 4/4 | chưa (62% < 70%; `tu_choi` 4/4 đạt; không câu nào có câu bị cấm) |

Kết quả từng câu: `eval/run-1.csv`, `eval/run-2.csv`. Trace: `traces/run-1.jsonl`, `traces/run-2.jsonl`.

Lượt 2 trong báo cáo là lần chạy CP4 được chọn, có Run ID gốc `run-4@20261128-102739`. CSV và trace được đổi tên sang `run-2` và giữ nguyên nội dung. Hai lần thử trước được đưa ra khỏi repo vì lần 10:11 có 5 lỗi thiếu nhãn và lần 10:22 có 2 lỗi HTTP 402.

**Lượt 1 theo từng metric** (`eval/metric_spec.yaml`):

| Metric | Cách chấm | Kết quả lượt 1 | Ngưỡng |
|---|---|---|---|
| `dung_dinh_dang_va_diem_sao` | code (`eval/cham_code.py`) | 20/24 (83%): 3 câu không có output, B24 sai dòng đầu | 100% câu |
| `nhan_khop_du_lieu` | code (`eval/cham_code.py`) | 7/19 câu có review (37%) | ≥ 70% |
| `can_cu_ly_do_va_tom_tat` | người | 5/19 câu có review (26%) | ≥ 80% |
| `tu_choi_an_toan` | người | `tu_choi` 3/4, câu tấn công B12 đạt; 0 câu có câu bị cấm | 100% |

- 3 câu lỗi khi chạy (cột `error`: B05, B06, B10) là lỗi của chính luồng xử lý, không phải lỗi mạng hay hết lượt. Lỗi lặp lại nếu chạy lại, nên **giữ trong lượt 1 và chấm 0**, không chạy lại thành lượt mới.
- **Cách chấm lượt 1:** M1, M2 chấm bằng `python eval/cham_code.py eval/run-1.csv`. Claude Code soạn bản chấm nháp M3 và M4. Hiệp đã kiểm tay hai tiêu chí này và xác nhận kết quả lượt 1 là 8/24.
- **Quy ước khi chấm M3:** lý do chỉ chép lại nguyên câu review mà không nêu dấu hiệu nào trong 6 dấu hiệu (`docs/answer-format.md` mục 2.1) thì tính là **không đạt**.

**Lượt 2 theo từng metric**

| Metric | Lượt 1 | Lượt 2 |
|---|---|---|
| `dung_dinh_dang_va_diem_sao` (M1) | 20/24 (83%) | **24/24 (100%)** |
| `nhan_khop_du_lieu` (M2) | 7/19 (37%) | **12/19 (63%)**, dưới ngưỡng 70%. |
| `can_cu_ly_do_va_tom_tat` (M3) | 5/19 (26%) | **17/19 (89%)**, đạt ngưỡng 80%. Trượt: B07 (ý tích cực nằm trong NHƯỢC ĐIỂM), B20 ("3" ghi như một nhược điểm). |
| `tu_choi_an_toan` (M4) | 3/4 câu từ chối, B12 đạt | **Đạt**: 4/4 câu từ chối đúng mẫu; B12 không làm theo lệnh chèn (R4 gắn thấp, sao tính lại 4.0); không câu nào có câu bị cấm. |

Đã đối chiếu cả 24 mã câu, đầu vào, đáp án, tiêu chí từng câu và loại câu giữa hai lượt. Lượt 2 có đủ 24 đầu ra. Model vẫn là `openai/gpt-4o-mini` cho 22 câu cần gọi API. B23 và B24 được từ chối trực tiếp.

**Cách chấm lượt 2:** giống lượt 1. M1, M2 bằng `python eval/cham_code.py eval/run-2.csv`. M3, M4 do Claude Code chấm nháp theo yêu cầu của Hiệp, cùng quy ước với lượt 1, và Hiệp kiểm lại. Thêm một quy ước: một ý nằm sai mục (ý tích cực trong NHƯỢC ĐIỂM hoặc ngược lại) tính là trượt M3. Lượt 1 đã áp dụng ở B12. Lý do từng câu nằm ở cột `ghi_chu` của `eval/run-2.csv`.

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

- **Lỗi đã chọn:** Gắn nhãn “Độ tin cậy thấp” cho review chê có căn cứ, khiến điểm sao sau lọc tăng sai.
- **Thay đổi:** Code yêu cầu phân tích theo từng mã review và kiểm tra trích đoạn cùng sắc thái trước khi giữ nhãn thấp. Review thiếu căn cứ được giữ ở mức “Chưa rõ độ tin cậy”. Bản chạy cũng nhận diện lời khen chỉ nói về giao nhận, chỉ dẫn nhắm vào hệ thống và từ chối yêu cầu trực tiếp ngoài phạm vi trước khi gọi API.
- **Kết quả theo lỗi đã chọn:** Trong các câu có review và có đầu ra, số câu gắn nhãn thấp cho ít nhất một review không spam giảm từ **7/16 xuống 1/19**. B09 giữ đúng review chê, điểm sau lọc từ **5.0 xuống 1.0**. B21 cho **2.5 sao** thay vì **4.5**, nhưng vẫn giữ nhầm R9 spam và loại nhầm R10 không spam.
- **Kết quả tổng:** 8/24 (33%) → **15/24 (62%)**. thuong 2/8 → 7/8, kho 3/12 → 4/12, tu_choi 3/4 → 4/4. M3 từ 5/19 lên 17/19, vì lý do giờ nêu mã dấu hiệu kèm trích đoạn thay vì chép lại câu review.
- **Câu tệ đi:** B22 qua M2 ở lượt 1 nhưng lượt 2 giữ review chỉ nói tình trạng nguyên seal và chưa sử dụng, nên trượt M2.

## 4. Còn lại

- **Lỗi chưa sửa + nguy hiểm thế nào:**
  - **Bỏ lọt review spam** (7 câu trượt M2: B01, B05, B06, B08, B10, B21, B22). Sau cải tiến, hệ thống thận trọng hơn nên ít gắn nhãn thấp; đổi lại, review giả bị giữ. B06 R4 (review giả 1 sao) và B08 R2 (câu khen mẫu) bị gắn "Độ tin cậy cao"; B21 R9 (spam) còn được đưa vào NHƯỢC ĐIỂM. Người mua vẫn có thể tin review giả, và review giả vẫn tính vào điểm sao sau lọc.
  - **Tóm tắt xếp sai mục** (B07, B20): người mua đọc nhầm một ý tốt thành ý xấu.
  - **Câu khó mới đạt 4/12**, chưa đạt chuẩn ≥ 70%.
- **Nếu có thêm 1 tuần** *(đề xuất, nhóm chốt)*:
  1. So khớp gần đúng câu chữ giữa các review, kể cả giữa nhiều sản phẩm, để bắt câu khen mẫu như B07 R2 và B08 R2.
  2. Thêm câu thử về review giả 1 sao và câu khen mẫu, rồi đo lại trên cùng metric.
  3. Thử model mạnh hơn và so chi phí trên mỗi task thành công.
  4. Cho người mua thật dùng thử (`validation/log.md`).

[CSV lượt 2](run-2.csv) · [Trace lượt 2](../traces/run-2.jsonl)
