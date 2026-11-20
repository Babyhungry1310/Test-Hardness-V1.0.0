---
schema: 1
id: DEC-0030
date: 2026-11-20
title: "Cập nhật test lõi scan trước khi TK-0014 giải mã base64"
proposed_by: LEAD
decided_by: OWNER
cycle: CYC-06
origin: TK-0014
supersedes: ""
cancels: []
waives: []
affects: [TK-0014, "tools/tests/test_scan_core.py"]
keywords: [scan, base64, limits, test_scan_core]
---
## Status (newest first)
- 2026-11-20 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
TK-0013 đã trên main. `tools/tests/test_scan_core.py` còn hai assertion đúng với lõi chưa giải mã: (1) chuỗi base64 dài của câu ghi đè phải ALLOW; (2) file đúng 5 MB toàn chữ `a` phải ALLOW. TK-0014 phải giải mã base64 liên tục từ 24 ký tự và áp hạn tổng byte sau giải mã. Hai assertion đó xung đột với ca 8 và ca 10. Task TK-0014 cấm sửa `test_scan_core.py`. OWNER đã OK tách DEC.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- Nới write_scope TK-0014 giữa run để sửa test lõi: bác bỏ.
- Giữ nguyên test lõi và bắt TK-0014 đạt verify: bác bỏ vì không thể.
- DEC + PR cập nhật test lõi trên main trước, rồi TK-0014 tiếp: OWNER chọn.
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
- Cập nhật `tools/tests/test_scan_core.py` trên main trước khi TK-0014 mở PR đạt.
- Đổi fixture file đúng 5 MB sạch sang nội dung có ký tự ngoài alphabet base64, để ca kích thước không bị biến thành `limit_exceeded` sau khi có giải mã.
- Thay `test_base64_not_decoded` bằng kiểm tra chuỗi base64 ngắn hơn 24 ký tự không bị giải mã. Ca giải mã đủ dài thuộc `tools/tests/test_scan_limits.py` của TK-0014.
- Không đổi giao diện `tools/scan.py` trong PR DEC này. Không thay SPEC_SCAN.
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
- Sau khi OWNER merge PR DEC này và `verify_default` vẫn 23 passed, LEAD gửi tiếp TK-0014 trên cùng dispatch hoặc run mới theo sổ.
- TK-0014 vẫn không được sửa `test_scan_core.py` ngoài phạm vi đã cập nhật ở đây; vẫn phải giữ các ca lõi còn lại đạt.
- TK-0022 không phụ thuộc DEC này và có thể merge riêng.
<!-- END: CONSEQUENCES -->
