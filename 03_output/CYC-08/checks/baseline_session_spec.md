# Baseline session spec — CYC-08 Bước 1

- Task: TK-0038
- Origin: DEC-0031 (đo nền); bổ sung chỉ số CS1–CS4 theo chỉ đạo OWNER 2026-11-23 / PHUONG_AN mục 2.2
- Scope: đóng băng điểm đo + 3 phiên chuẩn. **Không chạy phiên trong task này** (L1.1 / L5.1 chạy sau).
- Freeze: không đổi điểm đo, model, tuyến, hay đầu vào phiên chuẩn từ L1.1 tới hết Bước 5 (trừ DEC mới).

## 1. Điểm đo cố định

| Thành phần | Giá trị neo (L1.1 ghi xác nhận thực tế) |
| --- | --- |
| Relay đang chạy | Bản relay Orca/session đang dùng cho LEAD/WORKER/REVIEWER lúc L1.1; ghi **tên bản + cách nhận diện** (không ghi path máy) |
| 9Router | Endpoint local proxy đã dùng cho probe/giao việc (host:port logic, không secret); ghi version/build nếu đọc được |
| Nơi đọc usage | Metadata usage từ response relay/9Router theo lượt gọi; ưu tiên trường có nhãn vai nếu có. Artifact local only — không commit secret |
| Provider version | Ghi version/model id trả về thực tế mỗi vai khi L1.1 chạy (không đoán) |

Ghi chú đo: cùng điểm đo cho cả 6 lần chạy (3 phiên × 2). Nếu điểm đo buộc đổi giữa L1.1 và L5.1: ghi lại và **không so trực tiếp**.

## 2. Ba phiên chuẩn (nội dung cố định)

### Phiên 1 — LEAD hỏi trạng thái

| Trường | Neo |
| --- | --- |
| Vai chính | LEAD |
| Mục tiêu | Hỏi/tóm tắt trạng thái chu kỳ hiện tại từ STATE + sổ (không sửa repo) |
| Đầu vào cố định | Prompt: đọc `04_control/STATE.md` mục Progress/Next; trả lời ngắn: CYCLE, PHASE, task mở, rủi ro OPEN hạn gần nhất. Không mở PR, không sửa file |
| Tuyến yêu cầu | `xai/grok-4.5` (LEAD) |
| Model kỳ vọng (catalog) | `grok-4.5` hoặc actual mà preflight/relay xác minh cùng họ Grok đã duyệt |
| Provider version | Ghi khi L1.1 (actual từ metadata) |
| File luật được phép đọc nguyên (CS2) | `harness/rules/LEAD.md`, `harness/HARNESS.md`, `04_control/STATE.md` |

### Phiên 2 — LEAD review PR

| Trường | Neo |
| --- | --- |
| Vai chính | LEAD |
| Mục tiêu | Rà C1–C14 mức đọc trên **một PR đã merge mẫu** (cùng SHA neo dưới); xuất khối nhận xét ngắn, không merge |
| Đầu vào cố định | PR mẫu: `#94` (TK-0037) @ `e64f84a`; đọc diff/files qua `gh pr view` / `gh pr diff` (hoặc tương đương). Không sửa, không merge, không bật auto-merge |
| Tuyến yêu cầu | `xai/grok-4.5` (LEAD) |
| Model kỳ vọng (catalog) | cùng quy ước Phiên 1 |
| Provider version | Ghi khi L1.1 |
| File luật được phép đọc nguyên (CS2) | `harness/rules/LEAD.md`, `harness/HARNESS.md` (mục review/C1–C14), `harness/schemas/task.schema.json` |

### Phiên 3 — WORKER chạy task nhỏ

