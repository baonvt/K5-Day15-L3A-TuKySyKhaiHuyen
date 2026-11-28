# Chi phí khi dùng thật

**Kịch bản cơ sở, 610 người dùng trong tháng.** Với `openai/gpt-4o-mini`, Soi Review tốn khoảng **0,001199 USD/task thành công** và **0,9041 USD/tháng** tiền token. Mô phỏng chạy qua cùng luồng phân tích review của bản demo. Tỷ lệ đạt dùng trong phép tính là 15/24 = 62,5%. [Kết quả mô phỏng](simulate-1.csv) · [Đánh giá lượt 2](../eval/run-2.csv)

## 1. Ai dùng và dùng bao nhiêu lần?

Một lượt hỏi phân tích review của một sản phẩm. Một phiên có thể gồm hai lượt khi người mua so các lựa chọn. Các bài D01, D02, D04 và D05 cung cấp ví dụ về hành vi cân nhắc một máy, so nhiều máy hoặc tìm hiểu trong nhiều đợt. Tỷ trọng người dùng, tần suất và cách chia lượt trong bảng dưới là **tự ước tính**. [Các bài gốc](../evidence/data-mining.md) · [Cấu hình chạy](personas.yaml)

| Kiểu người dùng | Tỷ trọng | Phiên/người/tháng | Lượt hỏi/phiên |
|---|---:|---:|---:|
| Xem một sản phẩm | 60% | 1 | 1 |
| So hai sản phẩm | 30% | 2 | 2 |
| Tìm hiểu nhiều đợt | 10% | 4 | 2 |

Việt Nam có gần 61 triệu người mua sắm trực tuyến năm 2023. Lấy tròn 61 triệu làm mốc quy mô, ba kịch bản giả định lần lượt 0,0001%, 0,001% và 0,01% dùng Soi Review trong tháng, tương ứng **61, 610 và 6.100 người**. Các tỷ lệ tiếp cận này là *tự ước tính*. Nhóm chưa có số người dùng hoạt động thực tế. [Bộ Công Thương, Sách trắng TMĐT 2023](https://moit.gov.vn/quan-ly-thi-truong/-bung-no-thuong-mai-dien-tu-va-cuoc-chien-chong-hang-gia-hang-nhai-bao-ve-quyen-loi-nguoi-tieu-dung.html)

## 2. Kết quả chạy

Run ID `simulate-1@20261128-140543` · seed 42 · **50 phiên**, 67 lượt hỏi, 50 phiên hợp lệ, 0 phiên có lỗi. Khung rút ngẫu nhiên có hoàn lại từ các câu thường và khó trong benchmark. Các phiên hợp lệ ghi nhận 154.153 token vào, 23.924 token ra, 67 lượt gọi model và 0 lượt gọi công cụ. Thời gian dưới đây là trung bình tổng thời gian xử lý các lượt trong mỗi phiên. [CSV từng phiên](simulate-1.csv) · [Trace](../traces/simulate-1.jsonl) · [Tóm tắt tự động](simulate-1-summary.md)

| Kiểu người dùng | Phiên hợp lệ | Lượt hỏi/phiên | Token vào/phiên | Token ra/phiên | Giây/phiên |
|---|---:|---:|---:|---:|---:|
| Xem một sản phẩm | 33 | 1 | 2.363 | 387 | 7,8 |
| So hai sản phẩm | 15 | 2 | 4.407 | 629 | 11,8 |
| Tìm hiểu nhiều đợt | 2 | 2 | 5.030 | 854 | 15,3 |

## 3. Ba kịch bản chi phí

Đơn vị USD. Token đo trên `openai/gpt-4o-mini` qua OpenRouter. Giá chuẩn theo một triệu token vào/ra lần lượt là 0,15/0,60 USD cho GPT-4o mini và 2,00/10,00 USD cho GPT-6.2 Sol. Dòng GPT-6.2 Sol là phép tính theo giá khác với cùng lượng token và giả định tỷ lệ đạt 62,5%. Nhóm chỉ đo chất lượng của GPT-4o mini. Nguồn đơn giá là [bảng giá K5 do BTC tra ngày 25/11/2026](https://github.com/VinUni-AI20k/K5-L3-Day15-AI-Product-Hackathon/blob/main/further-reading/model-prices.md).

| Model tính giá | Mỗi phiên | Mỗi task thành công | Thấp · 61 người/tháng | Cơ sở · 610 người/tháng | Cao · 6.100 người/tháng | Mỗi người/tháng |
|---|---:|---:|---:|---:|---:|---:|
| openai/gpt-4o-mini | 0,000750 | 0,001199 | 0,0904 | 0,9041 | 9,04 | 0,001482 |
| gpt-6.2-sol | 0,010951 | 0,017521 | 1,3216 | 13,2157 | 132,16 | 0,021665 |

Chi phí phiên = (token vào × giá vào + token ra × giá ra) / 1.000.000. Theo cách tính của đề, chi phí mỗi task thành công = chi phí trung bình mỗi phiên / (15/24). Tỷ lệ 15/24 được đo theo câu thử. Chi phí tháng cộng riêng từng persona theo số người × tỷ trọng × số phiên/người/tháng × chi phí trung bình của persona. Giá trị hiển thị đã làm tròn sau phép tính. Phạm vi tính gồm tiền token chuẩn, trước thuế, chưa gồm phí hạ tầng hoặc nhân công.

## 4. Chi phí có đáng so với thời gian đọc?

Một lượt kiểm 5 review mất khoảng 5 phút đọc thủ công theo giả định ở §2. Với cơ cấu persona trên, một người có trung bình 2,6 lượt hỏi/tháng, tương ứng **13 phút đọc thủ công/tháng**. Nếu công cụ tiết kiệm được 1 phút/lượt và định giá thời gian ở 3 USD/giờ (cả hai đều *tự ước tính*), giá trị tiết kiệm là 2,6 × 3/60 = **0,13 USD/người/tháng**. So với tiền token của GPT-4o mini là **0,001482 USD/người/tháng**, chỉ cần tiết kiệm khoảng 1,8 giây/người/tháng để bù khoản này theo mức định giá giả định. [Căn cứ về số review và thời gian đọc](../spec.md)

**Nhóm chọn tiếp tục thử nghiệm.** Chi phí token cho phép thử ở quy mô cơ sở. Trước khi mở rộng, cần đo thời gian bằng cùng nhiệm vụ với người mua và kiểm lại lỗi bỏ lọt spam. Lượt 2 mới đạt 15/24, dưới chuẩn 70%. [Các câu còn sai](../eval/report.md)

Để chạy lại từ gốc repo với model đã cấu hình, dùng `python run.py simulate --rate-from eval/run-2.csv`. Mỗi lượt chính thức sinh CSV, trace và bảng tổng hợp mới.
