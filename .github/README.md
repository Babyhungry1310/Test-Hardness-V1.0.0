# .github

Vùng bảo vệ 🔒. PR chạm thư mục này phải được đánh dấu "OWNER cần đọc kỹ".

## Workflow

Cả ba workflow **chưa kích hoạt**: mỗi file chỉ có trigger `workflow_dispatch` và một bước rỗng, nên không tự chạy trên PR hay trên `main`. Điều kiện kích hoạt: script `validate` trong `harness/tools/` đã có.

| File | Sẽ làm gì khi kích hoạt | Trigger dự kiến | Quyền |
|---|---|---|---|
| `workflows/check.yml` | Chạy các kiểm tra C1–C14 của khung trên nội dung file thay đổi của PR. Bộ kiểm tra luôn lấy từ `main`; không chạy code của PR | PR vào `main` | Chỉ đọc |
| `workflows/test.yml` | Chạy test của PR (lệnh `verify_default` trong `harness.yaml`). Kết quả để tham khảo; không dùng secret | PR vào `main`, khi `kind` là `code` hoặc `mixed` | Token chỉ đọc |
| `workflows/alert-main.yml` | Mở cảnh báo khi có thay đổi vào `main` không do tài khoản OWNER merge | Push vào `main` | Đọc repo, ghi issue |

## CODEOWNERS

`CODEOWNERS` gán mọi vùng 🔒 và file ✍ của `harness/HARNESS.md` mục 5.1 cho tài khoản OWNER. Dự án code thêm file khai báo gói và lockfile của ngôn ngữ đang dùng vào danh sách này (mục 5.5).

## Việc OWNER tự thiết lập trên GitHub

- Bảo vệ nhánh `main` và thẻ `cycle/*` theo `harness/MAIN_PROTECTION.md#GITHUB_RULES`: bắt buộc PR, cấm đẩy thẳng, cấm ép đẩy, không cho bỏ qua luật (nếu gói GitHub hỗ trợ). Đây là lớp kiểm soát chính; hook cục bộ và chỉ dẫn cho tác tử chỉ chống nhầm.
- Chỉ cho phép squash merge; tắt auto-merge. Tự xóa nhánh nguồn sau merge: OWNER quyết theo `harness/GIT_CONVENTIONS.md#AUTO_DELETE`.
- Model dùng tài khoản GitHub riêng, không dùng chung tài khoản hay token với OWNER.
