---
schema: 1
id: SRC-0003
date: 2026-11-23
title: "Kế hoạch chi tiết Đợt Kaizen 1 — P6d (delta trên P5)"
decided_by: OWNER
related: [SRC-0002, SRC-0005, SRC-0006, DEC-0031, DEC-0032]
keywords: [kaizen, plan, dot-1, p6d]
---
<!-- ANCHOR: CONTEXT -->
## Context
Nguồn: OWNER chốt HANDOFF_P6D + QUYET_DINH_OWNER_HANDOFF_P6D (2026-11-23); LEAD Planning áp delta lên P5 @ 7ad7aa6. Không dùng P6/P6b/P6c làm nguồn (trừ bảng E27–E43 để tra Bước đích).

# KẾ HOẠCH CHI TIẾT — ĐỢT KAIZEN 1 (P6d)

- Phiên bản: **P6d** · origin: DEC-0031 + DEC-0032 · base P5 @ `7ad7aa6`
- P5 giữ làm nền; P6d chỉ thêm/đổi/hoãn theo **Bảng delta** và HANDOFF_P6D
- LEAD Planning · model phiên: `grok-4.5` · 2026-11-23
- Nhánh nháp: `lead/TK-0053-src0003-p6d` · **CHƯA mở PR** (chờ L1.1)

### Thay đổi so với P5 (tóm tắt)

1. Thêm B1b/B1b2/B1b3 (TK-0053/0057/0058), B3a1/B3a2/B3d2 (TK-0059/0055/0056), O3.4, O3.5.
2. Đổi thứ tự: B2a after B1b3; TK-0039 depends_on TK-0058; B3b after B3a2; B3e after B3d2 (`supersedes` → DEC-0032).
3. Verify thẻ đầy đủ B1b–B2 dùng `verify_doc_artifact.py` (Q-F).
4. HOÃN TK-0054 (ruleset JSON+REST) Đợt 2.
5. Thẻ YAML Bước 3–5 không viết trong P6d (Q-E cuốn chiếu).

## 0. Quy ước P4/P5 (áp toàn file)

1. **ID task** chỉ `TK-NNNN` (`^TK-\d{4}$`). Không còn `TK-0036b`.
2. **`depends_on`** chỉ chứa ID task. Điều kiện OWNER/E/cổng ghi ở `inputs` / `constraints` / bảng OWNER–LEAD.
3. **`write_scope`** ≤5 path cố định, không placeholder, không “nếu…”.
4. **Assignee khi sinh file task:** `W1`/`W2`/… Đúng schema. Trong kế hoạch, cột người nhận ghi **vai + `(đề xuất: <route/model>)`** theo mục 5; tỉ lệ theo dõi trên `SO_GIAO_VIEC.md`, không gắn cứng.
5. **Model đề xuất ≠ model đủ điều kiện.** Dùng duy nhất POOL hình thành ở L0.1 theo `MODEL_LINH_HOAT.md`; kiểm đúng catalog và ROUTE_CHECKS agent-tools cho toàn chuỗi. Actual lấy từ nhật ký phiên riêng; không suy từ tên tuyến.
6. **Thao tác chạy phiên chuẩn, GitHub UI, ảnh môi trường, probe tuyến:** bảng OWNER/LEAD — không cấp TK.
7. **REVIEWER:** preflight so model yêu cầu; lúc phiên/PR đọc actual; trùng hoặc `UNKNOWN` → dừng, không kết luận độc lập theo tên tuyến.

### Sai lệch chủ đích so với `KE_HOACH_KAIZEN.md`

