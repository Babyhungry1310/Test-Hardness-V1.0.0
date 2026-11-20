---
schema: 1
cycle: CYC-07
date: 2026-11-20
keywords: [batch, pytest, integrate, readme, upstream, regression, gpt-5.6-luna]
---
<!-- ANCHOR: RESULTS -->
## Results
- TK-0015 | DONE R1 | batch_check; L01 đạt 12 test và baseline 23; worker grok-4.7
- TK-0016 | DONE R1 | mẫu pytest.ini; L01 đạt 4 test và baseline 23; worker gemini
- TK-0024 | DONE R1 | pytest_ini_check; L01 đạt 18 test và baseline 23; worker gemini
- TK-0025 | DONE R1 | integrate_check; L01/L02 FAIL, L03 đạt 7 test và baseline 23; worker grok-4.7
- TK-0026 | DONE R1 | tools/README.md; L01 rồi L02 sửa TAB trong đường dẫn; verify tools/tests 338; worker gemini
- TK-0028 | DONE R1 | kiểm kê upstream dry-run 67a092f..tip; baseline 23; worker gemini
- TK-0017 | DONE R1 | hồi quy Windows; 23 + 338; assign_audit exit 2 ghi nhận; worker gemini
<!-- END: RESULTS -->
<!-- ANCHOR: DECISIONS -->
## Decisions
- DEC-0020 | Kiểm kê đầy đủ thay đổi dry run trước khi đề xuất chuyển về repo mẹ
- DEC-0018 | REVIEWER khác model thực tế của WORKER
- DEC-0030 | Cập nhật test_scan_core trước TK-0014 (đã dùng ở CYC-06)
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
- B1 bốn task song song; B2 README; B3 inventory; B4 hồi quy Windows
- verify_default vẫn 23; tools/tests riêng đạt 338
- Reviewer gpt-5.6-luna khác worker grok-4.7 và gemini
- assign_audit còn lỗi front matter thiếu dòng trống sau --- trên một số run cũ
- UPSTREAM_PROPOSALS.md vẫn cần sau cổng CYC-07 và OWNER duyệt trước khi chuyển repo mẹ
- Thẻ cycle/CYC-03 tới cycle/CYC-06 vẫn chưa có trên origin
<!-- END: LESSONS -->
