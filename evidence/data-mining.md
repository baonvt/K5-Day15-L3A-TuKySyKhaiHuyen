# Đào data — cách đếm và kết quả

**Kết quả CP3 ngày 27/11/2026: 6/8 bài (75%) nêu khó khăn khi dùng review để chọn mua.** Mục 1–5 ghi lại giai đoạn tìm tài liệu trước CP3. Mục 6–7 là cách chọn mẫu và kết quả đếm bài của người mua.

## 1. Cách thu thập nguồn công khai

Ngày thực hiện: 27/11/2026, giờ Việt Nam. Nhóm yêu cầu nguồn chuẩn và ít nhất 5 trích dẫn nguyên văn; tại thời điểm tìm tài liệu, nhóm chưa chọn ngách hoặc đặt ngưỡng kiểm chứng pain. Nhóm chọn ngách sản phẩm công nghệ sau bước này.

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

## 3. Phép đếm x/N ở thời điểm CP2

**Tại CP2, nhóm chưa thực hiện phép đếm.** Chưa có tập review được chọn theo một quy tắc cố định, nhãn từng dòng hoặc mẫu số N để báo cáo tỷ lệ pain. Các tỷ lệ trong tài liệu là kết quả của tác giả nguồn, không phải số nhóm tự đếm.

Vì chưa có phép đếm này, chưa có script đếm raw review để chạy lại. Không dựng một phép đếm tài liệu rồi coi đó là tỷ lệ người dùng gặp pain.

## 4. Năm trích dẫn có nguồn

