---
schema: 1
id: SRC-0003
date: 2026-11-22
title: "Kế hoạch chi tiết Đợt Kaizen 1 (TK-0036→0052)"
decided_by: OWNER
related: [SRC-0002, SRC-0005, SRC-0006]
keywords: [kaizen, plan, dot-1]
---
<!-- ANCHOR: CONTEXT -->
## Context
Nguồn: OWNER cung cấp/duyệt trong phiên lập kế hoạch Kaizen, 2026-11-21–22; thư mục làm việc ngoài repo ghi là `<SHARED>`. scan: BLOCK báo nhầm (`tools/scan.py`, scan-core-1, luật `zone3_openai_token` khớp đuôi tên file `RSK-0004_agent-tag-and-merge-bypass.md`); OWNER duyệt giữ nguyên 2026-11-22.

# KẾ HOẠCH CHI TIẾT — ĐỢT KAIZEN 1 (P5)

- Pha: P4 sửa theo `REVIEW_P3_LUNA.md` (KHÔNG ĐẠT) · Grok · model phiên: `grok-4.5` · 2026-11-21
- P5 cập nhật theo `MODEL_LINH_HOAT.md` và OWNER_TRA_LOI.md · Luna · model phiên thực tế: GPT-6-luna · 2026-11-21
- Bản P2 lưu: `KE_HOACH_CHI_TIET_DOT1_v1.md`
- Căn cứ: `KE_HOACH_KAIZEN.md`, `KE_HOACH_TONG_THE_DOT1.md` (mục 5), `SO_GIAO_VIEC.md`, `origin/main @ 15b030460a6771e09cfe86e6920aef13b75c2073`
- Ngoài Git trong `<SHARED>`; KHÔNG tạo nhánh, KHÔNG PR, KHÔNG sửa repo

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

## 1. Bảng tổng task (chỉ WORKER/LEAD-repo)

