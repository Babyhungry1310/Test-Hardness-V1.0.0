---
schema: 1
id: DEC-0015
date: 2026-11-14
title: "Nâng khung lên V1.0.1: bảo vệ main, ma trận model, chat và storage, dọn nhánh, scanner"
proposed_by: OWNER
decided_by: OWNER
cycle: NONE
origin: "REQ-0003"
supersedes: ""
cancels: []
waives: []
affects: ["harness/HARNESS.md", "harness/MAIN_PROTECTION.md", "harness/MODEL_POLICY.md", "harness/CHAT_UX.md", "harness/GIT_CONVENTIONS.md", "harness/tools/README.md", "harness/tools/PREFLIGHT.md", "harness/rules/LEAD.md", "harness/rules/WORKER.md", "harness/rules/REVIEWER.md", "04_control/MODEL_CATALOG.md", "04_control/MODEL_MATRIX.md", DEC-0011, DEC-0012, RSK-0004]
keywords: [harness-upgrade, main-protection, model-matrix, model-catalog, chat-ux, git-cleanup, scanner, trace-log]
---
## Status (newest first)
- 2026-11-14 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
REQ-0003 yêu cầu cập nhật khung theo tám nhóm, chỉ ở mức thiết kế. Khi soạn, trạng thái repo này là: nhánh `main` chưa có luật bảo vệ và chưa có ruleset; cách merge "merge commit" còn bật; tự xóa nhánh nguồn đang tắt; auto-merge đang tắt; 25 nhánh làm việc cũ còn trên máy chủ; PR của tác tử mở bằng chính tài khoản OWNER (RSK-0004). Khung V1.0.0 không nêu ai đặt thẻ, không có nguồn tra cứu model, và buộc thông điệp cuối chỉ gồm một khối.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- Giữ V1.0.0, xử lý từng điểm bằng DEC riêng của dự án
- Nâng khung lên V1.0.1 trong một PR `upgrade/1.0.1`, chỉ gồm đặc tả và luật, chưa có script
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
Chọn phương án sau. Lượt merge PR `upgrade/1.0.1` của OWNER là chữ ký cho quyết định này.

| Nhóm | Thay đổi | Nơi ghi |
|---|---|---|
| 1. Bảo vệ `main` | Tác tử không commit trên `main`, không đẩy, không merge, không bật auto-merge, không đụng thẻ; đọc `main` thì được. Luật bảo vệ nhánh phía GitHub là lớp chính; hook cục bộ, pre-flight gate và chỉ dẫn chỉ chống nhầm | `harness/MAIN_PROTECTION.md`; `harness/HARNESS.md` mục 10.1; ba file luật; ba file định tuyến; `PREFLIGHT.md` dòng 16 |
| 2. Ma trận model | Nguồn tra cứu phân công và fallback theo bốn vai; tier theo mã model cụ thể do OWNER duyệt; `DISCUSS` bắt buộc `T1`; hết model hợp lệ thì dừng | `harness/MODEL_POLICY.md`; `04_control/MODEL_MATRIX.md` |
| 3. Catalog model | Mã model cụ thể, bí danh, nhà cung cấp, nguồn, ngày cập nhật; không có nguồn thì ghi `unverified` hoặc `none` | `04_control/MODEL_CATALOG.md`; schema và mẫu tương ứng |
| 4. Trace log | Ba phương án A, B, C được giữ mở và so sánh; chưa chọn; định dạng log không đổi | `harness/rfc/RFC-0001_trace-attribution.md` |
| 5–6. Chat và Storage | Chat dạng dọc, có phần `SUMMARY` trước khối kết thúc; storage theo schema; không viết lại file cũ | `harness/CHAT_UX.md`; `harness/HARNESS.md` mục 3.4, 3.6, 8.4; `harness/templates/BLOCKS.md` |
| 7. Git và cleanup | Nhánh kiểm định `review/CYC-nn-Rk-xxxx`; phân tích tự xóa nhánh nguồn; đặc tả `clean` hai bước | `harness/GIT_CONVENTIONS.md` mục 7–10; `harness/tools/README.md#CLEAN` |
| 8. Scanner | `scan` xác định, độc lập, không sửa bản gốc, có giới hạn kích thước và độ sâu giải mã; thẻ `EXTERNAL_DATA` là lớp hỗ trợ | `harness/tools/README.md#SCAN_SPEC`; `harness/HARNESS.md` mục 10.2 |

Quan hệ với quyết định đang có:

- DEC-0011 (thẻ chỉ do OWNER đặt): không đổi; nội dung được đưa vào luật của khung như DEC-0011 đã dự kiến.
- DEC-0012 (CYC-02: WORKER nhóm Codex, REVIEWER nhóm Gemini): không đổi và không bị áp lại. DEC-0012 phân công theo nhóm, còn V1.0.1 yêu cầu mã model cụ thể; điểm lệch này chỉ áp cho phân công mới, và cần một DEC mới của OWNER khi có chu kỳ hay dự án kế tiếp.
- DEC-0014 (bản kiểm định ở PR #20 không tính là một vòng): không đổi. Verdict của RVW-CYC-02 và cổng CYC-02_PASS không đổi vì quy tắc mới.
- DEC-0007, DEC-0008 (phân công CYC-01): không đổi.

Số phiên bản: theo bảng mức nâng cấp ở `harness/HARNESS.md` mục 11, thay đổi thêm cơ chế là mức MINOR. OWNER đặt tên bản là 1.0.1; số này được giữ. Không schema hiện có nào bị đổi; chỉ thêm hai schema cho hai loại file mới.
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
- Chưa có script, hook hay workflow nào được viết; mọi phần mới là đặc tả. Chưa lập plan, chưa tạo task thi công.
- `04_control/MODEL_MATRIX.md` ở `status: PROPOSED`, `tier1` rỗng: theo `harness/MODEL_POLICY.md` mục 6, chưa mở được phiên `DISCUSS` mới cho tới khi OWNER duyệt ít nhất một mã `T1` bằng một DEC.
- RSK-0004 giữ `OPEN`: phần luật của khung đã có, phần luật bảo vệ nhánh và thẻ trên GitHub và tài khoản riêng cho tác tử do OWNER làm.
- Các điểm chờ OWNER quyết: danh sách mã `T1` và việc duyệt ma trận; phương án của RFC-0001; bật luật bảo vệ `main` và thẻ; tự xóa nhánh nguồn; danh sách nhánh cũ được xóa; trường `requested_model` trong schema.
- Bản này được thử trên repo này trước; đưa sang repo khung gốc là một PR `upgrade/1.0.1` riêng ở repo đó, không gồm các file `04_control/` của dự án này.
<!-- END: CONSEQUENCES -->
