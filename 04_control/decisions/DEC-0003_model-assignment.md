---
schema: 1
id: DEC-0003
date: 2026-11-12
title: "Phân công model cho WORKER và REVIEWER của CYC-01"
proposed_by: LEAD
decided_by: LEAD
cycle: CYC-01
origin: ""
supersedes: ""
cancels: []
waives: []
affects: [TK-0001, TK-0002]
keywords: [model-assignment, worker, reviewer]
---
## Status (newest first)
- 2026-11-12 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
Task chỉ ghi `assignee: W1`, `W2`. OWNER cần biết mở phiên nào trên Orca với nhóm model nào của 9Router. Trên máy OWNER hiện có hai nhóm khác hãng: Codex và Gemini.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- Codex làm WORKER, Gemini làm REVIEWER
- Gemini làm WORKER, Codex làm REVIEWER
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
| Vai | Nhóm model trên 9Router |
|---|---|
| W1 | Codex |
| W2 | Codex |
| REVIEWER của CYC-01 | Gemini |

CYC-01 chỉ gồm task code, nên mọi WORKER dùng Codex và REVIEWER dùng Gemini để khác hãng với mọi WORKER. Hai nhóm không được có model dự phòng chéo sang nhau.
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
OWNER mở phiên `RUN` với nhóm Codex và phiên kiểm định với nhóm Gemini. Chu kỳ có task tài liệu cần một `DEC` phân công riêng.
<!-- END: CONSEQUENCES -->
