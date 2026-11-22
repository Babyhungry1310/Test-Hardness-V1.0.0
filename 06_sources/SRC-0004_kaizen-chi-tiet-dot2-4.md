---
schema: 1
id: SRC-0004
date: 2026-11-22
title: "Kế hoạch chi tiết Đợt Kaizen 2–4 (bản tạm, chốt sau Đ5)"
decided_by: OWNER
related: [SRC-0002, SRC-0003, SRC-0005]
keywords: [kaizen, plan, dot-2-4, provisional]
---
<!-- ANCHOR: CONTEXT -->
## Context
Nguồn: OWNER cung cấp/duyệt trong phiên lập kế hoạch Kaizen, 2026-11-21–22; thư mục làm việc ngoài repo ghi là `<SHARED>`. scan: ALLOW (`tools/scan.py`, scan-core-1).

# KẾ HOẠCH CHI TIẾT — ĐỢT KAIZEN 2–4 (Q3 gộp)

- Pha: **Q3b** (sau Claude xem lại Q3) · model: `grok-4.5` · 2026-11-21
- Bản Q3 lưu: `KE_HOACH_CHI_TIET_DOT2-4_q3.md`
- Nguồn: `PLAN_DOT2.md`, `PLAN_DOT3-4.md`, `REVIEW_DOT2.md`, `REVIEW_DOT3-4.md`, kết luận Claude Q3
- Trạng thái: **BẢN TẠM (PROVISIONAL)** — chốt lại sau Đ5 Dot1 + OWNER; **đọc riêng được** (không phụ thuộc “xem PLAN_* §…”)
- Mã tạm `D2-nn` / `D3-nn` / `D4-nn`; khi mở đợt remap → `TK-NNNN` (id + depends_on)
- `origin` tạm: `01_plan/PLAN.md#CYC_0N` cho đến khi DEC đợt ACTIVE (không dùng `DEC-DOT2`)
- Ngoài Git `<SHARED>`; KHÔNG nhánh/PR/sửa repo; không secret/path máy trong nội dung sẽ commit
- Model: đề xuất + POOL (`MODEL_LINH_HOAT`); tỉ lệ trên `SO_GIAO_VIEC.md`

---

## 0. Quy ước chung (sau hai bản rà)

1. `depends_on` chỉ mã task (`D2-01`… hoặc sau map `TK-NNNN`).
2. `write_scope` ≤5 path cố định; không placeholder/`nếu có`.
3. Vai `LEAD` / `WORKER` / `REVIEWER` + `(đề xuất: …)`; khi xuất file task: `assignee: W1`…
4. Tạo/sửa **DEC, STATE, MODEL_CATALOG#ROUTE_CHECKS, H0 trạng thái E**: ưu tiên **bảng OWNER/LEAD** (Luna CHAN). Task WORKER chỉ output kỹ thuật có path cố định.
5. Ngưỡng breaker/W1–W4/timeout: cổng OWNER trước khi hardcode vào code.
6. D4-06 (dynamic context): **không cấp task** tới DEC+path; chỉ cổng OWNER/LEAD.

---

# PHẦN A — ĐỢT 2 (K4 còn lại + K5) · CYC-09 giả định

## A1. Điều kiện vào

| # | Điều kiện |
|---|---|
| V1 | Dot1 đóng (Đ5-C + gói Kaizen 2) |
| V2 | E14=tách đã chốt (Dot1) |
| V3 | Ruleset/thẻ/secret scanning/push protection theo E14 |
| V4 | validate + C9 + CI Windows trên main |
| V5 | Catalog/POOL L0.1 còn hiệu lực hoặc probe lại |
| V6 | OWNER mở lại chu kỳ sản phẩm |

**V7 (tuyến free + backup)** — **không** chặn mở chu kỳ; bắt buộc trước task định tuyến (D2-02) / O2.2 (sửa CHAN readiness).

## A2. Chỉ số & bước

| Chỉ số | Nền | Đích (chốt sau Đ5) |
|---|---|---|
| M1 — Lượt giao/kiểm định hỏng vì model | ~3/5 (hồ sơ) | Giảm; số cụ thể sau Đ5 |
| M2 — Đạt lần đầu theo tuyến × hạng T0/T1 | Chưa có | Có bảng sau W1–W4 |
| M3 — CLAIM_MISMATCH theo tuyến × hạng | Chưa đo | Có; ngưỡng UNQUALIFIED do OWNER |
| M4 — Cost per Accepted Task free vs trả phí | Chưa đo | Cặp số cùng điểm đo |
| M5 — Tắc vì thiếu ruleset/E11 | Lịch sử RSK-0004 | 0 sự cố mới sau E11 |

| Bước | Mục tiêu | Token |
|---|---|---|
| B0 | DEC Đợt 2 + STATE + H0 (LEAD L2-00) | nhẹ |
| B1 | E11 CODEOWNERS / xác nhận bypass OWNER | nhẹ |
| B2 | ELIGIBILITY free + P4 (E10) | vừa |
| B3 | Hạng T0/T1/T2 + CLAIM_MISMATCH (E17) | nặng |
| B4 | W1–W4 + mẫu T0/T1 | vừa–nặng |
| B5 | Timeout / hạn mức / ngắt mạch free (H3-17) | vừa |
| B6 | Chạy W1–W4 (LEAD) + ghi kết quả | nặng |
| B7 | scan `06_sources/` (E2) | vừa |
| B8 | Đo M1–M4 | vừa |

## A3. OWNER / LEAD Đợt 2

| Mã | Ai | Việc |
|---|---|---|
| L2-00 | LEAD | Sau V1–V6: tạo `04_control/decisions/DEC-0032_kaizen-dot2.md`, cập nhật `04_control/STATE.md`, đánh dấu E nhóm Đ2 trên H0 (lead/ PR do LEAD) |
| O2.0 | OWNER | Xác nhận V1–V6; ruleset code-owner + bypass chỉ OWNER (E11 UI) |
| O2.1 | OWNER | Lệnh trực tiếp nếu PR chạm `.github/` |
| O2.2 | OWNER | Chốt P4 + danh sách tuyến free + backup trả phí (Q-D2-1/2) |
| O2.3 | OWNER | Chốt tên field hạng trong task.schema |
| O2.4 | OWNER | Chốt ngưỡng W1–W4 và cỡ bộ mẫu |
| O2.5 | OWNER | Chốt timeout tổng task theo hạng |
| O2.5b | OWNER | Chốt ngưỡng free breaker (đề xuất 3 lỗi/30p → ngừng 60p) trước D2-07 |
| O2.6 | OWNER | Merge tuần tự; ≤1 lead/ + ≤1 upgrade/ |
| O2.7 | OWNER | Duyệt đóng Đợt 2 / quyết Dot3 |
| L2.0 | LEAD | Probe POOL |
| L2.1 | LEAD | Chạy W1–W4; artifact `W1W4_LOCAL_SUMMARY.md` |
| L2.2 | LEAD | Ghi `SO_GIAO_VIEC.md` mỗi lượt |
| L2.3 | LEAD | Cập nhật MODEL_CATALOG/ROUTE_CHECKS + H0 từ `W1W4_RESULTS.md` |
| L2.4 | LEAD | Cập nhật STATE sau milestone B4/B8 |
| L2.5 | LEAD | Thu hẹp DEC-0018 theo E10 (DEC/RATIONALE) |

