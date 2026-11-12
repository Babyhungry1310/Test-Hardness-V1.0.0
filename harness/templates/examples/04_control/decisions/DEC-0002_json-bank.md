---
schema: 1
id: DEC-0002
date: 2026-11-02
title: "Lưu ngân hàng câu hỏi dạng JSON và xuất handout Markdown"
proposed_by: LEAD
decided_by: OWNER
cycle: NONE
origin: "DSC-20261102-q7k2#E1"
supersedes: "DEC-0001"
cancels: []
waives: []
affects: ["data/bank.json"]
keywords: [quiz-bank, storage, handout]
---
## Status (newest first)
- 2026-11-02 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
Câu hỏi và đáp án thường có nhiều dòng; DEC-0001 buộc phải thoát ký tự xuống dòng.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- Giữ CSV
- JSON, mỗi câu có id, text, answer
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
Chọn JSON vì giữ nguyên câu nhiều dòng và có kiểu rõ cho từng trường. Đầu ra là handout Markdown để in và sửa tay được.
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
Mỗi câu phải có đủ id, text, answer; công cụ đọc báo lỗi khi thiếu trường.
<!-- END: CONSEQUENCES -->
