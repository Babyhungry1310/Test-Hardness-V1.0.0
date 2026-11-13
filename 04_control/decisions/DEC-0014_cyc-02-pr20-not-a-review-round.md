---
schema: 1
id: DEC-0014
date: 2026-11-13
title: "Bản kiểm định CYC-02 do gpt-6.1-sol chạy không tính là một vòng kiểm định"
proposed_by: LEAD
decided_by: OWNER
cycle: CYC-02
origin: "DEC-0012#RATIONALE"
supersedes: ""
cancels: []
waives: []
affects: [TK-0003, TK-0005]
keywords: [reviewer, model-assignment, review-round]
---
## Status (newest first)
- 2026-11-13 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
PR #20 nộp một bản `RVW-CYC-02` có `reviewer_model: gpt-6.1-sol`, `verdict: FAIL`, trong khi run TK-0003 R1 ghi `model: gpt-5.6-luna`. Hai model cùng nhóm Codex. DEC-0012 giao REVIEWER của CYC-02 cho nhóm Gemini. Bản ghi nêu hai điểm: F1 (LF bị đổi thành CRLF trên Windows) và A1 (số ký tự xuống dòng cuối file).
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- Không tính: đóng PR #20, sửa lỗi rồi giao nhóm Gemini kiểm định vòng 1
- Có tính: merge PR #20 làm vòng 1, nhóm Gemini kiểm định vòng 2
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
OWNER chọn phương án đầu. Bản ghi vi phạm tính độc lập model (nhóm Codex kiểm sản phẩm của nhóm Codex) và trái DEC-0012. PR #20 được đóng, không merge; `RVW-CYC-02` chưa tồn tại trên `main`. CYC-02 còn đủ 3 vòng kiểm định.

Hai điểm F1 và A1 vẫn được xử lý vì là lỗi của sản phẩm: quy tắc ở DEC-0013, thi công ở TK-0005.
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
Sau khi run của TK-0005 vào `main`, LEAD chạy pytest toàn repo rồi OWNER giao nhóm Gemini kiểm định vòng 1 trên nhánh `review/CYC-02` mới, tạo từ `main` mới nhất.
<!-- END: CONSEQUENCES -->