## A4. Bảng tổng task Đợt 2 (sau sửa)

| ID | Bước | Nhánh | Hạng | Người nhận (đề xuất) | REVIEWER (đề xuất) | W | depends_on | Batch |
|---|---|---|---|---|---|---|---|---|
| D2-01 | B1 | lead/ | T1 | WORKER (ag/gemini-3.8-flash) | REVIEWER (xai/grok-4.5) | W1 | [] | B1a |
| D2-02 | B2 | upgrade/ | T2 | WORKER (xai/grok-4.5) | REVIEWER (ag/gemini-3.8-flash) | W1 | [D2-01] | B2a |
| D2-03 | B3 | upgrade/ | T2 | WORKER (xai/grok-4.5) | REVIEWER (ag/gemini-3.8-flash) | W1 | [D2-02] | B3a |
| D2-04 | B3 | task/ | T2 | WORKER (xai/grok-4.5) | REVIEWER (ag/gemini-3.8-flash) | W2 | [D2-03] | B3b |
| D2-05 | B4 | lead/ | T1 | WORKER (ag/gemini-3.8-flash) | REVIEWER (cx/gpt-6.1-terra) | W1 | [D2-04] | B4a |
| D2-06 | B4 | task/ | T2 | WORKER (cx/gpt-6.1-terra) | REVIEWER (ag/gemini-3.8-flash) | W2 | [D2-05] | B4b |
| D2-07 | B5 | task/ | T2 | WORKER (xai/grok-4.5) | REVIEWER (ag/gemini-3.8-flash) | W1 | [D2-06] | B5a |
| D2-08 | B6 | lead/ | T1 | WORKER (ag/gemini-3.8-flash) | REVIEWER (xai/grok-4.5) | W1 | [D2-07] | B6a |
| D2-09 | B7 | task/ | T2 | WORKER (xai/grok-4.5) | REVIEWER (ag/gemini-3.8-flash) | W1 | [D2-08] | B7a |
| D2-10 | B8 | lead/ | T1 | WORKER (ag/gemini-3.8-flash) | REVIEWER (cx/gpt-6.1-terra) | W2 | [D2-09] | B8a |

```text
## CYC-09 batches
- B1a | tasks: D2-01 | after: L2-00
- B2a | tasks: D2-02 | after: B1a
- B3a | tasks: D2-03 | after: B2a
- B3b | tasks: D2-04 | after: B3a
- B4a | tasks: D2-05 | after: B3b
- B4b | tasks: D2-06 | after: B4a
- B5a | tasks: D2-07 | after: B4b
- B6a | tasks: D2-08 | after: B5a
- B7a | tasks: D2-09 | after: B6a
- B8a | tasks: D2-10 | after: B7a
```

## A5. Task Đợt 2 (đủ schema; id tạm)

### D2-01 — E11 văn bản + CODEOWNERS
```yaml
schema: 1
id: D2-01
cycle: CYC-09
origin: "01_plan/PLAN.md#CYC_09"
assignee: W1
goal: "Cap nhat luat E11 trong khung va CODEOWNERS; khong doi GitHub ruleset"
write_scope:
  - harness/rules/WORKER.md
  - harness/rules/REVIEWER.md
  - harness/MAIN_PROTECTION.md
  - .github/CODEOWNERS
  - 05_memory/upstream/00_tong_quan_upstream.md
constraints:
  - "O2.0 ruleset UI da xong; O2.1 neu PR cham .github/"
  - "Khong tao DEC/STATE trong task nay (L2-00)"
inputs:
  - .github/CODEOWNERS
  - harness/MAIN_PROTECTION.md
  - harness/rules/WORKER.md
  - 05_memory/upstream/02_quyen_worker_va_phong_thu_injection.md
read_also: ["harness/tools/PREFLIGHT.md"]
line_budget: 250
verify: "python -m pytest -q --tb=line tools/tests"
done_when:
  - "Van ban khop E11; CODEOWNERS cap nhat; H0 E11 trang thai theo O2.0 (LEAD L2-00/L2.4 chot dong neu can)"
size: "1 session · 5 files"
depends_on: []
fixes: ""
```

### D2-02 — E10 ELIGIBILITY + P4
```yaml
schema: 1
id: D2-02
cycle: CYC-09
origin: "01_plan/PLAN.md#CYC_09"
assignee: W1
goal: "Ghi ELIGIBILITY free co dieu kien va dinh nghia P4; VERSION"
write_scope:
  - harness/MODEL_POLICY.md
  - harness/HARNESS.md
  - harness/VERSION
  - 04_control/MODEL_CATALOG.md
constraints:
  - "O2.2/Q-D2-1/Q-D2-2 da chot P4 va danh sach free+backup"
  - "Khong sua DEC-0018 trong write_scope; L2.5 lam DEC rieng"
  - "Free: T0/T1 + W1-W4 + backup tra phi; khong REVIEWER chinh"
inputs:
  - harness/MODEL_POLICY.md
  - 04_control/MODEL_CATALOG.md
  - 05_memory/upstream/03_ha_tang_context_va_dieu_phoi_loop.md
  - 05_memory/upstream/00_tong_quan_upstream.md
read_also: ["MODEL_LINH_HOAT.md"]
line_budget: 350
verify: "python -m pytest -q --tb=line tools/tests"
done_when:
  - "ELIGIBILITY + P4 van ban; C12 VERSION"
size: "1 session · 4 files"
depends_on: [D2-01]
fixes: ""
```

