PHASE: VERIFY
CYCLE: CYC-01
PROFILE: SHORT

## Handover board (updated: 2026-11-12, main @ 193f2ed)
### 1. Progress
- CYC-01 | TK-0001 DONE R2; TK-0002 DONE R1; TK-0004 DONE R1 | kiểm định vòng 2 FAIL, còn 1 vòng
- CYC-02 | chưa có task | 01_plan/PLAN.md#CYC_02
### 2. Open risks
- RSK-0001 | OPEN | level: MEDIUM | due: 2026-11-26 | owner: LEAD
### 3. Recent decisions
- DEC-0007 | ACTIVE | Phân công model CYC-01: WORKER dùng Codex, REVIEWER dùng Claude
- DEC-0006 | ACTIVE | Khắc phục thu thập test bằng cách giới hạn pytest về tests/
- DEC-0004 | ACTIVE | So khớp id câu hỏi không phân biệt hoa thường
- DEC-0002 | ACTIVE | Lưu ngân hàng câu hỏi dạng JSON và xuất handout Markdown
- DEC-0005 | RETIRED
- DEC-0003 | SUPERSEDED_BY DEC-0007
- DEC-0001 | SUPERSEDED_BY DEC-0002
### 4. Next action
- OWNER merge PR đồng bộ này; giao kiểm định vòng 3 của CYC-01 (nhóm Claude theo DEC-0007) trên main mới nhất. Pytest toàn repo trên main 193f2ed đạt 13/13. Chưa tạo cổng PASS.
### 5. Never do
- Không xuất PDF
- Không dùng tên học viên thật trong dữ liệu thử