Xem [S01](public-sources.md#s01), [S02](public-sources.md#s02), [S03](public-sources.md#s03), [S04](public-sources.md#s04), [S05](public-sources.md#s05). Chưa coi là năm review sản phẩm đã xác thực hay lời của năm người được phỏng vấn.

## 5. Giới hạn và tiến độ CP2/CP3

Nguồn công khai hỗ trợ bối cảnh vấn đề và cung cấp số liệu nghiên cứu bên ngoài. Chưa đo thời gian đọc/tổng hợp review, quy mô pain tại Việt Nam, nguyên nhân đổi trả, hoặc hiệu quả giải pháp. Chưa có nguồn để tính impact mỗi tháng của người dùng mục tiêu.

Ở CP2, nhóm đã có tài liệu và trích dẫn. Đến CP3, nhóm dùng quy tắc chọn bài và gắn nhãn ở mục 6 để lập bảng tám bài ở mục 7. Người đọc có thể đếm lại từng dòng và mở nguồn gốc.

## 6. Cách chọn mẫu CP3, ghi trước khi tìm và đếm

Tìm các bài thảo luận công khai về chọn mua laptop hoặc tai nghe và đọc review, ưu tiên bài tiếng Việt. Nếu thiếu bài đọc được, mở rộng sang bài tiếng Anh và ghi rõ ngôn ngữ. Đọc theo thứ tự kết quả tìm kiếm, lấy tối đa 10 bài đủ điều kiện. Mỗi đường dẫn chỉ lấy bài mở đầu một lần. Giữ cả bài có và không có khó khăn.

- Đưa vào mẫu khi người viết kể việc chính họ đang cân nhắc mua hoặc đã mua đồ công nghệ, có nhắc đến việc đọc hoặc xem đánh giá trước khi chọn. Loại bài quảng cáo, bài tư vấn chung, bình luận trả lời và trang chỉ hiện đoạn trích tìm kiếm.
- Ghi **Có** nếu người viết nói rõ review trái chiều, khó tin, thiếu thông tin cần thiết hoặc khiến họ khó quyết định. Chỉ nói đã xem review, hoặc phân vân vì giá hay cấu hình thì ghi **Không**. Nếu lý do chưa rõ, giữ bài và ghi **Không**.
- N là số bài đủ điều kiện, x là số bài ghi Có. Tỷ lệ là 100 × x/N. Lưu đường dẫn, ngày xem và trích đoạn ngắn, bỏ tên người viết. Kết quả chỉ mô tả mẫu bài tìm được.

## 7. Bài đã đọc và kết quả đếm

Ngày xem của cả 8 bài là **27/11/2026**. Từ khóa tiếng Việt gồm `laptop "xem review" mua phân vân` và `"xem nhiều review" laptop "mua"` trên VOZ, Tinh tế. Phần tiếng Anh dùng các cụm như `buying headphones "reviews" conflicting confused` trên Reddit. Mỗi dòng dưới đây trích từ bài mở đầu, giữ cách viết của tác giả và lược tên tài khoản.

| Mã | Nguồn | Trích nguyên văn | Có gặp khó khăn khi dùng review? | Căn cứ |
|---|---|---|---|---|
| D01 | [VOZ · Chọn laptop gaming](https://voz.vn/t/phan-van-chon-laptop-gaming-co-35tr.309464/) | “em xem review nhưng không tin tưởng lắm” | Có | Đang chọn giữa Helios và Legion, người mua hỏi người đã dùng vì còn nghi ngờ đánh giá về độ chắc của máy. |
| D02 | [VOZ · Độ bền laptop](https://voz.vn/t/nho-anh-em-tu-van-mua-laptop-choi-game-phan-khuc-gia-re.932958/) | “Xem review trên mạng ko thấy nói nhiều về cái này” | Có | Đang so bốn máy. Chi tiết còn thiếu là độ bền của bản lề, chốt và ốc vít. |
| D03 | [Tinh tế · Mua IdeaPad](https://tinhte.vn/thread/review-laptop-lenovo-ideapad-5-pro-amd-5800h-sau-6-thang-su-dung.3502940/) | “Mình xem review khá nhiều cuối cùng chọn con lenovo ideapad pro5 ryzen 5600H” | Không | Đã chọn được máy sau khi xem. Người mua đổi sang bản 5800H vì bản đó về hàng trước. |
| D04 | [Tinh tế · Chọn MacBook Air](https://tinhte.vn/thread/da-e-chao-may-anh-chi-a-em-khong-ranh-ve-cong-nghe-em-xin-may-anh-chi-giup-voi-a.3375795/) | “nên em mới định lấy air 2020 i7” | Không | Sau khi đọc về lỗi phần mềm trên M1, người mua nghiêng về bản i7. Bài hỏi máy nào hợp công việc, chưa nói các review thiếu tin cậy hay mâu thuẫn. |
| D05 | [Reddit · Tìm tai nghe để nâng cấp](https://www.reddit.com/r/headphones/comments/17gamfe/how_do_you_get_info_from_this_sub_cause_im/) | “You can’t name a single headphone that has consistent reviews here.” | Có | Sau hai tuần xem video và đọc ý kiến, người mua vẫn gặp các nhận xét trái ngược về cùng tai nghe. |
| D06 | [Reddit · Chọn tai nghe trong mức 400 USD](https://www.reddit.com/r/HeadphoneAdvice/comments/1dnxq4m/tried_a_great_pair_and_now_i_cant_go_back_but/) | “Who do I believe?” | Có | Người mua lo ngay cả người đánh giá có vẻ cùng gu nghe cũng chưa chắc giúp họ chọn đúng. |
| D07 | [Reddit · Chọn tai nghe kín khi không thể nghe thử](https://www.reddit.com/r/headphones/comments/1k9f52d/would_you_ever_buy_a_headphone_without_being_able/) | “how much should I trust the reviewers' impressions?” | Có | Người mua đã xem nhiều review về ZMF nhưng chưa biết nên tin nhận xét đến đâu khi không thể thử trực tiếp. |
| D08 | [Reddit · So sánh tai nghe mở](https://hu.reddit.com/r/HeadphoneAdvice/comments/1uygpoa/open_back_headphones_for_under_1600_overwhelmed/) | “treble & soundstage reviews conflicting.” | Có | Khi cân nhắc Focal Clear MG, người mua gặp ý kiến trái chiều về dải cao và không gian âm thanh. |

Đếm cột kết quả được **6 Có, 2 Không**, tức **6/8 = 75%**. Riêng 4 bài tiếng Việt có **2/4** bài nêu khó khăn. Mẫu thiên về người đang hỏi mua và một số từ khóa chủ động tìm ý kiến trái chiều. Bốn bài tiếng Anh đều nói về tai nghe, còn bốn bài tiếng Việt đều nói về laptop, nên chưa thể tách ảnh hưởng của loại sản phẩm và ngôn ngữ.
