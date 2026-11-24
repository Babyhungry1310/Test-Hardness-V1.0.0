PHASE: BUILD
CYCLE: CYC-08
PROFILE: SHORT

## Handover board (updated: 2026-11-24, main @ 513fe87ed33b)
### 1. Progress
- CYC-01…CYC-07 | PASS | chi tiết theo thẻ cycle và RVW tương ứng
- CYC-08 | BUILD | Kaizen Dot1 | TK-0036 (#92), TK-0037 (#94), TK-0038 (#96), TK-0053 (#97), TK-0057 R2 (#100), TK-0058 (#101), TK-0060 (#102) DONE; L1.1 DONE, O1.5 duyệt; DEC-0033 ACTIVE; PR khuôn DEC-0032 + bản chụp sổ đang mở
### 2. Open risks
- RSK-0004 | OPEN | level: HIGH | due: 2026-11-26 | owner: OWNER | E14=tách; O1.1–O1.4 xong, chờ OWNER đóng
- RSK-0005 | OPEN | level: MEDIUM | due: 2026-12-12 | owner: LEAD
- RSK-0006 | OPEN | level: MEDIUM | due: 2026-12-12 | owner: LEAD
- RSK-0001 | OPEN | level: MEDIUM | due: 2026-11-26 | owner: LEAD
### 3. Recent decisions
- DEC-0033 | ACTIVE | Cửa sổ trước Bước 2: E44 model/review, V-RESP, quy tắc vận hành Đợt 1
- DEC-0032 | ACTIVE | Kaizen Dot1 P6d (E27–E43, Q-A…Q-I, supersedes batch) — ACCEPTED 2026-11-23; kế hoạch hiện hành SRC-0003 P6d (`06_sources/SRC-0003_kaizen-chi-tiet-dot1.md`); origin DSC-20261123-gsd1
- DEC-0031 | ACTIVE | Kaizen Dot1 Bước 0: E14=tách tài khoản; E15 chuyển repo mẹ theo nhóm PROPOSAL; 5 quyết định chặn = ĐỒNG Ý (SRC-0006)
- DEC-0030 | ACTIVE | cập nhật test_scan_core trước TK-0014 giải mã base64
- DEC-0029 | ACTIVE | hủy TK-0033; TK-0033 đã CANCELLED trên main
- DEC-0028 | ACTIVE | TK-0032 nguồn sửa, rồi TK-0018; snapshot/bàn giao theo quyền riêng
- DEC-0026 | ACTIVE | TK-0030 fixes TK-0007; PR38 merged; OWNER confirms Gemini PASS and main recheck
- DEC-0021 | ACTIVE | Phân biệt tuyến 9Router và model thực tế khi so sánh định danh
- DEC-0020 | ACTIVE | Kiểm kê đầy đủ thay đổi dry run trước khi đề xuất chuyển về repo mẹ; E15 (DEC-0031) sửa cách chuyển repo mẹ theo nhóm đã chốt
- DEC-0019 | ACTIVE | Lịch sử dry-run: tài khoản GitHub chung; vận hành Kaizen theo E14=tách (DEC-0031)
- DEC-0018 | SUPERSEDED_BY DEC-0033 | Khung 1.0.2: LEAD chọn model theo từng lần giao việc; REVIEWER khác model thực tế với WORKER của phần được kiểm
- DEC-0017 | ACTIVE | Phân công model của CYC-03 tới CYC-07 theo luật khung 1.0.2: dữ kiện kiểm tuyến 9Router và giới hạn khi chọn
- DEC-0016 | ACTIVE | Thử khung V1.0.1 trên repo này: nguồn chuẩn, nơi đặt code, duyệt ma trận model, ngoại lệ tạo task và nền tích hợp tạm
- DEC-0015 | ACTIVE | Nâng khung lên V1.0.1: bảo vệ main, ma trận model, chat và storage, dọn nhánh, scanner
- Quyết định cũ: DEC-0014, DEC-0013, DEC-0012, DEC-0011, DEC-0010, DEC-0008, DEC-0007, DEC-0006, DEC-0004, DEC-0002 ACTIVE; DEC-0009 SUPERSEDED_BY DEC-0012; DEC-0005 RETIRED. Chi tiết trong sổ gốc.
### 4. Next action
- OWNER merge PR khuôn DEC-0032 + bản chụp sổ phát hiện
- TK-0059 thu hẹp (B1b4): đưa 3 script + 2 test vào `tools/`
- Bước 2: TK-0039 (B2a) → TK-0040 (B2b) → TK-0041 (B2c)
### 5. Never do
- Không xuất PDF; không dùng tên học viên thật trong dữ liệu thử
