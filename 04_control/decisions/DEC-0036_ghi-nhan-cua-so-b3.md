---
schema: 1
id: DEC-0036
date: 2026-11-27
title: "Ghi nhận kết thúc cửa sổ trước Bước 3 và chuẩn bị O3.6"
proposed_by: LEAD
decided_by: OWNER
cycle: CYC-08
origin: "DEC-0035#CONSEQUENCES"
supersedes: ""
cancels: []
waives: []
affects: [DEC-0035, DEC-0033, "06_sources/SRC-0003_kaizen-chi-tiet-dot1.md", "01_plan/PLAN.md", "04_control/STATE.md", TK-0046, TK-0047, TK-0062, TK-0063, TK-0064, TK-0065, TK-0066]
keywords: [cua-so-buoc3, ghi-nhan, o3-6, gate-v5, plan-based-on, xac-minh-model]
---
## Status (newest first)
- 2026-11-27 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
- Cửa sổ trước Bước 3 xong: TK-0062 R2 (#112), TK-0063 (#113), TK-0064 (#114), TK-0065 (#115), thẻ TK-0066 (#116), TK-0066 R1 (#117); F24 (#118), F58 (#119). Base đã kiểm: `f4de9f1e90ac`.
- Trong cửa sổ, OWNER ra một số quyết định chỉ nằm trong phiếu giao việc, chưa nằm trong DEC nào. TK-0066 (B3p5) có thẻ trên main nhưng chưa có trong bảng delta và đồ thị của SRC-0003.
- `01_plan/PLAN.md` `based_on` còn 4 DEC không còn ACTIVE (DEC-0007, DEC-0018, DEC-0028, DEC-0029), trái LEAD luật 21. DEC-0033 có ghi `affects: 01_plan/PLAN.md` nhưng PLAN chưa được cập nhật.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- A (chọn): một DEC, hai phần. Phần A chỉ ghi điều đã xảy ra, kèm nguồn. Phần B chỉ ghi điều OWNER đã chốt.
- B: ghi từng quyết định thành DEC riêng. Không chọn vì quá nhiều DEC nhỏ cho cùng một cửa sổ (F30).
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale

### A. Ghi nhận (đã xảy ra; mỗi dòng có nguồn)
Mức bằng chứng model của REVIEWER: **mức C** = có dòng đúng model trong khung giờ review, chưa liên kết được với phiên (không có định danh phiên, không bảo đảm khung độc quyền).

Hash CSV ở A3, A4, A6, A7, A8 là sha256 mà `tools/usage_9router.py --out` in ra lúc tạo file, tính trên nội dung LF. Trên Windows, script ghi file bằng `write_text` không đặt `newline`, nên file trên đĩa là CRLF và băm trực tiếp ra giá trị khác. Đối chiếu: đổi CRLF thành LF rồi băm. Tác tử đã đối chiếu 5 file ngày 2026-11-27: khớp. CSV chỉ chứng minh mức C, không liên kết model với phiên.

| Mã | Ngày | Nội dung | Nguồn |
| --- | --- | --- | --- |
| A1 | 2026-11-25 | D2b: REVIEWER của TK-0062 là Grok, thay Gemini của DEC-0035 A. | Phiếu GIAO_TK-0062_R2_LUNA mục 0; PR #112 → `401aff5` |
| A2 | 2026-11-26 | Review TK-0062: **không có bằng chứng model REVIEWER** (không có CSV); ghi KHÔNG XÁC MINH. | OWNER xác nhận không có CSV (2026-11-27) |
| A3 | 2026-11-26 | D2c: REVIEWER của TK-0063 là Luna; review PASS @ `77420ade6654`; CSV `usage_PR113_review_luna.csv` 18 dòng `gpt-6-luna`, sha `14e96f5b035a` (mức C). | PR #113 → `098afac` |
| A4 | 2026-11-26 | D11: (a) miễn G5 cho TK-0064, khớp bảng hit `03_output/CYC-08/checks/TK-0064_R1_scan.json`; (b) gate của TK-0064 chạy bằng gate.py v4 (sha `81385d9fa9b0`) ngoài repo, vì DEC-0035 chỉ nêu TK-0062/0063. Review Luna PASS @ `248d6e77fc59`; CSV 14 dòng, sha `7a70f8cb0fbc` (mức C). | Phiếu GIAO_TK-0064_R1_GROK mục 0; PR #114 → `5fc53d4` |
| A5 | 2026-11-26 | Ngoại lệ gate của DEC-0035 hết khi TK-0064 merge; từ đó gate chạy bằng `tools/gate.py` lấy từ checkout `origin/main`. | DEC-0035 Consequences; PR #114 |
| A6 | 2026-11-26 | D12: miễn G5 cho TK-0065 trên `tools/tests/test_scan_core.py`, kế thừa 9 hit, mới 0 (`03_output/CYC-08/checks/TK-0065_R1_scan_delta.json`). REVIEWER là Luna (OWNER xác nhận 2026-11-27); review PASS @ `d249ea88a729`; CSV 5 dòng `gpt-6-luna`, sha `389a1d38a4da` (mức C). | Phiếu GIAO_TK-0065_R1_GROK mục 0; PR #115 → `d68a1e4`. |
| A7 | 2026-11-26 | O-V5: thêm B3p5/TK-0066 (gate.py v5: G5 chấm chênh lệch base–head, `--accept-scan` nhiều quy tắc, G4 cảnh báo ANSI, G11 `tools/tests` chênh lệch). Thẻ qua PR `lead/` (review Luna PASS @ `3e301d44eda5`; CSV 10 dòng, sha `dff00d2b3b18`, mức C); task TK-0066 R1. | PR #116 → `9d00ba7`; PR #117 → `f09f431` |
| A8 | 2026-11-26 | D5 ở #117: OWNER bác verdict FAIL của Luna (done_when 3) vì bằng chứng v5 tự chạy không thể chứa chính commit của nó; Claude 2 chạy v5 trên HEAD `be37b594ba3a` → ĐẠT G1–G11; CSV 5 dòng, sha `c8158574820d` (mức C). | PR #117 → `f09f431` |
| A9 | 2026-11-26 | L-F24: `.gitattributes` thêm `-text -working-tree-encoding` cho 6 file bằng chứng lịch sử. | PR #118 → `7ec7fd9` |
| A10 | 2026-11-26 | L-F58: xóa 3 file `P6D/` khỏi repo; `.gitignore` thêm `P6D/`. | PR #119 → `f4de9f1` |
| A11 | 2026-11-26 | F49: các phiên Grok làm WORKER cho TK-0063, 0064, 0065, 0066 có 0 dòng 9Router; run ghi "model CHƯA XÁC MINH". | `02_work/runs/TK-0063…TK-0066_R1_DONE.md` (`deviations.differences`) |
| A12 | 2026-11-26 | Lệnh gate chuẩn từ #117: `python <checkout origin/main>/tools/gate.py … --run-verify --run-tools-tests`. Hit quét kế thừa không cần miễn tay. | PR #117; `tools/gate.py` v5 (sha `89520378b496`) |

### B. Quyết định OWNER chốt trong DEC này

| Mã | Nội dung | Trạng thái |
| --- | --- | --- |
| B1 | O3.6 giữ đúng định nghĩa SRC-0003: 9 thẻ (TK-0061, TK-0042…0047, TK-0055, TK-0056) trong **một** PR Planning. Được chia commit để dễ review, không đổi định nghĩa O3.6. | OWNER chốt 2026-11-27 |
| B2 | E4: ACCEPTED. | OWNER chốt 2026-11-27 |
| B3 | E6: ACCEPTED một phần. **Có:** verify chạy trong worktree tạm của head, bằng gate lấy từ `origin/main`; một lần chạy chuẩn. Ghi đúng giới hạn: worktree tạm **chỉ tách thư mục checkout, không phải sandbox**; lệnh vẫn chạy với quyền, file hệ thống và mạng của tiến trình. **Hoãn:** lưu bản ghi thô kèm hash; cách ly đầy đủ (mở RSK). Việc lưu bản ghi thô chỉ thành task sau khi có thiết kế riêng (nơi lưu, xử lý secret, quyền đọc, test) được OWNER duyệt; **không** vào đường găng O3.6. | OWNER chốt 2026-11-27 |
| B4 | E9: ACCEPTED một phần. **Áp dụng:** UTF-8 không BOM; LF cho file khung tự viết; cấm `Out-File` của PowerShell 5.1 (DEC-0035 B); công cụ mới cài qua pip; binary theo E24; detect-secrets gọi từ `tools/hooks` (qua TK-0045, TK-0056, O3.4). **Chưa áp dụng:** `-text` cho toàn bộ `03_output/**/checks/` (chỉ 6 file lịch sử có, #118), hoãn cùng E22. Kiểm mã hóa (gate G4) **không** thay thế việc giữ nguyên byte. | OWNER chốt 2026-11-27 |
| B5 | Q13: YES, C9 đặt ở cuối Bước 3 (TK-0047), với 4 điều kiện cho thẻ TK-0047. (1) Task đã đóng (DONE/CANCELLED trong neo `TASKS` của file chu kỳ) không bị chấm theo trạng thái DEC hiện tại. (2) Task đã đóng chỉ đổi tên nguyên byte (blob không đổi) thì kiểm tự động theo trạng thái DEC tại ngày lập task. (3) Task đã đóng có thay đổi nội dung, hoặc thứ tự sự kiện không xác định được (cùng ngày, thiếu ngày), thì C9 báo **CẦN KIỂM TRA**, không tự PASS. (4) `PLAN.md` `based_on` kiểm theo LEAD luật 21: mọi DEC phải ACTIVE. | OWNER chốt 2026-11-27 |
| B6 | PLAN `based_on`: thay DEC-0018 bằng DEC-0033; bỏ DEC-0007, DEC-0028, DEC-0029 (RETIRED, không có DEC thay thế, phạm vi CYC-01/CYC-03 đã xong); thêm DEC-0036; PLAN nhận version 12. Không thêm DEC-0032, DEC-0035. | OWNER chốt 2026-11-27 |
| B7 | Không dùng Grok cho vai nào trong các bước tiếp theo, tới khi có bằng chứng log liên kết được phiên. | OWNER chốt 2026-11-27 |
| B8 | Phân vai: thử tuyến Luna và Gemini bằng lượt có gọi công cụ; xác minh model thực tế và khác họ; sau đó chọn một bên làm, một bên review. Chưa đủ bằng chứng thì dừng ở bước phân vai và trình OWNER; không tự hạ chuẩn. | OWNER chốt 2026-11-27 |
| B9 | Review: REVIEWER kiểm toàn bộ thay đổi thực chất. Lỗi ảnh hưởng tính đúng, phạm vi hoặc an toàn phải báo và xử lý, kể cả khi nằm ngoài checklist; PR chưa merge cho tới khi OWNER quyết. Lỗi trình bày ghi WARN. OWNER quyết định merge. | OWNER chốt 2026-11-27 |
| B10 | STATE ghi "base đã kiểm @ <sha12>", không ghi SHA merge của chính PR. | OWNER chốt 2026-11-27 |
| B11 | Ngoại lệ B8 cho riêng PR-A: WORKER là Terra (`cx/gpt-6.1-terra`, `group` chưa xác minh), REVIEWER là Luna; không thử tuyến trước. Nội dung do Claude 2 soạn, Terra chỉ chép nguyên văn theo sha256 và gate kiểm. Model của WORKER và REVIEWER ghi theo mức bằng chứng thực có (B/C/D), không ghi "đã xác minh" nếu chưa đạt mức B. Có thể Terra và Luna cùng họ `gpt`: OWNER chấp nhận cho PR này. Từ O3.6, B8 áp đầy đủ. | OWNER chốt 2026-11-27 |

### C. Câu hỏi mở (không quyết trong DEC này)
- C1. Hợp đồng hook, shebang, CRLF, exit, commit/push của DEC-0028 (DEC-0029 ghi "vẫn giữ") hiện chỉ còn sống qua code và test của TK-0032/0034/0035, vì DEC-0028 đã RETIRED. Có cần một DEC ACTIVE làm căn cứ không? Chờ OWNER.
- C2. Mức bằng chứng model tối thiểu để vòng review được tính (mức B/C), và cột của bảng `usageHistory` trong 9Router. Chờ OWNER.
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
- DEC-0035 giữ ACTIVE; DEC này ghi tiếp, không thay.
- SRC-0003 thêm dòng delta và đồ thị cho B3p5/TK-0066; `B3a0` đổi `after: B3p4, O3.6` thành `after: B3p5, O3.6`.
- PLAN `based_on` theo B6 khi B6 được chốt.
- O3.6 (P3b) bắt đầu sau khi DEC này merge, và sau khi B2–B5 được chốt.
<!-- END: CONSEQUENCES -->
