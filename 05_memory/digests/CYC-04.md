---
schema: 1
cycle: CYC-04
date: 2026-11-20
keywords: [model-catalog, model-matrix, model-select, assign-audit, route-identity, 9router, max-loops]
---
<!-- ANCHOR: RESULTS -->
## Results
- TK-0009 | DONE R3 | Kiểm catalog và ma trận; R1 và R2 BLOCKED vì ghi chú và token pending; R3 L01 đạt 20 test và baseline 23
- TK-0010 | DONE R1 | Chọn model đủ điều kiện; L01 đạt 12 test và baseline 23
- TK-0019 | DONE R2 | Đối chiếu model yêu cầu và thực tế; R1 BLOCKED sau 3 vòng FAIL; R2 L01 đạt 24 test và baseline 23
- TK-0029 | DONE R1 | Hồi quy tuyến và model thực tế; L01 đạt 4 test và baseline 23
<!-- END: RESULTS -->
<!-- ANCHOR: DECISIONS -->
## Decisions
- DEC-0018 | REVIEWER khác model thực tế của WORKER
- DEC-0021 | Phân biệt tuyến 9Router và model thực tế
- DEC-0017 | Phân công model của CYC-04 theo khung 1.0.2
<!-- END: DECISIONS -->
<!-- ANCHOR: RISKS -->
## Risks carried over
- RSK-0004 | Tác tử có shell trên máy OWNER có thể tự đẩy thẻ hoặc merge; mức HIGH, hạn 2026-11-26
- RSK-0001 | Ngân hàng câu hỏi thật có thể chứa tên học viên; hạn 2026-11-26
- RSK-0005 | Rủi ro trung bình, hạn 2026-12-12, owner LEAD
- RSK-0006 | Rủi ro trung bình, hạn 2026-12-12, owner LEAD
<!-- END: RISKS -->
<!-- ANCHOR: LESSONS -->
## Lessons
- Ghi chú ROUTE_CHECKS dài hơn 15 từ và match ngoài yes, no, pending làm catalog hoặc ma trận thật không đạt
- Run đủ 3 vòng FAIL phải BLOCKED; vòng thứ tư không được tính trong cùng run
- verify_default vẫn là 23 test vì pytest.ini chỉ thu thập tests/
- Reviewer gemini-3.8-flash-n khác worker grok-4.7; tuyến ag/gemini-3.8-flash-high đi qua 9router
- Câu 7 của cổng giữ CONDITIONAL vì RSK-0004 và tài khoản GitHub dùng chung
<!-- END: LESSONS -->
