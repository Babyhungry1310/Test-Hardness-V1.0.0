PHASE: EXECUTE
CYCLE: CYC-03
PROFILE: SHORT

## Handover board (updated: 2026-11-14, main @ 67a092f)
### 1. Progress
- CYC-01 | PASS | TK-0001 DONE R2, TK-0002 DONE R1, TK-0004 DONE R1 | thẻ cycle/CYC-01 @ e2b7944
- CYC-02 | PASS | TK-0003 DONE R1, TK-0005 DONE R1 | RVW-CYC-02 vòng 1 PASS | thẻ cycle/CYC-02 @ 36bafbe
- CYC-03 | ASSIGNED | TK-0006, TK-0007, TK-0008, TK-0018, TK-0027 | bảo vệ main
- CYC-04 | ASSIGNED | TK-0009, TK-0010, TK-0019 | model
- CYC-05 | ASSIGNED | TK-0011, TK-0012, TK-0020, TK-0021 | chat, storage, Git, trace
- CYC-06 | ASSIGNED | TK-0013, TK-0014, TK-0022, TK-0023 | scanner
- CYC-07 | ASSIGNED | TK-0015, TK-0016, TK-0024, TK-0025, TK-0026, TK-0028, TK-0017 | batch, pytest, hồi quy
### 2. Open risks
- RSK-0004 | OPEN | level: HIGH | due: 2026-11-26 | owner: OWNER
- RSK-0005 | OPEN | level: MEDIUM | due: 2026-12-12 | owner: LEAD
- RSK-0006 | OPEN | level: MEDIUM | due: 2026-12-12 | owner: LEAD
- RSK-0001 | OPEN | level: MEDIUM | due: 2026-11-26 | owner: LEAD
### 3. Recent decisions
- DEC-0020 | ACTIVE | Kiểm kê đầy đủ thay đổi dry run trước khi đề xuất chuyển về repo mẹ
- DEC-0019 | ACTIVE | OWNER và tác tử dùng chung tài khoản GitHub
- DEC-0018 | ACTIVE | Khung 1.0.2: LEAD chọn model theo từng lần giao việc; REVIEWER khác model thực tế với WORKER của phần được kiểm
- DEC-0017 | ACTIVE | Phân công model của CYC-03 tới CYC-07 theo luật khung 1.0.2: dữ kiện kiểm tuyến 9Router và giới hạn khi chọn
- DEC-0016 | ACTIVE | Thử khung V1.0.1 trên repo này: nguồn chuẩn, nơi đặt code, duyệt ma trận model, ngoại lệ tạo task và nền tích hợp tạm
- DEC-0015 | ACTIVE | Nâng khung lên V1.0.1: bảo vệ main, ma trận model, chat và storage, dọn nhánh, scanner
- DEC-0014 | ACTIVE | Bản kiểm định CYC-02 do gpt-6.1-sol chạy không tính là một vòng kiểm định
- DEC-0013 | ACTIVE | Handout kết thúc bằng đúng một LF và ghi file với newline LF
- DEC-0012 | ACTIVE | Phân công model CYC-02: WORKER dùng Codex, REVIEWER dùng nhóm Gemini; không gắn cứng Claude
- DEC-0011 | ACTIVE | Thẻ git chỉ do OWNER tạo và đẩy
- DEC-0010 | ACTIVE | Định dạng handout Markdown và giao diện dòng lệnh
- DEC-0008 | ACTIVE | Kiểm định vòng 3 của CYC-01 chạy Claude Code trực tiếp, ngoài 9Router
- DEC-0007 | ACTIVE | Phân công model CYC-01: WORKER dùng Codex, REVIEWER dùng Claude
- DEC-0006 | ACTIVE | Khắc phục thu thập test bằng cách giới hạn pytest về tests/
- DEC-0004 | ACTIVE | So khớp id câu hỏi không phân biệt hoa thường
- DEC-0002 | ACTIVE | Lưu ngân hàng câu hỏi dạng JSON và xuất handout Markdown
- DEC-0009 | SUPERSEDED_BY DEC-0012
- DEC-0005 | RETIRED
### 4. Next action
- OWNER dán prompt ở 01_plan/SPEC_ORCA_PROMPT.md#PROMPT vào một phiên Orca để chạy CYC-03 B1 (TK-0006, TK-0007, TK-0008); phiên đó dừng sau mỗi batch chờ OWNER squash-merge. LEAD chọn model theo từng lần giao (DEC-0018, DEC-0017, 01_plan/SPEC_MODELS.md) và kiểm tuyến bằng phiên tác tử có công cụ trước lần giao đầu của mỗi model; hạn mức chưa xác minh. Việc OWNER cần chốt: phương án RFC-0001; bật luật bảo vệ main và thẻ cycle/* (RSK-0004); tự xóa nhánh nguồn. Đóng dự án lùi sau CYC-07. Pytest toàn repo trên main 67a092f đạt 23/23.
### 5. Never do
- Không xuất PDF
- Không dùng tên học viên thật trong dữ liệu thử
