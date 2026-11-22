PHASE: BUILD
CYCLE: CYC-08
PROFILE: SHORT

## Handover board (updated: 2026-11-22, main @ df76bbb)
### 1. Progress
- CYC-01 | PASS | TK-0001 DONE R2, TK-0002 DONE R1, TK-0004 DONE R1 | thẻ cycle/CYC-01 @ e2b7944
- CYC-02 | PASS | TK-0003 DONE R1, TK-0005 DONE R1 | RVW-CYC-02 vòng 1 PASS | thẻ cycle/CYC-02 @ 36bafbe
- CYC-03 | PASS | TK-0006 R1 DONE, TK-0007 R1 DONE, TK-0008 R4 DONE, TK-0018 R1 DONE, TK-0027 R1 DONE, TK-0030 R1 DONE, TK-0032 R1 DONE, TK-0033 CANCELLED, TK-0034 R1 DONE, TK-0035 R1 DONE | RVW-CYC-03 vòng 1 PASS | chờ OWNER đặt thẻ cycle/CYC-03
- CYC-04 | PASS | TK-0009 R3 DONE, TK-0010 R1 DONE, TK-0019 R2 DONE, TK-0029 R1 DONE | cổng @ f310d9d | chờ OWNER đặt thẻ cycle/CYC-04
- CYC-05 | PASS | TK-0011 R1 DONE, TK-0012 R1 DONE, TK-0020 R1 DONE, TK-0021 R1 DONE | cổng @ 64b3ef2 | chờ OWNER đặt thẻ cycle/CYC-05
- CYC-06 | PASS | TK-0013 R1 DONE, TK-0014 R1 DONE, TK-0022 R1 DONE, TK-0023 R1 DONE | cổng @ c35fcfd | chờ OWNER đặt thẻ cycle/CYC-06
- CYC-07 | PASS | TK-0015 R1 DONE, TK-0016 R1 DONE, TK-0024 R1 DONE, TK-0025 R1 DONE, TK-0026 R1 DONE, TK-0028 R1 DONE, TK-0017 R1 DONE | RVW-CYC-07 vòng 1 PASS | chờ OWNER đặt thẻ cycle/CYC-07 @ 95a0e46
- CYC-08 | BUILD | Kaizen Dot1 | TK-0036 DONE R2 (#92 @ 2f282ea); activation #93 MERGED @ df76bbb; TK-0037 R1 DONE (DSC+DEC-0031+STATE+RSK-0004; awaiting OWNER merge); PR #37 CLOSED
### 2. Open risks
- RSK-0004 | OPEN | level: HIGH | due: 2026-11-26 | owner: OWNER | E14=tách (agent conchonomoconmeo-AIAIAI; OWNER Babyhungry1310); chờ O1.1–O1.3
- RSK-0005 | OPEN | level: MEDIUM | due: 2026-12-12 | owner: LEAD
- RSK-0006 | OPEN | level: MEDIUM | due: 2026-12-12 | owner: LEAD
- RSK-0001 | OPEN | level: MEDIUM | due: 2026-11-26 | owner: LEAD
### 3. Recent decisions
- DEC-0031 | ACTIVE | Kaizen Dot1 Bước 0: E14=tách tài khoản; E15 chuyển repo mẹ theo nhóm PROPOSAL; 5 quyết định chặn = ĐỒNG Ý (SRC-0006)
- DEC-0030 | ACTIVE | cập nhật test_scan_core trước TK-0014 giải mã base64
- DEC-0029 | ACTIVE | hủy TK-0033; TK-0033 đã CANCELLED trên main
- DEC-0028 | ACTIVE | TK-0032 nguồn sửa, rồi TK-0018; snapshot/bàn giao theo quyền riêng
- DEC-0026 | ACTIVE | TK-0030 fixes TK-0007; PR38 merged; OWNER confirms Gemini PASS and main recheck
- DEC-0021 | ACTIVE | Phân biệt tuyến 9Router và model thực tế khi so sánh định danh
- DEC-0020 | ACTIVE | Kiểm kê đầy đủ thay đổi dry run trước khi đề xuất chuyển về repo mẹ; E15 (DEC-0031) sửa cách chuyển repo mẹ theo nhóm đã chốt
- DEC-0019 | ACTIVE | Lịch sử dry-run: tài khoản GitHub chung; vận hành Kaizen theo E14=tách (DEC-0031)
- DEC-0018 | ACTIVE | Khung 1.0.2: LEAD chọn model theo từng lần giao việc; REVIEWER khác model thực tế với WORKER của phần được kiểm
- DEC-0017 | ACTIVE | Phân công model của CYC-03 tới CYC-07 theo luật khung 1.0.2: dữ kiện kiểm tuyến 9Router và giới hạn khi chọn
- DEC-0016 | ACTIVE | Thử khung V1.0.1 trên repo này: nguồn chuẩn, nơi đặt code, duyệt ma trận model, ngoại lệ tạo task và nền tích hợp tạm
- DEC-0015 | ACTIVE | Nâng khung lên V1.0.1: bảo vệ main, ma trận model, chat và storage, dọn nhánh, scanner
- Quyết định cũ: DEC-0014, DEC-0013, DEC-0012, DEC-0011, DEC-0010, DEC-0008, DEC-0007, DEC-0006, DEC-0004, DEC-0002 ACTIVE; DEC-0009 SUPERSEDED_BY DEC-0012; DEC-0005 RETIRED. Chi tiết trong sổ gốc.
### 4. Next action
- OWNER merge PR TK-0037 (DSC-20261121-kzn1 + DEC-0031 + STATE + RSK-0004) khi REVIEWER PASS
- Sau merge: Bước 1 / O1.1–O1.4 (ruleset, luật thẻ, quyền collaborator agent, secret scanning) rồi TK-0038
- OWNER đặt thẻ cycle/CYC-07 @ 95a0e46 (không chặn CYC-08); không mở PR repo mẹ trước khi chỉ định URL/version
- PR #37 CLOSED (draft, 2026-11-20) — O0.1 xong; không mở lại làm cổng Bước 0
### 5. Never do
- Không xuất PDF; không dùng tên học viên thật trong dữ liệu thử

