PHASE: EXECUTE
CYCLE: CYC-01
PROFILE: SHORT

## Handover board (updated: 2026-11-12, main @ 29aec90)
### 1. Progress
- CYC-01 | đang thi công | TK-0001 BLOCKED R1, TK-0002 ASSIGNED
- CYC-02 | chưa có task | 01_plan/PLAN.md#CYC_02
### 2. Open risks
- RSK-0003 | OPEN | level: LOW | due: 2026-11-19 | owner: LEAD
- RSK-0001 | OPEN | level: MEDIUM | due: 2026-11-26 | owner: LEAD
### 3. Recent decisions
- DEC-0005 | ACTIVE | Giữ phân công DEC-0003 dù run R1 của TK-0001 chạy Gemini
- DEC-0004 | ACTIVE | So khớp id câu hỏi không phân biệt hoa thường
- DEC-0003 | ACTIVE | Phân công model cho WORKER và REVIEWER của CYC-01
- DEC-0002 | ACTIVE | Lưu ngân hàng câu hỏi dạng JSON và xuất handout Markdown
- DEC-0001 | SUPERSEDED_BY DEC-0002
### 4. Next action
- Run TK-0001 lần hai (R2, loop từ L01) theo DEC-0004 và Run TK-0002, cả hai chạy nhóm Codex theo DEC-0003, DEC-0005
### 5. Never do
- Không xuất PDF
- Không dùng tên học viên thật trong dữ liệu thử
