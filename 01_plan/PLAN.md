---
schema: 1
id: PLAN
date: 2026-11-12
based_on: [DEC-0002, DEC-0006, DEC-0007, DEC-0010, DEC-0013, DEC-0015, DEC-0016, DEC-0017]
---
## Status (newest first)
- 2026-11-14 | ACTIVE | version: 4
- 2026-11-13 | ACTIVE | version: 3
- 2026-11-12 | ACTIVE | version: 2
- 2026-11-12 | ACTIVE | version: 1
<!-- ANCHOR: CYC_01 -->
## CYC-01
- TK-0001 | Tìm id câu hỏi bị trùng | depends: none | assignee: W1
- TK-0002 | Tạo data/bank.json 5 câu và hàm đọc ngân hàng câu hỏi | depends: none | assignee: W2
- TK-0004 | Giới hạn pytest về tests/ để lệnh kiểm toàn repo chạy được | depends: TK-0001, TK-0002 | assignee: W1
<!-- END: CYC_01 -->
<!-- ANCHOR: CYC_02 -->
## CYC-02
- TK-0003 | Xuất handout Markdown từ ngân hàng câu hỏi | depends: TK-0001, TK-0002 | assignee: W1
- TK-0005 | Handout kết thúc bằng đúng một LF và ghi file với newline LF | depends: TK-0003 | assignee: W1
<!-- END: CYC_02 -->
<!-- ANCHOR: CYC_03 -->
## CYC-03
- TK-0006 | Hook pre-commit và pre-push chặn commit trên main, đẩy vào main và thẻ | depends: none | assignee: W1
- TK-0007 | Kiểm pre-flight cho main theo vai và thời điểm | depends: none | assignee: W2
- TK-0008 | Kiểm chỉ đọc lớp bảo vệ main và thẻ phía GitHub | depends: none | assignee: W3
- TK-0018 | Ca biên và ca lách cho hook và pre-flight | depends: TK-0006, TK-0007 | assignee: W3
<!-- END: CYC_03 -->
<!-- ANCHOR: CYC_03_BATCHES -->
## CYC-03 batches
- B1 | tasks: TK-0006, TK-0007, TK-0008 | after: none
- B2 | tasks: TK-0018 | after: B1
<!-- END: CYC_03_BATCHES -->
<!-- ANCHOR: CYC_04 -->
## CYC-04
- TK-0009 | Kiểm schema và ràng buộc chéo của catalog và ma trận model | depends: none | assignee: W1
- TK-0010 | Chọn model theo vai, fallback và tính độc lập của REVIEWER | depends: TK-0009 | assignee: W1
- TK-0019 | Đối chiếu model yêu cầu và thực tế trên bản ghi | depends: TK-0009 | assignee: W3
<!-- END: CYC_04 -->
<!-- ANCHOR: CYC_04_BATCHES -->
## CYC-04 batches
- B1 | tasks: TK-0009 | after: none
- B2 | tasks: TK-0010, TK-0019 | after: B1
<!-- END: CYC_04_BATCHES -->
<!-- ANCHOR: CYC_05 -->
## CYC-05
- TK-0011 | Phân loại tên nhánh theo quy ước Git | depends: none | assignee: W1
- TK-0012 | Kiểm thông điệp cuối phiên theo CHAT_UX | depends: none | assignee: W2
- TK-0020 | Storage bất biến của CYC-01, CYC-02 và trace còn mở | depends: none | assignee: W3
- TK-0021 | clean ở chế độ liệt kê | depends: none | assignee: W2
<!-- END: CYC_05 -->
<!-- ANCHOR: CYC_05_BATCHES -->
## CYC-05 batches
- B1 | tasks: TK-0011, TK-0012, TK-0020, TK-0021 | after: none
<!-- END: CYC_05_BATCHES -->
<!-- ANCHOR: CYC_06 -->
## CYC-06
- TK-0013 | Lõi scan: dấu hiệu, bốn mức, ký tự ẩn, đồng hình, HTML | depends: none | assignee: W1
- TK-0014 | Scan: base64 lồng nhau và giới hạn xử lý | depends: TK-0013 | assignee: W1
- TK-0022 | Cách ly có đối chiếu băm và thẻ EXTERNAL_DATA | depends: TK-0013 | assignee: W2
- TK-0023 | Bộ test phản biện và dữ liệu lớn cho scan | depends: TK-0014, TK-0022 | assignee: W3
<!-- END: CYC_06 -->
<!-- ANCHOR: CYC_06_BATCHES -->
## CYC-06 batches
- B1 | tasks: TK-0013 | after: none
- B2 | tasks: TK-0014, TK-0022 | after: B1
- B3 | tasks: TK-0023 | after: B2
<!-- END: CYC_06_BATCHES -->
<!-- ANCHOR: CYC_07 -->
## CYC-07
- TK-0015 | Kiểm chia batch zero-overlap write_scope | depends: TK-0009 | assignee: W1
- TK-0016 | Chứng minh mẫu pytest.ini chỉ thu thập tests/ | depends: none | assignee: W2
- TK-0024 | Kiểm tương thích cấu hình pytest hiện có, không ghi đè | depends: none | assignee: W3
- TK-0025 | Kiểm thử worktree và nền tích hợp tạm | depends: none | assignee: W2
- TK-0026 | Tài liệu sử dụng tools/README.md | depends: TK-0006, TK-0007, TK-0008, TK-0009, TK-0010, TK-0011, TK-0012, TK-0013, TK-0014, TK-0015, TK-0016, TK-0018, TK-0019, TK-0020, TK-0021, TK-0022, TK-0023, TK-0024, TK-0025 | assignee: W2
- TK-0017 | Hồi quy toàn bộ trên Windows | depends: TK-0006, TK-0007, TK-0008, TK-0009, TK-0010, TK-0011, TK-0012, TK-0013, TK-0014, TK-0015, TK-0016, TK-0018, TK-0019, TK-0020, TK-0021, TK-0022, TK-0023, TK-0024, TK-0025, TK-0026 | assignee: W3
<!-- END: CYC_07 -->
<!-- ANCHOR: CYC_07_BATCHES -->
## CYC-07 batches
- B1 | tasks: TK-0015, TK-0016, TK-0024, TK-0025 | after: none
- B2 | tasks: TK-0026 | after: B1
- B3 | tasks: TK-0017 | after: B2
<!-- END: CYC_07_BATCHES -->
<!-- ANCHOR: RISKS -->
## Risks
- RSK-0001
- RSK-0004
- RSK-0005
<!-- END: RISKS -->
