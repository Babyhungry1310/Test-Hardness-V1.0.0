---
schema: 1
id: DEC-0006
date: 2026-11-12
title: "Khắc phục thu thập test bằng cách giới hạn pytest về tests/"
proposed_by: LEAD
decided_by: OWNER
cycle: CYC-01
origin: "RVW-CYC-01"
supersedes: ""
cancels: []
waives: []
affects: [TK-0001, TK-0002, TK-0004, "harness.yaml", "01_plan/PLAN.md#CYC_01"]
keywords: [pytest, test-collection, review]
---
## Status (newest first)
- 2026-11-12 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
OWNER đã merge PR #9, #10, #11. Main f8e9a6ae1b006a6a16d4d4b823aea756621850d6 có các run DONE nhưng `python -m pytest -q --tb=line` lỗi thu thập: `tests/test_dupes.py`, `tests/test_loader.py` trùng tên module với hai file cùng tên trong `harness/templates/examples/tests/`. RVW-CYC-01 vòng 2 trả `verdict: FAIL` vì tiêu chí pytest trên main của `01_plan/ACCEPTANCE.md#CYC_01` không đạt.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- A: thêm `tests/__init__.py` rỗng. Pytest chạy 20 test, trong đó 7 test mẫu của khung chạy trên `src/` của sản phẩm.
- B: thêm `pytest.ini` ở gốc repo với `testpaths = tests`. Pytest chạy đúng 13 test của sản phẩm.
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
OWNER chọn B. Bảy test trong `harness/templates/examples/tests/` là ví dụ của khung, không phải test của sản phẩm; phương án A buộc bộ test sản phẩm phụ thuộc vào `harness/`, thư mục bị thay nguyên khối khi nâng cấp khung. Bản thử ngoài repo trên main f8e9a6a với phương án B đạt 13/13.
`pytest.ini` được thêm vào `product_paths` của `harness.yaml` để nằm trong `write_scope` hợp lệ của TK-0004. LEAD lập TK-0004 với `fixes: TK-0002`.
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
OWNER merge task trước khi WORKER chạy TK-0004. Sau khi run sửa được merge, kiểm định vòng 3 trên main mới nhất; đây là vòng kiểm định cuối cùng được phép của CYC-01.
Không miễn trừ tiêu chí pytest trên main; không tạo cổng CYC-01_PASS hoặc digest khi REVIEWER còn FAIL.
Việc các file `test_*.py` mẫu trong `harness/templates/examples/` bị pytest thu thập là lỗi của khung; OWNER đưa bản sửa vào repo khung sau đợt chạy thử.
<!-- END: CONSEQUENCES -->