| TK | Bước | Nhánh | Hạng | Người nhận (đề xuất) | REVIEWER (đề xuất) | W-ID file | depends_on | Batch | Token |
|---|---|---|---|---|---|---|---|---|---|
| TK-0036 | Đ0 | lead/ | T1 | WORKER (đề xuất: ag/gemini-3.8-flash) `Q-GEMINI-TIER` | REVIEWER (đề xuất: cx/gpt-6.1-terra) | W1 | [] | B0a | nhẹ |
| TK-0037 | Đ0 | lead/ | T1 | WORKER (đề xuất: xai/grok-4.5) | REVIEWER (đề xuất: ag/gemini-3.8-flash) | W1 | [TK-0036] | B0b | nhẹ |
| TK-0038 | Đ1 | lead/ | T1 | WORKER (đề xuất: ag/gemini-3.8-flash) `Q-GEMINI-TIER` | REVIEWER (đề xuất: xai/grok-4.5) | W1 | [TK-0037] | B1a | nhẹ |
| TK-0039 | Đ2 | lead/ | T1 | WORKER (đề xuất: ag/gemini-3.8-flash) `Q-GEMINI-TIER` | REVIEWER (đề xuất: cx/gpt-6.1-terra) | W1 | [TK-0038] | B2a | nhẹ |
| TK-0040 | Đ2 | lead/ | T1 | WORKER (đề xuất: ag/gemini-3.8-flash) `Q-GEMINI-TIER` | REVIEWER (đề xuất: xai/grok-4.5) | W2 | [TK-0039] | B2b | nhẹ |
| TK-0041 | Đ2 | upgrade/ | T2 | WORKER (đề xuất: xai/grok-4.5) | REVIEWER (đề xuất: ag/gemini-3.8-flash) | W1 | [TK-0040] | B2c | nhẹ–vừa |
| TK-0042 | Đ3a | upgrade/ | T2 | WORKER (đề xuất: xai/grok-4.5) | REVIEWER (đề xuất: ag/gemini-3.8-flash) | W1 | [TK-0041] | B3a | vừa |
| TK-0043 | Đ3 | task/ | T2 | WORKER (đề xuất: xai/grok-4.5) | REVIEWER (đề xuất: ag/gemini-3.8-flash) | W1 | [TK-0042] | B3b | nặng |
| TK-0044 | Đ3 | task/ | T2 | WORKER (đề xuất: cx/gpt-6.1-terra) | REVIEWER (đề xuất: ag/gemini-3.8-flash) | W2 | [TK-0043] | B3c | vừa–nặng |
| TK-0045 | Đ3 | task/ | T2 | WORKER (đề xuất: xai/grok-4.5) | REVIEWER (đề xuất: ag/gemini-3.8-flash) | W1 | [TK-0044] | B3d | nặng |
| TK-0046 | Đ3b | upgrade/ | T2 | WORKER (đề xuất: cx/gpt-6.1-terra) | REVIEWER (đề xuất: ag/gemini-3.8-flash) | W2 | [TK-0045] | B3e | vừa |
| TK-0047 | Đ3-C9 | task/ | T2 | WORKER (đề xuất: xai/grok-4.5) | REVIEWER (đề xuất: ag/gemini-3.8-flash) | W1 | [TK-0046] | B3f | vừa–nặng |
| TK-0048 | Đ4-A | upgrade/ | T2 | WORKER (đề xuất: ag/gemini-3.8-flash) `Q-GEMINI-TIER` | REVIEWER (đề xuất: cx/gpt-6.1-terra) | W1 | [TK-0047] | B4a | vừa |
| TK-0049 | Đ4-B | upgrade/ | T1 | WORKER (đề xuất: ag/gemini-3.8-flash) `Q-GEMINI-TIER` | REVIEWER (đề xuất: xai/grok-4.5) | W2 | [TK-0048] | B4b | vừa |
| TK-0050 | Đ4-C | task/ | T2 | WORKER (đề xuất: xai/grok-4.5) | REVIEWER (đề xuất: ag/gemini-3.8-flash) | W1 | [TK-0049] | B4c | nặng |
| TK-0051 | Đ5-A | lead/ | T1 | WORKER (đề xuất: ag/gemini-3.8-flash) `Q-GEMINI-TIER` | REVIEWER (đề xuất: cx/gpt-6.1-terra) | W2 | [TK-0050] | B5a | nhẹ |
| TK-0052 | Đ5-B | lead/ | T1 | WORKER (đề xuất: ag/gemini-3.8-flash) `Q-GEMINI-TIER` | REVIEWER (đề xuất: xai/grok-4.5) | W1 | [TK-0051] | B5b | nhẹ–vừa |

Đ5-C: cổng OWNER — không cấp TK.

**Tỉ lệ Gemini:** không gắn cứng. Mỗi lượt giao ghi `SO_GIAO_VIEC.md`; cột “thực nhận” là nguồn tính ~50% WORKER Gemini và LEAD 2:1.

---

## 2. Batch `CYC_08_BATCHES`

```text
## CYC-08 batches
- B0a | tasks: TK-0036 | after: none
- B0b | tasks: TK-0037 | after: B0a
- B1a | tasks: TK-0038 | after: B0b
- B2a | tasks: TK-0039 | after: B1a
- B2b | tasks: TK-0040 | after: B2a
- B2c | tasks: TK-0041 | after: B2b
- B3a | tasks: TK-0042 | after: B2c
- B3b | tasks: TK-0043 | after: B3a
- B3c | tasks: TK-0044 | after: B3b
- B3d | tasks: TK-0045 | after: B3c
- B3e | tasks: TK-0046 | after: B3d
- B3f | tasks: TK-0047 | after: B3e
- B4a | tasks: TK-0048 | after: B3f
- B4b | tasks: TK-0049 | after: B4a
- B4c | tasks: TK-0050 | after: B4b
- B5a | tasks: TK-0051 | after: B4c
- B5b | tasks: TK-0052 | after: B5a
```

Mỗi batch một task → zero-overlap; ≤1 `lead/` và ≤1 `upgrade/` mở nhờ tuần tự.

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

---

## 4. Task đủ trường `task.schema.json`

