---
schema: 1
id: DEC-0006
date: 2026-11-12
title: "Khắc phục thu thập test và kiểm định lại CYC-01"
proposed_by: LEAD
decided_by: LEAD
cycle: CYC-01
origin: "RVW-CYC-01"
supersedes: ""
cancels: []
waives: []
affects: [TK-0001, TK-0002, TK-0003]
keywords: [pytest, test-collection, review]
---
## Status (newest first)
- 2026-11-12 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
OWNER đã merge PR #9 và #10. Main ff861809755ae3a3cd1c0dd0b62b4760f4db645c có các run DONE nhưng pytest toàn repo lỗi trùng tên module test.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- Thêm tests/__init__.py rỗng để tách namespace và giữ toàn bộ test.
- Giới hạn phạm vi thu thập pytest, không chọn vì làm giảm số test được chạy.
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
Lập TK-0003 sửa tích hợp của TK-0002 bằng một file package rỗng. Bản thử ngoài repo đạt 20 test, không thay đổi test hiện có.
OWNER cho phép REVIEWER khác gemini-3.8-flash-k và gpt-6.1-sol. Vòng 2 dùng claude-sonnet-4-6 vì các tuyến Gemini text/code độc lập không hoạt động và tuyến image trả ảnh.
Đây là ngoại lệ model cho vòng 2 theo chỉ định mới của OWNER; không đổi phân công WORKER của DEC-0003 và DEC-0005.
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
OWNER merge task trước khi WORKER chạy TK-0003. Sau khi run sửa được merge, kiểm định vòng 3 trên main mới nhất.
Không miễn trừ tiêu chí pytest trên main; không tạo cổng CYC-01_PASS hoặc digest khi REVIEWER còn FAIL.
<!-- END: CONSEQUENCES -->
