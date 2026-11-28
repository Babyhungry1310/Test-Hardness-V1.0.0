---
schema: 1
id: DEC-0043
date: "2026-11-28"
title: "Soát thẻ: mỗi done_when có phép kiểm đối chiếu được trước khi giao"
proposed_by: LEAD
decided_by: OWNER
cycle: CYC-08
origin: "DEC-0041#CONTEXT"
supersedes: ""
cancels: []
waives: []
affects: ["02_work/tasks", "06_sources/SRC-0003_kaizen-chi-tiet-dot1.md"]
keywords: [quy-trinh, verify, done-when, soat-the]
---
## Status (newest first)
- 2026-11-28 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
TK-0043 R1: L01, L02 PASS (11 test) nhưng audit thấy C1–C3, E20, E40, SAME_MODEL chưa có test. Lệnh verify của thẻ (pytest chung + validate trên main) không chứng minh từng done_when. R2 lặp lại: L04 PASS, Luna review vòng 1 FAIL vì E40 thiếu ca test.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
Giữ cách soạn thẻ hiện tại; hoặc yêu cầu ánh xạ done_when sang phép kiểm và soát thẻ độc lập trước khi giao. Chọn cách sau.
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
V1 (LEAD, soạn thẻ): mỗi done_when ánh xạ tới ít nhất một test hoặc lệnh kiểm có kết quả đối chiếu được, do lệnh verify thực sự chạy; ghi một phần tử constraints dạng "done_when n → <test hoặc lệnh>" (hợp task.schema.json hiện tại). Tiêu chí hành vi có ít nhất một ca dương và một ca âm. Thẻ thiếu ánh xạ thì không giao.
V2 (LEAD, trước khi giao): một model khác người soạn soát thẻ theo V1, kiểm ba việc: n trỏ đúng tiêu chí; phép kiểm nằm trong lệnh verify; kết quả kiểm đúng hành vi (không chỉ exit code). Ghi kết quả vào phiếu giao.
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
Hiệu lực: V1, V2 áp dụng cho các thẻ giao sau ngày quyết định (TK-0044 trở đi); không áp ngược cho TK-0043 R2, đã có DEC-0042. Không sửa harness/rules trong DEC này. Hai điểm đã bàn chưa thuộc quyết định: V3 (verify và review là hai sự kiện riêng; lần chạy verify sau finding tiêu thụ một loop) và V4 (PR nháp đến khi DONE; tiếp tục cùng run khi BLOCKED) đưa vào bản sửa LEAD.md, WORKER.md sau khi TK-0043 khép, cần lệnh OWNER 🔒; V5 (ghi nhận LEAD đi cùng PR task) để sau.
<!-- END: CONSEQUENCES -->