Chu kỳ: `CYC-08` (A1). `origin` trước DEC merge: `01_plan/PLAN.md#CYC_08`; sau TK-0037: `DEC-0031`.  
`fixes`: `""` mọi task dưới. `log_level`/`max_loops` tùy chọn — khi xuất file: `LOOP`, `3` trừ khi ghi khác.

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

### TK-0039 — Retire đúng 5 DEC (đề xuất mặc định; khóa sau O2.2)

Đề xuất mặc định (chờ O2.2): `DEC-0007`, `DEC-0012`, `DEC-0014`, `DEC-0028`, `DEC-0029`.

```yaml
schema: 1
id: TK-0039
cycle: CYC-08
origin: "DEC-0031"
assignee: W1
goal: "Ghi RETIRED cho dung 5 DEC OWNER da chot (mac dinh 0007 0012 0014 0028 0029)"
write_scope:
  - 04_control/decisions/DEC-0007_cyc-01-reviewer-claude.md
  - 04_control/decisions/DEC-0012_cyc-02-reviewer-gemini.md
  - 04_control/decisions/DEC-0014_cyc-02-pr20-not-a-review-round.md
  - 04_control/decisions/DEC-0028_tk-0018-source-handoff.md
  - 04_control/decisions/DEC-0029_split-tk-0033-session-detector.md
constraints:
  - "Chi 5 file trong write_scope; chuyen kho lanh neu can thi cung PR nhung khong them path ngoai 5 file status — neu bat buoc path superseded/, tach PR lead/ moi sau khi OWNER cap nhat Q14"
  - "O2.2 phai khoa dung 5 ma truoc khi giao; neu doi ma, cap nhat write_scope truoc Run"
inputs:
  - 04_control/STATE.md
  - 04_control/decisions/DEC-0007_cyc-01-reviewer-claude.md
  - 04_control/decisions/DEC-0012_cyc-02-reviewer-gemini.md
  - 04_control/decisions/DEC-0014_cyc-02-pr20-not-a-review-round.md
  - 04_control/decisions/DEC-0028_tk-0018-source-handoff.md
  - 04_control/decisions/DEC-0029_split-tk-0033-session-detector.md
read_also:
  - "harness/rules/LEAD.md"
line_budget: 150
verify: "python -m pytest -q --tb=line tools/tests"
done_when:
  - "Moi DEC trong scope co dong RETIRED moi nhat"
  - "Khong sua DEC ngoai danh sach"
size: "1 session · 5 files"
depends_on: [TK-0038]
fixes: ""
```

### TK-0040 — Catalog model Đợt 1 + STATE + H0 nhóm E

```yaml
schema: 1
id: TK-0040
cycle: CYC-08
origin: "DEC-0031"
assignee: W2
goal: "Them code catalog cho model Dot1 dang dung va DeepSeek/Nano UNQUALIFIED; rut STATE muc 3; cap nhat trang thai nhom E Buoc 3 tren H0"
write_scope:
  - 04_control/MODEL_CATALOG.md
  - 04_control/STATE.md
  - 05_memory/upstream/00_tong_quan_upstream.md
constraints:
  - "Them/cap nhat code grok-4.5 (va alias xai/grok-4.5); dam bao gpt-6.1-terra va gemini-3.8-flash-n/alias con dung; them DeepSeek va Nvidia Nano o availability unconfirmed/UNQUALIFIED"
  - "Khong danh availability confirmed neu chua co ROUTE_CHECKS agent-tools OK moi; L0.1 la tien quyet ghi vao catalog khi co"
  - "Khong xoa muc catalog cu"
inputs:
  - 04_control/MODEL_CATALOG.md
  - 04_control/STATE.md
  - 05_memory/upstream/00_tong_quan_upstream.md
  - 04_control/decisions/DEC-0007_cyc-01-reviewer-claude.md
read_also:
  - "harness/MODEL_POLICY.md"
  - "harness/schemas/model_catalog.schema.json"
line_budget: 250
verify: "python -m pytest -q --tb=line tools/tests"
done_when:
  - "Catalog co grok-4.5, DeepSeek, Nvidia Nano; terra/gemini alias khong gay SAME_MODEL sai"
  - "STATE muc 3 gon sau retire"
  - "H0 nhom E B3 co trang thai theo O2.1"
size: "1 session · 3 files"
depends_on: [TK-0039]
fixes: ""
```

