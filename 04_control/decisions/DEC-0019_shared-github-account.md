---
schema: 1
id: DEC-0019
date: 2026-11-14
title: "OWNER và tác tử dùng chung tài khoản GitHub"
proposed_by: LEAD
decided_by: OWNER
cycle: NONE
origin: "REQ-0006"
supersedes: ""
cancels: []
waives: []
affects: [DEC-0015, DEC-0016, RSK-0004, TK-0008, "harness/HARNESS.md", "harness/MAIN_PROTECTION.md", "harness/tools/PREFLIGHT.md", "01_plan/SPEC_ORCA_PROMPT.md"]
keywords: [github, shared-account, owner, merge, permissions]
---
## Status (newest first)
- 2026-11-14 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
OWNER quyết định dùng một tài khoản GitHub cho OWNER và tác tử. Luật cũ yêu cầu tài khoản riêng và chặn phiên dùng tài khoản OWNER.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- Tài khoản riêng cho tác tử; tài khoản GitHub chung cho OWNER và tác tử. OWNER chọn tài khoản chung.
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
Tác tử được dùng tài khoản OWNER để đẩy nhánh làm việc và tạo PR. Chỉ OWNER quyết định và thực hiện merge; tác tử không commit trên `main`, đẩy trực tiếp vào `main`, merge hay bật auto-merge. Lệnh cấm thẻ theo DEC-0011 vẫn áp dụng.
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
- Phần yêu cầu tài khoản riêng trong DEC-0015 và DEC-0016 được thay bằng quyết định này; các phần khác giữ nguyên, lịch sử không sửa.
- RSK-0004 giữ OPEN: GitHub không phân biệt thao tác của OWNER và tác tử dùng chung tài khoản; luật theo danh tính không ngăn được tác tử sử dụng quyền của tài khoản đó.
- Pre-flight, tài liệu bảo vệ, hand-off và TK-0008 phải phản ánh tài khoản chung; thay đổi plan được OWNER merge mới có hiệu lực.
<!-- END: CONSEQUENCES -->