### D2-03 — Hạng T0/T1/T2 schema
```yaml
schema: 1
id: D2-03
cycle: CYC-09
origin: "01_plan/PLAN.md#CYC_09"
assignee: W1
goal: "Them hang T0/T1/T2 vao task.schema + SPEC + thang leo; VERSION"
write_scope:
  - harness/schemas/task.schema.json
  - harness/schemas/EVOLUTION.md
  - 01_plan/SPEC_TOOLS.md
  - harness/HARNESS.md
  - harness/VERSION
constraints:
  - "Ten field hang dung O2.3"
  - "MINOR schema"
inputs:
  - harness/schemas/task.schema.json
  - 05_memory/upstream/03_ha_tang_context_va_dieu_phoi_loop.md
  - harness/VERSION
read_also: ["harness/schemas/EVOLUTION.md"]
line_budget: 300
verify: "python -m pytest -q --tb=line tools/tests"
done_when:
  - "Schema co enum hang; SPEC/HARNESS mo ta thang leo; C12"
size: "1 session · 5 files"
depends_on: [D2-02]
fixes: ""
```

### D2-04 — CLAIM_MISMATCH
```yaml
schema: 1
id: D2-04
cycle: CYC-09
origin: "01_plan/PLAN.md#CYC_09"
assignee: W2
goal: "Script CLAIM_MISMATCH sau luot WORKER; gan validate"
write_scope:
  - tools/claim_mismatch.py
  - tools/tests/test_claim_mismatch.py
  - tools/validate.py
  - tools/README.md
constraints:
  - "Khong sua .github/"
  - "CLAIM_MISMATCH khong retry cung tuyen free"
inputs:
  - tools/validate.py
  - 01_plan/SPEC_TOOLS.md
  - 05_memory/upstream/03_ha_tang_context_va_dieu_phoi_loop.md
  - harness/schemas/run.schema.json
read_also: ["tools/README.md"]
line_budget: 350
verify: "python -m pytest -q --tb=line tools/tests/test_claim_mismatch.py"
done_when:
  - "Script+test PASS; README mo ta"
size: "1 session · 4 files"
depends_on: [D2-03]
fixes: ""
```

### D2-05 — W1–W4 SPEC + index + 2 fixture mẫu (không STATE/catalog)
```yaml
schema: 1
id: D2-05
cycle: CYC-09
origin: "01_plan/PLAN.md#CYC_09"
assignee: W1
goal: "SPEC W1-W4; index mau; hai fixture task mau T0/T1 path co dinh"
write_scope:
  - 01_plan/SPEC_ROUTE_QUALIFICATION.md
  - 02_work/tasks/CYC-09/fixtures/W_SAMPLE_INDEX.md
  - 02_work/tasks/CYC-09/fixtures/SAMPLE_T0_format.md
  - 02_work/tasks/CYC-09/fixtures/SAMPLE_T1_logic.md
constraints:
  - "Nguong W dung O2.4; chua chot thi ghi CHO_OWNER"
  - "Khong ghi STATE/MODEL_CATALOG (L2.3/L2.4)"
  - "Han muc tuyen: chi mo ta trong SPEC; LEAD dien so vao catalog sau"
inputs:
  - 05_memory/upstream/03_ha_tang_context_va_dieu_phoi_loop.md
  - harness/MODEL_POLICY.md
  - 04_control/MODEL_CATALOG.md
read_also: ["05_memory/upstream/00_tong_quan_upstream.md"]
line_budget: 300
verify: "python -m pytest -q --tb=line tools/tests"
done_when:
  - "SPEC + INDEX + 2 SAMPLE ton tai; tieu chi W1-W4 ro"
size: "1 session · 4 files"
depends_on: [D2-04]
fixes: ""
```

### D2-06 — route_preflight
```yaml
schema: 1
id: D2-06
cycle: CYC-09
origin: "01_plan/PLAN.md#CYC_09"
assignee: W2
goal: "Preflight ELIGIBILITY/hang/han muc/backup; chan giao sai"
write_scope:
  - tools/route_preflight.py
  - tools/tests/test_route_preflight.py
  - tools/model_select.py
  - tools/README.md
constraints:
  - "Khong suy actual tu ten tuyen"
  - "Q-D2-6: ag/ chua duoc tinh free WORKER den khi OWNER tra loi"
inputs:
  - tools/model_select.py
  - 04_control/MODEL_CATALOG.md
  - harness/MODEL_POLICY.md
  - 01_plan/SPEC_ROUTE_QUALIFICATION.md
read_also: ["MODEL_LINH_HOAT.md"]
line_budget: 350
verify: "python -m pytest -q --tb=line tools/tests/test_route_preflight.py"
done_when:
  - "Preflight exit 0/1/2/3; test PASS"
size: "1 session · 4 files"
depends_on: [D2-05]
fixes: ""
```

### D2-07 — free circuit (ngưỡng OWNER)
```yaml
schema: 1
id: D2-07
cycle: CYC-09
origin: "01_plan/PLAN.md#CYC_09"
assignee: W1
goal: "Ngat mach/timeout free theo nguong O2.5/O2.5b; leo bac khi qua khung"
write_scope:
  - tools/free_circuit.py
  - tools/tests/test_free_circuit.py
  - tools/route_preflight.py
  - 01_plan/SPEC_ROUTE_QUALIFICATION.md
  - tools/README.md
constraints:
  - "Cam hardcode 3/30/60 neu O2.5b chua YES; doc tu SPEC/config"
  - "Chi free; breaker chung moi tuyen = Dot3"
inputs:
  - tools/route_preflight.py
  - 01_plan/SPEC_TOOLS.md
  - 05_memory/upstream/03_ha_tang_context_va_dieu_phoi_loop.md
read_also: ["01_plan/SPEC_ROUTE_QUALIFICATION.md"]
line_budget: 300
verify: "python -m pytest -q --tb=line tools/tests/test_free_circuit.py"
done_when:
  - "Test PASS; SPEC ghi nguong da chot"
size: "1 session · 5 files"
depends_on: [D2-06]
fixes: ""
```

### D2-08 — Bảng W1W4_RESULTS (không catalog/H0)
```yaml
schema: 1
id: D2-08
cycle: CYC-09
origin: "01_plan/PLAN.md#CYC_09"
assignee: W1
goal: "Ghi bang W1-W4 tu artifact L2.1; LEAD L2.3 cap nhat catalog/H0 sau"
write_scope:
  - 03_output/CYC-09/checks/W1W4_RESULTS.md
constraints:
  - "Khong chay W1-W4; khong sua MODEL_CATALOG/H0/STATE"
  - "Actual tu L2.1; Q-D2-6 gate cho ag/"
inputs:
  - 03_output/CYC-09/checks/W1W4_LOCAL_SUMMARY.md
  - 01_plan/SPEC_ROUTE_QUALIFICATION.md
  - 02_work/tasks/CYC-09/fixtures/W_SAMPLE_INDEX.md
read_also: ["harness/MODEL_POLICY.md"]
line_budget: 150
verify: "python -m pytest -q --tb=line tools/tests"
done_when:
  - "W1W4_RESULTS.md du tuyen ung vien x T0/T1"
size: "1 session · 1 file"
depends_on: [D2-07]
fixes: ""
```

