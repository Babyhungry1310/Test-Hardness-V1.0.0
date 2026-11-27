---
schema: 1
id: DEC-0037
date: 2026-11-27
title: "O3.6 — thẻ Bước 3: chốt E5/E7/E16/E18, nguồn TK-0056, cách làm PR P3b"
proposed_by: LEAD
decided_by: OWNER
cycle: CYC-08
origin: "DEC-0036#RATIONALE"
supersedes: ""
cancels: []
waives: []
affects: [DEC-0032, DEC-0036, "06_sources/SRC-0003_kaizen-chi-tiet-dot1.md", "04_control/STATE.md", "05_memory/upstream/00_tong_quan_upstream.md", TK-0061, TK-0042, TK-0043, TK-0044, TK-0045, TK-0055, TK-0056, TK-0046, TK-0047]
keywords: [o3-6, the-buoc3, e5, e7, e16, e18, tk-0056, gsd-core, injection-scan]
---
## Status (newest first)
- 2026-11-27 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
- DEC-0036 đã chốt O3.6 giữ 9 thẻ trong một PR (B1), E4/E6/E9/Q13 (B2–B5). Base đã kiểm: origin/main `01eb881` (sau #120).
- Thẻ P5 của TK-0042 (SRC-0003 @ `7ad7aa6`) đặt điều kiện "O2.1 phải đã chấp E5 E7 E16 E18 E21". O2.1 (DEC-0034) chỉ chốt E20–E26. DEC-0031 dòng 39 ghi E1–E13, E16–E26 còn PROPOSAL/QUESTION. Bốn mã E5, E7, E16, E18 chưa được chốt ở DEC nào.
- TK-0056 cần nguồn mẫu quét từ GSD Core; DEC-0032 đã ACCEPTED E39 → TK-0056.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- A (chọn): chốt bốn mã trong DEC này, viết đủ 9 thẻ trong một PR, chia commit theo đợt để review.
- B: tách O3.6 thành nhiều PR. Không chọn: trái DEC-0036 B1.
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale

### A. Ghi nhận (có nguồn)
| Mã | Nội dung | Nguồn |
| --- | --- | --- |
| A1 | Trạng thái E27–E43 hiện hành là bảng truy vết SRC-0003 và DEC-0032: E33, E36, E37, E39 ACCEPTED; E43 ACCEPTED một phần; E29, E38, E40 ACCEPTED, gán task khi viết thẻ Bước 3; E35 một phần. H0 (`05_memory/upstream/00_tong_quan_upstream.md`) vẫn ghi PROPOSAL cho các mã này, nhưng dòng đầu H0 tự ghi "Nguồn hiện hành: SRC-0003 P6d, DEC-0032". | DEC-0032 mục 1; SRC-0003 "Bảng truy vết E27–E43" |
| A2 | Nguồn TK-0056: `https://github.com/open-gsd/gsd-core`, commit `663f9ad90d31b09b457253bcff0d622c98d6b10f` (2026-11-22), tree `13d6b9b1c3d9ad2de99df18000e4468ab58125d1`. `LICENSE`: blob `d47f8ea21c0c46de01da7f0f61f92d4bee44631b`, sha256 `3a160aec61eeb28e75e8017346ee190db07986a09c4bd72555cc706f1d99e27e`, MIT "Copyright (c) 2026 Open GSD". `scripts/prompt-injection-scan.sh`: blob `3b8e6adbcbc84bfe77ff988cf4c4a64d31225852`, sha256 `132ec5c0af7ed7e08d8fe407e79c365c4fbfefcc979643d85dee71440a5a79e2`. `scripts/base64-scan.sh`: blob `8f99db627e10172194f4bf6aeabd3a19dc563e91`, sha256 `fd14c0d3c02bc7c049d5c5d8d8ede09a202d96355aca79e4ee3a652cab5d2f39`. Repo gốc không có file NOTICE. Khớp SRC-0008 dòng 14. | Claude 2 đối chiếu bằng `git ls-tree`/`git show`, 2026-11-27 |
| A3 | `tools/gate.py` v5 (#117) có 4 docstring, trái HARNESS 8.4 (C13). `tools/usage_9router.py --out` ghi CRLF trên Windows trong khi hash in ra tính trên LF (DEC-0036 ghi chú phần A). Cả hai sửa ở một task `tools/` riêng sau O3.6; không thuộc 9 thẻ. | `tools/gate.py` dòng 195, 242, 336, 362; `tools/usage_9router.py` hàm `main` |
| A4 | 24/55 file run lịch sử (`02_work/runs/`) không qua `harness/schemas/run.schema.json` hiện hành (khuôn cũ). Thẻ sửa `run.schema` kiểm "không thêm file FAIL", không đòi toàn bộ đạt. | Claude 2 chạy jsonschema trên main `01eb881` |
| A5 | Dãy số DEC trên main thiếu DEC-0022, 0023, 0024, 0025, 0027 (không có file ở `decisions/` lẫn `superseded/`; DEC-0027 chỉ có trong một commit nhánh chưa merge). Đây là khoảng trống lịch sử đã biết; kiểm "DEC liên tục" (TK-0044) chấm theo chênh lệch, không báo các khoảng trống này. | `ls 04_control/decisions/DEC-* 04_control/decisions/superseded/DEC-*`; `git log --all --diff-filter=A` |
| A6 | `01_plan/SPEC_TOOLS.md#CONVENTIONS` chỉ cho thư viện ngoài `jsonschema`, `ruamel.yaml`, `pytest`. TK-0045 (pre-push, E23) và TK-0056 (baseline, Q-C) cần `detect-secrets`; theo E24 (ACCEPTED, công cụ Python mới cài qua pip), TK-0042 thêm `detect-secrets` vào danh sách đó. | SPEC_TOOLS dòng "Thư viện ngoài chuẩn"; DEC-0034 O2.1 (E23, E24) |
| A7 | C12 (HARNESS 8.3): `harness/VERSION` phải khớp dòng "Phiên bản" ở `harness/HARNESS.md` (dòng 10, hiện 1.0.2). Thẻ đợt 1 TK-0061 và TK-0055 tăng VERSION nhưng không có `HARNESS.md` trong write_scope, nên sẽ làm lệch C12. | HARNESS dòng 10, dòng C12 bảng 8.3 |

### B. Quyết định OWNER
| Mã | Nội dung | Trạng thái |
| --- | --- | --- |
| B1 | E5: ACCEPTED. Mã thoát 0 đạt, 1 FAIL, 2 lỗi dùng hoặc môi trường, 3 không rõ (lỗi nội bộ). Lỗi quyền, môi trường không tính loop, tối đa 2 lần thử. Mã 66 NO_INPUT thêm theo E36 (TK-0055). | OWNER chốt 2026-11-27 |
| B2 | E7: ACCEPTED một phần. Nhận: khóa model dạng danh sách và khóa loại bằng chứng trong `run.schema` (TK-0042). Hoãn: raw capture, cùng E6 (DEC-0036 B3) và E22. | OWNER chốt 2026-11-27 |
| B3 | E16: hook gặp mã 3 thì chặn, báo BLOCKED kèm chẩn đoán. Quy ước ở TK-0042, hành vi hook ở TK-0045 (nhất quán E37). | OWNER chốt 2026-11-27 |
| B4 | E18: ACCEPTED. Bảng lỗi thống nhất ở `01_plan/SPEC_TOOLS.md#CONVENTIONS` (TK-0042). | OWNER chốt 2026-11-27 |
| B5 | TK-0056 viết lại bằng Python, phái sinh từ nguồn A2; NOTICE chép nguyên văn LICENSE kèm repo, SHA, blob id; mức cảnh báo (E39); không gọi shell, không mạng. | OWNER chốt 2026-11-27 |
| B6 | PR P3b (O3.6) là một PR `lead/`, ba commit theo đợt: đợt 1 = DEC này + thẻ TK-0061, TK-0042, TK-0055; đợt 2 = TK-0043, TK-0044, TK-0045; đợt 3 = TK-0056, TK-0046, TK-0047 + STATE. Review từng commit; OWNER merge sau đợt 3. | OWNER chốt 2026-11-27 |
| B7 | Phân vai P3b: Claude 2 soạn nội dung; Terra chép nguyên văn theo sha256 và chạy gate; Luna review (khác họ với người soạn). Model của Terra, Luna ghi theo mức bằng chứng thực có (như DEC-0036 B11). | OWNER chốt 2026-11-27 |
| B8 | Sửa theo A7: TK-0061 đổi sang nhánh `task/`, không tăng VERSION (chỉ sửa `tools/`); quy ước ON_CRASH (E37) chuyển sang TK-0042; TK-0055 thay `01_plan/SPEC_TOOLS.md` bằng `harness/HARNESS.md` trong write_scope; con trỏ tới `exit_codes.json` trong SPEC_TOOLS do TK-0046 ghi. Chuỗi VERSION: TK-0042 1.0.3, TK-0055 1.0.4, TK-0046 1.0.5; thẻ nào tăng VERSION thì verify kiểm C12. | OWNER chốt 2026-11-27 |
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
- Thẻ Bước 3 trong SRC-0003 có `origin: DEC-0037`.
- TK-0042 không còn điều kiện chờ E5/E7/E16/E18.
- Mỗi task sửa `harness/` cần lệnh OWNER 🔒 trước khi mở PR task (ghi trong constraints của thẻ).
<!-- END: CONSEQUENCES -->
