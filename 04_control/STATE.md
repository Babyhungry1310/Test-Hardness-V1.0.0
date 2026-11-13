PHASE: EXECUTE
CYCLE: CYC-02
PROFILE: SHORT

## Handover board (updated: 2026-11-13, main @ e2b7944)
### 1. Progress
- CYC-01 | PASS | TK-0001 DONE R2, TK-0002 DONE R1, TK-0004 DONE R1 | thẻ cycle/CYC-01 @ e2b7944
- CYC-02 | chờ kích hoạt | TK-0003 ASSIGNED
### 2. Open risks
- RSK-0004 | OPEN | level: HIGH | due: 2026-11-26 | owner: OWNER
- RSK-0001 | OPEN | level: MEDIUM | due: 2026-11-26 | owner: LEAD
### 3. Recent decisions
- DEC-0011 | ACTIVE | Thẻ git chỉ do OWNER tạo và đẩy
- DEC-0010 | ACTIVE | Định dạng handout Markdown và giao diện dòng lệnh
- DEC-0009 | ACTIVE | Phân công model CYC-02: WORKER dùng Codex, REVIEWER dùng Claude Code trực tiếp
- DEC-0008 | ACTIVE | Kiểm định vòng 3 của CYC-01 chạy Claude Code trực tiếp, ngoài 9Router
- DEC-0007 | ACTIVE | Phân công model CYC-01: WORKER dùng Codex, REVIEWER dùng Claude
- DEC-0006 | ACTIVE | Khắc phục thu thập test bằng cách giới hạn pytest về tests/
- DEC-0004 | ACTIVE | So khớp id câu hỏi không phân biệt hoa thường
- DEC-0002 | ACTIVE | Lưu ngân hàng câu hỏi dạng JSON và xuất handout Markdown
- DEC-0005 | RETIRED
- DEC-0003 | SUPERSEDED_BY DEC-0007
- DEC-0001 | SUPERSEDED_BY DEC-0002
### 4. Next action
- OWNER merge PR mở CYC-02 rồi Run TK-0003 (nhóm Codex, R1). Sau khi merge run: LEAD chạy pytest toàn repo trên main, đồng bộ CYC-02.md và STATE.md, rồi mới giao kiểm định (Claude Code). Thẻ chỉ do OWNER đặt theo DEC-0011.
### 5. Never do
- Không xuất PDF
- Không dùng tên học viên thật trong dữ liệu thử
