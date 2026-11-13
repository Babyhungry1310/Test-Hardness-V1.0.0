PHASE: EXECUTE
CYCLE: CYC-02
PROFILE: SHORT

## Handover board (updated: 2026-11-13, main @ 663e3f9)
### 1. Progress
- CYC-01 | PASS | TK-0001 DONE R2, TK-0002 DONE R1, TK-0004 DONE R1
- CYC-02 | chưa có task | 01_plan/PLAN.md#CYC_02
### 2. Open risks
- RSK-0001 | OPEN | level: MEDIUM | due: 2026-11-26 | owner: LEAD
### 3. Recent decisions
- DEC-0008 | ACTIVE | Kiểm định vòng 3 của CYC-01 chạy Claude Code trực tiếp, ngoài 9Router
- DEC-0007 | ACTIVE | Phân công model CYC-01: WORKER dùng Codex, REVIEWER dùng Claude
- DEC-0006 | ACTIVE | Khắc phục thu thập test bằng cách giới hạn pytest về tests/
- DEC-0004 | ACTIVE | So khớp id câu hỏi không phân biệt hoa thường
- DEC-0002 | ACTIVE | Lưu ngân hàng câu hỏi dạng JSON và xuất handout Markdown
- DEC-0005 | RETIRED
- DEC-0003 | SUPERSEDED_BY DEC-0007
- DEC-0001 | SUPERSEDED_BY DEC-0002
### 4. Next action
- Đặt thẻ cycle/CYC-01 sau khi OWNER merge cổng PASS. Ghi DEC phân công model cho CYC-02, tạo TK-0003 từ 01_plan/PLAN.md#CYC_02 trong một PR, chờ OWNER merge rồi kích hoạt CYC-02
### 5. Never do
- Không xuất PDF
- Không dùng tên học viên thật trong dữ liệu thử
