# 04_control

**Chứa:**
- `STATE.md` — trạng thái dự án, bản chiếu do script sinh (≤ 40 dòng).
- `decisions/` 🔒 — `DEC` đang `ACTIVE`; `decisions/superseded/` là kho lạnh.
- `risks/` — `RSK` đang mở; `risks/closed/` là kho lạnh.
- `requests/` — `REQ` chưa xử lý; `requests/resolved/` là kho lạnh.
- `gates/` ✍ — `PLAN_GO.md`, `CYC-nn_PASS.md`, `FINAL_PASS.md`, `CLOSED.md`.

**Ai ghi:** chỉ LEAD, qua PR. File trong `gates/` chỉ có hiệu lực khi OWNER merge. WORKER và REVIEWER không ghi.

**Quy tắc:** dòng trạng thái chỉ thêm, chèn ngay dưới `## Status (newest first)`; chuyển kho lạnh trong cùng PR với dòng trạng thái đóng, chỉ đi một chiều.

**Lưu ý:** file cổng không được tạo sẵn. Sự tồn tại của file là dấu hiệu tiến độ.