### D2-09 — scan 06_sources
```yaml
schema: 1
id: D2-09
cycle: CYC-09
origin: "01_plan/PLAN.md#CYC_09"
assignee: W1
goal: "Mo rong tools/scan cho 06_sources/; cam clipboard/thu muc tam"
write_scope:
  - tools/scan.py
  - tools/tests/test_scan_sources.py
  - 06_sources/README.md
  - tools/README.md
  - harness/rules/LEAD.md
constraints:
  - "Q-D2-8; mo rong scan hien co"
inputs:
  - tools/scan.py
  - 06_sources/README.md
  - 05_memory/upstream/00_tong_quan_upstream.md
  - 05_memory/upstream/01_brainstorm_va_tra_cuu_ngoai.md
read_also: ["01_plan/SPEC_SCAN.md"]
line_budget: 350
verify: "python -m pytest -q --tb=line tools/tests/test_scan_sources.py tools/tests/test_scan_core.py"
done_when:
  - "Test sources PASS; README+LEAD.md mo ta quy trinh"
size: "1 session · 5 files"
depends_on: [D2-08]
fixes: ""
```

### D2-10 — DOT2_METRICS (không H0/STATE)
```yaml
schema: 1
id: D2-10
cycle: CYC-09
origin: "01_plan/PLAN.md#CYC_09"
assignee: W2
goal: "Tong hop M1-M4; LEAD L2.3/L2.4 cap nhat H0/STATE sau"
write_scope:
  - 03_output/CYC-09/checks/DOT2_METRICS.md
constraints:
  - "Cung diem do Dot1; khong sua H0/STATE"
inputs:
  - 03_output/CYC-09/checks/W1W4_RESULTS.md
  - 03_output/CYC-08/checks/remeasure_token_usage.md
  - 03_output/CYC-08/checks/baseline_session_spec.md
read_also: ["README_GOI_KAIZEN.md"]
line_budget: 200
verify: "python -m pytest -q --tb=line tools/tests"
done_when:
  - "DOT2_METRICS.md co M1-M4 va de xuat Dot3 thu nho/gop"
size: "1 session · 1 file"
depends_on: [D2-09]
fixes: ""
```

## A6. Câu hỏi OWNER Đợt 2

| ID | Câu hỏi |
|---|---|
| Q-D2-1 | Danh sách tuyến free ứng viên và tuyến trả phí dự phòng mặc định từng hạng? |
| Q-D2-2 | Định nghĩa P4 cụ thể? |
| Q-D2-3 | Tên field hạng trong `task.schema.json`? |
| Q-D2-4 | Ngưỡng W1–W4 và số task mẫu mỗi hạng? |
| Q-D2-5 | Timeout tổng task T0/T1/T2 và ngưỡng CLAIM_MISMATCH/FAIL → UNQUALIFIED? |
| Q-D2-6 | `ag/` free được làm WORKER T0/T1 sau W1–W4 hay vẫn cấm? |
| Q-D2-7 | CYC-09 khóa khi mở đợt? |
| Q-D2-8 | E2: bắt buộc mọi nguồn ngoài qua `06_sources/`+scan ngay Đợt 2, hay chỉ bật tooling? |
| Q-D2-9 | Chấp nhận ngưỡng breaker 3 lỗi/30p → ngừng 60p (O2.5b)? |

## A7. SẴN SÀNG GIAO Đợt 2
| Task | Cần |
|---|---|
| L2-00 | V1–V6 |
| D2-01 | L2-00; O2.0; O2.1 nếu `.github/` |
| D2-02 | O2.2, Q-D2-1, Q-D2-2 |
| D2-03 | O2.3 |
| D2-04 | D2-03 merged |
| D2-05 | O2.4 |
| D2-06 | D2-05; Q-D2-6 trước khi tính ag/ free |
| D2-07 | O2.5 + Q-D2-9 |
| L2.1→D2-08 | D2-05…07 trên main |
| L2.3 | sau D2-08 |
| D2-09 | Q-D2-8 |
| D2-10 | D2-08+D2-09 |

---

# PHẦN B — ĐỢT 3 (K6) · CYC-10 giả định

## B1. Điều kiện vào

| # | Điều kiện |
|---|---|
| V3-1 | Đợt 1 đóng; gói Đ5 phân biệt lỗi hạ tầng vs chất lượng/sẵn sàng (định nghĩa, mẫu số, điểm đo) |
| V3-2 | Đợt 2 đóng **hoặc** OWNER chốt thứ tự khác (Q-D3-5) |
| V3-3 | E18 / bảng lỗi thống nhất đã được chấp thuận (từ Dot1 B3) |
| V3-4 | OWNER chốt E13 / phạm vi K6 (Q-D3-1, Q-D3-2); nếu lỗi hạ tầng hiếm → thu nhỏ/gộp |
| V3-5 | Nếu H4-6 đo qua relay: OWNER duyệt đối chứng khi đổi điểm đo (Q-D3-3) |
| V3-6 | Không đưa credential/token/session/cấu hình máy vào repo |

## B2. Mục tiêu / chỉ số

| Chỉ số | Mô tả |
|---|---|
| K6-M1 | Số lần chờ OWNER vì lỗi hạ tầng (E18) / tổng lượt run — cùng định nghĩa Đ5 |
| K6-M2 | Tỷ lệ phiên cũ bị deny sau handoff |
| K6-M3 | Thay cấu hình một tuyến không ảnh hưởng tuyến khác (pass/fail kiểm) |
| K6-M4 | Tỷ lệ log phê duyệt đủ trường H4-3 |

Không đặt ngưỡng số trước khi đọc gói Đ5.

| Bước | Việc | Xong khi |
|---|---|---|
| 0 | Phân loại Đ5 + OWNER chọn đủ/thu nhỏ/gộp | Baseline + quyết định phạm vi |
| 1 | Đặc tả breaker/E18/retry/denylist/handoff | SPEC + OWNER chốt policy còn mở |
| 2 | Breaker chung + cô lập tuyến | Test transition/retry/reset/isolation |
| 3 | Relay version/hash + deny phiên cũ | Test deny/pass |
| 4 | Docs runtime + runbook token hết hạn (credential giả) | Không secret trong repo |
| 5 | Audit native approval log | Coverage md |
| 5b | Logger tối thiểu (chỉ nếu thiếu native) | Test logger |
| 6 | Đo lại + gói thẩm định | Outcome truy nguồn được |

## B3. OWNER / LEAD Đợt 3

