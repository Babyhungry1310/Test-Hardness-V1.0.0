---
schema: 1
id: DEC-0034
date: 2026-11-25
title: "Cửa sổ trước Bước 3 — REVIEWER theo log, phản bác verdict, ghi file, preflight, đồ thị B3p"
proposed_by: LEAD
decided_by: OWNER
cycle: CYC-08
origin: "DSC-20261121-kzn1#E45"
supersedes: ""
cancels: []
waives: []
affects: [DEC-0033, "06_sources/SRC-0003_kaizen-chi-tiet-dot1.md", "04_control/STATE.md", "05_memory/upstream/00_tong_quan_upstream.md", "harness/rules/REVIEWER.md", "harness/rules/WORKER.md"]
keywords: [cua-so-buoc3, reviewer, preflight, gate, f50-f57]
---
## Status (newest first)
- 2026-11-25 | SUPERSEDED_BY DEC-0035
- 2026-11-25 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
- Bước 2 xong: TK-0039 (#106), TK-0040 (#108), TK-0041 (#109); sửa thẻ TK-0040 (#107).
- Các lỗi lộ ra từ #104 tới #109 được ghi vào sổ phát hiện Kaizen Đợt 1 (F50–F57); bản chụp sổ ở `03_output/CYC-08/checks/SO_PHAT_HIEN_2026-11-24.md`.
- OWNER chốt toàn bộ khuyến nghị của QUYET_DINH_OWNER_CUA_SO_B3 ngày 2026-11-24, riêng D2 đổi REVIEWER sang Gemini.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- A: sửa văn luật ngay trong cửa sổ. Loại: văn luật sửa ở Bước 4 (TK-0049 và thẻ Bước 4).
- B (chọn): một DEC ghi quy tắc vận hành mới, mỗi quy tắc một dòng kèm mã; văn luật sửa ở Bước 4.
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale

### A. REVIEWER và verdict
- REVIEWER của chuỗi cửa sổ trước Bước 3 là Gemini (`gemini-3.8-flash`, tuyến `ag/`), khác họ WORKER Luna và có log 9Router; không cần ngoại lệ cùng họ. (OWNER D2, 2026-11-24)
- REVIEWER chỉ đủ điều kiện khi `usage_9router.py` có dòng của REVIEWER trong khung review; không có dòng thì vòng đó không tính, báo OWNER. (OWNER D3, 2026-11-24)
- Vòng WORKER–REVIEWER tự chạy tới PASS, tối đa 3 vòng mỗi PR; quá 3 vòng hoặc tranh chấp không kiểm được bằng lệnh thì dừng, báo OWNER. (OWNER D4, 2026-11-24)
- OWNER được bác verdict REVIEWER khi findings sai, kiểm bằng lệnh; lý do ghi vào CẦN REVIEW. (OWNER D5, 2026-11-24)
- Mỗi mục FAIL của REVIEW phải có trích dòng, lệnh đã chạy và SHA head; mục cơ học thuộc `gate.py`, không thuộc checklist. (F05, F42)

### B. Ghi file, nhánh, run
- Tác tử ghi file bằng Python, UTF-8 không BOM, LF; không dùng PowerShell 5.1 để ghi file văn bản. (F56)
- Nhánh `task/` phải có file run và bằng chứng trong `03_output/CYC-08/checks/`. (F54)
- Nhánh `lead/` và `upgrade/` dùng chữ thường. (F52)
- Danh tính commit của tác tử đặt ở cấu hình local của repo; không dùng danh tính OWNER. (F50)
- Lệnh verify trong thẻ viết một dấu gạch chéo cho regex, chạy đúng cả cmd.exe và bash. (F57)

### C. Preflight và cổng máy
- PREFLIGHT bằng `preflight_phieu.py`; thẻ nhắc mã O, D, L thì phiếu phải trích quyết định tương ứng. (F57, F55)
- `gate.py` chạy từ checkout `origin/main`, không từ nhánh tác tử. (F50)
- Merge PR Planning P3a là `Go` cho mọi phiếu WORKER không chạm 🔒 của cửa sổ này. (OWNER D6, 2026-11-24)

### D. Nội dung và đồ thị
- O2.1, trạng thái nhóm E Bước 3 trên H0: E20 ACCEPTED (TK-0043); E21 ACCEPTED (DEC-0033 A); E22 HOÃN Đợt 2; E23 ACCEPTED (TK-0045, TK-0056); E24 ACCEPTED (TK-0046); E25 REJECTED, giữ "mỗi PR `upgrade/` tăng VERSION một lần"; E26 ACCEPTED một phần, phần manifest bằng script hoãn Đợt 2. (OWNER O2.1, 2026-11-24)
- O2.4: TK-0041 gộp dòng 1–3 của REVIEW_SECTION_9 vào HARNESS mục 9; VERSION 1.0.2. (OWNER O2.4, 2026-11-24)
- Đồ thị: B3p1 (TK-0062) → B3p2 (TK-0063) → B3p3 (TK-0064) → B3p4 (TK-0065) → O3.6 (PR thẻ Bước 3) → B3a0 (TK-0061) → B3a (TK-0042) → B3a2 (TK-0055). (OWNER D8, D9, 2026-11-24)
- Tái cấu trúc SRC thành chỉ mục và phần theo Bước hoãn tới cửa sổ trước Bước 4, cùng TK-0048. (OWNER D7, 2026-11-24; F30)

### Thay thế
- Dòng O2.1 trong bảng O của SRC-0003: cổng "trước TK-0042" đổi thành "đã chốt 2026-11-24". (F55)
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
- Có hiệu lực khi PR P3a merge. Văn luật REVIEWER.md, WORKER.md sửa ở Bước 4; tới lúc đó chỗ luật cũ trái DEC-0034 thì DEC-0034 thắng.
- TK-0062…TK-0065 giao tuần tự sau P3a; PR Planning P3b viết thẻ Bước 3 sau TK-0065.
- Sau TK-0064, nguồn chuẩn của `preflight_phieu.py`, `gate.py` chuyển sang repo `tools/`.
<!-- END: CONSEQUENCES -->
