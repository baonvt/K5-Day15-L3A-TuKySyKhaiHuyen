# Tóm tắt mô phỏng simulate-1@20261128-140543

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| xem_mot_san_pham | 33 | 1 | 2363 | 387 | 1.0 | 0.0 |
| so_hai_san_pham | 15 | 2 | 4407 | 629 | 2.0 | 0.0 |
| tim_hieu_nhieu_dot | 2 | 2 | 5030 | 854 | 2.0 | 0.0 |

Tỉ lệ đạt dùng để tính: 15/24 (62%) — lượt run-4@20261128-102739

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-2.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (61 người) | Chi phí / tháng — cơ sở (610 người) | Chi phí / tháng — cao (6.100 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| openai/gpt-4o-mini (vào 0.15 · ra 0.6 $/1M) | $0.00075 | $0.0012 | $0.00089 | $0.0904 | $0.9041 | $9.04 | $0.0015 |
| gpt-6.2-sol (vào 2.0 · ra 10.0 $/1M) | $0.0110 | $0.0175 | $0.0131 | $1.32 | $13.22 | $132.16 | $0.0217 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (1.3) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: openai/gpt-4o-mini. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