| Thời điểm | OWNER | LEAD |
|---|---|---|
| Trước Đ3 | Quyết thứ tự Đ2/3 theo Đ5; chốt E13/phạm vi/điểm đo (Q-D3-1…5) | Phân loại evidence; dừng nếu thiếu E18/baseline |
| Trong Đ3 | Merge tuần tự; duyệt đổi relay/điểm đo; quyết quyền/credential/logging (Q-D3-4) | Preflight schema/model/scope; ≤1 lead/ + ≤1 upgrade/; review |
| Đóng Đ3 | Duyệt gói thẩm định / trạng thái E | Ghi outcome; không sửa evidence lịch sử |
| Credential GitHub hết hạn | OWNER cập nhật ngoài repo | Task chỉ runbook + test giả — không cấp task dán token |

## B4. Bảng tổng task

| ID | Bước | Nhánh | Hạng | Người nhận (đề xuất) | REVIEWER (đề xuất) | W | depends_on | Batch |
|---|---|---|---|---|---|---|---|---|
| D3-01 | 0 | lead/ | T1 | LEAD (xai/grok-4.5) | REVIEWER (ag/gemini-3.8-flash) | W1 | [] | B0 |
| D3-02 | 1 | lead/ | T1 | LEAD (cx/gpt-6.1-terra) | REVIEWER (ag/gemini-3.8-flash) | W1 | [D3-01] | B1 |
| D3-03 | 2 | task/ | T2 | WORKER (xai/grok-4.5) | REVIEWER (ag/gemini-3.8-flash) | W1 | [D3-02] | B2 |
| D3-04 | 3 | task/ | T2 | WORKER (cx/gpt-6.1-terra) | REVIEWER (ag/gemini-3.8-flash) | W2 | [D3-03] | B3 |
| D3-05 | 4 | upgrade/ | T1 | WORKER (ag/gemini-3.8-flash) | REVIEWER (xai/grok-4.5) | W1 | [D3-02, D3-04] | B4 |
| D3-06 | 5 | lead/ | T1 | LEAD (xai/grok-4.5) | REVIEWER (ag/gemini-3.8-flash) | W1 | [D3-02] | B5 |
| D3-08 | 5b | task/ | T2 | WORKER (xai/grok-4.5) | REVIEWER (ag/gemini-3.8-flash) | W2 | [D3-06] | B5b |
| D3-07 | 6 | lead/ | T1 | LEAD (xai/grok-4.5) | REVIEWER (cx/gpt-6.1-terra) | W1 | [D3-03, D3-04, D3-05, D3-06] | B6 |

`D3-08` (đổi từ D3-06b): chỉ mở nếu Q-D3-4 = thiếu native log. Tuần tự; D3-04 after merge D3-03 (`tools/README.md`).

```text
## CYC-10 batches
- B0 | tasks: D3-01 | after: none
- B1 | tasks: D3-02 | after: B0
- B2 | tasks: D3-03 | after: B1
- B3 | tasks: D3-04 | after: B2
- B4 | tasks: D3-05 | after: B3
- B5 | tasks: D3-06 | after: B1
- B5b | tasks: D3-08 | after: B5
- B6 | tasks: D3-07 | after: B4,B5
```
≤1 `lead/` mở: không chạy B5 song song B0/B1 nếu cùng lúc mở lead khác.

## B5. Task Đợt 3 (đủ schema)

### D3-01
```yaml
schema: 1
id: D3-01
cycle: CYC-10
origin: "01_plan/PLAN.md#CYC_10"
assignee: W1
goal: "Phan loai so do D5 va de xuat pham vi K6 (du/thu nho/gop)"
write_scope:
  - 03_output/CYC-10/checks/k6_scope_baseline.md
constraints:
  - "Khong sua evidence lich su; OWNER quyet pham vi; khong suy nguong tu mau thieu"
inputs:
  - 03_output/CYC-08/checks/remeasure_token_usage.md
  - 03_output/CYC-09/checks/DOT2_METRICS.md
  - 05_memory/upstream/00_tong_quan_upstream.md
  - 05_memory/upstream/04_nhat_ky_kiem_toan_va_quan_tri_van_hanh.md
read_also:
  - 05_memory/upstream/03_ha_tang_context_va_dieu_phoi_loop.md
line_budget: 150
verify: "python -m pytest -q --tb=line tools/tests"
done_when:
  - "Baseline, mau so, dinh nghia, khuyen nghi pham vi ro trong k6_scope_baseline.md"
size: "1 session · 1 file"
depends_on: []
fixes: ""
```

### D3-02
```yaml
schema: 1
id: D3-02
cycle: CYC-10
origin: "01_plan/PLAN.md#CYC_10"
assignee: W1
goal: "Dac ta breaker chung, E18, retry/reset, denylist/handoff, test matrix"
write_scope:
  - 01_plan/SPEC_INFRA_RECOVERY.md
constraints:
  - "Khong dung endpoint/credential/session that; khong tu quyet chinh sach OWNER"
inputs:
  - 03_output/CYC-10/checks/k6_scope_baseline.md
  - 01_plan/SPEC_TOOLS.md
  - 05_memory/upstream/03_ha_tang_context_va_dieu_phoi_loop.md
read_also:
  - 05_memory/upstream/00_tong_quan_upstream.md
line_budget: 180
verify: "python -m pytest -q --tb=line tools/tests"
done_when:
  - "SPEC co state machine, retry/reset, handoff, chu the quyet dinh, test matrix"
size: "1 session · 1 file"
depends_on: [D3-01]
fixes: ""
```

### D3-03
```yaml
schema: 1
id: D3-03
cycle: CYC-10
origin: "01_plan/PLAN.md#CYC_10"
assignee: W1
goal: "Implement circuit breaker chung va kiem route isolation"
write_scope:
  - tools/circuit_breaker.py
  - tools/tests/test_circuit_breaker.py
  - tools/README.md
constraints:
  - "Khong doi nghia E18/policy ngoai SPEC; khong cham .github/"
inputs:
  - 01_plan/SPEC_INFRA_RECOVERY.md
  - 01_plan/SPEC_TOOLS.md
  - tools/README.md
read_also:
  - harness/schemas/run.schema.json
line_budget: 350
verify: "python -m pytest -q --tb=line tools/tests/test_circuit_breaker.py"
done_when:
  - "Transitions/retry/reset/isolation dat; README mo ta"
size: "1 session · 3 files"
depends_on: [D3-02]
fixes: ""
```

