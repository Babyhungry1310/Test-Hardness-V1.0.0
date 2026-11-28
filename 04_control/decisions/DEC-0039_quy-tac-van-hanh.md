---
schema: 1
id: DEC-0039
date: 2026-11-27
title: "Quy tắc vận hành Đợt 1: gói bằng chứng, manifest, ngoại lệ bằng chứng model"
proposed_by: LEAD
decided_by: OWNER
cycle: CYC-08
origin: "DEC-0038#CONSEQUENCES"
supersedes: ""
cancels: []
waives: []
affects: [DEC-0033, DEC-0036, DEC-0037, DEC-0038, "harness/MODEL_POLICY.md"]
keywords: [van-hanh, goi-bang-chung, manifest, bang-chung-model, ngoai-le-dot1]
---
## Status (newest first)
- 2026-11-27 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
- Từ PR #120 tới #123, nhiều vòng review kết thúc bằng FAIL hoặc CẦN OWNER mà không phải lỗi nội dung. Năm nguyên nhân gốc (Claude 2 rà lại):
  1. Bằng chứng kiểm của Claude 2 chỉ nằm trong hội thoại, không thành tệp có hash; reviewer không đối chiếu được (PR #121 R2, PR #123 A2).
  2. Gói chép theo hash không có đường cập nhật; sửa hợp lệ vẫn làm R1 FAIL (PR #123).
  3. Tiêu chí review chưa định nghĩa đủ ("FAIL đúng chỗ", cấu hình gate theo loại PR) (PR #121 R6, R7, WARN G7).
  4. Lỗi kỹ thuật của Claude 2 do chưa chạy một bộ kiểm cố định trên bản nháp (đếm từ bằng `wc -w`, C12, verify TK-0061 và F01, email nguyên văn trong DEC, docstring trong `gate.py`).
  5. Bằng chứng model không xác minh được ở mọi PR, nên mọi review đều báo "chưa xác minh" (DEC-0036 C2, DEC-0038 A3).
- Base đã kiểm: origin/main sau khi TK-0042 merge (ghi trong mô tả PR).
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- A (chọn): ghi ba quy tắc vận hành và một ngoại lệ trong Đợt 1; tài liệu hướng dẫn và công cụ kiểm gói để ngoài repo (P6D).
- B: sửa văn luật `harness/rules/REVIEWER.md`. Không chọn: văn luật sửa ở Bước 4 (DEC-0033).
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
| Mã | Nội dung | Trạng thái |
| --- | --- | --- |
| B1 | **Gói bằng chứng.** Mỗi gói Claude 2 phát (zip) kèm tệp `KIEM_CLAUDE2.txt`: lệnh đã chạy, đầu ra, sha256 của từng file trong gói. Reviewer trích bằng chứng theo tên tệp và sha256 đó. Mệnh đề chỉ có trong hội thoại không được dùng làm nguồn trong DEC hay review. | OWNER chốt 2026-11-27 |
| B2 | **Manifest.** Gói chép theo hash có manifest đánh số (bản N, sha256 từng file); mô tả PR ghi số bản manifest. Ai cần sửa nội dung thì dừng, báo người soạn; người soạn phát bản N+1 trước khi review. Review đối chiếu hash với bản manifest mới nhất. | OWNER chốt 2026-11-27 |
| B3 | **Ngoại lệ bằng chứng model trong Đợt 1.** Từ khi DEC này merge tới hết Đợt 1 (Đ5-C): không yêu cầu xác minh model thực tế của WORKER hay REVIEWER; trường `model` ghi để tham khảo; review không báo CẦN OWNER vì model. Vẫn giữ: REVIEWER là tác tử khác người làm. Ngoại lệ thay DEC-0036 B8 (thử tuyến trước khi giao) và thay việc hỏi OWNER theo `harness/MODEL_POLICY.md` mục SAME_MODEL trong phạm vi Đợt 1. Không áp hồi tố; TK-0042 dùng quyết định phân vai riêng (D-T42). | OWNER chốt 2026-11-27 |
| B4 | **Tài liệu và công cụ ngoài repo.** Hướng dẫn review (`P6D/HUONG_DAN_REVIEW.md`) và công cụ kiểm gói (`P6D/tools/kiem_goi.py`) nằm ở thư mục P6D của OWNER, ngoài repo, không phải luật; sửa chúng không cần PR. Phiếu review trỏ tới hướng dẫn theo sha256. | OWNER chốt 2026-11-27 |
| B5 | **Thứ tự:** lượt 1 (DEC này, PR `lead/`), lượt 2 (hướng dẫn review, P6D), lượt 3 (`kiem_goi.py`, P6D), bắt đầu sau khi TK-0042 merge. | OWNER chốt 2026-11-27 |
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
- Từ gói sau DEC này, Claude 2 chạy `kiem_goi.py` (khi có) trên mọi bản nháp và đưa kết quả vào `KIEM_CLAUDE2.txt`.
- Hết Đợt 1, ngoại lệ B3 hết hiệu lực; DEC-0036 B8 và MODEL_POLICY SAME_MODEL áp lại, trừ khi có DEC mới.
<!-- END: CONSEQUENCES -->