### TK-0041 — Gộp mục 9 + VERSION

```yaml
schema: 1
id: TK-0041
cycle: CYC-08
origin: "DEC-0031"
assignee: W1
goal: "Gop harness muc 9 theo REVIEW_SECTION_9; tang VERSION khop HARNESS"
write_scope:
  - harness/HARNESS.md
  - harness/rules/LEAD.md
  - harness/VERSION
  - harness/tools/README.md
constraints:
  - "Chi van ban khung; khong code script moi"
  - "Moi PR upgrade/ tang VERSION mot lan"
inputs:
  - harness/HARNESS.md
  - harness/rules/LEAD.md
  - harness/VERSION
  - harness/tools/README.md
read_also:
  - "harness/tools/README.md#REVIEW_SECTION_9"
line_budget: 300
verify: "python -m pytest -q --tb=line tools/tests"
done_when:
  - "VERSION khop dong phien ban HARNESS"
  - "Muc 9 phan anh gop dong 1-3 OWNER da chon huong"
size: "1 session · 4 files"
depends_on: [TK-0040]
fixes: ""
```

### TK-0042 — Đ3a quy ước schema + CONVENTIONS

```yaml
schema: 1
id: TK-0042
cycle: CYC-08
origin: "DEC-0031"
assignee: W1
goal: "Schema run MINOR theo E7/E21; CONVENTIONS ma 0/1/2/3 va bang loi E5/E16/E18; chi van ban+schema"
write_scope:
  - harness/schemas/run.schema.json
  - harness/schemas/EVOLUTION.md
  - 01_plan/SPEC_TOOLS.md
  - harness/VERSION
  - harness/HARNESS.md
constraints:
  - "Khong viet tools/*.py trong task nay"
  - "O2.1 phai da chap E5 E7 E16 E18 E21 (ghi o inputs H0)"
inputs:
  - harness/schemas/run.schema.json
  - 01_plan/SPEC_TOOLS.md
  - 05_memory/upstream/00_tong_quan_upstream.md
  - harness/VERSION
read_also:
  - "01_plan/SPEC_TOOLS.md#CONVENTIONS"
  - "harness/MODEL_POLICY.md#SAME_MODEL"
line_budget: 350
verify: "python -m pytest -q --tb=line tools/tests"
done_when:
  - "run.schema phan anh model list/ngu nghia E21 va khoa loai bang chung"
  - "CONVENTIONS co ma 3 va bang loi"
  - "C12 dat"
size: "1 session · 5 files"
depends_on: [TK-0041]
fixes: ""
```

### TK-0043 — validate lõi C1–C3 + SAME_MODEL (warn)

```yaml
schema: 1
id: TK-0043
cycle: CYC-08
origin: "DEC-0031"
assignee: W1
goal: "Implement tools/validate.py cot loi C1-C3 va SAME_MODEL; che do canh bao mac dinh"
write_scope:
  - tools/validate.py
  - tools/tests/test_validate_core.py
  - tools/README.md
constraints:
  - "Khong sua .github/"
  - "E20: neu sua test cu, khai bao ten test trong constraints truoc Run; mac dinh khong sua test cu"
inputs:
  - harness/schemas/run.schema.json
  - 01_plan/SPEC_TOOLS.md
  - harness/HARNESS.md
  - tools/README.md
read_also:
  - "harness/HARNESS.md"
  - "harness/MODEL_POLICY.md#SAME_MODEL"
line_budget: 400
verify: "python -m pytest -q --tb=line tools/tests/test_validate_core.py"
done_when:
  - "validate.py chay duoc; test_validate_core PASS"
  - "Mac dinh warn; SAME_MODEL kiem tap model REVIEWER khong giao WORKER"
size: "1 session · 3 files · code"
depends_on: [TK-0042]
fixes: ""
```

### TK-0044 — Kiểm trôi

