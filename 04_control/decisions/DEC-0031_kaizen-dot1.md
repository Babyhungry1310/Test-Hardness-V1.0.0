---
schema: 1
id: DEC-0031
date: 2026-11-22
title: "Kaizen Dot1 Bước 0: E14 tách tài khoản, E15 chuyển repo mẹ, 5 quyết định chặn"
proposed_by: LEAD
decided_by: OWNER
cycle: CYC-08
origin: "DSC-20261121-kzn1"
supersedes: ""
cancels: []
waives: []
affects: [DEC-0019, DEC-0020, RSK-0004, "01_plan/PLAN.md#CYC_08", "05_memory/upstream/00_tong_quan_upstream.md"]
keywords: [kaizen, e14, e15, github-accounts, upstream]
---
## Status (newest first)
- 2026-11-22 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
Sau TK-0036 (H0–H4 DỰ THẢO trên main), OWNER trả lời Q1–Q4 trong SRC-0006 và ra lệnh Start CYC-08. Bước 0 cần chốt E14, E15 và năm quyết định chặn trước các bước Kaizen tiếp theo; ghi nhận trong DSC-20261121-kzn1.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- E14: giữ tài khoản GitHub chung (DEC-0019) hoặc tách tài khoản máy. OWNER chọn tách.
- E15: giữ DEC-0020 (chờ kiểm kê cuối sau CYC-07) hoặc chuyển repo mẹ theo từng nhóm PROPOSAL đã chốt. OWNER chọn chuyển theo nhóm.
- Năm quyết định chặn Bước 0: đồng ý từng ý hoặc hoãn. OWNER đồng ý cả năm.
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
1. **E14 = tách:** tác tử dùng tài khoản GitHub `conchonomoconmeo-AIAIAI`; OWNER giữ `Babyhungry1310`. Ruleset và luật thẻ đặt bypass chỉ cho OWNER (thực hiện ở Bước 1 / O1.1–O1.3). DEC-0019 vẫn ACTIVE về lịch sử dry-run dùng chung; thực tế vận hành Kaizen từ đây theo tài khoản tách.
2. **E15 = đồng ý:** chuyển về repo mẹ theo từng nhóm PROPOSAL đã chốt, không chờ kiểm kê cuối sau CYC-07. Chốt E15 trước mọi nhóm E còn lại.
3. **Năm quyết định chặn = ĐỒNG Ý:** (a) tạm dừng chu kỳ sản phẩm; (b) Kaizen lấy origin từ DEC; (c) bật ruleset Nhánh 1; (d) dữ liệu run cũ chỉ kiểm từ mốc; (e) trường `model` dạng danh sách, mỗi phần tử là model thực tế đã xác minh, không ghi tên tuyến (E21).
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
- Task sau TK-0037 lấy `origin: "DEC-0031"` thay cho `01_plan/PLAN.md#CYC_08` khi DEC này đã merge.
- RSK-0004 cập nhật dòng trạng thái E14=tách; giữ OPEN tới khi OWNER xác nhận ruleset, luật thẻ và quyền collaborator thực tế (O1.1–O1.3).
- PR #37 CLOSED đã được xác nhận (O0.1); không mở lại draft đó làm cổng Bước 0.
- E1–E13 và E16–E26 còn PROPOSAL/QUESTION trong DSC; chưa ACCEPTED trừ E14 và E15.
<!-- END: CONSEQUENCES -->
