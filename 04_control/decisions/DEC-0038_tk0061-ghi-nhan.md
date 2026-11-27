---
schema: 1
id: DEC-0038
date: 2026-11-27
title: "Ghi nhận TK-0061 (B3a0): phân vai, G5, model UNKNOWN, việc sửa công cụ còn treo"
proposed_by: LEAD
decided_by: OWNER
cycle: CYC-08
origin: "DEC-0037#RATIONALE"
supersedes: ""
cancels: []
waives: []
affects: [DEC-0036, DEC-0037, TK-0061, "04_control/STATE.md", "tools/validate_task_schema.py", "tools/gate.py", "tools/usage_9router.py"]
keywords: [tk-0061, ghi-nhan, phan-vai, g5, model-unknown, sua-cong-cu]
---
## Status (newest first)
- 2026-11-27 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
- TK-0061 (B3a0) merge ở PR #122 (merge commit `1e718d9`, head `a3f11df992a8`), base `b26962a2ca93` (#121, O3.6). Base đã kiểm của DEC này: origin/main `1e718d9`.
- DEC-0036 B8 áp đầy đủ từ O3.6; ngoại lệ DEC-0036 B11 và DEC-0037 B7 chỉ áp cho PR-A và P3b. TK-0061 cần quyết định phân vai riêng.
- `harness/MODEL_POLICY.md` mục SAME_MODEL: thiếu nguồn đúng thời điểm thì actual là `UNKNOWN`, "Hỏi OWNER. Không cho qua kiểm độc lập."
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- A (chọn): ghi các quyết định và phát hiện của TK-0061 vào một DEC, kèm nguồn.
- B: để trong phiếu giao việc. Không chọn: trái F57 (quyết định OWNER phải có mã và nằm trong DEC).
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale

### A. Ghi nhận (có nguồn)
| Mã | Nội dung | Nguồn |
| --- | --- | --- |
| A1 | TK-0061 R1 DONE: 3 kiểm ngữ nghĩa (`--base-ref`/ID_MEANING_CHANGED, O_UNKNOWN, GRAPH_CYCLE, GOAL_PATH_OUT_OF_SCOPE) trong `tools/validate_task_schema.py`; CRLF trước `--regex`, BOM, MOJIBAKE trong `tools/verify_doc_artifact.py`; 25 test (21 cũ không sửa + 4 mới). Gate v5 từ main ĐẠT; G11 không có test hỏng mới (kế thừa `test_live_catalog_passes`, F59). | PR #122; `02_work/runs/TK-0061_R1_DONE.md`; `03_output/CYC-08/checks/TK-0061_R1_L01_verify.txt` |
| A2 | OWNER cung cấp tóm tắt kiểm ngược PR #122 của Claude 2; chưa đối chiếu được báo cáo gốc. Luna tái lập độc lập trên head `a3f11df992a8`: validator bắt đường dẫn ngoài write_scope, `O9.9`, vòng đồ thị và đổi goal so với base; file BOM, chuỗi vỡ bị bắt; CRLF và tiếng Việt đúng được kiểm. | `20261127_LUNA_DEC0038_A2_REPRO.md`, sha256 `ec69f7949a1d5f81405088f55bc5e1759e6311972aa015d0c81e7b4621475635` (bằng chứng ngoài repo) |
| A3 | Model WORKER của TK-0061 R1 ghi `UNKNOWN` (không liên kết được nhật ký với phiên): mức D. Model REVIEWER: chưa xác minh. Kiểm độc lập (SAME_MODEL) không tự qua; OWNER quyết theo B1. | File run TK-0061 R1 (`model`, `deviations.differences`); MODEL_POLICY SAME_MODEL |
| A4 | Ba điểm nhỏ của `validate_task_schema.py --base-ref`, không chặn TK-0061: (1) file kế hoạch chưa có trên base thì báo lỗi mã 2, thay vì coi mọi thẻ là mới; (2) tìm gốc repo theo thư mục đang đứng, không theo vị trí file kế hoạch; (3) test CRLF và BOM thiếu ca âm tách riêng. | `tools/validate_task_schema.py` hàm `semantic_findings`; `tools/tests/test_verify_doc_artifact.py` |
| A5 | Việc sửa công cụ còn treo, gom vào một task `tools/` sau Bước 3a: A4; 4 docstring trong `tools/gate.py` (DEC-0037 A3); `tools/usage_9router.py --out` ghi CRLF trên Windows (DEC-0036 phần A, DEC-0037 A3). Thẻ viết ở PR `lead/` riêng khi OWNER duyệt. | DEC-0037 A3; A4 |

### B. Quyết định OWNER
| Mã | Nội dung | Trạng thái |
| --- | --- | --- |
| B1 | D-T61: ngoại lệ DEC-0036 B8 cho TK-0061: Terra làm, Luna review; không thử tuyến trước; model ghi theo mức bằng chứng thực có (A3). OWNER chấp nhận kết quả kiểm độc lập không tự qua (MODEL_POLICY SAME_MODEL). | OWNER chốt 2026-11-27 (merge #122) |
| B2 | D-T61b: chấp nhận đúng 1 hit mới `zone2_email` (mức WARN) trong `tools/tests/test_validate_task_schema.py`: email giả thuộc miền `.invalid` cho Git trong repo tạm của test. Gate chạy với `--accept-scan tools/tests/test_validate_task_schema.py=zone2_email:1`. | OWNER chốt 2026-11-27 |
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
- Từ TK-0042, mỗi task cần quyết định phân vai riêng (thử tuyến theo DEC-0036 B8, hoặc ngoại lệ có mã) trước khi giao.
- Task sửa công cụ ở A5 chưa vào đồ thị; cần OWNER duyệt thẻ.
<!-- END: CONSEQUENCES -->
