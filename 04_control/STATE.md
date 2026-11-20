PHASE: EXECUTE
CYCLE: CYC-04
PROFILE: SHORT

## Handover board (updated: 2026-11-20, main @ 2c039a3)
### 1. Progress
- CYC-01 | PASS | TK-0001 DONE R2, TK-0002 DONE R1, TK-0004 DONE R1 | thẻ cycle/CYC-01 @ e2b7944
- CYC-02 | PASS | TK-0003 DONE R1, TK-0005 DONE R1 | RVW-CYC-02 vòng 1 PASS | thẻ cycle/CYC-02 @ 36bafbe
- CYC-03 | PASS | TK-0006 R1 DONE, TK-0007 R1 DONE, TK-0008 R4 DONE, TK-0018 R1 DONE, TK-0027 R1 DONE, TK-0030 R1 DONE, TK-0032 R1 DONE, TK-0033 CANCELLED, TK-0034 R1 DONE, TK-0035 R1 DONE | RVW-CYC-03 vòng 1 PASS | cổng @ 2c039a3 | chờ OWNER đặt thẻ cycle/CYC-03
- CYC-04 | EXECUTE | TK-0009 B1 đang làm | TK-0010, TK-0019 chờ B1 | TK-0029 chờ TK-0010 và TK-0019
- CYC-05 | ASSIGNED | TK-0011, TK-0012, TK-0020, TK-0021 | chat, storage, Git, trace
- CYC-06 | ASSIGNED | TK-0013, TK-0014, TK-0022, TK-0023 | scanner
- CYC-07 | ASSIGNED | TK-0015, TK-0016, TK-0024, TK-0025, TK-0026, TK-0028, TK-0017 | batch, pytest, hồi quy
### 2. Open risks
- RSK-0004 | OPEN | level: HIGH | due: 2026-11-26 | owner: OWNER
- RSK-0005 | OPEN | level: MEDIUM | due: 2026-12-12 | owner: LEAD
- RSK-0006 | OPEN | level: MEDIUM | due: 2026-12-12 | owner: LEAD
- RSK-0001 | OPEN | level: MEDIUM | due: 2026-11-26 | owner: LEAD
### 3. Recent decisions
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
- Làm TK-0009 trên task/TK-0009-R1; batch B2 gồm TK-0010 và TK-0019 chỉ bắt đầu sau khi PR TK-0009 đã merge và verify_default trên main đạt
- OWNER vẫn đặt thẻ cycle/CYC-03; LEAD không tạo thẻ
### 5. Never do
- Không xuất PDF; không dùng tên học viên thật trong dữ liệu thử