### D3-04
```yaml
schema: 1
id: D3-04
cycle: CYC-10
origin: "01_plan/PLAN.md#CYC_10"
assignee: W2
goal: "Relay version/hash, deny phien cu, gate phien moi"
write_scope:
  - tools/relay_handoff.py
  - tools/tests/test_relay_handoff.py
  - tools/README.md
constraints:
  - "Khong commit binary/credential/config ca nhan; khong doi diem do am tham"
  - "Tuan tu sau D3-03 (cung tools/README.md)"
inputs:
  - 01_plan/SPEC_INFRA_RECOVERY.md
  - tools/circuit_breaker.py
  - 05_memory/upstream/03_ha_tang_context_va_dieu_phoi_loop.md
read_also:
  - 05_memory/upstream/00_tong_quan_upstream.md
line_budget: 350
verify: "python -m pytest -q --tb=line tools/tests/test_relay_handoff.py"
done_when:
  - "Test deny/pass/version/hash PASS; handoff an toan"
size: "1 session · 3 files"
depends_on: [D3-03]
fixes: ""
```

### D3-05
```yaml
schema: 1
id: D3-05
cycle: CYC-10
origin: "01_plan/PLAN.md#CYC_10"
assignee: W1
goal: "Mo ta relay/Codex CLI/pwsh va runbook token GitHub het han bang credential gia"
write_scope:
  - harness/HARNESS.md
  - harness/tools/PREFLIGHT.md
constraints:
  - "Khong yeu cau dan token; credential that = OWNER ngoai repo"
inputs:
  - 01_plan/SPEC_INFRA_RECOVERY.md
  - harness/MAIN_PROTECTION.md
  - 05_memory/upstream/03_ha_tang_context_va_dieu_phoi_loop.md
read_also:
  - harness/VERSION
line_budget: 250
verify: "python -m pytest -q --tb=line tools/tests"
done_when:
  - "Version/hash/vai tro/phuc hoi ro; khong secret trong diff"
size: "1 session · 2 files"
depends_on: [D3-02, D3-04]
fixes: ""
```

### D3-06
```yaml
schema: 1
id: D3-06
cycle: CYC-10
origin: "01_plan/PLAN.md#CYC_10"
assignee: W1
goal: "Kiem native approval log vs H4-3; ghi coverage"
write_scope:
  - 03_output/CYC-10/checks/approval_log_coverage.md
constraints:
  - "Khong log secret; liet ke command, require_escalated, approve/reject, approver, timestamp"
inputs:
  - 01_plan/SPEC_INFRA_RECOVERY.md
  - 05_memory/upstream/04_nhat_ky_kiem_toan_va_quan_tri_van_hanh.md
  - harness/tools/PREFLIGHT.md
read_also:
  - 05_memory/upstream/00_tong_quan_upstream.md
line_budget: 200
verify: "python -m pytest -q --tb=line tools/tests"
done_when:
  - "Coverage md ket luan du/thieu tung truong H4-3"
size: "1 session · 1 file"
depends_on: [D3-02]
fixes: ""
```

### D3-08 (optional logger; chỉ khi Q-D3-4 thiếu native)
```yaml
schema: 1
id: D3-08
cycle: CYC-10
origin: "01_plan/PLAN.md#CYC_10"
assignee: W2
goal: "Logger phe duyet toi thieu du truong H4-3 khi native thieu"
write_scope:
  - tools/approval_log.py
  - tools/tests/test_approval_log.py
  - tools/README.md
constraints:
  - "Chi mo khi OWNER Q-D3-4 = thieu native; khong log secret"
inputs:
  - 03_output/CYC-10/checks/approval_log_coverage.md
  - 01_plan/SPEC_INFRA_RECOVERY.md
  - tools/README.md
read_also:
  - 05_memory/upstream/04_nhat_ky_kiem_toan_va_quan_tri_van_hanh.md
line_budget: 300
verify: "python -m pytest -q --tb=line tools/tests/test_approval_log.py"
done_when:
  - "Logger+test PASS; README mo ta"
size: "1 session · 3 files"
depends_on: [D3-06]
fixes: ""
```

### D3-07
```yaml
schema: 1
id: D3-07
cycle: CYC-10
origin: "01_plan/PLAN.md#CYC_10"
assignee: W1
goal: "So truoc/sau K6 va lap goi tham dinh (LEAD tong ket)"
write_scope:
  - 03_output/CYC-10/checks/k6_outcome.md
constraints:
  - "Cung dinh nghia/mau so/diem do; khong sua evidence niem phong"
  - "Vai LEAD: de xuat xai/grok-4.5 (khong Gemini cho tong ket LEAD)"
inputs:
  - 03_output/CYC-10/checks/k6_scope_baseline.md
  - 03_output/CYC-10/checks/approval_log_coverage.md
  - 01_plan/SPEC_INFRA_RECOVERY.md
  - 05_memory/upstream/00_tong_quan_upstream.md
read_also:
  - README_GOI_KAIZEN.md
line_budget: 200
verify: "python -m pytest -q --tb=line tools/tests"
done_when:
  - "k6_outcome.md co ket luan/gioi han/khuyen nghi truy nguon"
size: "1 session · 1 file"
depends_on: [D3-03, D3-04, D3-05, D3-06]
fixes: ""
```

## B6. Câu hỏi OWNER Đợt 3

| ID | Câu hỏi |
|---|---|
| Q-D3-1 | K6 đủ hay thu nhỏ/gộp nếu lỗi hạ tầng hiếm? |
| Q-D3-2 | E13 gồm breaker, relay version/hash và denylist phiên cũ? |
| Q-D3-3 | H4-6 đo qua relay; duyệt đối chứng khi đổi điểm đo? |
| Q-D3-4 | Native log đủ H4-3? Nếu thiếu → mở D3-08; retention? |
| Q-D3-5 | Thứ tự Đ2/3/4 theo Đ5? |
| Q-D3-9 | CYC-10 / DEC origin còn rảnh? |

## B7. SẴN SÀNG GIAO Đợt 3
| Task | Cần |
|---|---|
| D3-01 | V3-1…V3-6; Q-D3-1 sơ bộ |
| D3-02 | D3-01; Q-D3-2 |
| D3-03…05 | D3-02 merged |
| D3-06 | D3-02 |
| D3-08 | Q-D3-4 = thiếu native |
| D3-07 | D3-03…06 merged |

---

# PHẦN C — ĐỢT 4 (K7) · CYC-11 giả định

## C1. Điều kiện vào

| # | Điều kiện |
|---|---|
| V4-1 | Đợt 1 đóng; `state` và `validate` ổn định trên main (SHA/check LEAD xác minh) |
| V4-2 | Đợt 2/3 đóng **hoặc** OWNER chốt thứ tự khác (Q-D3-5) |
| V4-3 | OWNER chấp thuận **E1 và E3 cùng nhau** (Q-D4-6) |
| V4-4 | Dynamic context chỉ xét nếu evidence Đ1 cho thấy tách tĩnh/`get` chưa đủ (Q-D4-8) |
| V4-5 | Không thêm H3-15, H4-2, H4-8 hay `.github/` khi chưa duyệt/lệnh |

