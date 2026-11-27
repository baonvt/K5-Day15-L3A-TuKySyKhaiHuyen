# Đào data — cách đếm và kết quả

## 1. Cách thu thập nguồn công khai

Ngày thực hiện: 27/11/2026, giờ Việt Nam. Nhóm yêu cầu nguồn chuẩn và ít nhất 5 trích dẫn nguyên văn; chưa chốt ngách sản phẩm hoặc ngưỡng kiểm chứng pain.

Giai đoạn này là nghiên cứu tài liệu công khai. Chưa thực hiện lấy mẫu review của sản phẩm hay bài kể trải nghiệm của người mua. Nội dung dưới ghi quy trình đã làm, không nhận là một kế hoạch lấy mẫu đã đăng ký trước.

- Tìm bằng tiếng Việt và tiếng Anh, kết hợp tên vấn đề với tên miền cơ quan quản lý hoặc nhà xuất bản nghiên cứu.
- Các truy vấn đã dùng gồm: `site.gov.vn đánh giá giả mua sắm trực tuyến đánh giá ảo người tiêu dùng`, `site.vcc.gov.vn "review" "đánh giá"`, `site.ftc.gov fake reviews consumers rule 2024 2025 online reviews`, và `site.gov.uk "Amazon" "fake reviews" "June" "2025"`.
- Đọc trực tiếp trang gốc; dùng nguồn gốc cho trích dẫn, không dùng đoạn tóm tắt của blog thương mại hay kết quả tìm kiếm làm lời phỏng vấn.
- Giữ tài liệu liên quan đến khó nhận biết review giả, tác hại hoặc thao túng điểm sao; chọn 4 tài liệu quản lý và 1 nghiên cứu đã xuất bản. Loại bài bán dịch vụ seeding, blog quảng bá sản phẩm, kết quả không liên quan; chưa dùng preprint làm bằng chứng chính.
- Ghi ngày công bố, ngày truy cập, vị trí và một đoạn ngắn nguyên văn mỗi tài liệu trong `public-sources.md`. Không chép toàn bài.

## 2. Kết quả đã có

| Hạng mục | Kết quả thực tế | Cách kiểm |
|---|---|---|
| Tài liệu nguồn gốc được lưu dẫn nguồn | 5 tài liệu | Mở các URL S01–S05 trong `public-sources.md` |
| Trích dẫn nguyên văn ngắn | 5 đoạn, mỗi tài liệu một đoạn | Đối chiếu đoạn và vị trí ghi kèm |
| Tài liệu quản lý Việt Nam | S01 | Xem nguồn và giới hạn |
| Nghiên cứu định lượng đã công bố | S02 | Đọc phương pháp và phạm vi ở báo cáo gốc; chưa tái phân tích dữ liệu của nghiên cứu |
| Bộ review do nhóm thu và gán nhãn | Chưa có | Không ghi x/N hay precision/recall/F1 của nhóm |

Số tài liệu không phải số người gặp pain. Không dùng tỷ lệ tài liệu đề cập vấn đề để suy ra tỷ lệ review giả hoặc tỷ lệ người mua bị ảnh hưởng.

## 3. Phép đếm x/N của nhóm

**Chưa thực hiện.** Chưa có tập review được chọn theo một quy tắc cố định, nhãn từng dòng hoặc mẫu số N để báo cáo tỷ lệ pain. Các tỷ lệ trong tài liệu là kết quả của tác giả nguồn, không phải số nhóm tự đếm.

Vì chưa có phép đếm này, chưa có script đếm raw review để chạy lại. Không dựng một phép đếm tài liệu rồi coi đó là tỷ lệ người dùng gặp pain.

## 4. Năm trích dẫn có nguồn

Xem [S01](public-sources.md#s01), [S02](public-sources.md#s02), [S03](public-sources.md#s03), [S04](public-sources.md#s04), [S05](public-sources.md#s05). Chưa coi là năm review sản phẩm đã xác thực hay lời của năm người được phỏng vấn.

## 5. Giới hạn và tiến độ CP2/CP3

Nguồn công khai hỗ trợ bối cảnh vấn đề và cung cấp số liệu nghiên cứu bên ngoài. Chưa đo thời gian đọc/tổng hợp review, quy mô pain tại Việt Nam, nguyên nhân đổi trả, hoặc hiệu quả giải pháp. Chưa có nguồn để tính impact mỗi tháng của người dùng mục tiêu.

CP2: đã bắt đầu tìm bằng chứng và có tài liệu, trích dẫn. CP3: đã bổ sung phần trích dẫn; chưa tự đánh dấu đủ toàn bộ ngưỡng bằng chứng. Nếu tiếp tục đường đào data, cần chọn mẫu, định nghĩa nhãn và phép đếm trước khi thu mẫu tiếp theo, rồi ghi x/N, tỷ lệ và ví dụ kiểm lại được theo guide 1.2.
