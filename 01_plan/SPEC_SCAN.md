# SPEC_SCAN — BỘ KIỂM THỬ CỦA `scan`

Nguồn: `harness/tools/README.md#SCAN_SPEC`, `harness/tools/README.md#SCAN_SIGNALS`, DEC-0016. Quy ước chung: `01_plan/SPEC_TOOLS.md#CONVENTIONS`.

<!-- ANCHOR: INTERFACE -->
## 1. Giao diện
- `python tools/scan.py <file> [--rules tools/scan_rules.json] [--json]`. Mã thoát: `0` cho `ALLOW`, `WARN`; `1` cho `QUARANTINE`, `BLOCK`; `2` lỗi.
- Đầu ra: `level`, `ruleset`, `sha256`, `reasons` (mỗi lý do: `rule`, `group`, `position`, `layer`), `decoded_skipped`. Không có đoạn trích nội dung.
- `tools/scan_rules.json`: phiên bản bộ luật, mẫu dấu hiệu kèm mức, năm giới hạn của `SCAN_SPEC`. Không có khóa ghi chú.
- `tools/scan_wrap.py`: bọc một đoạn vào thẻ `EXTERNAL_DATA` với `source`, `sha256`, `scan`, `ruleset` và số lần chuỗi đóng thẻ xuất hiện trong nội dung.
- `tools/scan_quarantine.py`: nhận file gốc, file JSON kết quả của `scan` và thư mục cách ly; chuyển nguyên file khi mức là `QUARANTINE`, so SHA-256 trước và sau.
<!-- END: INTERFACE -->

<!-- ANCHOR: FIXTURES -->
## 2. Dữ liệu thử
- Mọi dữ liệu thử dựng lúc chạy test trong `tmp_path`. Câu ví dụ lấy từ bảng `SCAN_SIGNALS` đã có trong repo.
- Chuỗi có dạng token, khối khóa PEM, file lớn hơn 5 MB được ghép lúc chạy từ các mảnh, để lệnh quét bí mật ở `harness/tools/PREFLIGHT.md` dòng 7 không trúng file nào trong repo.
- Không dùng dữ liệu ngoài, không tải gì từ mạng.
<!-- END: FIXTURES -->

<!-- ANCHOR: CASES -->
## 3. Ca kiểm bắt buộc
| # | Nhóm | Đầu vào | Kết quả phải có | Task |
|:---:|---|---|---|---|
| 1 | Sạch | Văn bản Việt có dấu, văn bản Anh, file rỗng | `ALLOW`, `reasons` rỗng | TK-0013 |
| 2 | Độc | Từng "ví dụ độc" của năm nhóm `SCAN_SIGNALS` | `QUARANTINE` hoặc `BLOCK` đúng bảng mức | TK-0013 |
| 3 | False positive | Từng "ví dụ lành" của năm nhóm; câu mô tả lệnh Git; địa chỉ `user@example.com`; mã nguồn có từ `system`, `ignore` | `ALLOW` hoặc `WARN`; không `QUARANTINE`, không `BLOCK` | TK-0013 |
| 4 | Zero-width | Câu ghi đè bị chẻ bằng U+200B, U+200C, U+200D, U+2060, U+FEFF giữa file; ký tự đổi hướng U+202E | Lý do ký tự ẩn và lý do ghi đè sau khi bỏ ký tự trên bản sao; `QUARANTINE` hoặc `BLOCK` | TK-0013 |
| 5 | Zero-width lành | U+FEFF ở đầu file; U+200D trong chuỗi emoji ghép | Không vì thế mà `QUARANTINE` | TK-0013 |
| 6 | Đồng hình | Từ trộn Latin với Cyrillic hoặc Hy Lạp trong câu ghi đè và trong tên miền | Lý do đồng hình; quét lại sau chuẩn hóa | TK-0013 |
| 7 | HTML | Câu lệnh trong `<!-- -->`; phần tử có thuộc tính ẩn; chú thích HTML vô hại | Hai ca đầu tính là che giấu; ca cuối không là dấu hiệu độc | TK-0013 |
| 8 | Base64 một lớp | Chuỗi giải ra câu ghi đè; chuỗi giải ra byte không phải văn bản; chuỗi ngắn hơn 24 ký tự | Ca một `QUARANTINE` hoặc `BLOCK` với `layer` 1; ca hai bỏ qua và đếm; ca ba không giải mã | TK-0014 |
| 9 | Base64 lồng | Câu ghi đè bọc 2 lớp, 3 lớp, 4 lớp | 2 và 3 lớp: phát hiện đúng `layer`; 4 lớp: `QUARANTINE`, lý do `depth_exceeded` | TK-0014 |
| 10 | Quá lớn | File 5 MB + 1 byte; file đúng 5 MB sạch | Ca một `QUARANTINE`, lý do `too_large`, không quét một phần; ca hai được quét hết | TK-0014 |
| 11 | Giới hạn xử lý | 201 chuỗi base64; tổng byte sau giải mã vượt 1 MB | `QUARANTINE`, lý do `limit_exceeded` | TK-0014 |
| 12 | Không trích được văn bản | Byte nhị phân ngẫu nhiên có hạt giống cố định | `QUARANTINE` | TK-0014 |
| 13 | Xác định | Cùng đầu vào chạy hai lần; đổi phiên bản bộ luật | Hai đầu ra giống nhau từng byte; `ruleset` đổi theo | TK-0013, TK-0014 |
| 14 | Giữ bản gốc | So SHA-256 file đầu vào trước và sau mọi ca; cách ly | Không đổi; lệch băm khi cách ly thì mã thoát `2` | TK-0013, TK-0014, TK-0022 |
| 15 | Thẻ bọc | Nội dung chứa chuỗi đóng thẻ `EXTERNAL_DATA` | Thuộc tính ghi đúng số lần gặp; nội dung không bị sửa | TK-0022 |
| 16 | Thời gian | File 5 MB sạch; file 5 MB toàn chuỗi dạng base64 | Kết thúc; thời gian đo được ghi vào bằng chứng, không đặt ngưỡng cứng trong test | TK-0023 |
| 17 | Phản biện | False positive mở rộng; biến thể che giấu; các cách lách đã biết; dữ liệu lớn dị dạng | Ca phải bắt được thì bắt; ca lành không bị báo nhầm; ca lách được ghi là giới hạn đã biết | TK-0023 |
<!-- END: CASES -->

<!-- ANCHOR: CLAIMS -->
## 4. Điều được và không được kết luận
- Được: `scan` cho đúng mức trên các ca ở mục 3, với phiên bản bộ luật đã ghi.
- Không được: `scan` chặn được mọi prompt injection; `ALLOW` nghĩa là an toàn. Các cách lách ở `harness/tools/README.md` mục 2.10.3 nằm ngoài bộ test này.
- Vượt giới hạn không bao giờ dẫn tới `ALLOW`.
<!-- END: CLAIMS -->
