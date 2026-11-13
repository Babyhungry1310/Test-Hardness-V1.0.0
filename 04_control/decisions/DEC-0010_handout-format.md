---
schema: 1
id: DEC-0010
date: 2026-11-13
title: "Định dạng handout Markdown và giao diện dòng lệnh"
proposed_by: LEAD
decided_by: OWNER
cycle: CYC-02
origin: "01_plan/PLAN.md#CYC_02"
supersedes: ""
cancels: []
waives: []
affects: [TK-0003, "01_plan/ACCEPTANCE.md#CYC_02"]
keywords: [handout, markdown, cli]
---
## Status (newest first)
- 2026-11-13 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
DEC-0002 chốt đầu ra là handout Markdown nhưng chưa nêu bố cục, có in đáp án hay không, và cách gọi công cụ. Đây là thứ người dùng cuối nhìn thấy nên OWNER quyết.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- Mỗi câu một mục, đáp án in ngay dưới câu hỏi
- Mỗi câu một mục, không in đáp án
- Câu hỏi ở trên, toàn bộ đáp án gom ở cuối file
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
Chọn phương án đầu: handout dùng để ôn tập, người học xem được đáp án ngay.

Bố cục file, mã hóa UTF-8, kết thúc bằng đúng một ký tự xuống dòng:

```text
# Handout

## Q-001

<text của câu>

**Đáp án:** <answer của câu>

## Q-002
```

Các mục theo đúng thứ tự trong ngân hàng, cách nhau một dòng trống. `text` và `answer` giữ nguyên văn, kể cả khi nhiều dòng.

Cách gọi: `python -m src.handout <đường dẫn bank.json> <đường dẫn handout.md>`.

| Tình huống | Hành vi | Mã thoát |
|---|---|---|
| Ngân hàng hợp lệ, không trùng id | Ghi file handout | 0 |
| Có id trùng theo DEC-0004 | In các id trùng ra stderr, không tạo file | 1 |
| Đường dẫn đầu ra không kết thúc bằng `.md` | In lỗi ra stderr, không tạo file | 2 |
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
TK-0003 thi công đúng bố cục và bảng hành vi trên. Đổi bố cục sau này cần một `DEC` thay quyết định này.
<!-- END: CONSEQUENCES -->
