PHASE: EXECUTE
CYCLE: CYC-01
PROFILE: SHORT

## Handover board (updated: 2026-11-12, main @ ff86180)
### 1. Progress
- CYC-01 | TK-0001 DONE R2; TK-0002 DONE R1; TK-0003 ASSIGNED | kiểm định vòng 2 FAIL
- CYC-02 | chưa có task | 01_plan/PLAN.md#CYC_02
### 2. Open risks
- RSK-0003 | OPEN | level: LOW | due: 2026-11-19 | owner: LEAD
- RSK-0001 | OPEN | level: MEDIUM | due: 2026-11-26 | owner: LEAD
### 3. Recent decisions
- DEC-0006 | ACTIVE | Sửa namespace test bằng TK-0003; chưa đủ điều kiện đóng CYC-01
- DEC-0005 | ACTIVE | Giữ phân công DEC-0003 dù run R1 của TK-0001 chạy Gemini
- DEC-0004 | ACTIVE | So khớp id câu hỏi không phân biệt hoa thường
- DEC-0003 | ACTIVE | Phân công model cho WORKER và REVIEWER của CYC-01
- DEC-0002 | ACTIVE | Lưu ngân hàng câu hỏi dạng JSON và xuất handout Markdown
- DEC-0001 | SUPERSEDED_BY DEC-0002
### 4. Next action
- OWNER merge task TK-0003, giao Codex chạy; merge run sửa rồi kiểm định vòng 3 trên main. Chưa tạo cổng PASS.
### 5. Never do
- Không xuất PDF
- Không dùng tên học viên thật trong dữ liệu thử