| Sai lệch | Lý do P4 | Hỏi OWNER |
|---|---|---|
| Thêm task **C9** ở **cuối Bước 3** (TK-0047), trước Đ4-A | Nguồn Bước 4 đòi C9 trên main trước khi tách file; P2 đặt C9 trong Đ4-C sau tách → không đạt | Q13 |
| Bước 2: **2 PR lead/** tuần tự + 1 upgrade/ (3 merge) thay vì 2 merge | Retire 5 DEC + STATE/catalog/H0 vượt 5 path một task | Q14 |
| Bước 3: **6 merge** (thêm TK-0047 C9) thay vì 5 | Hệ quả của việc đưa C9 về cuối B3 | Q13 |

---

---

## Bảng không đổi

Mọi mã P5 dưới đây giữ nguyên nghĩa. Định nghĩa chép từ `06_sources/SRC-0003_kaizen-chi-tiet-dot1.md` @ 7ad7aa6 (bảng tổng task / batch / bảng OWNER-LEAD / câu hỏi).

| Mã | Loại (TK/O/Q/batch) | Định nghĩa P5 (nguyên văn) |
| --- | --- | --- |
| TK-0036 | TK | Copy H0-H4 tu SHARED vao 05_memory/upstream o trang thai DU THAO de co SHA — Đ0 · lead/ · T1 · depends_on [] · batch B0a |
| TK-0037 | TK | Tao DSC E1-E26, DEC-0031 Kaizen, cap nhat STATE va RSK-0004 theo E14=tach tai khoan sau khi OWNER chot E15 va 5 quyet dinh chan — Đ0 · lead/ · T1 · depends_on [TK-0036] · batch B0b |
| TK-0038 | TK | Ghi neo diem do token va bo 3 phien chuan co dinh vao file checks CYC-08 — Đ1 · lead/ · T1 · depends_on [TK-0037] · batch B1a |
| TK-0043 | TK | Implement tools/validate.py cot loi C1-C3 va SAME_MODEL; che do canh bao mac dinh — Đ3 · task/ · T2 · depends_on [TK-0042] · batch B3b |
| TK-0044 | TK | Bon kiem troi: <=1 lead/ mo; DEC lien tuc; VERSION; STATE/C6 — Đ3 · task/ · T2 · depends_on [TK-0043] · batch B3c |
| TK-0045 | TK | CI verify windows-latest tren PR; pre-push detect-secrets; chan exit 3; permissions contents read — Đ3 · task/ · T2 · depends_on [TK-0044] · batch B3d |
| TK-0046 | TK | Template diem dung E4; cach ly verify E6; LF/raw E9/E22; binary allowlist E24; VERSION — Đ3b · upgrade/ · T2 · depends_on [TK-0045] · batch B3e |
| TK-0047 | TK | Implement va bat kiem C9 (con tro/origin DEC ACTIVE) trong validate; merge truoc moi tach file Buoc 4 — Đ3-C9 · task/ · T2 · depends_on [TK-0046] · batch B3f |
| TK-0048 | TK | Tach phu luc A-D sang RATIONALE.md; tach muc 8 sang DATA_CONTRACT.md; cap nhat neo/con tro; VERSION — Đ4-A · upgrade/ · T2 · depends_on [TK-0047] · batch B4a |
| TK-0049 | TK | Viet lai LEAD.md <=1300 tu; co dinh thu tu prefix H3-2; VERSION — Đ4-B · upgrade/ · T1 · depends_on [TK-0048] · batch B4b |
| TK-0050 | TK | Them C5 C7 C12 C13 vao validate/CI; nen output H3-7 (ban du+hash; context tom tat+path) — Đ4-C · task/ · T2 · depends_on [TK-0049] · batch B4c |
| TK-0051 | TK | Ghi bang doi chung 6 luot remasure da che vao checks; actual model tu nhat ky phien do L5.1 cung cap — Đ5-A · lead/ · T1 · depends_on [TK-0050] · batch B5a |
| TK-0052 | TK | Cap nhat trang thai E tren H0 theo bang chung Dot1; soan nhap goi Kaizen 2 theo README (thu cong neu chua co script) — Đ5-B · lead/ · T1 · depends_on [TK-0051] · batch B5b |
| O0.1 | O | OWNER: Xác nhận PR #37 CLOSED — đầu ra: Ghi nhận trong STATE sau TK-0037 — cổng: — |
| O0.2 | O | OWNER: Chốt E15 — đầu ra: Trạng thái E15 trên H0 qua TK-0037 — cổng: Trước ACCEPTED E15 |
| O0.3 | O | OWNER: Chốt E14: tách tài khoản tác tử và OWNER — đầu ra: E14=tách; cập nhật RSK-0004 qua TK-0037 — cổng: Trước O1.* |
| O0.4 | O | OWNER: Chốt 5 quyết định chặn — đầu ra: YES/NO từng ý — cổng: Trước TK-0037 DEC |
| O0.5 | O | OWNER: Merge PR lead TK-0036 — đầu ra: main có H0–H4 — cổng: — |
| O0.6 | O | OWNER: Merge PR lead TK-0037 — đầu ra: DSC+DEC+STATE+RSK-0004 trên main — cổng: Sau O0.2–O0.4 |
| L0.1 | L | LEAD: Probe agent-tools toàn bộ chuỗi ở mục 2 của `MODEL_LINH_HOAT.md`; ghi kết quả/actual và hình thành POOL theo mục 3 — đầu ra: Probe đủ chuỗi; POOL có thể dùng cho lượt giao đầu — cổng: Trước TK-0036; đủ ít nhất một WORKER và một REVIEWER khác họ trong POOL |
| O1.1 | O | OWNER: Bật ruleset nhánh; bypass chỉ OWNER — đầu ra: Bảo vệ nhánh bật, tác tử không bypass — cổng: E14 đã chốt |
| O1.2 | O | OWNER: Bật luật thẻ; chỉ OWNER bypass — đầu ra: Luật thẻ bật, bypass chỉ OWNER — cổng: E14 đã chốt |
| O1.3 | O | OWNER: Kiểm quyền collaborator/token của tài khoản tác tử riêng; không tạo tài khoản mới — đầu ra: Quyền tối thiểu cần thiết đã xác nhận — cổng: E14=tách |
| O1.4 | O | OWNER: Bật secret scanning và push protection — đầu ra: Cả hai bật — cổng: Trước L1.1 |
| L1.1 | L | LEAD: Chạy 3 phiên chuẩn × 2; thu usage theo vai; chụp môi trường **local only** — đầu ra: Artifact local (không commit path máy/secret) — cổng: TK-0038 merged; O1.1–O1.4 hoàn tất |
| O1.5 | O | OWNER: Xác nhận baseline + điểm đo — đầu ra: Đồng ý dùng cho Đ5 — cổng: Trước Bước 2 kết luận nền |
| O2.1 | O | OWNER: Chốt nhóm E B3 + cột Thay — đầu ra: Trạng thái E — cổng: Trước TK-0042 |
| O2.2 | O | OWNER: Chốt đúng 5 DEC retire (mặc định đề xuất dưới) + đích ACTIVE — đầu ra: Danh sách khóa — cổng: Trước TK-0039 |
| O2.3 | O | OWNER: Merge TK-0039, TK-0040, TK-0041 tuần tự (3 merge) — đầu ra: Bước 2 xong — cổng: — |
| O3.1 | O | OWNER: Lệnh trực tiếp cho PR chạm `.github/` — đầu ra: Lệnh văn bản — cổng: **Trước mở PR TK-0045** |
| O3.2 | O | OWNER: Chốt mẫu warn&gt;20% (Q7); chấp nhận C9 cuối B3 (Q13) — đầu ra: Số PR mẫu; YES C9 — cổng: Trước đóng B3 |
| O3.3 | O | OWNER: 6 merge B3: TK-0042…TK-0047 — đầu ra: C9 trên main — cổng: Trước B4 |
| L4.0 | L | LEAD: Xác nhận C9 PASS trên main sau TK-0047 — đầu ra: Ghi nhận — cổng: Trước giao TK-0048 |
| O4.1 | O | OWNER: 3 merge TK-0048…0050 — đầu ra: B4 xong — cổng: — |
| L5.1 | L | LEAD: Chạy lại 3×2 phiên chuẩn; artifact local — đầu ra: Artifact local remasure — cổng: TK-0050 merged |
| O5.1 | O | OWNER: Xác nhận bảng đối chứng so được — đầu ra: YES/NO — cổng: — |
| O5.2–O5.3 | O | OWNER: Đ5-C: duyệt Kaizen 2; nhóm E về mẹ; CI required; điểm dừng &lt;15% token LEAD — đầu ra: Đóng Đợt 1 — cổng: — |
| Q1 | Q | Path H0–H4 = `05_memory/upstream/`? — ĐÃ TRẢ LỜI — ĐỒNG Ý |
| Q2 | Q | E14 giữ chung hay tách tài khoản máy? — ĐÃ TRẢ LỜI — TÁCH; tài khoản tác tử riêng đã có; kiểm quyền ở O1.3, không tạo mới |
| Q3 | Q | E15 chuyển repo mẹ theo nhóm PROPOSAL? — ĐÃ TRẢ LỜI — ĐỒNG Ý |
| Q4 | Q | 5 quyết định chặn Bước 0: YES/NO từng ý? — ĐÃ TRẢ LỜI — ĐỒNG Ý cả 5 |
| Q5 | Q | Khóa 5 DEC retire = 0007,0012,0014,0028,0029? Đích ACTIVE 15 vs 16? — CHỜ OWNER |
| Q6 | Q | `ag/` free hay trả phí? Model nào trong POOL được dùng cho task T2 theo giới hạn Đợt 1? — CHỜ OWNER |
| Q7 | Q | Số PR mẫu tối thiểu cho warn&gt;20%? — CHỜ OWNER |
| Q8 | Q | `CYC-08` cho Kaizen Đợt 1? — CHỜ OWNER |
| Q9 | Q | VERSION sau B2 bắt đầu `1.0.2`? E25 REJECTED Đợt 1? — CHỜ OWNER |
| Q10 | Q | Chuẩn đếm từ LEAD = `Measure-Object -Word` UTF-8? — CHỜ OWNER |
| Q11 | Q | Tên script dựng gói hay giữ thủ công? — CHỜ OWNER |
| Q12 | Q | Xác nhận điểm đo/baseline trước kết luận Đ5? — CHỜ OWNER |
| Q13 | Q | Chấp nhận **C9 ở cuối Bước 3** (TK-0047) dù KE_HOACH_KAIZEN ghi C9 ở Bước 4? — CHỜ OWNER |
| Q14 | Q | Chấp nhận Bước 2 **3 merge** (2 lead/ + 1 upgrade/) vì giới hạn 5 path? — CHỜ OWNER |
| Q15 | Q | Cho phép cập nhật catalog/probe toàn chuỗi model linh hoạt trước giao WORKER theo `MODEL_LINH_HOAT.md`? — ĐÃ ĐƯỢC THAY THẾ — áp dụng `MODEL_LINH_HOAT.md`; L0.1 probe toàn chuỗi, TK-0040 ghi nhận model đạt |
| Q-GEMINI-TIER | Q | Nhãn trên task đề xuất Gemini: chờ Q6 (tuyến `ag/` free hay trả phí) |
| B0a | batch | `B0a \| tasks: TK-0036 \| after: none` |
| B0b | batch | `B0b \| tasks: TK-0037 \| after: B0a` |
| B1a | batch | `B1a \| tasks: TK-0038 \| after: B0b` |
| B2b | batch | `B2b \| tasks: TK-0040 \| after: B2a` |
| B2c | batch | `B2c \| tasks: TK-0041 \| after: B2b` |
| B3a | batch | `B3a \| tasks: TK-0042 \| after: B2c` |
| B3c | batch | `B3c \| tasks: TK-0044 \| after: B3b` |
| B3f | batch | `B3f \| tasks: TK-0047 \| after: B3e` |
| B4a | batch | `B4a \| tasks: TK-0048 \| after: B3f` |
| B4b | batch | `B4b \| tasks: TK-0049 \| after: B4a` |
| B4c | batch | `B4c \| tasks: TK-0050 \| after: B4b` |
| B5a | batch | `B5a \| tasks: TK-0051 \| after: B4c` |
| B5b | batch | `B5b \| tasks: TK-0052 \| after: B5a` |


## Bảng delta

| Mã | Thay đổi (THÊM / ĐỔI / HOÃN) | P5 | P6d | E/M | Quyết định OWNER | Bước |
| --- | --- | --- | --- | --- | --- | --- |
| TK-0042 | ĐỔI (thẻ giữ nguyên P5) | Schema run MINOR E7/E21; CONVENTIONS mã 0/1/2/3, bảng lỗi E5/E16/E18; write_scope 5/5 path | Việc Q-B (sửa `$defs/path` + test) **chuyển sang TK-0055** vì write_scope P5 đã đủ 5 path. Không đổi nghĩa TK-0042; không cần `supersedes` | E7, E21 | Q-B | Đ3 |
| TK-0039 | ĐỔI · `supersedes: TK-0039.depends_on (P5)` | `depends_on: [TK-0038]`; verify `python -m pytest -q --tb=line tools/tests` | `depends_on: [TK-0058]`; verify `verify_doc_artifact.py` theo 5.5; goal, scope, done_when giữ P5 | — | SAI LỆCH 1 (QUYET_DINH_OWNER); Q-E, Q-F | Đ2 |
| B2a | ĐỔI · `supersedes: B2a (P5)` | `after: B1a` | `after: B1b3` | — | SAI LỆCH 1 | Đ2 |
| B3b | ĐỔI · `supersedes: B3b (P5)` | `after: B3a` | `after: B3a2` | — | Đồ thị B3 | Đ3 |
| B3e | ĐỔI · `supersedes: B3e (P5)` | `after: B3d` | `after: B3d2` | — | Đồ thị B3 | Đ3 |
| TK-0040 | ĐỔI (chỉ verify) | như TK-0039 | như TK-0039 | — | Q-E, Q-F | Đ2 |
| TK-0041 | ĐỔI (chỉ verify) | như TK-0039 | như TK-0039 | — | Q-E, Q-F | Đ2 |
| B3d | ĐỔI | `B3d \| tasks: TK-0045 \| after: B3c` | `B3d \| tasks: TK-0045 \| after: B3c, O3.1` (O3.1 đã là cổng chữ trong constraint P5; nay ghi vào đồ thị). Không đổi nghĩa | — | Q-D | Đ3 |
| TK-0053 | THÊM | — | Nạp SRC-0003 bản P6d + DSC + DEC-0032 + STATE (thẻ đầy đủ bên dưới) | E27–E43 (truy vết) | Q-E, Q-H | Đ1 (B1b) |
| TK-0057 | THÊM | — | Đồng bộ `KE_HOACH_KAIZEN_DOT_1.md` + upstream 00/01/03/04 đã sanitize (thẻ đầy đủ) | — | Q-E | Đ1 (B1b2) |
| TK-0058 | THÊM | — | Đồng bộ upstream 02 + SRC GSD/PHUONG_AN/README đã sanitize (thẻ đầy đủ) | — | Q-E | Đ1 (B1b3) |
| TK-0059 | THÊM | — | Task bộ kiểm ngữ nghĩa, `upgrade/`, ngay sau TK-0042: đưa `validate_task_schema.py`, `verify_doc_artifact.py` + test vào repo; 3 kiểm: `--base-ref origin/main`, mã O có trong bảng O và đồ thị batch+O không vòng, path trong goal ∈ write_scope. Scope dự kiến: `tools/validate_task_schema.py`, `tools/verify_doc_artifact.py`, `tools/tests/test_validate_task_schema.py`, `tools/tests/test_verify_doc_artifact.py`, `harness/VERSION` (5). Mã TK-0059 chưa có trên main (chỉ từng xuất hiện trong nháp P6c V2 đã bỏ, với nghĩa khác) | E33, E43 | Q-I | Đ3 (B3a1) |
| TK-0055 | THÊM | — | Nhận phần schema task chuyển từ TK-0042: sửa `$defs/path` thành `^(?:\.github/)?[A-Za-z0-9_][A-Za-z0-9_./-]*$` + test 4 ca (`.github/workflows/verify.yml` hợp lệ; `.secrets.baseline`, `.git/config`, `../x` không hợp lệ); kèm sổ mã thoát (mã 66) và quy ước `ON_CRASH` theo nội dung P6. Scope dự kiến: `harness/schemas/task.schema.json`, `tools/tests/test_task_schema_path.py`, `harness/exit_codes.json`, `01_plan/SPEC_TOOLS.md`, `harness/VERSION` (5) | E36, E37 | Q-B | Đ3 (B3a2) |
| TK-0056 | THÊM | — | Quét injection + base64 Python mức cảnh báo, NOTICE MIT; **+ baseline detect-secrets** `tools/ci/secrets_baseline.json`. Scope dự kiến: `tools/injection_scan.py`, `tools/NOTICE_injection_scan.md`, `tools/tests/test_injection_scan.py`, `tools/ci/run_checks.py`, `tools/ci/secrets_baseline.json` (5) | E39 | Q-C | Đ3 (B3d2) |
| O3.4 | THÊM (sửa mốc) | — | OWNER chạy `git config core.hooksPath tools/hooks` trên máy chạy tác tử; **sau khi TK-0056 merge**. Mã O3.3 đã dùng trên main (6 merge B3) nên mã O3.x chưa dùng tiếp theo là **O3.4** | — | Q-C, Q-A; Đồ thị B3 | Đ3 |
| O3.5 | THÊM (sửa mốc) | — | OWNER merge các task B3 mới: TK-0059, TK-0055, TK-0056; **trước B3f** (O3.3 giữ đúng nghĩa P5 "6 merge B3: TK-0042…TK-0047") | — | Q-A; Đồ thị B3 | Đ3 |
| TK-0054 | HOÃN | — | Đợt 2; không cấp mã task trong P6d | — | SAI LỆCH 2 | Đợt 2 |
| B1b | THÊM | — | `B1b \| tasks: TK-0053 \| after: B1a, L1.1` | — | Q-E, Q-H | Đ1 |
| B1b2 | THÊM | — | `B1b2 \| tasks: TK-0057 \| after: B1b` | — | Q-E | Đ1 |
| B1b3 | THÊM | — | `B1b3 \| tasks: TK-0058 \| after: B1b2` | — | Q-E | Đ1 |
| B3a1 | THÊM | — | `B3a1 \| tasks: TK-0059 \| after: B3a` (giữ) | — | Q-I; Đồ thị B3 | Đ3 |
| B3a2 | THÊM | — | `B3a2 \| tasks: TK-0055 \| after: B3a1` (giữ) | — | Q-B; Đồ thị B3 | Đ3 |
| B3d2 | THÊM | — | `B3d2 \| tasks: TK-0056 \| after: B3d` | — | Q-C | Đ3 |
| Script ghép log model | HOÃN | — | Đợt 2: ghép log phiên Codex + log 9Router, ghi sha256 bản xuất gốc | — | Q-G | Đợt 2 |
| Relay ghi `model` | HOÃN | — | Đợt 2: sửa relay ghi trường `model` của response vào log usage | — | Q-G | Đợt 2 |

Các dòng B2a, TK-0039, B3b, B3e đổi thứ tự so với P5, có `supersedes`, ghi vào DEC-0032.


## Bảng truy vết E27–E43

Đối chiếu nháp P6 (E→task) và SAI LỆCH 3 / DEC-0032 mục 1. Cột **Bước đích** theo OWNER: E29/E38/E40 → Bước 3; E27/E28/E30/E31 → Bước 4. Các mã ACCEPTED gán task ngay: theo bảng delta.

| Mã | Nghĩa rút gọn | Trạng thái P6d | Task / ghi chú | Bước đích |
| --- | --- | --- | --- | --- |
| E27 | Vai con ghi file + 1 dòng | ACCEPTED — gán khi viết thẻ đầu Bước | TK-0049 (khi viết thẻ B4) | Bước 4 |
| E28 | Độ sâu đọc frontmatter | ACCEPTED — gán khi viết thẻ đầu Bước | TK-0048, TK-0049 | Bước 4 |
| E29 | Vùng AUTO + state validate (không sync ghi) | ACCEPTED — gán khi viết thẻ đầu Bước | Thẻ Bước 3 (cùng state validate); marker AUTO không kiểm ở TK-0040 | Bước 3 |
| E30 | Template checkpoint + đo CS4 (không script 50/70) | ACCEPTED — gán khi viết thẻ đầu Bước | TK-0038 (CS4), TK-0049 | Bước 4 |
| E31 | Ba lý do tách việc (không ngưỡng free) | ACCEPTED — gán khi viết thẻ đầu Bước | TK-0049 | Bước 4 |
| E32 | Ước lượng token hiệu chỉnh | DEFERRED Đợt 2 | — | Đợt 2 |
| E33 | Phủ DoD bằng test | ACCEPTED | TK-0059 (bộ kiểm); phần checker PLAN_GO → Đợt 2 | Bước 3 |
| E34 | Thang tier / max_escalations | DEFERRED Đợt 2 | — | Đợt 2 |
| E35 | Enum lớp lỗi + HTTP | Một phần Đợt 1 / DEFERRED | Enum Đợt 1 qua TK-0055; HTTP → Đợt 2 | Bước 3 / Đợt 2 |
| E36 | exit_codes.json + mã 66 | ACCEPTED | TK-0055 | Bước 3 |
| E37 | ON_CRASH bắt buộc trên hook | ACCEPTED | TK-0055 (quy ước), TK-0045 (hook) | Bước 3 |
| E38 | Casefold secret names + sổ append-only | ACCEPTED — gán khi viết thẻ đầu Bước | TK-0046, TK-0044 | Bước 3 |
| E39 | Injection/base64 warn trên `.md` PR | ACCEPTED | TK-0056 | Bước 3 |
| E40 | self_check schema + CLAIM_MISMATCH | ACCEPTED — gán khi viết thẻ đầu Bước | TK-0042, TK-0043 | Bước 3 |
| E41 | Verifier ngược REVIEWER | DEFERRED Đợt 2 | — | Đợt 2 |
| E42 | Node Repair / gap YAML | DEFERRED Đợt 2/4 | — | Đợt 2 |
| E43 | Ruleset JSON+script; runner guard; cắt list; ratchet | ACCEPTED một phần | TK-0059 (bộ kiểm); TK-0054 ruleset HOÃN Đợt 2 | Bước 3 / Đợt 2 |

---

## 1. Bảng tổng task (chỉ WORKER/LEAD-repo)

| TK | Bước | Nhánh | Hạng | Người nhận (đề xuất) | REVIEWER (đề xuất) | W-ID file | depends_on | Batch | Token |
|---|---|---|---|---|---|---|---|---|---|
| TK-0036 | Đ0 | lead/ | T1 | WORKER (đề xuất: ag/gemini-3.8-flash) `Q-GEMINI-TIER` | REVIEWER (đề xuất: cx/gpt-6.1-terra) | W1 | [] | B0a | nhẹ |
| TK-0037 | Đ0 | lead/ | T1 | WORKER (đề xuất: xai/grok-4.5) | REVIEWER (đề xuất: ag/gemini-3.8-flash) | W1 | [TK-0036] | B0b | nhẹ |
| TK-0038 | Đ1 | lead/ | T1 | WORKER (đề xuất: ag/gemini-3.8-flash) `Q-GEMINI-TIER` | REVIEWER (đề xuất: xai/grok-4.5) | W1 | [TK-0037] | B1a | nhẹ |
| TK-0053 | Đ1 | lead/ | T1 | WORKER (đề xuất: xai/grok-4.5) | REVIEWER (đề xuất: ag/gemini-3.8-flash) | W1 | [TK-0038] | B1b | nhẹ–vừa |
| TK-0057 | Đ1 | lead/ | T1 | WORKER (đề xuất: ag/gemini-3.8-flash) `Q-GEMINI-TIER` | REVIEWER (đề xuất: cx/gpt-6.1-terra) | W1 | [TK-0053] | B1b2 | nhẹ |
| TK-0058 | Đ1 | lead/ | T1 | WORKER (đề xuất: ag/gemini-3.8-flash) `Q-GEMINI-TIER` | REVIEWER (đề xuất: xai/grok-4.5) | W1 | [TK-0057] | B1b3 | nhẹ |
| TK-0039 | Đ2 | lead/ | T1 | WORKER (đề xuất: ag/gemini-3.8-flash) `Q-GEMINI-TIER` | REVIEWER (đề xuất: cx/gpt-6.1-terra) | W1 | [TK-0058] | B2a | nhẹ |
| TK-0040 | Đ2 | lead/ | T1 | WORKER (đề xuất: ag/gemini-3.8-flash) `Q-GEMINI-TIER` | REVIEWER (đề xuất: xai/grok-4.5) | W2 | [TK-0039] | B2b | nhẹ |
| TK-0041 | Đ2 | upgrade/ | T2 | WORKER (đề xuất: xai/grok-4.5) | REVIEWER (đề xuất: ag/gemini-3.8-flash) | W1 | [TK-0040] | B2c | nhẹ–vừa |
| TK-0042 | Đ3a | upgrade/ | T2 | WORKER (đề xuất: xai/grok-4.5) | REVIEWER (đề xuất: ag/gemini-3.8-flash) | W1 | [TK-0041] | B3a | vừa |
| TK-0059 | Đ3 | upgrade/ | T2 | WORKER (đề xuất: xai/grok-4.5) | REVIEWER (đề xuất: ag/gemini-3.8-flash) | W1 | [TK-0042] | B3a1 | vừa |
| TK-0055 | Đ3 | upgrade/ | T2 | WORKER (đề xuất: xai/grok-4.5) | REVIEWER (đề xuất: ag/gemini-3.8-flash) | W1 | [TK-0059] | B3a2 | vừa |
| TK-0043 | Đ3 | task/ | T2 | WORKER (đề xuất: xai/grok-4.5) | REVIEWER (đề xuất: ag/gemini-3.8-flash) | W1 | [TK-0055] | B3b | nặng |
| TK-0044 | Đ3 | task/ | T2 | WORKER (đề xuất: cx/gpt-6.1-terra) | REVIEWER (đề xuất: ag/gemini-3.8-flash) | W2 | [TK-0043] | B3c | vừa–nặng |
| TK-0045 | Đ3 | task/ | T2 | WORKER (đề xuất: xai/grok-4.5) | REVIEWER (đề xuất: ag/gemini-3.8-flash) | W1 | [TK-0044] | B3d | nặng |
| TK-0056 | Đ3 | task/ | T2 | WORKER (đề xuất: xai/grok-4.5) | REVIEWER (đề xuất: ag/gemini-3.8-flash) | W1 | [TK-0045] | B3d2 | vừa |
| TK-0046 | Đ3b | upgrade/ | T2 | WORKER (đề xuất: cx/gpt-6.1-terra) | REVIEWER (đề xuất: ag/gemini-3.8-flash) | W2 | [TK-0056] | B3e | vừa |
| TK-0047 | Đ3-C9 | task/ | T2 | WORKER (đề xuất: xai/grok-4.5) | REVIEWER (đề xuất: ag/gemini-3.8-flash) | W1 | [TK-0046] | B3f | vừa–nặng |
| TK-0048 | Đ4-A | upgrade/ | T2 | WORKER (đề xuất: ag/gemini-3.8-flash) `Q-GEMINI-TIER` | REVIEWER (đề xuất: cx/gpt-6.1-terra) | W1 | [TK-0047] | B4a | vừa |
| TK-0049 | Đ4-B | upgrade/ | T1 | WORKER (đề xuất: ag/gemini-3.8-flash) `Q-GEMINI-TIER` | REVIEWER (đề xuất: xai/grok-4.5) | W2 | [TK-0048] | B4b | vừa |
| TK-0050 | Đ4-C | task/ | T2 | WORKER (đề xuất: xai/grok-4.5) | REVIEWER (đề xuất: ag/gemini-3.8-flash) | W1 | [TK-0049] | B4c | nặng |
| TK-0051 | Đ5-A | lead/ | T1 | WORKER (đề xuất: ag/gemini-3.8-flash) `Q-GEMINI-TIER` | REVIEWER (đề xuất: cx/gpt-6.1-terra) | W2 | [TK-0050] | B5a | nhẹ |
| TK-0052 | Đ5-B | lead/ | T1 | WORKER (đề xuất: ag/gemini-3.8-flash) `Q-GEMINI-TIER` | REVIEWER (đề xuất: xai/grok-4.5) | W1 | [TK-0051] | B5b | nhẹ–vừa |

Đ5-C: cổng OWNER — không cấp TK. **TK-0054 HOÃN Đợt 2** (không cấp mã trong P6d).

**Tỉ lệ Gemini:** không gắn cứng. Mỗi lượt giao ghi `SO_GIAO_VIEC.md`; cột “thực nhận” là nguồn tính ~50% WORKER Gemini và LEAD 2:1.

Thẻ YAML đầy đủ trong mục 4 chỉ cho B1b–Bước 2 (Q-E). Bước 3–5: xem **Bảng delta**; thẻ YAML viết ở đầu mỗi Bước sau L1.1.

---

## 2. Đồ thị batch


<!-- code:text -->
    ## CYC-08 batches (P6d)
    - B1a | tasks: TK-0038 | after: B0b
    - B1b | tasks: TK-0053 | after: B1a, L1.1
    - B1b2 | tasks: TK-0057 | after: B1b
    - B1b3 | tasks: TK-0058 | after: B1b2
    - B2a | tasks: TK-0039 | after: B1b3
    - B2b | tasks: TK-0040 | after: B2a
    - B2c | tasks: TK-0041 | after: B2b
    - B3a | tasks: TK-0042 | after: B2c
    - B3a1 | tasks: TK-0059 | after: B3a
    - B3a2 | tasks: TK-0055 | after: B3a1
    - B3b | tasks: TK-0043 | after: B3a2
    - B3c | tasks: TK-0044 | after: B3b
    - B3d | tasks: TK-0045 | after: B3c, O3.1
    - B3d2 | tasks: TK-0056 | after: B3d
    - B3e | tasks: TK-0046 | after: B3d2
    - B3f | tasks: TK-0047 | after: B3e
    - B4a | tasks: TK-0048 | after: B3f
    - B4b | tasks: TK-0049 | after: B4a
    - B4c | tasks: TK-0050 | after: B4b
    - B5a | tasks: TK-0051 | after: B4c
    - B5b | tasks: TK-0052 | after: B5a
<!-- /code:text -->

Một chuỗi thẳng từ B1b tới B5b; O-task chen ở B1b (L1.1) và B3d (O3.1).


<!-- code:mermaid -->
    flowchart TB
      B1a[B1a TK-0038] --> B1b[B1b TK-0053]
      L11((L1.1)) --> B1b
      B1b --> B1b2[B1b2 TK-0057] --> B1b3[B1b3 TK-0058]
      B1b3 --> B2a[B2a TK-0039] --> B2b[B2b TK-0040] --> B2c[B2c TK-0041]
      B2c --> B3a[B3a TK-0042] --> B3a1[B3a1 TK-0059] --> B3a2[B3a2 TK-0055]
      B3a2 --> B3b[B3b TK-0043] --> B3c[B3c TK-0044] --> B3d[B3d TK-0045]
      O31((O3.1)) --> B3d
      B3d --> B3d2[B3d2 TK-0056] --> B3e[B3e TK-0046] --> B3f[B3f TK-0047]
      B3f --> B4a[B4a TK-0048] --> B4b[B4b TK-0049] --> B4c[B4c TK-0050]
      B4c --> B5a[B5a TK-0051] --> B5b[B5b TK-0052]
<!-- /code:mermaid -->

---

## 3. Bảng OWNER / LEAD (không cấp TK)

| Mã | Ai | Việc | Đầu vào (path) | Đầu ra | Cổng trước |
|---|---|---|---|---|---|
| O0.1 | OWNER | Xác nhận PR #37 CLOSED | GitHub PR 37 | Ghi nhận trong STATE sau TK-0037 | — |
| O0.2 | OWNER | Chốt E15 | `05_memory/upstream/00_tong_quan_upstream.md` (sau TK-0036) | Trạng thái E15 trên H0 qua TK-0037 | Trước ACCEPTED E15 |
| O0.3 | OWNER | Chốt E14: tách tài khoản tác tử và OWNER | `OWNER_TRA_LOI.md`; H0; `04_control/risks/RSK-0004_agent-tag-and-merge-bypass.md` | E14=tách; cập nhật RSK-0004 qua TK-0037 | Trước O1.* |
| O0.4 | OWNER | Chốt 5 quyết định chặn | `KE_HOACH_KAIZEN.md` Bước 0 | YES/NO từng ý | Trước TK-0037 DEC |
| O0.5 | OWNER | Merge PR lead TK-0036 | PR | main có H0–H4 | — |
| O0.6 | OWNER | Merge PR lead TK-0037 | PR | DSC+DEC+STATE+RSK-0004 trên main | Sau O0.2–O0.4 |
| L0.1 | LEAD | Probe agent-tools toàn bộ chuỗi ở mục 2 của `MODEL_LINH_HOAT.md`; ghi kết quả/actual và hình thành POOL theo mục 3 | 9Router; `04_control/MODEL_CATALOG.md` | Probe đủ chuỗi; POOL có thể dùng cho lượt giao đầu | Trước TK-0036; đủ ít nhất một WORKER và một REVIEWER khác họ trong POOL |
| O1.1 | OWNER | Bật ruleset nhánh; bypass chỉ OWNER | GitHub rulesets; E14=tách | Bảo vệ nhánh bật, tác tử không bypass | E14 đã chốt |
| O1.2 | OWNER | Bật luật thẻ; chỉ OWNER bypass | GitHub rulesets; E14=tách | Luật thẻ bật, bypass chỉ OWNER | E14 đã chốt |
| O1.3 | OWNER | Kiểm quyền collaborator/token của tài khoản tác tử riêng; không tạo tài khoản mới | GitHub collaborator/access settings | Quyền tối thiểu cần thiết đã xác nhận | E14=tách |
| O1.4 | OWNER | Bật secret scanning và push protection | GitHub settings | Cả hai bật | Trước L1.1 |
| L1.1 | LEAD | Chạy 3 phiên chuẩn × 2; thu usage theo vai; chụp môi trường **local only** | `03_output/CYC-08/checks/baseline_session_spec.md` (sau TK-0038) | Artifact local (không commit path máy/secret) | TK-0038 merged; O1.1–O1.4 hoàn tất |
| O1.5 | OWNER | Xác nhận baseline + điểm đo | Bảng local L1.1 | Đồng ý dùng cho Đ5 | Trước Bước 2 kết luận nền |
| O2.1 | OWNER | Chốt nhóm E B3 + cột Thay | H0 | Trạng thái E | Trước TK-0042 |
| O2.2 | OWNER | Chốt đúng 5 DEC retire (mặc định đề xuất dưới) + đích ACTIVE | Q5 | Danh sách khóa | Trước TK-0039 |
| O2.3 | OWNER | Merge TK-0039, TK-0040, TK-0041 tuần tự (3 merge) | PR | Bước 2 xong | — |
| O3.1 | OWNER | Lệnh trực tiếp cho PR chạm `.github/` | PREFLIGHT / chat | Lệnh văn bản | **Trước mở PR TK-0045** |
| O3.2 | OWNER | Chốt mẫu warn&gt;20% (Q7); chấp nhận C9 cuối B3 (Q13) | — | Số PR mẫu; YES C9 | Trước đóng B3 |
| O3.3 | OWNER | 6 merge B3: TK-0042…TK-0047 | PR | C9 trên main | Trước B4 |
| L4.0 | LEAD | Xác nhận C9 PASS trên main sau TK-0047 | CI/validate | Ghi nhận | Trước giao TK-0048 |
| O4.1 | OWNER | 3 merge TK-0048…0050 | PR | B4 xong | — |
| L5.1 | LEAD | Chạy lại 3×2 phiên chuẩn; artifact local | `baseline_session_spec.md`; điểm đo B1 | Artifact local remasure | TK-0050 merged |
| O5.1 | OWNER | Xác nhận bảng đối chứng so được | Sau TK-0051 | YES/NO | — |
| O5.2–O5.3 | OWNER | Đ5-C: duyệt Kaizen 2; nhóm E về mẹ; CI required; điểm dừng &lt;15% token LEAD | TK-0052 outputs | Đóng Đợt 1 | — |
| O3.4 | OWNER | chạy `git config core.hooksPath tools/hooks` trên máy chạy tác tử | Sau khi TK-0056 merge | Hook pre-push chạy được trên máy tác tử | Sau TK-0056 merge |
| O3.5 | OWNER | merge TK-0059, TK-0055, TK-0056 | Trước B3f | Ba task trên main | Trước B3f |


---

## 4. Task đủ trường `task.schema.json`

Chu kỳ: `CYC-08`. `origin` sau TK-0037: `DEC-0031`.

### TK-0036 — H0–H4 DỰ THẢO

```yaml
schema: 1
id: TK-0036
cycle: CYC-08
origin: "01_plan/PLAN.md#CYC_08"
assignee: W1
goal: "Copy H0-H4 tu SHARED vao 05_memory/upstream o trang thai DU THAO de co SHA"
write_scope:
  - 05_memory/upstream/00_tong_quan_upstream.md
  - 05_memory/upstream/01_brainstorm_va_tra_cuu_ngoai.md
  - 05_memory/upstream/02_quyen_worker_va_phong_thu_injection.md
  - 05_memory/upstream/03_ha_tang_context_va_dieu_phoi_loop.md
  - 05_memory/upstream/04_nhat_ky_kiem_toan_va_quan_tri_van_hanh.md
constraints:
  - "Chi van ban DU THAO; khong ghi ACCEPTED/REJECTED cho E"
  - "Khong secret, token, duong dan may ca nhan"
  - "Q1: path 05_memory/upstream/ da duoc OWNER chap nhan truoc khi giao"
inputs:
  - "<SHARED>/00_tong_quan_upstream.md"
  - "<SHARED>/01_brainstorm_va_tra_cuu_ngoai.md"
  - "<SHARED>/02_quyen_worker_va_phong_thu_injection.md"
  - "<SHARED>/03_ha_tang_context_va_dieu_phoi_loop.md"
  - "<SHARED>/04_nhat_ky_kiem_toan_va_quan_tri_van_hanh.md"
read_also:
  - "KE_HOACH_KAIZEN.md"
  - "harness/MAIN_PROTECTION.md"
line_budget: 400
verify: "python -m pytest -q --tb=line tools/tests"
done_when:
  - "Nam file write_scope ton tai tren nhanh lead/"
  - "Moi file mang nhan DU THAO; khong co credential"
size: "1 session · 5 files · copy+label"
depends_on: []
fixes: ""
```
- Nhánh: `lead/kaizen-h0-h4` · Outputs = write_scope · Token: nhẹ · Điểm dừng: Q1 chưa YES

### TK-0037 — DSC + DEC Kaizen + STATE

```yaml
schema: 1
id: TK-0037
cycle: CYC-08
origin: "01_plan/PLAN.md#CYC_08"
assignee: W1
goal: "Tao DSC E1-E26, DEC-0031 Kaizen, cap nhat STATE va RSK-0004 theo E14=tach tai khoan sau khi OWNER chot E15 va 5 quyet dinh chan"
write_scope:
  - 05_memory/discussions/2026/DSC-20261121-kzn1.md
  - 04_control/decisions/DEC-0031_kaizen-dot1.md
  - 04_control/STATE.md
  - 04_control/risks/RSK-0004_agent-tag-and-merge-bypass.md
constraints:
  - "Khong mo PR truoc O0.2 O0.3 O0.4 DONE"
  - "DSC path co dinh DSC-20261121-kzn1.md; khong placeholder"
  - "Mot PR lead/; khong chinh H0-H4 (da o TK-0036)"
inputs:
  - 05_memory/upstream/00_tong_quan_upstream.md
  - 05_memory/upstream/01_brainstorm_va_tra_cuu_ngoai.md
  - 05_memory/upstream/02_quyen_worker_va_phong_thu_injection.md
  - 05_memory/upstream/03_ha_tang_context_va_dieu_phoi_loop.md
  - 05_memory/upstream/04_nhat_ky_kiem_toan_va_quan_tri_van_hanh.md
  - 04_control/STATE.md
  - 04_control/risks/RSK-0004_agent-tag-and-merge-bypass.md
read_also:
  - "harness/templates/discussion.md"
  - "harness/templates/decision.md"
  - "harness/rules/LEAD.md"
line_budget: 200
verify: "python -m pytest -q --tb=line tools/tests"
done_when:
  - "DSC-20261121-kzn1.md co du su kien E1-E26"
  - "DEC-0031 ACTIVE; DSC co dong ACCEPTED tuong ung cho E14 E15 neu OWNER chap"
  - "STATE muc 3-4 phan anh Kaizen Dot1; PR37 CLOSED duoc ghi nhan"
  - "RSK-0004 ghi nhan E14=tach; giu OPEN toi khi OWNER xac nhan ruleset va quyen thuc te"
size: "1 session · 4 files"
depends_on: [TK-0036]
fixes: ""
```
- Outputs: 4 path write_scope · Merge: O0.6 · Điểm dừng: thiếu chốt OWNER

### TK-0038 — Đóng băng đặc tả 3 phiên chuẩn

```yaml
schema: 1
id: TK-0038
cycle: CYC-08
origin: "DEC-0031"
assignee: W1
goal: "Ghi neo diem do token va bo 3 phien chuan co dinh vao file checks CYC-08"
write_scope:
  - 03_output/CYC-08/checks/baseline_session_spec.md
constraints:
  - "Khong chay phien trong task nay; L1.1 chay sau"
  - "Khong ghi secret; khong duong dan thu muc user"
  - "Khong doi diem do/model/tuyen chuan tu day toi het Buoc 5"
inputs:
  - 04_control/STATE.md
  - 04_control/MODEL_CATALOG.md
read_also:
  - "KE_HOACH_KAIZEN.md"
line_budget: 120
verify: "python -m pytest -q --tb=line tools/tests"
done_when:
  - "baseline_session_spec.md mo ta relay/9Router/diem usage va 3 phien (input, route, model ky vong, provider version)"
  - "Du de L1.1 va L5.1 chay lai"
size: "1 session · 1 file"
depends_on: [TK-0037]
fixes: ""
```


Chung cho 6 thẻ: `tools/verify_doc_artifact.py` và `tools/validate_task_schema.py` chưa có trên main → constraint "verify chạy bằng bản cục bộ tới khi task Q-I (TK-0059) merge". Nhánh: TK-0053/0057/0058/0039/0040 `lead/`, TK-0041 `upgrade/` (ghi ngoài YAML vì schema không có khóa `branch`).

### TK-0053 — B1b · `lead/`

```yaml
schema: 1
id: TK-0053
cycle: CYC-08
origin: DEC-0031
assignee: W1
goal: Cap nhat 06_sources/SRC-0003_kaizen-chi-tiet-dot1.md len P6d (delta tren P5); tao 05_memory/discussions/2026/DSC-20261123-gsd1.md va 04_control/decisions/DEC-0032_gsd-dot1.md; cap nhat 04_control/STATE.md
write_scope:
  - 06_sources/SRC-0003_kaizen-chi-tiet-dot1.md
  - 05_memory/discussions/2026/DSC-20261123-gsd1.md
  - 04_control/decisions/DEC-0032_gsd-dot1.md
  - 04_control/STATE.md
constraints:
  - "CAM mo PR truoc khi L1.1 xong (Q-H)"
  - "Giu nguyen phan P5 khong doi; chi ap bang delta cua goi HANDOFF_P6D"
  - "Khong sua DEC-0031"
  - "verify chay bang ban cuc bo toi khi task Q-I (TK-0059) merge"
inputs:
  - 06_sources/SRC-0003_kaizen-chi-tiet-dot1.md
  - 04_control/decisions/DEC-0031_kaizen-dot1.md
  - 04_control/STATE.md
  - 03_output/CYC-08/checks/baseline_session_spec.md
read_also:
  - harness/rules/LEAD.md
  - harness/templates/decision.md
line_budget: 300
verify: >-
  python tools/verify_doc_artifact.py 06_sources/SRC-0003_kaizen-chi-tiet-dot1.md --contains "P6d" --heading "Bảng delta"
  && python tools/validate_task_schema.py 06_sources/SRC-0003_kaizen-chi-tiet-dot1.md --schema harness/schemas/task.schema.json --known-ids 06_sources/SRC-0003_kaizen-chi-tiet-dot1.md
  && python tools/verify_doc_artifact.py 04_control/decisions/DEC-0032_gsd-dot1.md --contains "DEC-0032" --contains "ACCEPTED"
  && python tools/verify_doc_artifact.py 05_memory/discussions/2026/DSC-20261123-gsd1.md --contains "Q-A" --contains "Q-I"
  && python tools/verify_doc_artifact.py 04_control/STATE.md --contains "DEC-0032"
done_when:
  - "SRC-0003 co chuoi P6d va muc Bang delta (--contains P6d, --heading)"
  - "The trong SRC-0003 qua validate_task_schema ma 0, tru loi da biet (validate_task_schema)"
  - "DEC-0032 co ma DEC-0032 va trang thai ACCEPTED (--contains x2)"
  - "DSC ghi du Q-A den Q-I (--contains Q-A, Q-I)"
  - "STATE nhac DEC-0032 (--contains)"
  - "Noi dung DEC-0032 dung muc 5.8 cua goi (kiem o cong REVIEWER)"
size: "1 session · 4 files"
depends_on:
  - TK-0038
fixes: ""
log_level: LOOP
max_loops: 3
```

### TK-0057 — B1b2 · `lead/`

```yaml
schema: 1
id: TK-0057
cycle: CYC-08
origin: DEC-0031
assignee: W1
goal: Nap 06_sources/KE_HOACH_KAIZEN_DOT_1.md va cap nhat 05_memory/upstream 00 01 03 04 tu ban da sanitize, scan ALLOW
write_scope:
  - 06_sources/KE_HOACH_KAIZEN_DOT_1.md
  - 05_memory/upstream/00_tong_quan_upstream.md
  - 05_memory/upstream/01_brainstorm_va_tra_cuu_ngoai.md
  - 05_memory/upstream/03_ha_tang_context_va_dieu_phoi_loop.md
  - 05_memory/upstream/04_nhat_ky_kiem_toan_va_quan_tri_van_hanh.md
constraints:
  - "Chi chep file khi tools/scan.py tra ALLOW; nguon QUARANTINE thi BLOCKED kem QUESTION"
  - "LEAD dien sha256 cua 5 ban sanitize vao lenh verify truoc khi giao"
  - "Bo file khong doi so voi repo (so sha256) khoi commit"
  - "verify chay bang ban cuc bo toi khi task Q-I (TK-0059) merge"
inputs:
  - 05_memory/upstream/00_tong_quan_upstream.md
  - 06_sources/SRC-0003_kaizen-chi-tiet-dot1.md
read_also:
  - tools/scan.py
  - harness/rules/WORKER.md
line_budget: 150
verify: >-
  python tools/verify_doc_artifact.py 06_sources/KE_HOACH_KAIZEN_DOT_1.md 05_memory/upstream/00_tong_quan_upstream.md
  05_memory/upstream/01_brainstorm_va_tra_cuu_ngoai.md 05_memory/upstream/03_ha_tang_context_va_dieu_phoi_loop.md
  05_memory/upstream/04_nhat_ky_kiem_toan_va_quan_tri_van_hanh.md --no-links
  --sha256 06_sources/KE_HOACH_KAIZEN_DOT_1.md=SHA_KH --sha256 05_memory/upstream/00_tong_quan_upstream.md=SHA_00
  --sha256 05_memory/upstream/01_brainstorm_va_tra_cuu_ngoai.md=SHA_01 --sha256 05_memory/upstream/03_ha_tang_context_va_dieu_phoi_loop.md=SHA_03
  --sha256 05_memory/upstream/04_nhat_ky_kiem_toan_va_quan_tri_van_hanh.md=SHA_04
done_when:
  - "Nam file ton tai, UTF-8, khong bi mat hay duong dan may (kiem mac dinh cua verify_doc_artifact)"
  - "Moi file trung sha256 ban sanitize (--sha256 tung file)"
  - "Moi file scan ALLOW (kiem o cong REVIEWER)"
size: "1 session · 5 files"
depends_on:
  - TK-0053
fixes: ""
log_level: LOOP
max_loops: 3
```

### TK-0058 — B1b3 · `lead/`

```yaml
schema: 1
id: TK-0058
cycle: CYC-08
origin: DEC-0031
assignee: W1
goal: Nap 05_memory/upstream/02_quyen_worker_va_phong_thu_injection.md va 06_sources/SRC-0007 SRC-0008 SRC-0009 tu ban da sanitize; cap nhat 06_sources/README.md
write_scope:
  - 05_memory/upstream/02_quyen_worker_va_phong_thu_injection.md
  - 06_sources/SRC-0007_phuong-an-tich-hop-gsd-dot1.md
  - 06_sources/SRC-0008_gsd-core-de-xuat-kaizen.md
  - 06_sources/SRC-0009_readme-goi-kaizen.md
  - 06_sources/README.md
constraints:
  - "Chi chep file khi tools/scan.py tra ALLOW; nguon QUARANTINE thi BLOCKED kem QUESTION; khong bo path im lang"
  - "LEAD dien sha256 cua 4 ban sanitize vao lenh verify truoc khi giao"
  - "Ghi NOTICE MIT neu noi dung phai sinh tu GSD Core"
  - "verify chay bang ban cuc bo toi khi task Q-I (TK-0059) merge"
inputs:
  - 05_memory/upstream/02_quyen_worker_va_phong_thu_injection.md
  - 06_sources/README.md
read_also:
  - tools/scan.py
line_budget: 150
verify: >-
  python tools/verify_doc_artifact.py 05_memory/upstream/02_quyen_worker_va_phong_thu_injection.md
  06_sources/SRC-0007_phuong-an-tich-hop-gsd-dot1.md 06_sources/SRC-0008_gsd-core-de-xuat-kaizen.md
  06_sources/SRC-0009_readme-goi-kaizen.md --no-links
  --sha256 05_memory/upstream/02_quyen_worker_va_phong_thu_injection.md=SHA_02
  --sha256 06_sources/SRC-0007_phuong-an-tich-hop-gsd-dot1.md=SHA_07 --sha256 06_sources/SRC-0008_gsd-core-de-xuat-kaizen.md=SHA_08
  --sha256 06_sources/SRC-0009_readme-goi-kaizen.md=SHA_09
  && python tools/verify_doc_artifact.py 06_sources/README.md --contains "SRC-0007" --contains "SRC-0009"
done_when:
  - "Bon file nap ton tai, UTF-8, khong bi mat hay duong dan may (kiem mac dinh)"
  - "Bon file nap trung sha256 ban sanitize (--sha256 tung file)"
  - "06_sources/README.md liet ke SRC-0007 den SRC-0009 (--contains)"
  - "Khong file QUARANTINE nao trong commit (kiem o cong REVIEWER)"
size: "1 session · 5 files"
depends_on:
  - TK-0057
fixes: ""
log_level: LOOP
max_loops: 3
```

### TK-0039 — B2a · `lead/` (P5, chỉ đổi verify)

```yaml
schema: 1
id: TK-0039
cycle: CYC-08
origin: DEC-0031
assignee: W1
goal: Ghi RETIRED cho dung 5 DEC OWNER da chot (mac dinh 0007 0012 0014 0028 0029)
write_scope:
  - 04_control/decisions/DEC-0007_cyc-01-reviewer-claude.md
  - 04_control/decisions/DEC-0012_cyc-02-reviewer-gemini.md
  - 04_control/decisions/DEC-0014_cyc-02-pr20-not-a-review-round.md
  - 04_control/decisions/DEC-0028_tk-0018-source-handoff.md
  - 04_control/decisions/DEC-0029_split-tk-0033-session-detector.md
constraints:
  - "Chi 5 file trong write_scope; chuyen kho lanh neu can thi cung PR nhung khong them path ngoai 5 file status — neu bat buoc path superseded/, tach PR lead/ moi sau khi OWNER cap nhat Q14"
  - "O2.2 phai khoa dung 5 ma truoc khi giao; neu doi ma, cap nhat write_scope truoc Run"
  - "verify chay bang ban cuc bo toi khi task Q-I (TK-0059) merge"
inputs:
  - 04_control/STATE.md
  - 04_control/decisions/DEC-0007_cyc-01-reviewer-claude.md
  - 04_control/decisions/DEC-0012_cyc-02-reviewer-gemini.md
  - 04_control/decisions/DEC-0014_cyc-02-pr20-not-a-review-round.md
  - 04_control/decisions/DEC-0028_tk-0018-source-handoff.md
  - 04_control/decisions/DEC-0029_split-tk-0033-session-detector.md
read_also:
  - harness/rules/LEAD.md
line_budget: 150
verify: >-
  python tools/verify_doc_artifact.py 04_control/decisions/DEC-0007_cyc-01-reviewer-claude.md
  04_control/decisions/DEC-0012_cyc-02-reviewer-gemini.md 04_control/decisions/DEC-0014_cyc-02-pr20-not-a-review-round.md
  04_control/decisions/DEC-0028_tk-0018-source-handoff.md 04_control/decisions/DEC-0029_split-tk-0033-session-detector.md
  --contains "RETIRED"
done_when:
  - "Moi DEC trong scope co dong RETIRED moi nhat (--contains RETIRED tren ca 5 file)"
  - "Khong sua DEC ngoai danh sach (kiem o cong REVIEWER)"
size: "1 session · 5 files"
depends_on:
  - TK-0058
fixes: ""
```

### TK-0040 — B2b · `lead/` (P5, chỉ đổi verify)

```yaml
schema: 1
id: TK-0040
cycle: CYC-08
origin: DEC-0031
assignee: W2
goal: Them code catalog cho model Dot1 dang dung va DeepSeek/Nano UNQUALIFIED; rut STATE muc 3; cap nhat trang thai nhom E Buoc 3 tren H0
write_scope:
  - 04_control/MODEL_CATALOG.md
  - 04_control/STATE.md
  - 05_memory/upstream/00_tong_quan_upstream.md
constraints:
  - "Them/cap nhat code grok-4.5 (va alias xai/grok-4.5); dam bao gpt-6.1-terra va gemini-3.8-flash-n/alias con dung; them DeepSeek va Nvidia Nano o availability unconfirmed/UNQUALIFIED"
  - "Khong danh availability confirmed neu chua co ROUTE_CHECKS agent-tools OK moi; L0.1 la tien quyet ghi vao catalog khi co"
  - "Khong xoa muc catalog cu"
  - "verify chay bang ban cuc bo toi khi task Q-I (TK-0059) merge"
inputs:
  - 04_control/MODEL_CATALOG.md
  - 04_control/STATE.md
  - 05_memory/upstream/00_tong_quan_upstream.md
  - 04_control/decisions/DEC-0007_cyc-01-reviewer-claude.md
read_also:
  - harness/MODEL_POLICY.md
  - harness/schemas/model_catalog.schema.json
line_budget: 250
verify: >-
  python tools/verify_doc_artifact.py 04_control/MODEL_CATALOG.md --contains "grok-4.5" --contains "DeepSeek" --contains "Nano" --contains "UNQUALIFIED"
  && python tools/verify_doc_artifact.py 04_control/STATE.md
  && python tools/verify_doc_artifact.py 05_memory/upstream/00_tong_quan_upstream.md --regex "^- E2[0-6] \\| "
done_when:
  - "Catalog co grok-4.5, DeepSeek, Nvidia Nano (--contains x4)"
  - "Terra/gemini alias khong gay SAME_MODEL sai (kiem o cong REVIEWER)"
  - "STATE muc 3 gon sau retire (kiem o cong REVIEWER; verify chi kiem file hop le)"
  - "H0 nhom E B3 co trang thai theo O2.1 (--regex dong E; doi chieu O2.1 o cong REVIEWER)"
size: "1 session · 3 files"
depends_on:
  - TK-0039
fixes: ""
```

### TK-0041 — B2c · `upgrade/` (P5, chỉ đổi verify)

```yaml
schema: 1
id: TK-0041
cycle: CYC-08
origin: DEC-0031
assignee: W1
goal: Gop harness muc 9 theo REVIEW_SECTION_9; tang VERSION khop HARNESS
write_scope:
  - harness/HARNESS.md
  - harness/rules/LEAD.md
  - harness/VERSION
  - harness/tools/README.md
constraints:
  - "Chi van ban khung; khong code script moi"
  - "Moi PR upgrade/ tang VERSION mot lan"
  - "verify chay bang ban cuc bo toi khi task Q-I (TK-0059) merge"
inputs:
  - harness/HARNESS.md
  - harness/rules/LEAD.md
  - harness/VERSION
  - harness/tools/README.md
read_also:
  - harness/tools/README.md#REVIEW_SECTION_9
line_budget: 300
verify: >-
  python tools/verify_doc_artifact.py harness/VERSION harness/HARNESS.md harness/rules/LEAD.md harness/tools/README.md
  && python tools/verify_doc_artifact.py harness/tools/README.md --heading "REVIEW_SECTION_9"
done_when:
  - "Bon file hop le UTF-8, khong bi mat, link khong gay (kiem mac dinh)"
  - "VERSION khop dong phien ban HARNESS (kiem o cong REVIEWER)"
  - "Muc 9 phan anh gop dong 1-3 OWNER da chon huong (kiem o cong REVIEWER)"
size: "1 session · 4 files"
depends_on:
  - TK-0040
fixes: ""
```


### Bước 3–5 — không thẻ YAML trong P6d (Q-E)

Chỉ áp **Bảng delta** (và đồ thị batch). Thẻ YAML đủ trường cho TK-0042…TK-0052 / TK-0055/0056/0059 viết ở đầu mỗi Bước, PR `lead/` riêng, sau khi có số đo L1.1.
Thẻ P5 của TK-0043, 0044, 0046, 0049 **không sửa nghĩa** trong P6d (SAI LỆCH 3).

---

## 5. CÂU HỎI CHO OWNER

| ID | Câu hỏi | Trạng thái |
|---|---|---|
| Q1 | Path H0–H4 = `05_memory/upstream/`? | ĐÃ TRẢ LỜI — ĐỒNG Ý |
| Q2 | E14 giữ chung hay tách tài khoản máy? | ĐÃ TRẢ LỜI — TÁCH; tài khoản tác tử riêng đã có; kiểm quyền ở O1.3, không tạo mới |
| Q3 | E15 chuyển repo mẹ theo nhóm PROPOSAL? | ĐÃ TRẢ LỜI — ĐỒNG Ý |
| Q4 | 5 quyết định chặn Bước 0: YES/NO từng ý? | ĐÃ TRẢ LỜI — ĐỒNG Ý cả 5 |
| Q5 | Khóa 5 DEC retire = 0007,0012,0014,0028,0029? Đích ACTIVE 15 vs 16? | CHỜ OWNER |
| Q6 | `ag/` free hay trả phí? Model nào trong POOL được dùng cho task T2 theo giới hạn Đợt 1? | CHỜ OWNER |
| Q7 | Số PR mẫu tối thiểu cho warn&gt;20%? | CHỜ OWNER |
| Q8 | `CYC-08` cho Kaizen Đợt 1? | CHỜ OWNER |
| Q9 | VERSION sau B2 bắt đầu `1.0.2`? E25 REJECTED Đợt 1? | CHỜ OWNER |
| Q10 | Chuẩn đếm từ LEAD = `Measure-Object -Word` UTF-8? | CHỜ OWNER |
| Q11 | Tên script dựng gói hay giữ thủ công? | CHỜ OWNER |
| Q12 | Xác nhận điểm đo/baseline trước kết luận Đ5? | CHỜ OWNER |
| Q13 | Chấp nhận **C9 ở cuối Bước 3** (TK-0047) dù KE_HOACH_KAIZEN ghi C9 ở Bước 4? | CHỜ OWNER |
| Q14 | Chấp nhận Bước 2 **3 merge** (2 lead/ + 1 upgrade/) vì giới hạn 5 path? | CHỜ OWNER |
| Q15 | Cho phép cập nhật catalog/probe toàn chuỗi model linh hoạt trước giao WORKER theo `MODEL_LINH_HOAT.md`? | ĐÃ ĐƯỢC THAY THẾ — áp dụng `MODEL_LINH_HOAT.md`; L0.1 probe toàn chuỗi, TK-0040 ghi nhận model đạt |

---
## 6. GIẢ ĐỊNH / CHƯA XÁC MINH

| ID | Loại | Nội dung |
|---|---|---|
| A1 | Giả định | CYC-08 |
| A2 | Giả định | DEC-0031 |
| A3 | Giả định | Path upstream Q1 |
| A4 | CHƯA XN | 15 vs 16 ACTIVE |
| A5 | CHƯA XN | Free/paid `ag/` |
| A6 | Giả định | windows-latest đủ |
| A7 | Giả định | Điểm đo 9Router+relay khóa B1 |
| A8 | Giả định | DSC cố định `DSC-20261121-kzn1.md` |
| A9 | Giả định | Đ5 chạy phiên = L5.1; TK-0051 chỉ ghi bảng |
| A10 | Giả định | Gói Kaizen 2 thủ công tới Q11 |
| A11 | CHƯA XN | `grok-4.5` chưa có catalog; terra thiếu agent-tools mới; không tự ELIGIBLE |
| A12 | Giả định | Tách mục 8 → `DATA_CONTRACT.md` đủ “mục lớn” Đ4-A; nếu HARNESS vẫn quá lớn sau TK-0048, P4 sau/OWNER thêm task lead không mở rộng scope lúc này |

---

## 7. Khung Đợt 2–4 (giữ bảng ngắn)

| Đợt | Trọng tâm | Hướng |
|---|---|---|
| 2 — K4/K5 | An toàn còn lại, định tuyến, WORKER free | Sau Đợt 1 + E14; W1–W4; free chỉ sau đủ điều kiện; scan nguồn ngoài nếu thiếu |
| 3 — K6 | Hạ tầng / khôi phục | Theo số liệu tách lỗi Đợt 1; có thể thu nhỏ nếu hiếm |
| 4 — K7 | OWNER / Brainstorm | Sau `state`+`validate` ổn; ADVISOR/Basic Plan; cắt ngữ cảnh động chỉ nếu tách tĩnh chưa đủ |

---

## 8. Chọn model linh hoạt

Quy tắc đầy đủ, thứ tự dự phòng theo vai, xử lý lỗi giữa loop và ghi nhận nằm trong `MODEL_LINH_HOAT.md` mục 1–5. Đây là nguồn điều hành phân công; model đề xuất trong task chỉ là gợi ý.

Cổng chung cho mọi lượt giao: **POOL từ L0.1 (probe toàn chuỗi)**. Chỉ giao model có trong catalog và có ROUTE_CHECKS `agent-tools` OK mới nhất cho đúng tuyến. Ghi lần giao/đổi vào `SO_GIAO_VIEC.md`. REVIEWER phải khác họ với actual WORKER; actual trùng hoặc `UNKNOWN` thì dừng. Không dùng tên tuyến thay actual.

L0.1 probe toàn bộ chuỗi trong mục 2 của `MODEL_LINH_HOAT.md`; chỉ các model đủ điều kiện theo mục 3 mới vào POOL. Khi lỗi model/tuyến, chỉ fallback sang model kế tiếp đã ở POOL; đổi model không cộng/reset loop. Dừng khi cả chuỗi vai đó không còn model trong POOL.

---
## 9. SẴN SÀNG GIAO

| Task / cổng | Có thể giao khi |
|---|---|
| L0.1 | Trước lượt WORKER đầu: probe agent-tools toàn bộ chuỗi model ở `MODEL_LINH_HOAT.md` mục 2; lập POOL từ những model đạt mục 3. Không đủ kết quả thì không giao model ngoài POOL. |
| TK-0036 | Giao ngay sau L0.1 khi POOL có ít nhất một model WORKER và một REVIEWER khác họ; Q1 đã ĐỒNG Ý. Quét SHARED không secret trước khi chuyển nội dung. |
| TK-0037 | Sau TK-0036 merged; Q2/Q3/Q4 đã trả lời; Q8 về CYC-08 còn chờ OWNER; ghi E14 và RSK-0004 theo quyết định tách. |
| TK-0038 | Sau TK-0037 merged. |
| L1.1 / O1.1–O1.5 | Sau đặc tả TK-0038; ruleset, luật thẻ, secret scanning, push protection và quyền tài khoản riêng được xác minh trước baseline. |
| TK-0039 | Q5 khóa 5 mã và đích ACTIVE; Q14 nếu cần chốt scope/merge. |
| TK-0040 | Sau TK-0039; O2.1 nhóm E; ghi candidate/ROUTE_CHECKS đạt từ L0.1 theo `MODEL_LINH_HOAT.md`. |
| TK-0041 | Sau TK-0040; Q9. |
| TK-0042…0044 | Sau Bước 2 merge; O2.1; model lấy từ POOL chung. |
| TK-0045 | O3.1 lệnh trực tiếp OWNER trước khi mở PR; model lấy từ POOL chung. |
| TK-0046 | Sau khi E4/E6/E9/E22/E24 được chốt. |
| TK-0047 | Q13 YES; sau TK-0046. |
| TK-0048…0050 | L4.0 C9 PASS; Q10 cho TK-0049; Q6 nếu lựa chọn model Gemini bị ảnh hưởng bởi điều kiện free/paid. |
| TK-0051 | L5.1 xong và file đầu vào đã che có mặt. |
| TK-0052 | TK-0051; Q11/Q12. |
| Đ5-C | O5.* hoàn tất. |

Mọi task dùng cùng cổng POOL ở mục 8; model trong cột đề xuất không tự tạo quyền giao. Q15 đã được thay bằng chỉ dẫn `MODEL_LINH_HOAT.md`; không chặn TK-0036 nếu L0.1 đã có cặp model đủ điều kiện trong POOL.

---
## 10. Xử lý rà soát P3

| Dòng review | Đã sửa / chuyển OWNER | Cách xử lý |
|---|---|---|
| TK-0036b sai pattern | Đã sửa | Đổi thành **TK-0037** (bắt buộc); bỏ hậu tố chữ |
| B0b/B1a overlap STATE + 2 lead/ | Đã sửa | B0b=TK-0037; B1a=TK-0038 chỉ ghi `baseline_session_spec.md`; không còn “nếu có” |
| TK-0036 goal/scope lệch; O0.5 một merge | Đã sửa | TK-0036 chỉ H0–H4; TK-0037 DSC/DEC/STATE; O0.5+O0.6 = 2 merge |
| Thiếu trường schema | Đã sửa | Mỗi TK có đủ required schema |
| DSC placeholder | Đã sửa | `05_memory/discussions/2026/DSC-20261121-kzn1.md` |
| TK-0038 không hợp assignee/scope | Đã sửa | Chạy phiên/ảnh → L1.1; TK-0038 chỉ file spec cố định |
| TK-0039 vượt 5 file / follow-up | Đã sửa + Q14 | Tách TK-0039 (5 DEC) và TK-0040 (STATE/catalog/H0); cập nhật 3 merge B2 |
| depends_on chứa O/E/lệnh | Đã sửa | Chỉ TK id; O/E → constraints/inputs/bảng OWNER |
| Bảng tổng vs chi tiết E/lệnh | Đã sửa | Đồng bộ; E/lệnh không nằm depends_on |
| C9 sau tách file | Đã sửa + Q13 | **TK-0047 C9 cuối B3**; ghi sai lệch KE_HOACH |
| Đ4-A thiếu mục lớn/neo | Đã sửa | Thêm `DATA_CONTRACT.md` + danh sách neo nghiệm thu |
| TK-0047 scope có điều kiện WORKER.md | Đã sửa | Scope cố định 3 file; không WORKER.md |
| TK-0049 chạy phiên / local scope | Đã sửa | L5.1 chạy; TK-0051 chỉ path checks cố định |
| Thiếu inputs/outputs path; phụ thuộc P1 | Đã sửa | inputs/write_scope path; P1 chỉ truy vết ở header |
| Assignee không theo mục 5 | Đã sửa | Cột vai `(đề xuất: …)` + W-ID khi xuất file |
| grok-4.5 chưa catalog / đủ điều kiện | Đã thay cổng từng dòng bằng POOL chung; Q15 được thay bởi chỉ dẫn OWNER về model linh hoạt | L0.1 probe toàn chuỗi; model chỉ dùng sau khi vào POOL |
| Tỉ lệ Gemini gắn cứng 7/14 | Đã sửa | Theo `SO_GIAO_VIEC.md` thực nhận |
| REVIEWER chỉ khác route | Đã sửa | Mục 8 preflight actual |
| Không secret trong plan | Đạt — giữ | Giữ scan; không path máy trong write_scope |
