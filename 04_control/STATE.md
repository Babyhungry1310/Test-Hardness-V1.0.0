PHASE: BUILD
CYCLE: CYC-08
PROFILE: SHORT

## Handover board (updated: 2026-11-27, base đã kiểm @ f4de9f1e90ac)
### 1. Progress
- CYC-01…CYC-07 | PASS | chi tiết theo thẻ cycle và RVW tương ứng
- CYC-08 | BUILD | Kaizen Đợt 1 | Bước 1, Bước 2 DONE; cửa sổ trước Bước 3 DONE: TK-0062…TK-0066, F24, F58 (#111–#119); ghi nhận ở DEC-0036
### 2. Open risks
- RSK-0004 | OPEN | HIGH | owner: OWNER | E14=tách; chờ đóng
- RSK-0005 | OPEN | MEDIUM | owner: LEAD
- RSK-0006 | OPEN | MEDIUM | owner: LEAD
- RSK-0001 | OPEN | MEDIUM | owner: LEAD
### 3. Recent decisions
- DEC-0036 | ACTIVE | Ghi nhận cửa sổ trước Bước 3; chuẩn bị O3.6
- DEC-0035 | ACTIVE | Ngoại lệ gate G1 tạm thời (đã hết khi TK-0064 merge)
- DEC-0033 | ACTIVE | E44 model/review, V-RESP, vận hành Đợt 1
- DEC-0032 | ACTIVE | P6d; SRC-0003
- DEC-0031 | ACTIVE | E14=tách; E15 chuyển repo mẹ
- DEC-0030 | ACTIVE | cập nhật test_scan_core trước TK-0014 giải mã base64
- DEC-0026 | ACTIVE | TK-0030 fixes TK-0007
- DEC-0021 | ACTIVE | Phân biệt tuyến và model thực tế
- DEC-0019 | ACTIVE | Vận hành Kaizen theo E14
- Danh sách DEC ACTIVE đầy đủ: `04_control/decisions/`.
### 4. Next action
- Chờ OWNER: phân vai (thử tuyến Luna, Gemini); câu mở C1, C2 của DEC-0036.
- O3.6 (PR thẻ Bước 3, 9 thẻ) → B3a0 TK-0061 → B3a TK-0042 → B3a2 TK-0055 → B3b → B3c → B3d → B3d2 → B3e → B3f → B4a → B4b → B4c → B5a → B5b → Đ5-C; đồ thị tại SRC-0003
- Gate chuẩn: `tools/gate.py` v5 từ checkout `origin/main`, với `--run-verify --run-tools-tests`
### 5. Never do
- Không xuất PDF; không dùng tên học viên thật trong dữ liệu thử