| Trường | Neo |
| --- | --- |
| Vai chính | WORKER (có LEAD điều phối ngoài phiên đo) |
| Mục tiêu | Chạy một task **read-only** nhỏ: liệt kê `02_work/tasks/CYC-08/*.md` và xác nhận đủ TK-0036..TK-0038; ghi kết quả vào file run local (không commit trong L1.1) |
| Đầu vào cố định | Prompt WORKER: chỉ đọc `02_work/tasks/CYC-08/`; không sửa; trả về danh sách id task + một dòng CONFIRM. LEAD không nhét toàn bộ luật vào prompt — chỉ trỏ path |
| Tuyến yêu cầu WORKER | `ag/gemini-3.8-flash` (hoặc alias high nếu POOL L0.1 chỉ có bản đó; ghi rõ lúc L1.1) |
| Model kỳ vọng WORKER | `gemini-3.8-flash-n` (hoặc actual đã verify) |
| Tuyến LEAD kèm (điều phối) | `xai/grok-4.5` — usage LEAD tách dòng riêng |
| Provider version | Ghi khi L1.1 cho từng vai |
| Nguồn CS3 | Số dòng nội dung trong **lượt trả về cuối** của WORKER cho LEAD (file run / transcript đã che) |

## 3. Chỉ số CS1–CS4

| Mã | Chỉ số | Định nghĩa | Nguồn | Đo được? |
| --- | --- | --- | --- | --- |
| CS1 | Tỷ lệ output/input theo vai | Σ `completion_tokens` / Σ `prompt_tokens` (gồm cached) theo vai, mỗi phiên | Usage có nhãn vai | **Bắt buộc** — L1.1 phải thu được; thiếu thì BLOCKED/QUESTION |
| CS2 | Số lần đọc nguyên file | Số lần một file trong danh sách cố định (luật, HARNESS, SPEC_*) được đọc **toàn bộ**, không theo neo/khoảng dòng | Log lệnh gọi công cụ phiên LEAD | Nếu không có log: ghi **Chưa thu thập được** — không ước lượng |
| CS3 | Số dòng WORKER trả về | Số dòng nội dung lượt trả về cuối WORKER → LEAD (phiên 3) | File run / transcript | **Bắt buộc** (phiên 3) |
| CS4 | Đỉnh `prompt_tokens` | Max `prompt_tokens` một lượt gọi trong phiên; kèm giới hạn context tuyến nếu MODEL_CATALOG đã có | Usage | **Bắt buộc**; giới hạn context: ghi nếu biết, không thì để trống (không bịa) |

## 4. Lịch chạy L1.1 / L5.1

- Mỗi phiên chạy **2 lần** (lần A, lần B).
- Báo cả hai lần; thêm cột trung bình và độ lệch (\|A−B\| hoặc mẫu đã chọn — ghi công thức trong artifact local).
- Artifact: local only (`<project>.local`); bản che mới được copy vào `03_output/CYC-08/checks/` khi task sau yêu cầu.

## 5. Mẫu bảng kết quả

Điền khi L1.1 (không điền số giả trong TK-0038):

| Phiên | Lần | Vai | prompt_tokens | cached_tokens | completion_tokens | CS1 | CS2 | CS3 | CS4 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | A | LEAD |  |  |  |  |  | n/a |  |
| 1 | B | LEAD |  |  |  |  |  | n/a |  |
| 2 | A | LEAD |  |  |  |  |  | n/a |  |
| 2 | B | LEAD |  |  |  |  |  | n/a |  |
| 3 | A | LEAD |  |  |  |  | n/a | n/a |  |
| 3 | A | WORKER |  |  |  |  | n/a |  |  |
| 3 | B | LEAD |  |  |  |  | n/a | n/a |  |
| 3 | B | WORKER |  |  |  |  | n/a |  |  |

Hàng tổng hợp (sau đủ 2 lần):

| Phiên | Vai | CS1 TB | CS1 lệch | CS2 TB | CS3 TB | CS4 max(A,B) |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | LEAD |  |  |  | n/a |  |
| 2 | LEAD |  |  |  | n/a |  |
| 3 | WORKER |  |  | n/a |  |  |

## 6. Điều kiện đủ để L1.1 / L5.1

- [x] Điểm đo cố định đã mô tả (relay, 9Router, nơi usage)
- [x] Ba phiên có input, tuyến, model kỳ vọng
- [x] CS1–CS4 định nghĩa + trạng thái đo được / chưa thu thập
- [x] Mẫu bảng phiên × lần × vai
- [ ] O1.1–O1.4 OWNER xong (ngoài spec)
- [ ] Chạy thật + bảng số (L1.1; ngoài task này)
