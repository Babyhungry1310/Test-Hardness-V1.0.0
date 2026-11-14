---
schema: 1
id: REQ-0006
date: 2026-11-14
title: "Đổi quy định tài khoản GitHub cho dự án"
proposed_by: OWNER
cycle: NONE
affects: [DEC-0015, DEC-0016, RSK-0004, TK-0008, "harness/HARNESS.md", "harness/MAIN_PROTECTION.md", "harness/tools/PREFLIGHT.md", "01_plan/SPEC_ORCA_PROMPT.md"]
keywords: [github, shared-account, owner, merge, permissions]
---
## Status (newest first)
- 2026-11-14 | RESOLVED_BY DEC-0019
- 2026-11-14 | PENDING
<!-- ANCHOR: CONTEXT -->
## Context
OWNER chọn một tài khoản GitHub chung, cho phép tác tử đẩy nhánh làm việc và tạo PR; OWNER giữ quyền quyết định và thực hiện merge.
<!-- END: CONTEXT -->
<!-- ANCHOR: IMPACT -->
## Impact
Điều chỉnh luật, pre-flight, hand-off, task kiểm toán và plan; giữ cấm đẩy trực tiếp vào `main`, merge, auto-merge và đẩy thẻ đối với tác tử.
<!-- END: IMPACT -->
