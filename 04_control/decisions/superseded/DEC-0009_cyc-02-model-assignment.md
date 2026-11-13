---
schema: 1
id: DEC-0009
date: 2026-11-13
title: "Phân công model CYC-02: WORKER dùng Codex, REVIEWER dùng Claude Code trực tiếp"
proposed_by: LEAD
decided_by: LEAD
cycle: CYC-02
origin: "01_plan/PLAN.md#CYC_02"
supersedes: ""
cancels: []
waives: []
affects: [TK-0003]
keywords: [model-assignment, worker, reviewer]
---
## Status (newest first)
- 2026-11-13 | SUPERSEDED_BY DEC-0012
- 2026-11-13 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
CYC-02 có một task code, TK-0003, giao W1. Ở CYC-01, nhóm Codex trên 9Router chạy ổn định với `gpt-6.1-sol`; các tuyến Gemini văn bản và code không hoạt động; 9Router không có tuyến Claude nên kiểm định vòng 3 chạy Claude Code trực tiếp theo DEC-0008.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- W1 dùng Codex qua 9Router; REVIEWER dùng Claude Code trực tiếp
- W1 dùng Codex; REVIEWER dùng Gemini qua 9Router
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
| Vai | Model | Công cụ chạy |
|---|---|---|
| W1 | Nhóm Codex (`gpt-6.1-sol`) | Orca qua 9Router |
| REVIEWER của CYC-02 | `claude-sonnet-5-5` | Claude Code trực tiếp, ngoài 9Router |

Cả hai tuyến đã chạy được ở CYC-01. Không chọn Gemini vì tuyến văn bản và code chưa hoạt động lại. Nhóm Codex không được có model dự phòng thuộc Claude.
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
OWNER mở phiên `RUN` với nhóm Codex và phiên kiểm định bằng Claude Code. Trước khi giao kiểm định, LEAD đối chiếu trường `model` của mọi run trong CYC-02; có run ghi một model Claude thì phải đổi REVIEWER bằng một `DEC` mới. LEAD hiện cũng là một model Claude; LEAD không viết sản phẩm.
<!-- END: CONSEQUENCES -->
