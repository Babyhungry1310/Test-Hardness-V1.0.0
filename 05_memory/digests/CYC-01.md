---
schema: 1
cycle: CYC-01
date: 2026-11-13
keywords: [quiz-bank, duplicate-id, loader, pytest, test-collection, model-assignment]
---
<!-- ANCHOR: RESULTS -->
## Results
- TK-0001 | DONE R2 | R1 BLOCKED vì ràng buộc hoa thường trái done_when; DEC-0004 sửa task, R2 đạt ở L01 với 8 test
- TK-0002 | DONE R1 | Viết test trước nên L01 FAIL, L02 đạt 5 test; data/bank.json có 5 câu Q-001 tới Q-005
- TK-0004 | DONE R1 | Thêm pytest.ini với testpaths = tests; pytest toàn repo đạt 13 test ở L01
<!-- END: RESULTS -->
<!-- ANCHOR: DECISIONS -->
## Decisions
- DEC-0002 | Lưu ngân hàng câu hỏi dạng JSON và xuất handout Markdown; thay DEC-0001
- DEC-0004 | So khớp id câu hỏi không phân biệt hoa thường, id trả về giữ dạng gốc ở lần xuất hiện đầu
- DEC-0006 | Giới hạn pytest về tests/ bằng pytest.ini; pytest.ini thuộc product_paths
- DEC-0007 | WORKER dùng Codex, REVIEWER dùng Claude; thay DEC-0003, DEC-0005 thành RETIRED
- DEC-0008 | Kiểm định vòng 3 chạy Claude Code trực tiếp vì 9Router không có tuyến Claude
<!-- END: DECISIONS -->
<!-- ANCHOR: RISKS -->
## Risks carried over
- RSK-0001 | Ngân hàng câu hỏi thật có thể chứa tên học viên; hạn 2026-11-26
<!-- END: RISKS -->
<!-- ANCHOR: LESSONS -->
## Lessons
- verify của từng task chỉ chạy file test riêng nên không bắt được lỗi tích hợp; LEAD phải chạy verify_default trên main sau mỗi lượt merge run
- Chỉ giao kiểm định khi mọi run đã vào main và CYC-nn.md, STATE.md đã đồng bộ; vòng 1 chạy sớm nên mất một trong ba vòng
- Model của REVIEWER phải được xác nhận chạy được trước khi ghi DEC phân công; vòng 1 rơi vào model ảnh, DEC-0007 ghi sai là Claude có trên 9Router
- File test mẫu trong harness/templates/examples/ trùng tên với test sản phẩm và bị pytest thu thập; cần sửa ở khung
- Mã task trong PLAN.md là mã đã cấp; task sửa phát sinh lấy mã kế tiếp sau mã lớn nhất của cả plan và thư mục tasks
- done_when có so khớp chuỗi phải nêu rõ có phân biệt hoa thường hay không
<!-- END: LESSONS -->
