PHASE: CLOSE
CYCLE: CYC-02
PROFILE: SHORT

## Handover board (updated: 2026-11-14, main @ cc0c4f9)
### 1. Progress
- CYC-01 | PASS | TK-0001 DONE R2, TK-0002 DONE R1, TK-0004 DONE R1 | thẻ cycle/CYC-01 @ e2b7944
- CYC-02 | PASS | TK-0003 DONE R1, TK-0005 DONE R1 | RVW-CYC-02 vòng 1 PASS | chờ OWNER đặt thẻ cycle/CYC-02
### 2. Open risks
- RSK-0004 | OPEN | level: HIGH | due: 2026-11-26 | owner: OWNER
- RSK-0001 | OPEN | level: MEDIUM | due: 2026-11-26 | owner: LEAD
### 3. Recent decisions
- DEC-0014 | ACTIVE | Bản kiểm định CYC-02 do gpt-6.1-sol chạy không tính là một vòng kiểm định
- DEC-0013 | ACTIVE | Handout kết thúc bằng đúng một LF và ghi file với newline LF
- DEC-0012 | ACTIVE | Phân công model CYC-02: WORKER dùng Codex, REVIEWER dùng nhóm Gemini; không gắn cứng Claude
- DEC-0011 | ACTIVE | Thẻ git chỉ do OWNER tạo và đẩy
- DEC-0010 | ACTIVE | Định dạng handout Markdown và giao diện dòng lệnh
- DEC-0008 | ACTIVE | Kiểm định vòng 3 của CYC-01 chạy Claude Code trực tiếp, ngoài 9Router
- DEC-0007 | ACTIVE | Phân công model CYC-01: WORKER dùng Codex, REVIEWER dùng Claude
- DEC-0006 | ACTIVE | Khắc phục thu thập test bằng cách giới hạn pytest về tests/
- DEC-0004 | ACTIVE | So khớp id câu hỏi không phân biệt hoa thường
- DEC-0002 | ACTIVE | Lưu ngân hàng câu hỏi dạng JSON và xuất handout Markdown
- DEC-0009 | SUPERSEDED_BY DEC-0012
- DEC-0005 | RETIRED
- DEC-0003 | SUPERSEDED_BY DEC-0007
- DEC-0001 | SUPERSEDED_BY DEC-0002
### 4. Next action
- OWNER merge PR cổng CYC-02_PASS rồi tự đặt thẻ cycle/CYC-02 tại commit merge theo DEC-0011. PLAN.md không còn chu kỳ nào. Tiếp theo LEAD đóng dự án trong một PR: viết 05_memory/CORE.md (≤ 300 dòng), soạn 04_control/gates/CLOSED.md để OWNER ký bằng lượt merge. Trước đó OWNER quyết cách xử lý RSK-0004 và RSK-0001 (đóng, hoặc ghi rõ phần bàn giao trong CORE.md). Pytest toàn repo trên main cc0c4f9 đạt 23/23.
### 5. Never do
- Không xuất PDF
- Không dùng tên học viên thật trong dữ liệu thử
