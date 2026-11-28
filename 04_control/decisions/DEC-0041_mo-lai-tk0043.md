---
schema: 1
id: DEC-0041
date: "2026-11-28"
title: "Mở lại TK-0043 sau R1 BLOCKED"
proposed_by: LEAD
decided_by: LEAD
cycle: CYC-08
origin: "DEC-0037#RATIONALE"
supersedes: ""
cancels: []
waives: []
affects: [TK-0043, "01_plan/SPEC_TOOLS.md", "02_work/cycles/CYC-08.md", "04_control/STATE.md"]
keywords: [tk-0043, validate, reopen]
---
## Status (newest first)
- 2026-11-28 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
TK-0055 R1 DONE (#127). TK-0043 R1 BLOCKED (#128): L01, L02 đạt lệnh verify nhưng còn điều kiện chưa xác minh. Xem hồ sơ TK-0043_R1_BLOCKED và bằng chứng blocker kèm run.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
Mở lại với ca hồi quy cho các thiếu sót của R1 hoặc dừng task.
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
LEAD mở R2 theo luật 28. Phạm vi sản phẩm và done_when giữ theo thẻ TK-0043. Áp dụng cách kiểm tại SPEC_TOOLS#VALIDATE_R2. Terra thực hiện, Luna review độc lập theo DEC-0039 B3.
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
R2 có tối đa hai loop mới, L03 và L04. Nếu R2 vẫn BLOCKED, đưa về OWNER. Giữ bằng chứng của R1 trên main.
<!-- END: CONSEQUENCES -->
