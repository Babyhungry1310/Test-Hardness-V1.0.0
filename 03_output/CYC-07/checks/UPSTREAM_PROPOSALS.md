# Đề xuất chuyển về repo mẹ (UPSTREAM_PROPOSALS)

- Bản này: sau kiểm định CYC-07 PASS (DEC-0020, SPEC_DRYRUN §8)
- Baseline dry-run: `67a092fc469809d7d11c22a751bdba22f5aa9651`
- Tip hiện tại: `95a0e462f3be3cf0046c1c15b9fb07848e9f770b` (PR #88, 2026-11-20T15:15:51Z)
- Thời điểm soạn: 2026-11-20
- Kiểm kê gốc: `03_output/CYC-07/checks/TK-0028_upstream_inventory.md` (tip khi đó `c1f6082`)
- Bổ sung sau TK-0028: PR #84, #85, #88 (inventory, TK-0017, RVW/cổng/digest CYC-07)

> Không tự chuyển sang repo mẹ. Không mở PR ở repo mẹ trước khi OWNER duyệt từng mục và phiên bản đích.
> Chạy thử / cổng PASS không đồng nghĩa được phép chuyển.

---

## 0. Xác nhận dry-run sản phẩm đã kết thúc

| Hạng mục | Trạng thái |
|---|---|
| CYC-03 … CYC-07 cổng PASS trên main | Đạt (`04_control/gates/CYC-0n_PASS.md`) |
| STATE | PHASE CLOSE, CYCLE CYC-07 PASS @ tip `95a0e46` |
| verify_default | 23 passed trên tip |
| tools/tests (TK-0017) | 338 passed (Windows) |
| RVW độc lập CYC-07 | PASS, reviewer `gpt-5.6-luna` |
| Thẻ `cycle/CYC-03` … `cycle/CYC-07` | **Chưa** trên origin (OWNER đặt) |
| PR #37 quyền WORKER / CYC-08 | OPEN draft CONFLICTING — OWNER xử lý sau dry-run |
| Hồi quy Linux (SPEC_DRYRUN RERUN) | **Chưa chạy** trong dry-run này |
| `assign_audit --root .` | Exit 2 (front matter một số run cũ) — ghi trong TK-0017 |

**Kết luận LEAD:** Chuỗi thi công dry-run CYC-03→CYC-07 đã đóng cổng trên main. Việc còn lại để “kết thúc vận hành” là thẻ chu kỳ (OWNER) và duyệt đề xuất dưới đây trước khi chuyển repo mẹ. PR #37 nằm ngoài phạm vi đóng dry-run sản phẩm.

---

## 1. Delta sau inventory TK-0028 (`c1f6082` → `95a0e46`)

| STT | Nguồn | Phạm vi | Trạng thái | Bằng chứng | Đề xuất |
|---|---|---|---|---|---|
| D1 | PR #84; TK-0028 | `TK-0028_upstream_inventory.md`, run/checks | MERGED | baseline 23 | **Không chuyển** — kiểm kê nội bộ dry-run |
| D2 | PR #85; TK-0017 | `TK-0017_regression_windows.txt`, run/checks | MERGED | 23 + 338; assign_audit exit 2 ghi nhận | **Không chuyển** — bằng chứng hồi quy Windows của dự án thử |
| D3 | PR #88; RVW-CYC-07; CYC-07_PASS; digest; STATE; cycle file | cổng và sổ đóng CYC-07 | MERGED | RVW PASS; gate PASS | **Không chuyển** — vận hành chu kỳ dry-run |

Toàn bộ 279 file trong `67a092f..95a0e46` đã được phủ bởi inventory TK-0028 (268 file tới `c1f6082`) cộng 11 file delta trên.

---

## 2. Đề xuất theo nhóm (OWNER duyệt từng dòng)

### A. Đề xuất chuyển (Transfer)

| ID | Nội dung | Nguồn chính | Ghi chú |
|---|---|---|---|
| T1 | Hook bảo vệ main: `pre-commit`, `pre-push`, `pre-merge-commit` + test | TK-0006, TK-0032 | Cần `core.hooksPath`; OWNER cài mỗi clone |
| T2 | `preflight_main.py` + test (kể cả detector session sau DEC-0029) | TK-0007, TK-0030, TK-0034, TK-0035 | |
| T3 | `github_audit.py` + test shared account | TK-0008, TK-0027 | **Điều chỉnh tham số** repo/org trước khi dùng |
| T4 | Test biên main guard | TK-0018 | Suite dài |
| T5 | `model_check.py`, `model_select.py` + test | TK-0009, TK-0010 | |
| T6 | `assign_audit.py`, `test_model_route_identity.py` | TK-0019, TK-0029 | Sửa front matter run cũ nếu mang audit vào CI |
| T7 | `branch_names.py`, `chat_blocks.py`, `clean_list.py` + test | TK-0011, TK-0012, TK-0021 | |
| T8 | Storage freeze + trace-open tests | TK-0020 | Trace A/B/C vẫn OPEN (RFC-0001) |
| T9 | Scanner: `scan.py`, `scan_rules.json`, quarantine, wrap + tests (core/limits/adversarial) | TK-0013..TK-0023, DEC-0030 | Không claim chặn hết prompt injection |
| T10 | `batch_check.py`, `integrate_check.py`, `pytest_ini_check.py`, `test_pytest_template.py` | TK-0015, TK-0016, TK-0024, TK-0025 | |
| T11 | `tools/README.md` (+ `tools/requirements.txt` nếu repo mẹ chưa có pin tương đương) | TK-0026 | |

### B. Đề xuất điều chỉnh rồi chuyển (Adjust)

| ID | Nội dung | Lý do |
|---|---|---|
| A1 | Bổ sung harness rules / MAIN_PROTECTION / SPEC_* từ DEC-0016..0020 | Repo mẹ có thể đã có bản khác — diff chọn lọc |
| A2 | `github_audit` / shared-account policy | Phụ thuộc tài khoản và ruleset GitHub cụ thể |
| A3 | Catalog/matrix **schema tooling** (T5) tách khỏi **nội dung** MODEL_CATALOG/MATRIX của repo thử | Nội dung catalog local: không chuyển (N2) |

### C. Đề xuất không chuyển (Do not transfer)

| ID | Nội dung | Lý do |
|---|---|---|
| N1 | `02_work/`, `03_output/` runs/checks/RVW, digests, STATE, gates CYC-* của dry-run | Nhật ký vận hành thử nghiệm |
| N2 | `04_control/MODEL_CATALOG.md`, `MODEL_MATRIX.md` (nội dung) | Gắn router/tài khoản môi trường thử |
| N3 | Inventory TK-0028, UPSTREAM_PROPOSALS, TK-0017 evidence | Tài liệu đóng dry-run, không phải sản phẩm khung |
| N4 | PR #34 closed, runs BLOCKED đã superseded | Đã thay bằng run DONE |
| N5 | TK-0033 CANCELLED | Đã tách TK-0034/0035 |
| N6 | PR #37 (sau dry-run) | OWNER xử lý riêng; chưa xác minh đủ |

---

## 3. Khoảng trống còn lại

1. Thẻ `cycle/CYC-03` … `cycle/CYC-07` chưa đặt.
2. Hồi quy Linux chưa chạy trong dry-run này.
3. `assign_audit` exit 2 trên một số run thiếu newline sau `---`.
4. Chưa chọn RFC-0001 trace A/B/C; chưa có SCAN_HIT log; `clean_list --delete` vẫn bị chặn (đúng thiết kế hiện tại).
5. Repo mẹ đích và phiên bản đích: **OWNER ghi rõ khi duyệt**.

---

## 4. Cách OWNER duyệt

Với mỗi ID ở mục 2, chọn một: `APPROVE transfer` | `APPROVE adjust` | `REJECT` | `DEFER`.

Sau khi duyệt, LEAD mới được mở PR sang repo mẹ theo đúng các ID được APPROVE, trên phiên bản đích OWNER chỉ định.

---

## 5. Phê duyệt OWNER

- Ngày: 2026-11-20
- Lời OWNER trong phiên LEAD: `ok duyệt`
- Phạm vi: chấp nhận nguyên văn khuyến nghị LEAD trong mục 2 của bản này

| ID | Quyết định OWNER |
|---|---|
| T1 … T11 | APPROVE transfer |
| A1 … A3 | APPROVE adjust |
| N1 … N6 | APPROVE do-not-transfer (không chuyển) |

Ghi chú còn thiếu trước khi LEAD mở PR sang repo mẹ:
1. OWNER chỉ định **URL repo mẹ** và **phiên bản/commit đích**.
2. OWNER đặt thẻ `cycle/CYC-03` … `cycle/CYC-07` (không bắt buộc để chuyển, nhưng còn nợ vận hành).
3. PR #37 vẫn DEFER / xử lý riêng (N6).

LEAD không mở PR ở repo mẹ cho đến khi có URL và phiên bản đích.
