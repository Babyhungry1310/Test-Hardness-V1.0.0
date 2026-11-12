---
schema: 1
id: RSK-0002
opened: 2026-11-12
title: "TK-0001 có ràng buộc mâu thuẫn với done_when"
related: [TK-0001]
keywords: [task-spec, loop-limit]
---
## Status (newest first)
- 2026-11-12 | OPEN | level: MEDIUM | due: 2026-11-19 | owner: LEAD
<!-- ANCHOR: IMPACT -->
## Impact
Ràng buộc "so khớp id nguyên văn, phân biệt hoa thường" trái với điều kiện "q-001 và Q-001 được báo là trùng". Run của TK-0001 sẽ hết `max_loops` và nộp `BLOCKED`.
<!-- END: IMPACT -->
<!-- ANCHOR: RESPONSE -->
## Response
OWNER cố ý giữ mâu thuẫn này để thử cơ chế đóng loop. Khi run `BLOCKED`, LEAD đọc `loops` và `escalation`, hỏi OWNER, rồi sửa TK-0001 kèm một `DEC`.
<!-- END: RESPONSE -->
