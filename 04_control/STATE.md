PHASE: BUILD
CYCLE: CYC-08
PROFILE: SHORT

## Handover board (updated: 2026-11-27, base đã kiểm @ 01eb881010bb)
### 1. Progress
- CYC-01…CYC-07 | PASS | chi tiết theo thẻ cycle và RVW tương ứng
- CYC-08 | BUILD | Kaizen Đợt 1 | Bước 1, Bước 2 DONE; cửa sổ trước Bước 3 DONE: TK-0062…TK-0066, F24, F58 (#111–#119); ghi nhận ở DEC-0036
### 2. Open risks
- RSK-0004 | OPEN | HIGH | owner: OWNER | E14=tách; chờ đóng
- RSK-0005 | OPEN | MEDIUM | owner: LEAD
- RSK-0006 | OPEN | MEDIUM | owner: LEAD
- RSK-0001 | OPEN | MEDIUM | owner: LEAD
### 3. Recent decisions
- DEC-0037 | ACTIVE | O3.6: thẻ Bước 3; chốt E5/E7/E16/E18; nguồn TK-0056
- DEC-0036 | ACTIVE | Ghi nhận cửa sổ trước Bước 3; chuẩn bị O3.6
- DEC-0035 | ACTIVE | Ngoại lệ gate G1 tạm thời (đã hết khi TK-0064 merge)
- DEC-0033 | ACTIVE | E44 model/review, V-RESP, vận hành Đợt 1
- DEC-0032 | ACTIVE | P6d; SRC-0003
- DEC-0031 | ACTIVE | E14=tách; E15 chuyển repo mẹ
- Danh sách DEC ACTIVE đầy đủ: `04_control/decisions/`.
### 4. Next action
- O3.6 (PR thẻ Bước 3, 9 thẻ) chờ OWNER merge; sau đó TK-0061 (task/).
- Task sửa harness/ (TK-0042, TK-0055, TK-0046) và TK-0045 (.github/, O3.1) cần lệnh OWNER 🔒 trước khi mở PR.
- Chuỗi Bước 3–5: TK-0061 → TK-0042 → TK-0055 → TK-0043 → TK-0044 → TK-0045 → TK-0056 → TK-0046 → TK-0047 → Bước 4, 5; đồ thị SRC-0003 mục 2
- Câu mở DEC-0036 C1, C2: chờ OWNER
- Gate chuẩn: tools/gate.py v5 từ checkout origin/main, với --run-verify --run-tools-tests
### 5. Never do
- Không xuất PDF; không dùng tên học viên thật trong dữ liệu thử
