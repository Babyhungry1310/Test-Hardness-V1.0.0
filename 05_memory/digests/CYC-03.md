---
schema: 1
cycle: CYC-03
date: 2026-11-20
keywords: [hooks, preflight, pre-merge-commit, session-detector, model-independence, 9router, review-round]
---
<!-- ANCHOR: RESULTS -->
## Results
- TK-0006 | DONE R1 | Hook pre-commit và pre-push; L01 đạt 4 test
- TK-0007 | DONE R1 | Preflight main; L01 lỗi, L02 và L03 đạt 11 test
- TK-0008 | DONE R4 | Hoàn tất phần hook còn lại; L01 đạt 39 test
- TK-0018 | DONE R1 | Test mép và đường vòng; L01 lỗi 3, L02 đạt 134 test
- TK-0027 | DONE R1 | Sửa phần đã chốt của chu kỳ; L01 đạt 18 test
- TK-0030 | DONE R1 | Sửa TK-0007; L01 đạt 62 test công cụ và baseline 23
- TK-0032 | DONE R1 | Hook pre-merge-commit; L01 đạt 3 test và baseline 23
- TK-0033 | CANCELLED | DEC-0029 hủy task; không có run
- TK-0034 | DONE R1 | Detector phiên; L01 lỗi 1, L02 đạt 32 test
- TK-0035 | DONE R1 | Nối detector vào preflight; L01 đạt 45 test và baseline 23
<!-- END: RESULTS -->
<!-- ANCHOR: DECISIONS -->
## Decisions
- DEC-0016 | Nguồn chuẩn, nơi đặt code và ngoại lệ tạo task cho khung V1.0.1
- DEC-0017 | Phân công model CYC-03 tới CYC-07 theo khung 1.0.2
- DEC-0018 | LEAD chọn model từng lần giao; REVIEWER khác model thực tế của WORKER
- DEC-0019 | OWNER và tác tử dùng chung tài khoản GitHub
- DEC-0021 | Phân biệt tuyến 9router và model thực tế
- DEC-0026 | TK-0030 sửa TK-0007
- DEC-0028 | TK-0032 là nguồn sửa, rồi tới TK-0018
- DEC-0029 | Hủy TK-0033; thứ tự TK-0034, TK-0035, rồi TK-0018
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
- Nhật ký Codex qua 9router ghi model được yêu cầu, không ghi model do API trả về; OWNER cho phép dùng chuỗi gpt-5.6-luna trong nhật ký phiên làm reviewer_model
- Gemini không kiểm được CYC-03 vì run TK-0007 dùng gemini-3.8-flash-n, cùng mã gốc với tuyến ag/gemini-3.8-flash
- Route ag/claude-sonnet-5-5 trả HTTP 404 dù catalog còn ghi confirmed
- Run của TK-0018 và TK-0032 vào main sau commit sản phẩm, bằng PR sổ #48
- Câu 7 của cổng giữ CONDITIONAL vì RSK-0004 và tài khoản GitHub dùng chung
<!-- END: LESSONS -->
