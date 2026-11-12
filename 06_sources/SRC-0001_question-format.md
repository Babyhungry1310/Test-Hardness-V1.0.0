---
schema: 1
id: SRC-0001
date: 2026-11-12
title: "Định dạng một câu hỏi do OWNER cung cấp"
decided_by: OWNER
related: [DEC-0002]
keywords: [quiz-bank, question-format]
---
<!-- ANCHOR: CONTEXT -->
## Context
Nguồn: OWNER cung cấp trong phiên lập plan (`mau-b.txt`), 2026-11-12; scan: ALLOW.

Mỗi câu hỏi là một đối tượng JSON có đúng ba trường:

| Trường | Kiểu | Bắt buộc |
|---|---|---|
| `id` | chuỗi, dạng `Q-nnn` | Có |
| `text` | chuỗi | Có |
| `answer` | chuỗi | Có |
<!-- END: CONTEXT -->
