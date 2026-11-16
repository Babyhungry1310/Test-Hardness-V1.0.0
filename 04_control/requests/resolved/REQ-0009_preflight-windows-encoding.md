---
schema: 1
id: REQ-0009
date: 2026-11-16
title: "Sửa lỗi mã hóa Windows làm preflight trả sai mã thoát"
proposed_by: OWNER
cycle: CYC-03
affects: [TK-0007, TK-0030, "tools/preflight_main.py", "tools/tests/test_preflight_main.py"]
keywords: [windows, encoding, preflight, regression]
---
## Status (newest first)
- 2026-11-16 | RESOLVED_BY DEC-0026
- 2026-11-16 | PENDING
<!-- ANCHOR: CONTEXT -->
## Context
OWNER báo test_cli_usage_and_errors lỗi UnicodeEncodeError trên nền tích hợp PR31 với main 8dcf58b; bật PYTHONUTF8=1 và PYTHONIOENCODING=utf-8 thì 54/54 test tools đạt. Yêu cầu xác minh main mới nhất, giao Grok sửa, Gemini kiểm định, giữ hành vi/mã thoát và trình PR.
<!-- END: CONTEXT -->
<!-- ANCHOR: IMPACT -->
## Impact
LEAD tái hiện trên main sạch 8dcf58b1e680cfade770acd7678165714f7b3d09, Python 3.14.5 Windows, stdout cp1252. Task mới TK-0030 fixes TK-0007; kết quả trong 03_output/CYC-03/checks/TK-0030_main_reproduction.md. Không sửa run đã merge; không lấy việc bật UTF-8 của người dùng làm cách khắc phục.
<!-- END: IMPACT -->
