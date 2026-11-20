---
schema: 1
cycle: CYC-06
date: 2026-11-20
keywords: [scan, base64, quarantine, EXTERNAL_DATA, adversarial, gpt-5.6-luna]
---
<!-- ANCHOR: RESULTS -->
## Results
- TK-0013 | DONE R1 | Lõi scan; L01 FAIL 13 đạt 1 lỗi; L02 đạt 17 test và baseline 23; worker grok-4.7
- TK-0014 | DONE R1 | Base64 và hạn; L01 đạt 28 test và baseline 23; worker gemini; DEC-0030 trước đó
- TK-0022 | DONE R1 | Cách ly và thẻ EXTERNAL_DATA; L01 đạt 16 test và baseline 23; worker gemini
- TK-0023 | DONE R1 | Test phản biện 23 ca và bằng chứng giới hạn; baseline 23; worker gemini
<!-- END: RESULTS -->
<!-- ANCHOR: DECISIONS -->
## Decisions
- DEC-0030 | Cập nhật test_scan_core trước khi TK-0014 giải mã base64
- DEC-0018 | REVIEWER khác model thực tế của WORKER
- DEC-0019 | OWNER và tác tử dùng chung tài khoản GitHub
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
- Batch B1 lõi scan, B2 song song limits và quarantine, B3 adversarial sau khi cả B2 trên main
- verify_default vẫn 23 test vì pytest.ini chỉ thu thập tests/; bộ scan riêng đạt nhiều hơn
- Reviewer gpt-5.6-luna khác worker grok-4.7 và gemini-3.8-flash-high
- DEC-0030 cần thiết vì assertion TK-0013 xung đột với giải mã base64 của TK-0014
- Câu 7 của cổng giữ CONDITIONAL vì RSK-0004 và tài khoản GitHub dùng chung
- Thẻ cycle/CYC-03, cycle/CYC-04 và cycle/CYC-05 vẫn chưa có trên origin
<!-- END: LESSONS -->