## C2. Mục tiêu / chỉ số

OWNER thấy đối tượng/thay đổi/blocker/rủi ro nhanh; đúng vai ADVISOR/LEAD intake; sinh STATE và phần cơ học gói Kaizen.

| Chỉ số | Mô tả |
|---|---|
| K7-M1 | Thời gian walkthrough tìm trạng thái (trước/sau, cùng kịch bản) |
| K7-M2 | Đúng grammar STATUS 4 dòng; PR report &lt;30 dòng |
| K7-M3 | Độ chính xác fixture STATE/get/kaizen |
| K7-M4 | Tỷ lệ output phải sửa tay |

| Bước | Việc | Xong khi |
|---|---|---|
| 0 | Xác minh state/validate + OWNER E1/E3/dynamic | SHA/check/decision |
| 1 | Sinh STATE tự động | Idempotent; fixture+validate |
| 2 | STATUS 4 dòng + PR &lt;30 dòng | Grammar/CHAT_UX |
| 3 | ADVISOR + LEAD intake E1/E3 | Flow câu hỏi trước PLAN_GO |
| 4 | Sinh phần cơ học gói Kaizen | Fixture/link; không DEC |
| 5 | `get` theo pointer | valid/invalid/archive tests |
| 6 | Dynamic context (cổng) | Chỉ sau DEC+path |
| 7 | Walkthrough + thẩm định | Outcome |

## C3. OWNER / LEAD Đợt 4

| Thời điểm | OWNER | LEAD |
|---|---|---|
| Trước Đ4 | Xác nhận state/validate; chốt E1/E3, UX, dynamic (Q-D4-6…8) | Fixture/metrics; câu hỏi chặn; không biến proposal thành quyết định |
| Trong Đ4 | Duyệt PR/cổng và phạm vi automation | Kiểm UX/STATE/anchors/report; REVIEWER khác họ |
| Đóng Đ4 | Duyệt gói thẩm định / E / chuyển repo mẹ | Outcome + giới hạn |

## C4. Bảng tổng task

| ID | Bước | Nhánh | Hạng | Người nhận (đề xuất) | REVIEWER (đề xuất) | W | depends_on | Batch |
|---|---|---|---|---|---|---|---|---|
| D4-01 | 1 | task/ | T2 | WORKER (xai/grok-4.5) | REVIEWER (ag/gemini-3.8-flash) | W1 | [] | B0a |
| D4-02 | 2 | upgrade/ | T1 | WORKER (ag/gemini-3.8-flash) | REVIEWER (cx/gpt-6.1-terra) | W2 | [] | B0b |
| D4-03 | 3 | upgrade/ | T1 | WORKER (ag/gemini-3.8-flash) | REVIEWER (xai/grok-4.5) | W1 | [D4-02] | B1 |
| D4-04 | 4 | task/ | T2 | WORKER (cx/gpt-6.1-terra) | REVIEWER (ag/gemini-3.8-flash) | W2 | [D4-01] | B2 |
| D4-05 | 5 | task/ | T2 | WORKER (xai/grok-4.5) | REVIEWER (ag/gemini-3.8-flash) | W1 | [D4-01] | B3 |
| D4-07 | 7 | lead/ | T1 | LEAD (xai/grok-4.5) | REVIEWER (cx/gpt-6.1-terra) | W1 | [D4-01, D4-02, D4-03, D4-04, D4-05] | B5 |

**D4-06:** không cấp task tới khi OWNER Q-D4-8 YES + DEC + ≤5 path cố định (cổng LEAD/OWNER).

```text
## CYC-11 batches
- B0a | tasks: D4-01 | after: none
- B0b | tasks: D4-02 | after: none
- B1 | tasks: D4-03 | after: B0b
- B2 | tasks: D4-04 | after: B0a
- B3 | tasks: D4-05 | after: B0a
- B5 | tasks: D4-07 | after: B1,B2,B3
```
B0a∥B0b khi zero-overlap (`tools/*` vs `harness/CHAT_UX|STATUS_GRAMMAR|BLOCKS`). D4-05 phụ thuộc D4-01 vì cùng có thể đụng README — **đã cố định** `depends_on: [D4-01]` và write_scope **không** gồm README.

## C5. Task Đợt 4 (đủ schema)

### D4-01
```yaml
schema: 1
id: D4-01
cycle: CYC-11
origin: "01_plan/PLAN.md#CYC_11"
assignee: W1
goal: "Sinh phan STATE tu dong; bao toan history/Next action"
write_scope:
  - tools/state.py
  - tools/tests/test_state.py
  - tools/README.md
constraints:
  - "Idempotent; khong tu ghi ledger/cap ma"
inputs:
  - 04_control/STATE.md
  - harness/templates/state.md
  - harness/rules/LEAD.md
read_also:
  - harness/tools/README.md
line_budget: 350
verify: "python -m pytest -q --tb=line tools/tests/test_state.py"
done_when:
  - "Fixtures on; history giu; validate/state dat"
size: "1 session · 3 files"
depends_on: []
fixes: ""
```

### D4-02
```yaml
schema: 1
id: D4-02
cycle: CYC-11
origin: "01_plan/PLAN.md#CYC_11"
assignee: W2
goal: "STATUS 4 dong va PR report <30 dong (H4-9)"
write_scope:
  - harness/CHAT_UX.md
  - harness/schemas/STATUS_GRAMMAR.md
  - harness/templates/BLOCKS.md
constraints:
  - "STATUS dung 4 dong; report <30 dong; khong cat path"
inputs:
  - harness/CHAT_UX.md
  - harness/schemas/STATUS_GRAMMAR.md
  - 05_memory/upstream/04_nhat_ky_kiem_toan_va_quan_tri_van_hanh.md
read_also:
  - harness/templates/BLOCKS.md
line_budget: 250
verify: "python -m pytest -q --tb=line tools/tests"
done_when:
  - "Grammar dung; blocker/rui ro ro trong mau"
size: "1 session · 3 files"
depends_on: []
fixes: ""
```

