---
schema: 1
id: DEC-0005
date: 2026-11-12
title: "Giữ phân công DEC-0003 dù run R1 của TK-0001 chạy Gemini"
proposed_by: LEAD
decided_by: OWNER
cycle: CYC-01
origin: "TK-0001"
supersedes: ""
cancels: []
waives: []
affects: [TK-0001, TK-0002, DEC-0003]
keywords: [model-assignment, reviewer, worker]
---
## Status (newest first)
- 2026-11-12 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
DEC-0003 giao W1, W2 cho nhóm Codex và REVIEWER của CYC-01 cho nhóm Gemini. Run R1 của TK-0001 lại ghi `model: gemini-3.8-flash-k`. Run này là `BLOCKED`, `outputs: []`, `loops: []`: không viết mã, không chạy `verify`, chỉ nêu mâu thuẫn trong đặc tả.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- Đổi vai: Gemini làm WORKER, Codex làm REVIEWER, thay DEC-0003
- Giữ DEC-0003, ghi nhận run R1 không tạo sản phẩm
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
Giữ DEC-0003. Run R2 của TK-0001 và run của TK-0002 chạy nhóm Codex; REVIEWER của CYC-01 là nhóm Gemini. Run R1 của TK-0001 không tạo sản phẩm nào để kiểm định, nên Gemini không kiểm việc do chính mình làm. Mọi sản phẩm của CYC-01 phải đến từ run chạy nhóm Codex.
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
Phiên kiểm định CYC-01 sẽ thấy model của mình trùng `model` của run R1 và dừng bằng khối `QUESTION`; OWNER trả lời tiếp tục theo quyết định này. Câu 2 của cổng `CYC-01_PASS` trả `CONDITIONAL`, trỏ RSK-0003. Nếu một run `DONE` của CYC-01 chạy nhóm Gemini thì quyết định này không còn áp dụng và phải đổi REVIEWER.
<!-- END: CONSEQUENCES -->
