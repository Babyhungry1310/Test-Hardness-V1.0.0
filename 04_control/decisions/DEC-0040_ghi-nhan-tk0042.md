---
schema: 1
id: DEC-0040
date: 2026-11-28
title: "Ghi nhận TK-0042 và kết quả DEC-0039; cập nhật CYC-08"
proposed_by: LEAD
decided_by: OWNER
cycle: CYC-08
origin: "DEC-0039#CONSEQUENCES"
supersedes: ""
cancels: []
waives: []
affects: [DEC-0033, DEC-0036, DEC-0038, DEC-0039, "02_work/cycles/CYC-08.md", "04_control/STATE.md"]
keywords: [tk-0042, ghi-nhan, phan-vai, cyc-08, review-ngoai-checklist]
---
## Status (newest first)
- 2026-11-28 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
| Mã | Dữ kiện | Nguồn |
| --- | --- | --- |
| A1 | TK-0042 R1 merge ở #124 (`a47f692`): sửa 5 file theo lệnh 🔒, `harness/VERSION` và dòng "Phiên bản" của `harness/HARNESS.md` cùng là 1.0.3; run schema nhận `schema` 1 hoặc 2 trong một file. | `git log a47f692 -1`; `02_work/runs/TK-0042_R1_DONE.md` |
| A2 | Model WORKER của TK-0042 R1 ghi `UNKNOWN`; run ghi "model chưa xác minh". Kiểm độc lập theo `harness/MODEL_POLICY.md` mục SAME_MODEL không tự qua; REVIEWER dừng và hỏi OWNER trước khi merge. | File run TK-0042 R1 (`model`, `deviations.differences`) |
| A3 | DEC-0039 merge ở #125 (`c96da73`). Lượt 2: `P6D/HUONG_DAN_REVIEW.md` bản 2, sha256 `24e6a80ec14b7ac4b14cec0705e91228d3f579846e400083ef60a4f83229fd11`, REVIEWER xác nhận đạt. Lượt 3: `P6D/tools/kiem_goi.py`, sha256 `d33457fc50056f9c239579f87efbb16836c5ca202d9798118af5d07f1cc7b9a0`; bộ test đóng băng sha256 `9658dd6761e7b70e853c16be3832af4d1ecc8146ac9c19c6a1a98ce3a3a98100` không đổi, thêm `test_kiem_goi_limits.py`, 29/29 test đạt. Giới hạn: liên kết thư mục (symlink) chưa kiểm khi chạy vì Windows từ chối tạo (WinError 1314); REVIEWER đã đọc mã xử lý. | Các file ở P6D theo sha256 (ngoài repo, DEC-0039 B4) |
| A4 | `02_work/cycles/CYC-08.md` dừng ở #95, chỉ ghi TK-0036…TK-0038; TK-0038 còn ghi ASSIGNED dù đã merge ở #96. Từ #97 tới #124 có thêm 15 task merge chưa ghi. Năm task `lead/` (TK-0038, TK-0053, TK-0057, TK-0058, TK-0060) merge không có file run. `harness/rules/REVIEWER.md` mục 1 dùng file này làm gói đọc khi kiểm định chu kỳ. | `git log --oneline ddf3b7b..a47f692`; `ls 02_work/runs` |
| A5 | DEC-0033 mục A ghi "lỗi ngoài checklist ghi WARN". DEC-0036 ra sau, có `affects: DEC-0033`, và B9 quy định lỗi ngoài checklist ảnh hưởng tính đúng, phạm vi hoặc an toàn phải báo và xử lý trước khi merge. DEC-0036 chưa ghi rõ câu nào của DEC-0033 bị thay. | DEC-0033 mục A; DEC-0036 B9 |
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- A (chọn): ghi các quyết định đã dùng cho TK-0042; nói rõ phạm vi DEC-0036 B9 so với DEC-0033; cập nhật `CYC-08.md` và STATE trong cùng PR.
- B: ghi `supersedes: DEC-0033`. Không chọn: phần còn lại của DEC-0033 vẫn áp.
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
| Mã | Nội dung | Trạng thái |
| --- | --- | --- |
| B1 | L-T42: lệnh 🔒 cho TK-0042 sửa `harness/schemas/run.schema.json`, `harness/schemas/EVOLUTION.md`, `harness/VERSION`, `harness/HARNESS.md` (chỉ dòng "Phiên bản") và `01_plan/SPEC_TOOLS.md`. | OWNER chốt 2026-11-27 |
| B2 | D-T42: ngoại lệ DEC-0036 B8 cho TK-0042, như D-T61 (DEC-0038 B1): Terra làm, Luna review; không thử tuyến trước; model ghi theo mức bằng chứng thực có (A2). OWNER chấp nhận kết quả kiểm độc lập không tự qua (MODEL_POLICY SAME_MODEL). Đây là cơ sở merge #124. | OWNER chốt 2026-11-28 |
| B3 | D-T42a = A1: run dùng `schema` 1 hoặc 2 trong cùng `run.schema.json`; ba khóa `models`, `evidence_kind`, `self_check` chỉ hợp lệ khi `schema: 2` (ghi ở EVOLUTION mục 4). | OWNER chốt 2026-11-27 |
| B4 | D-T42b: TK-0042 làm trên nhánh `task/TK-0042-R1` thay cho `upgrade/tk-0042-r1`; file run ghi nhánh thực tế. | OWNER chốt 2026-11-27 |
| B5 | DEC-0036 B9 thay câu "lỗi ngoài checklist ghi WARN" của DEC-0033 mục A đối với lỗi tính đúng, phạm vi hoặc an toàn; câu đó chỉ còn áp cho lỗi trình bày. Phần còn lại của DEC-0033 giữ nguyên. | OWNER chốt 2026-11-28 |
| B6 | `CYC-08.md` ghi đủ task đã merge trong CYC-08 tới TK-0042. Task `lead/` không có file run ghi `run: none`. LEAD cập nhật file này trong PR ghi nhận sau mỗi task merge. | OWNER chốt 2026-11-28 |
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
- Kế tiếp: TK-0055 (sửa `harness/`, cần lệnh 🔒). Phân vai theo DEC-0039 B3; B2 chỉ áp cho TK-0042.
- Gói Claude 2 từ nay kèm `MANIFEST.sha256`; phiếu WORKER và REVIEWER chạy `kiem_goi.py` ở bước đầu (DEC-0039 B1, B4).
<!-- END: CONSEQUENCES -->
