---
schema: 1
cycle: CYC-02
date: 2026-11-14
keywords: [handout, markdown, cli, newline, lf, crlf, model-assignment, review-round, git-tag]
---
<!-- ANCHOR: RESULTS -->
## Results
- TK-0003 | DONE R1 | src/handout.py có build_handout và CLI với mã thoát 0 / 1 / 2 theo DEC-0010; đạt ở L01 với 19 test
- TK-0005 | DONE R1 | Sửa TK-0003: handout kết thúc bằng đúng một LF, mở file đầu ra với newline LF; đạt ở L01 với 23 test, có bằng chứng thử đột biến
<!-- END: RESULTS -->
<!-- ANCHOR: DECISIONS -->
## Decisions
- DEC-0009 | WORKER dùng Codex, REVIEWER dùng Claude Code trực tiếp; bị DEC-0012 thay trong cùng chu kỳ
- DEC-0010 | Handout mỗi câu một mục, đáp án in ngay dưới câu hỏi; cách gọi dòng lệnh và mã thoát 0 / 1 / 2
- DEC-0011 | Thẻ git chỉ do OWNER tạo và đẩy; mọi tác tử không đụng tới thẻ
- DEC-0012 | WORKER dùng Codex, REVIEWER dùng nhóm Gemini; không gắn cứng Claude; thay DEC-0009
- DEC-0013 | File handout kết thúc bằng đúng một LF và ghi với newline LF; bổ sung DEC-0010
- DEC-0014 | Bản kiểm định do gpt-6.1-sol chạy ở PR #20 không tính là một vòng; PR đóng, không merge
<!-- END: DECISIONS -->
<!-- ANCHOR: RISKS -->
## Risks carried over
- RSK-0001 | Ngân hàng câu hỏi thật có thể chứa tên học viên; hạn 2026-11-26; chuyển sang phase CLOSE
- RSK-0004 | Tác tử có shell trên máy OWNER có thể tự đẩy thẻ hoặc merge; mức HIGH, hạn 2026-11-26; chuyển sang phase CLOSE
<!-- END: RISKS -->
<!-- ANCHOR: LESSONS -->
## Lessons
- Trước khi giao kiểm định phải đối chiếu nhóm model của REVIEWER với trường model của mọi run; PR #20 dùng model cùng nhóm Codex với WORKER nên bị loại
- Bản kiểm định bị loại về thủ tục vẫn có thể nêu lỗi thật của sản phẩm; xử lý lỗi bằng DEC và task có fixes, tách khỏi việc tính vòng
- DEC mô tả định dạng file phải nêu rõ ký tự xuống dòng, hành vi ở cuối file và hệ điều hành; DEC-0010 để hai yêu cầu mâu thuẫn nhau tới khi kiểm định mới lộ
- Test về xuống dòng phải đọc file ở dạng byte; đọc ở chế độ văn bản che mất CRLF trên Windows
- done_when dạng "có test thất bại nếu bỏ X" cần bằng chứng thử đột biến lưu trong checks, không chỉ dựa vào test đạt
- Phân công model nên ghi theo nhóm và điều kiện độc lập, không gắn cứng một model; DEC-0009 phải thay sau một ngày
- Khung chưa nêu ai đặt thẻ cycle; DEC-0011 và RSK-0004 cần đưa vào bản khung sau
- Giao kiểm định sau khi mọi run và bản đồng bộ đã vào main giúp CYC-02 đạt ngay ở vòng 1
<!-- END: LESSONS -->
