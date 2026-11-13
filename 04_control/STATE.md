PHASE: VERIFY
CYCLE: CYC-02
PROFILE: SHORT

## Handover board (updated: 2026-11-13, main @ 7898fc6)
### 1. Progress
- CYC-01 | PASS | TK-0001 DONE R2, TK-0002 DONE R1, TK-0004 DONE R1 | thẻ cycle/CYC-01 @ e2b7944
- CYC-02 | TK-0003 DONE R1 | chờ kiểm định vòng 1
### 2. Open risks
- RSK-0004 | OPEN | level: HIGH | due: 2026-11-26 | owner: OWNER
- RSK-0001 | OPEN | level: MEDIUM | due: 2026-11-26 | owner: LEAD
### 3. Recent decisions
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
- OWNER merge PR chứa DEC-0012, rồi giao kiểm định CYC-02 cho nhóm Gemini theo DEC-0012 trên main mới nhất. PR #20 (RVW-CYC-02, `gpt-6.1-sol`, FAIL) chưa merge và không khớp REVIEWER của DEC-0012: chờ OWNER quyết có tính là một vòng kiểm định hay không. Pytest toàn repo trên main 7898fc6 đạt 19/19. Chưa tạo cổng PASS. Thẻ chỉ do OWNER đặt theo DEC-0011.
### 5. Never do
- Không xuất PDF
- Không dùng tên học viên thật trong dữ liệu thử
