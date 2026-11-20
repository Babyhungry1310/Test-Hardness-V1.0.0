PHASE: EXECUTE
CYCLE: CYC-06
PROFILE: SHORT

## Handover board (updated: 2026-11-20, main @ 1958b19)
### 1. Progress
- CYC-01 | PASS | TK-0001 DONE R2, TK-0002 DONE R1, TK-0004 DONE R1 | thẻ cycle/CYC-01 @ e2b7944
- CYC-02 | PASS | TK-0003 DONE R1, TK-0005 DONE R1 | RVW-CYC-02 vòng 1 PASS | thẻ cycle/CYC-02 @ 36bafbe
- CYC-03 | PASS | TK-0006 R1 DONE, TK-0007 R1 DONE, TK-0008 R4 DONE, TK-0018 R1 DONE, TK-0027 R1 DONE, TK-0030 R1 DONE, TK-0032 R1 DONE, TK-0033 CANCELLED, TK-0034 R1 DONE, TK-0035 R1 DONE | RVW-CYC-03 vòng 1 PASS | chờ OWNER đặt thẻ cycle/CYC-03
- CYC-04 | PASS | TK-0009 R3 DONE, TK-0010 R1 DONE, TK-0019 R2 DONE, TK-0029 R1 DONE | cổng @ f310d9d | chờ OWNER đặt thẻ cycle/CYC-04
- CYC-05 | PASS | TK-0011 R1 DONE, TK-0012 R1 DONE, TK-0020 R1 DONE, TK-0021 R1 DONE | cổng @ 64b3ef2 | chờ OWNER đặt thẻ cycle/CYC-05
- CYC-06 | EXECUTE | TK-0013 R1 DONE @ 1958b19 | TK-0022 PR #71 mở; TK-0014 chờ merge DEC-0030
- CYC-07 | ASSIGNED | TK-0015, TK-0016, TK-0024, TK-0025, TK-0026, TK-0028, TK-0017 | batch, pytest, hồi quy
### 2. Open risks
- RSK-0004 | OPEN | level: HIGH | due: 2026-11-26 | owner: OWNER
- RSK-0005 | OPEN | level: MEDIUM | due: 2026-12-12 | owner: LEAD
- RSK-0006 | OPEN | level: MEDIUM | due: 2026-12-12 | owner: LEAD
- RSK-0001 | OPEN | level: MEDIUM | due: 2026-11-26 | owner: LEAD
### 3. Recent decisions
- DEC-0030 | ACTIVE | cập nhật test_scan_core trước TK-0014 giải mã base64
- DEC-0029 | ACTIVE | hủy TK-0033; TK-0033 đã CANCELLED trên main
- DEC-0028 | ACTIVE | TK-0032 nguồn sửa, rồi TK-0018; snapshot/bàn giao theo quyền riêng
- DEC-0026 | ACTIVE | TK-0030 fixes TK-0007; PR38 merged; OWNER confirms Gemini PASS and main recheck
- DEC-0021 | ACTIVE | Phân biệt tuyến 9Router và model thực tế khi so sánh định danh
- DEC-0020 | ACTIVE | Kiểm kê đầy đủ thay đổi dry run trước khi đề xuất chuyển về repo mẹ
- DEC-0019 | ACTIVE | OWNER và tác tử dùng chung tài khoản GitHub
- DEC-0018 | ACTIVE | Khung 1.0.2: LEAD chọn model theo từng lần giao việc; REVIEWER khác model thực tế với WORKER của phần được kiểm
- DEC-0017 | ACTIVE | Phân công model của CYC-03 tới CYC-07 theo luật khung 1.0.2: dữ kiện kiểm tuyến 9Router và giới hạn khi chọn
- DEC-0016 | ACTIVE | Thử khung V1.0.1 trên repo này: nguồn chuẩn, nơi đặt code, duyệt ma trận model, ngoại lệ tạo task và nền tích hợp tạm
- DEC-0015 | ACTIVE | Nâng khung lên V1.0.1: bảo vệ main, ma trận model, chat và storage, dọn nhánh, scanner
- Quyết định cũ: DEC-0014, DEC-0013, DEC-0012, DEC-0011, DEC-0010, DEC-0008, DEC-0007, DEC-0006, DEC-0004, DEC-0002 ACTIVE; DEC-0009 SUPERSEDED_BY DEC-0012; DEC-0005 RETIRED. Chi tiết trong sổ gốc.
### 4. Next action
- OWNER merge DEC-0030; sau đó LEAD gửi tiếp TK-0014
- OWNER merge PR #71 (TK-0022) khi sẵn sàng; TK-0023 chỉ sau cả B2 trên main
- OWNER vẫn đặt thẻ cycle/CYC-03, cycle/CYC-04 và cycle/CYC-05; LEAD không tạo thẻ
### 5. Never do
- Không xuất PDF; không dùng tên học viên thật trong dữ liệu thử
