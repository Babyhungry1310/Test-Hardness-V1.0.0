---
schema: 1
id: DEC-0004
date: 2026-11-06
title: "So sánh id câu hỏi không phân biệt hoa thường"
proposed_by: LEAD
decided_by: OWNER
cycle: CYC-01
origin: "TK-0001.L03"
supersedes: ""
cancels: []
waives: []
affects: [TK-0001]
keywords: [quiz-bank, duplicate-id]
---
## Status (newest first)
- 2026-11-06 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
TK-0001 R1 đóng loop sau L01–L03 FAIL: task không nói id có phân biệt hoa thường, nên Q-001 và q-001 không bị coi là trùng.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- Phân biệt hoa thường; sửa done_when còn 1 id trùng
- Không phân biệt hoa thường
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
Không phân biệt hoa thường, vì giáo viên gõ tay id và handout in id dạng chữ hoa.
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
Thêm ràng buộc vào TK-0001 và mở lại task bằng run R2.
<!-- END: CONSEQUENCES -->
