---
schema: 1
id: DEC-0008
date: 2026-11-13
title: "Kiểm định vòng 3 của CYC-01 chạy Claude Code trực tiếp, ngoài 9Router"
proposed_by: LEAD
decided_by: OWNER
cycle: CYC-01
origin: "RVW-CYC-01"
supersedes: ""
cancels: []
waives: []
affects: [DEC-0007]
keywords: [model-assignment, reviewer]
---
## Status (newest first)
- 2026-11-13 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
DEC-0007 giao REVIEWER của CYC-01 cho nhóm Claude và ghi nhóm này nằm trên 9Router. OWNER xác nhận 9Router trên máy không có tuyến Claude. Kiểm định vòng 3 vì vậy chạy bằng Claude Code trên cloud; RVW-CYC-01 ghi `reviewer_model: claude-sonnet-5-5`.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- Chờ thêm tuyến Claude vào 9Router rồi mới kiểm định
- Chạy phiên kiểm định bằng Claude Code trực tiếp, không qua 9Router
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
Chấp nhận phiên kiểm định chạy Claude Code trực tiếp. Điều DEC-0007 cần giữ là REVIEWER khác model với mọi WORKER; `claude-sonnet-5-5` khác `gpt-6.1-sol` và `gemini-3.8-flash-k`. Phiên chạy ngoài 9Router nên không có nguy cơ bị chuyển sang model dự phòng của nhóm Codex hay Gemini. Phân công WORKER của DEC-0007 giữ nguyên.
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
`reviewer_model` của vòng 3 lấy từ phiên Claude Code, không lấy từ nhật ký 9Router. LEAD của các PR từ #12 cũng là một model Claude; LEAD không viết sản phẩm, nên luật "REVIEWER khác WORKER" vẫn được giữ. Phân công model cho CYC-02 cần một `DEC` riêng, ghi rõ công cụ chạy từng vai.
<!-- END: CONSEQUENCES -->
