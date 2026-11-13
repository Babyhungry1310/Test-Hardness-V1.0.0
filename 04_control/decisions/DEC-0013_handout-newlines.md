---
schema: 1
id: DEC-0013
date: 2026-11-13
title: "Handout kết thúc bằng đúng một LF và ghi file với newline LF"
proposed_by: LEAD
decided_by: OWNER
cycle: CYC-02
origin: "DEC-0010#RATIONALE"
supersedes: ""
cancels: []
waives: []
affects: [DEC-0010, TK-0003, TK-0005, "01_plan/ACCEPTANCE.md#CYC_02"]
keywords: [handout, markdown, newline, crlf]
---
## Status (newest first)
- 2026-11-13 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
DEC-0010 yêu cầu file handout kết thúc bằng đúng một ký tự xuống dòng và giữ nguyên văn `text`, `answer`. Hai yêu cầu này mâu thuẫn khi `answer` của câu cuối đã kết thúc bằng ký tự xuống dòng. `src/handout.py` của TK-0003 R1 mở file đầu ra ở chế độ văn bản mặc định, nên trên Windows mọi LF bị đổi thành CRLF, kể cả LF nằm trong `text` và `answer`.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- Giữ nguyên văn `answer` của câu cuối, chấp nhận file kết thúc bằng nhiều ký tự xuống dòng
- File luôn kết thúc bằng đúng một LF; ghi file với `newline="\n"`
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
OWNER chọn phương án sau. Quy tắc này bổ sung DEC-0010 và thắng yêu cầu giữ nguyên văn ở đúng vị trí cuối file.

- File handout luôn kết thúc bằng đúng một ký tự LF (`\n`).
- Khi nối chuỗi: `answer` của câu cuối đã kết thúc bằng `\n` thì không thêm `\n`; chưa có thì thêm đúng một `\n`. `answer` của câu cuối kết thúc bằng nhiều `\n` thì file vẫn chỉ kết thúc bằng một `\n`.
- Khi ghi file: mở file đầu ra với `newline="\n"`, để kết quả giống nhau trên Linux và Windows.
- Ngoài vị trí cuối file, `text` và `answer` giữ nguyên văn theo DEC-0010. Bố cục, cách gọi và mã thoát của DEC-0010 không đổi.
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
TK-0005 sửa `src/handout.py` và thêm test ở mức byte. `01_plan/ACCEPTANCE.md#CYC_02` thêm một điều kiện nghiệm thu. `01_plan/PLAN.md` lên `version: 3`.
<!-- END: CONSEQUENCES -->
