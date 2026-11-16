---
schema: 1
id: DEC-0026
date: 2026-11-16
title: "Sửa preflight Windows bằng task mới, Grok thực hiện và Gemini kiểm delta"
proposed_by: LEAD
decided_by: OWNER
cycle: CYC-03
origin: REQ-0009
supersedes: ""
cancels: []
waives: []
affects: [TK-0030, TK-0007, TK-0018, "04_control/MODEL_MATRIX.md", "tools/preflight_main.py", "tools/tests/test_preflight_main.py"]
keywords: [windows, encoding, preflight, grok, gemini, regression]
---
## Status (newest first)
- 2026-11-16 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
REQ-0009. OWNER yêu cầu sửa lỗi mã hóa Windows, giao Grok, LEAD chỉ điều phối, Gemini kiểm định. LEAD tái hiện lỗi trên main mới nhất 8dcf58b, không cần PR31: cp1252 làm test nhận mã 1 thay vì 2; chỉ khi bật UTF-8 mới đạt 54/54. Bằng chứng tại 03_output/CYC-03/checks/TK-0030_main_reproduction.md.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- Yêu cầu người dùng bật UTF-8: không đáp ứng yêu cầu OWNER.
- Sửa đầu ra của CLI trong task mới, giữ nghĩa 0/1/2 và thêm kiểm hồi quy: chọn theo yêu cầu OWNER.
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
Tạo TK-0030 fixes TK-0007, R1 tối đa 3 loop; không mở lại run cũ. Grok qua xai/grok-4.7 thực hiện, actual cần xác minh từ metadata phiên. Gemini qua ag/gemini-3.8-flash kiểm độc lập delta TK-0030 trên SHA cố định; actual phải khác mọi WORKER đã sửa delta này. Đây là kiểm task, không phải RVW toàn CYC-03 hoặc tái nghiệm thu code TK-0007 vốn do Gemini làm.

Chỉ sửa sau khi OWNER merge PR giao việc theo luật 25 LEAD. Được kiểm readiness chỉ đọc trước đó, không verify hay viết sản phẩm. Yêu cầu hiện tại của OWNER cho phép thực hiện sau cổng này, không cần GO lặp. Lượt merge là chữ ký; quyết định chưa merge không thay luật đang có.
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
- Chưa mở B2 trong lúc sửa lỗi đã biết; TK-0018 chờ bản sửa được merge và main đạt. Không sửa PLAN hoặc batch khác trong PR này; PR31/TK-0029 vẫn độc lập.
- Test phải chạy với môi trường mặc định Windows và mã hóa hẹp có kiểm soát, không nới assertion, không đổi thiết lập toàn cục. Đầu ra Unicode và JSON giữ nội dung; baseline 23 test phải đạt.
- Ngân sách mới chỉ thuộc TK-0030; không sửa bằng chứng TK-0007 hay TK-0008. LEAD không viết code sửa. Gemini không tự sửa code trong bước review.
- Không merge, đẩy main, bật auto-merge, đụng thẻ, hoặc sửa .claude/settings.local.json. PR sản phẩm chỉ trình OWNER sau LEAD rà và Gemini kết luận.
<!-- END: CONSEQUENCES -->