```yaml
schema: 1
id: TK-0044
cycle: CYC-08
origin: "DEC-0031"
assignee: W2
goal: "Bon kiem troi: <=1 lead/ mo; DEC lien tuc; VERSION; STATE/C6"
write_scope:
  - tools/drift_check.py
  - tools/tests/test_drift_check.py
  - tools/validate.py
  - tools/README.md
constraints:
  - "Tuan tu sau TK-0043; khong song song cung write_scope"
inputs:
  - tools/validate.py
  - 04_control/STATE.md
  - harness/VERSION
  - harness/HARNESS.md
read_also:
  - "harness/HARNESS.md"
line_budget: 300
verify: "python -m pytest -q --tb=line tools/tests/test_drift_check.py"
done_when:
  - "Bon kiem troi chay tu dong qua validate hoac drift_check"
size: "1 session · 4 files"
depends_on: [TK-0043]
fixes: ""
```

### TK-0045 — CI Windows + pre-push secrets

```yaml
schema: 1
id: TK-0045
cycle: CYC-08
origin: "DEC-0031"
assignee: W1
goal: "CI verify windows-latest tren PR; pre-push detect-secrets; chan exit 3; permissions contents read"
write_scope:
  - .github/workflows/verify.yml
  - tools/hooks/pre-push
  - tools/tests/test_hooks_secret.py
  - tools/requirements.txt
  - tools/README.md
constraints:
  - "CAM mo PR truoc khi O3.1 lenh truc tiep OWNER da co van ban"
  - "Khong cap secret cho job CI"
inputs:
  - .github/workflows/check.yml
  - tools/hooks/pre-push
  - 01_plan/SPEC_TOOLS.md
  - tools/requirements.txt
read_also:
  - "harness/MAIN_PROTECTION.md"
  - "harness/tools/PREFLIGHT.md"
line_budget: 350
verify: "python -m pytest -q --tb=line tools/tests/test_hooks_secret.py"
done_when:
  - "verify.yml runs-on windows-latest; permissions contents read"
  - "Hook hieu exit 3 va chan; test PASS"
size: "1 session · 5 files"
depends_on: [TK-0044]
fixes: ""
```

### TK-0046 — Đ3b thi hành văn bản

```yaml
schema: 1
id: TK-0046
cycle: CYC-08
origin: "DEC-0031"
assignee: W2
goal: "Template diem dung E4; cach ly verify E6; LF/raw E9/E22; binary allowlist E24; VERSION"
write_scope:
  - harness/rules/WORKER.md
  - harness/templates/BLOCKS.md
  - harness/HARNESS.md
  - harness/VERSION
  - 01_plan/SPEC_TOOLS.md
constraints:
  - "O2.1 da chap E4 E6 E9 E22 E24"
  - "Bo diem dung khong ro model; chuyen preflight E21"
inputs:
  - harness/rules/WORKER.md
  - harness/templates/BLOCKS.md
  - 05_memory/upstream/00_tong_quan_upstream.md
  - harness/VERSION
read_also:
  - "05_memory/upstream/02_quyen_worker_va_phong_thu_injection.md"
line_budget: 300
verify: "python -m pytest -q --tb=line tools/tests"
done_when:
  - "Van ban khung co E4 E6 E9 E22 E24; C12 dat"
size: "1 session · 5 files"
depends_on: [TK-0045]
fixes: ""
```

### TK-0047 — C9 cuối Bước 3 (sai lệch KE_HOACH — Q13)

```yaml
schema: 1
id: TK-0047
cycle: CYC-08
origin: "DEC-0031"
assignee: W1
goal: "Implement va bat kiem C9 (con tro/origin DEC ACTIVE) trong validate; merge truoc moi tach file Buoc 4"
write_scope:
  - tools/validate.py
  - tools/tests/test_validate_c9.py
  - tools/README.md
constraints:
  - "Day la cuoi Buoc 3; SAI LECH KE_HOACH_KAIZEN (C9 nam Buoc 4) — OWNER Q13"
  - "Sau merge, C9 PASS tren main la dieu kien vao TK-0048"
inputs:
  - tools/validate.py
  - harness/HARNESS.md
  - harness/schemas/POINTER_GRAMMAR.md
  - 04_control/decisions/DEC-0031_kaizen-dot1.md
read_also:
  - "harness/HARNESS.md"
line_budget: 300
verify: "python -m pytest -q --tb=line tools/tests/test_validate_c9.py"
done_when:
  - "C9 chay trong validate; test_validate_c9 PASS"
  - "CI hoac validate tren main PASS C9 (L4.0 xac nhan)"
size: "1 session · 3 files"
depends_on: [TK-0046]
fixes: ""
```

