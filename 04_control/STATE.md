PHASE: CLOSE
CYCLE: CYC-02
PROFILE: SHORT

## Handover board (updated: 2026-11-14, main @ 36bafbe)
### 1. Progress
- CYC-01 | PASS | TK-0001 DONE R2, TK-0002 DONE R1, TK-0004 DONE R1 | thẻ cycle/CYC-01 @ e2b7944
- CYC-02 | PASS | TK-0003 DONE R1, TK-0005 DONE R1 | RVW-CYC-02 vòng 1 PASS | thẻ cycle/CYC-02 @ 36bafbe
- Khung | V1.0.1 | DEC-0015 | đặc tả, chưa có script
### 2. Open risks
- RSK-0004 | OPEN | level: HIGH | due: 2026-11-26 | owner: OWNER
- RSK-0001 | OPEN | level: MEDIUM | due: 2026-11-26 | owner: LEAD
### 3. Recent decisions
- DEC-0015 | ACTIVE | Nâng khung lên V1.0.1: bảo vệ main, ma trận model, chat và storage, dọn nhánh, scanner
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
- OWNER merge PR upgrade/1.0.1 rồi thử khung V1.0.1 trên repo này. Việc OWNER cần chốt: mã model T1 và duyệt 04_control/MODEL_MATRIX.md (đang PROPOSED); phương án của harness/rfc/RFC-0001_trace-attribution.md; bật luật bảo vệ main và thẻ cycle/* trên GitHub (main hiện chưa được bảo vệ, RSK-0004); tự xóa nhánh nguồn; danh sách nhánh cũ được dọn. Đóng dự án vẫn còn: LEAD viết 05_memory/CORE.md, soạn 04_control/gates/CLOSED.md; trước đó xử lý RSK-0004 và RSK-0001. Pytest toàn repo trên main 36bafbe đạt 23/23.
### 5. Never do
- Không xuất PDF
- Không dùng tên học viên thật trong dữ liệu thử
