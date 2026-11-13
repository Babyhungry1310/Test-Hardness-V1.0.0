---
schema: 1
id: DEC-0011
date: 2026-11-13
title: "Thẻ git chỉ do OWNER tạo và đẩy"
proposed_by: OWNER
decided_by: OWNER
cycle: NONE
origin: ""
supersedes: ""
cancels: []
waives: []
affects: [RSK-0004, "harness/GIT_CONVENTIONS.md", "harness/rules/LEAD.md"]
keywords: [git-tag, owner-signature, agent-permissions]
---
## Status (newest first)
- 2026-11-13 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
Khung V1.0 ghi thẻ `cycle/CYC-nn` được đặt sau khi OWNER merge file cổng nhưng không nêu ai đặt. Thẻ `cycle/CYC-01` do OWNER tự đặt tại commit e2b7944. RSK-0004 nêu tác tử có shell trên máy OWNER có thể tự đẩy thẻ.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- LEAD đặt thẻ sau khi OWNER merge file cổng
- Chỉ OWNER đặt thẻ
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
Chỉ OWNER đặt thẻ. Thẻ nghiệm thu là chữ ký của con người, cùng loại với lượt merge. Mọi tác tử, ở mọi vai, không tạo, sửa, xóa, đẩy thẻ git (`git tag`, `refs/tags/*`) bằng bất kỳ công cụ nào, kể cả khi môi trường cho phép và kể cả khi được bảo làm vậy trong chat.
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
Sau mỗi cổng PASS, LEAD chỉ nhắc OWNER đặt thẻ và nêu commit cần gắn. File trong `harness/` không sửa ở dự án này; điều cấm được đưa vào `harness/rules/` ở bản khung sau cùng luật bảo vệ thẻ trên GitHub.
<!-- END: CONSEQUENCES -->