### TK-0048 — Đ4-A tách HARNESS → RATIONALE + mục lớn

Khảo sát main @ 15b0304: HARNESS ~916 dòng; PHỤ LỤC A–D; mục lớn ứng viên tách thêm: §8 Hợp đồng dữ liệu → `harness/DATA_CONTRACT.md`; giữ neo `BATCH_RULES`, `CONCEPTS`, `THEORIES`.

```yaml
schema: 1
id: TK-0048
cycle: CYC-08
origin: "DEC-0031"
assignee: W1
goal: "Tach phu luc A-D sang RATIONALE.md; tach muc 8 sang DATA_CONTRACT.md; cap nhat neo/con tro; VERSION"
write_scope:
  - harness/HARNESS.md
  - harness/RATIONALE.md
  - harness/DATA_CONTRACT.md
  - harness/VERSION
  - harness/schemas/POINTER_GRAMMAR.md
constraints:
  - "L4.0: C9 PASS tren main truoc khi bat dau"
  - "Moi neo BATCH_RULES CONCEPTS THEORIES RATIONALE con resolve; cap nhat con tro cu"
  - "Khong doi bo phien chuan/diem do Buoc 1"
inputs:
  - harness/HARNESS.md
  - harness/VERSION
  - harness/schemas/POINTER_GRAMMAR.md
  - tools/validate.py
read_also:
  - "harness/HARNESS.md"
line_budget: 400
verify: "python -m tools.validate --checks C9 ; python -m pytest -q --tb=line tools/tests"
done_when:
  - "RATIONALE.md chua phu luc A-D; DATA_CONTRACT.md chua noi dung muc 8; HARNESS khong nhan doi"
  - "C9 PASS tren diff; danh sach neo da tach: CONCEPTS THEORIES BATCH_RULES + neo muc 8 moi"
size: "1 session · 5 files"
depends_on: [TK-0047]
fixes: ""
```

### TK-0049 — Đ4-B LEAD.md ≤1300 từ + prefix H3-2

```yaml
schema: 1
id: TK-0049
cycle: CYC-08
origin: "DEC-0031"
assignee: W2
goal: "Viet lai LEAD.md <=1300 tu; co dinh thu tu prefix H3-2; VERSION"
write_scope:
  - harness/rules/LEAD.md
  - harness/VERSION
  - harness/HARNESS.md
constraints:
  - "Dem tu: PowerShell Measure-Object -Word tren file UTF-8 (Q10)"
  - "Prefix: system prompt co dinh -> schema tool co dinh -> brief/ngu canh task"
  - "Khong sua WORKER.md trong task nay"
inputs:
  - harness/rules/LEAD.md
  - harness/VERSION
  - 05_memory/upstream/03_ha_tang_context_va_dieu_phoi_loop.md
read_also:
  - "harness/CHAT_UX.md"
line_budget: 200
verify: "python -c \"import pathlib; t=pathlib.Path('harness/rules/LEAD.md').read_text(encoding='utf-8').split(); assert len(t)<=1300, len(t)\""
done_when:
  - "LEAD.md <=1300 tu theo quy tac Q10"
  - "Thu tu prefix H3-2 nam trong LEAD.md; C12 dat"
size: "1 session · 3 files"
depends_on: [TK-0048]
fixes: ""
```

### TK-0050 — Đ4-C C5/C7/C12/C13 + H3-7 (không phải C9 lần đầu)

