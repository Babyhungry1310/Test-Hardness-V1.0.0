# CHAT UX VÀ STORAGE

Chi tiết của `harness/HARNESS.md` mục 3.6. Hai nơi có hai người đọc khác nhau nên có hai bộ quy tắc khác nhau.

| | Chat | Storage |
|---|---|---|
| Là gì | Mọi thứ tác tử viết cho OWNER trong phiên: câu trả lời, giải thích, phần tóm tắt và khối chuẩn ở cuối phiên | Mọi file trong repo: bản ghi, sổ, bằng chứng, tài liệu khung, sản phẩm; mô tả PR |
| Ai đọc | OWNER, thường trên khung chat hẹp | Script, model ở phiên sau, người đọc repo |
| Ưu tiên | Đọc nhanh, biết việc cần chốt, tới được bằng chứng | Đúng schema, tra được bằng con trỏ, nguyên vẹn theo thời gian |

## 1. Chat: dọc trước (vertical-first)

<!-- ANCHOR: CHAT_RULES -->
1. Trao đổi, hỏi đáp và giải thích dùng danh sách dọc và cặp `khóa: giá trị`, mỗi ý một dòng.
2. Tránh bảng Markdown nhiều cột trong chat. So sánh nhiều phương án thì viết mỗi phương án một cụm dọc, các cụm dùng cùng bộ khóa theo cùng thứ tự.
3. Code, lệnh, đường dẫn, log đặt trong khối code và để khung chat tự xuống dòng mềm (soft wrap). Không tự chèn ký tự xuống dòng, dấu `\`, dấu `…` hay khoảng trắng vào giữa một lệnh, một đường dẫn, một mã, một URL hoặc một dòng log.
4. Nội dung quá dài để dán nguyên: lưu thành file bằng chứng rồi đưa con trỏ hoặc đường dẫn; nếu trích thì trích nguyên dòng và nói rõ là trích.
5. Không lặp lại nội dung đã có trong bản ghi; trỏ tới bản ghi.
6. Không xã giao, không lời dẫn, không tự đánh giá.
<!-- END: CHAT_RULES -->

Quy tắc 1–2 chỉ áp cho chat. Chúng **không** áp cho schema, mẫu, bản ghi, sổ, tài liệu khung và mọi file lưu trữ hiện hành; bảng trong các file đó giữ nguyên.

## 2. Chat: thông điệp cuối phiên

<!-- ANCHOR: FINAL_MESSAGE -->
Thông điệp cuối gồm, theo đúng thứ tự:

1. Phần `SUMMARY` — tùy chọn với WORKER và REVIEWER; bắt buộc với LEAD khi phiên có sửa file.
2. Không, một hoặc nhiều khối `QUESTION` (tối đa 5) — chỉ khi có việc cần OWNER chốt.
3. Đúng một khối chuẩn kết thúc: `CONFIRM`, `RESULT`, `MERGE` hoặc `REVIEW`.

```text
SUMMARY
did: <1–3 dòng, mỗi dòng một việc đã làm>
changed: <số file> · <con trỏ hoặc đường dẫn tới danh sách: mô tả PR>
decide: <số việc cần chốt, khớp số khối QUESTION>
limits: <điều chưa làm được hoặc chưa kiểm được; none nếu không có>
evidence: <con trỏ hoặc đường dẫn; none nếu không có>
```

- `SUMMARY` tối đa 12 dòng. Danh sách file đầy đủ nằm ở mô tả PR, không chép vào chat.
- Không có lời dẫn trước `SUMMARY` và không có gì sau khối kết thúc.
- Phiên `ASK` trả lời theo mục 1 và không cần khối kết thúc.
<!-- END: FINAL_MESSAGE -->

## 3. Storage

<!-- ANCHOR: STORAGE_RULES -->
1. Mỗi loại dữ liệu dùng định dạng và schema của chính nó: bản ghi là YAML đầu file theo `harness/schemas/`; sổ có dòng trạng thái theo `STATUS_GRAMMAR.md`; log theo `LOG_GRAMMAR.md`; dữ liệu dạng bảng dùng bảng.
2. Không đưa vào file lưu trữ: lời chào, lời dẫn, tóm tắt kiểu chat, biểu tượng trang trí, định dạng chỉ để dễ nhìn trong chat. Quy tắc không ghi chú (`harness/HARNESS.md` mục 8.4) giữ nguyên.
3. Quy tắc của chat không phải lý do để viết lại một file đã có. Bản ghi, neo, tên file, mã và bằng chứng cũ giữ nguyên từng byte, trừ khi một task hoặc một `DEC` yêu cầu sửa đúng file đó.
4. Neo đã dùng không đổi tên, không xóa. Thêm quy tắc mới thì thêm neo mới.
5. Mô tả PR là storage: chứa tóm tắt nghiệm thu, danh sách file 🔒 và ✍, kết quả kiểm; không chứa log thô.
<!-- END: STORAGE_RULES -->

## 4. Ranh giới

| Tình huống | Áp bộ quy tắc nào |
|---|---|
| Trả lời OWNER trong phiên | Chat |
| Khối chuẩn ở cuối phiên | Chat; khóa và thứ tự theo `harness/templates/BLOCKS.md` |
| Mô tả PR, tiêu đề commit | Storage |
| Bản ghi, sổ, `STATE.md`, digest, file cổng | Storage |
| Nội dung một file được dán vào chat để OWNER xem | Dán nguyên trong khối code; không dàn lại thành dạng dọc |