### D4-03
```yaml
schema: 1
id: D4-03
cycle: CYC-11
origin: "01_plan/PLAN.md#CYC_11"
assignee: W1
goal: "Luat ADVISOR + LEAD intake Basic Plan (E1/E3)"
write_scope:
  - harness/rules/LEAD.md
  - harness/HARNESS.md
  - harness/templates/plan_go.md
constraints:
  - "E1/E3 dong thoi; ADVISOR khong lap DSC/DEC/PLAN; LEAD khong quyet thay OWNER; toi da 2 vong; cau hoi chan truoc PLAN_GO"
  - "Khong them path thu 4"
inputs:
  - harness/rules/LEAD.md
  - 05_memory/upstream/00_tong_quan_upstream.md
  - 05_memory/upstream/01_brainstorm_va_tra_cuu_ngoai.md
read_also:
  - harness/CHAT_UX.md
line_budget: 300
verify: "python -m pytest -q --tb=line tools/tests"
done_when:
  - "Vai/escalation/question/decision flow khop van ban"
size: "1 session · 3 files"
depends_on: [D4-02]
fixes: ""
```

### D4-04
```yaml
schema: 1
id: D4-04
cycle: CYC-11
origin: "01_plan/PLAN.md#CYC_11"
assignee: W2
goal: "Sinh phan co hoc goi Kaizen tu ANCHOR; khong sinh DEC"
write_scope:
  - tools/kaizen_package.py
  - tools/tests/test_kaizen_package.py
  - tools/README.md
constraints:
  - "Tro nguon; anchor thieu/trung bao loi; khong ghi history/DEC"
inputs:
  - tools/state.py
  - tools/README.md
  - 05_memory/upstream/00_tong_quan_upstream.md
read_also:
  - harness/rules/LEAD.md
line_budget: 350
verify: "python -m pytest -q --tb=line tools/tests/test_kaizen_package.py"
done_when:
  - "Fixtures dung/thieu/trung dat; loi nguon ro"
size: "1 session · 3 files"
depends_on: [D4-01]
fixes: ""
```

### D4-05 (write_scope cố định — không README)
```yaml
schema: 1
id: D4-05
cycle: CYC-11
origin: "01_plan/PLAN.md#CYC_11"
assignee: W1
goal: "tools/get tra doan ANCHOR-END theo POINTER_GRAMMAR"
write_scope:
  - tools/get.py
  - tools/tests/test_get.py
constraints:
  - "Khong doc toan log; con tro thieu/trung/mo ho bao loi; khong dynamic context"
  - "Khong sua tools/README.md (tranh overlap D4-01/D4-04); tai lieu get nam trong docstring/test"
inputs:
  - harness/schemas/POINTER_GRAMMAR.md
  - tools/state.py
  - harness/rules/LEAD.md
read_also:
  - tools/README.md
line_budget: 300
verify: "python -m pytest -q --tb=line tools/tests/test_get.py"
done_when:
  - "valid/invalid/duplicate/archive/UTF-8 tests PASS"
size: "1 session · 2 files"
depends_on: [D4-01]
fixes: ""
```

### D4-07
```yaml
schema: 1
id: D4-07
cycle: CYC-11
origin: "01_plan/PLAN.md#CYC_11"
assignee: W1
goal: "Walkthrough truoc/sau va goi tham dinh K7 (LEAD)"
write_scope:
  - 03_output/CYC-11/checks/k7_outcome.md
constraints:
  - "Khong tuyen bo cai thien thieu baseline; khong du lieu ca nhan"
  - "LEAD de xuat xai/grok-4.5; REVIEWER khac ho"
inputs:
  - 03_output/CYC-10/checks/k6_outcome.md
  - tools/tests/test_state.py
  - tools/tests/test_get.py
  - harness/CHAT_UX.md
read_also:
  - README_GOI_KAIZEN.md
line_budget: 200
verify: "python -m pytest -q --tb=line tools/tests"
done_when:
  - "k7_outcome.md tro nguon/gioi han; san OWNER nhan"
size: "1 session · 1 file"
depends_on: [D4-01, D4-02, D4-03, D4-04, D4-05]
fixes: ""
```

## C6. Câu hỏi OWNER Đợt 4

| ID | Câu hỏi |
|---|---|
| Q-D4-6 | E1/E3 được chấp thuận cùng lúc? |
| Q-D4-7 | Ưu tiên usability metric nào (K7-M1…)? |
| Q-D4-8 | Dynamic context cần sau static split/get? Nếu YES → DEC+path trước khi cấp task |
| Q-D4-9 | CYC-11 / DEC origin còn rảnh? |

## C7. SẴN SÀNG GIAO Đợt 4
| Task | Cần |
|---|---|
| D4-01 | V4-1…V4-2 |
| D4-02 | V4-1 |
| D4-03 | Q-D4-6 YES; D4-02 |
| D4-04 | D4-01 |
| D4-05 | D4-01 |
| D4-07 | D4-01…05 merged |
| (D4-06 sau này) | Q-D4-8 YES + DEC + path |

---

# PHẦN D — Chốt lại sau Đ5 (gộp)

1. Khóa thứ tự Đ2/3/4 và thu nhỏ K6 nếu lỗi hạ tầng hiếm.  
2. Khóa baseline/mẫu số/điểm đo; nối số nếu đổi relay.  
3. Remap mọi `D*-nn` → `TK-NNNN`; `origin` → DEC ACTIVE.  
4. Khảo sát lại path trên main trước Run.  
5. POOL L0.1; REVIEWER khác họ actual.  
6. Không thêm H3-15/H4-2/H4-8/`.github/` ngoài lệnh OWNER.

---

# PHẦN E — Xử lý rà soát

## E1. Q2 REVIEW_DOT2 / REVIEW_DOT3-4
(Giữ các dòng đã xử lý ở Q3 — xem `KE_HOACH_CHI_TIET_DOT2-4_q3.md` PHẦN E.)

## E2. Claude xem lại Q3 → Q3b

| Điểm Claude | Đã sửa |
|---|---|
| Dot3 thẻ chỉ tóm tắt | Đủ YAML schema từng D3-01…08 |
| Dot4 chỉ bảng/path | Đủ YAML D4-01…05, D4-07 |
| Bản gộp phụ thuộc “như PLAN_* §” | Chép điều kiện vào, OWNER/LEAD, câu hỏi vào PHẦN B/C |
| `D3-06b` chữ cái | Đổi **D3-08** |
| D4-05 “hoặc…” | Khóa 2 path `get.py`+test; `depends_on: [D4-01]`; không README |
| D3-07 đề xuất Gemini | Đổi LEAD `(xai/grok-4.5)` + REVIEWER terra |

---

# PHẦN F — Kết luận Q3b

- Bản này **đọc riêng được** cho Đợt 2–4 ở mức thẻ task.  
- Vẫn **PROVISIONAL** (chờ Đ5 + OWNER).  
- Sẵn sàng Claude kiểm lại lần cuối trước PR gộp 4 đợt.  
- Báo: `DONE-Q3b-grok-4.5` + đường dẫn file này.
