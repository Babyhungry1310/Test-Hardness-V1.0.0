PHASE: EXECUTE
CYCLE: CYC-03
PROFILE: SHORT

## Handover board (updated: 2026-11-16, main @ 8dcf58b)
### 1. Progress
- CYC-01 | PASS | TK-0001 DONE R2, TK-0002 DONE R1, TK-0004 DONE R1 | thẻ cycle/CYC-01 @ e2b7944
- CYC-02 | PASS | TK-0003 DONE R1, TK-0005 DONE R1 | RVW-CYC-02 vòng 1 PASS | thẻ cycle/CYC-02 @ 36bafbe
- CYC-03 | EXECUTE | B1 DONE: TK-0006, TK-0007, TK-0008 đã merge; TK-0030 awaiting merge; B2 HOLD: TK-0018, TK-0027 | bảo vệ main
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
- DEC-0026 | ACTIVE | TK-0030 fixes TK-0007; Grok, Gemini; awaiting task merge
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
- TK-0030 fixes TK-0007: Windows cp1252 reproduction on clean main 8dcf58b failed expected exit 2, got 1; UTF-8 control tools/tests passed 54. Evidence: 03_output/CYC-03/checks/TK-0030_main_reproduction.md.
- Await OWNER merge of task/DEC-0026 before product work (LEAD rule 25). Grok xai/grok-4.7 implements, Gemini ag/gemini-3.8-flash reviews only new delta at fixed SHA after actual-model checks. R1 max_loops=3; no historical loop changes.
- Hold B2 until this repair is merged and main verification passes; TK-0018 overlaps preflight, TK-0027 not launched. No cycle gate or next cycle opened.
- PR31 remains separate and OPEN; DEC-0021 belongs to PR31, TK-0029 allocated there. Local DEC-0022..0025 and collision migration remain in lead-cyc02, not copied or overwritten by this PR.
- GitHub audit configuration remains FAIL1-6/PASS7-8/UNKNOWN9 per merged TK-0008 snapshot; OWNER handles RSK-0004. No main/tag push probes.
### 5. Never do
- Không xuất PDF
- Không dùng tên học viên thật trong dữ liệu thử