```yaml
schema: 1
id: TK-0050
cycle: CYC-08
origin: "DEC-0031"
assignee: W1
goal: "Them C5 C7 C12 C13 vao validate/CI; nen output H3-7 (ban du+hash; context tom tat+path)"
write_scope:
  - tools/validate.py
  - tools/tests/test_validate_c5_c13.py
  - tools/context_compact.py
  - tools/tests/test_context_compact.py
  - tools/README.md
constraints:
  - "C9 da co tu TK-0047; task nay khong thay the C9"
  - "Khong doi baseline Buoc 1"
inputs:
  - tools/validate.py
  - tools/tests/test_validate_c9.py
  - harness/rules/LEAD.md
  - .github/workflows/verify.yml
read_also:
  - "05_memory/upstream/03_ha_tang_context_va_dieu_phoi_loop.md"
line_budget: 400
verify: "python -m pytest -q --tb=line tools/tests/test_validate_c5_c13.py tools/tests/test_context_compact.py"
done_when:
  - "C5 C7 C12 C13 chay tu dong; H3-7 co test hash khop"
  - "LEAD.md van <=1300; >=8/14 C theo KE_HOACH Buoc 4"
size: "1 session · 5 files"
depends_on: [TK-0049]
fixes: ""
```

### TK-0051 — Ghi bảng đối chứng Đ5-A (không chạy phiên)

```yaml
schema: 1
id: TK-0051
cycle: CYC-08
origin: "DEC-0031"
assignee: W2
goal: "Ghi bang doi chung 6 luot remasure da che vao checks; actual model tu nhat ky phien do L5.1 cung cap"
write_scope:
  - 03_output/CYC-08/checks/remeasure_token_usage.md
constraints:
  - "Khong chay phien trong task; L5.1 da chay"
  - "Khong commit secret; khong path may tuyet doi"
  - "Khong suy actual tu ten tuyen"
inputs:
  - 03_output/CYC-08/checks/baseline_session_spec.md
  - 03_output/CYC-08/checks/baseline_token_usage.md
  - 03_output/CYC-08/checks/remeasure_local_summary.md
read_also:
  - "KE_HOACH_KAIZEN.md"
line_budget: 150
verify: "python -m pytest -q --tb=line tools/tests"
done_when:
  - "remeasure_token_usage.md du 6 luot hoac ly do khong so duoc tung luot"
  - "Moi dong co actual/provider/diem do/usage"
size: "1 session · 1 file"
depends_on: [TK-0050]
fixes: ""
```
Ghi chú inputs: `baseline_token_usage.md` và `remeasure_local_summary.md` do L1.1/L5.1 tạo (local → copy đã che vào `03_output/CYC-08/checks/` trước Run TK-0051). Nếu chưa có `baseline_token_usage.md` trên repo, LEAD thêm file đã che bằng lead/ nhỏ trước B5a (cùng path cố định) — không dùng `<project>.local` trong write_scope.

### TK-0052 — H0 trạng thái E + nháp gói Kaizen 2

```yaml
schema: 1
id: TK-0052
cycle: CYC-08
origin: "DEC-0031"
assignee: W1
goal: "Cap nhat trang thai E tren H0 theo bang chung Dot1; soan nhap goi Kaizen 2 theo README (thu cong neu chua co script)"
write_scope:
  - 05_memory/upstream/00_tong_quan_upstream.md
  - 03_output/CYC-08/checks/KAIZEN2_DRAFT.md
  - 04_control/STATE.md
constraints:
  - "Khong bia ten script; Q11: thu cong theo README_GOI_KAIZEN"
  - "Moi E doi trang thai phai co con tro PR/CI/so do"
inputs:
  - 05_memory/upstream/00_tong_quan_upstream.md
  - 03_output/CYC-08/checks/remeasure_token_usage.md
  - <SHARED>/README_GOI_KAIZEN.md
  - 04_control/STATE.md
read_also:
  - "03_output/CYC-08/checks/baseline_session_spec.md"
line_budget: 250
verify: "python -m pytest -q --tb=line tools/tests"
done_when:
  - "H0 cap nhat E co bang chung"
  - "KAIZEN2_DRAFT.md san trinh OWNER; STATE next action tro Dong Dot1/O5"
size: "1 session · 3 files"
depends_on: [TK-0051]
fixes: ""
```

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
