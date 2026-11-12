# Hardness-V1.0.0

Repo mẫu của Harness V1.0: bộ khung để nhiều mô hình AI cùng làm một dự án dài hạn trên một repo Git, có vai trò rõ, bộ nhớ dự án chuẩn hóa và kiểm tra bằng máy.

## Bắt đầu trong 3 bước

1. **Tạo repo và thư mục trên máy.** Tạo repo mới từ mẫu này, clone về, rồi tạo thư mục `<project>.local` nằm cạnh bản checkout (không nằm trong Git):

   ```text
   git clone https://github.com/<account>/<project>.git
   mkdir <project>.local\scratch <project>.local\logs <project>.local\quarantine <project>.local\transcripts <project>.local\cache
   ```

2. **Khai báo dự án.** Sửa `harness.yaml` (`kind`, `product_paths`, `verify_default`), đổi tài khoản trong `.github/CODEOWNERS` thành tài khoản OWNER, và bật bảo vệ nhánh `main` với cách merge squash theo `.github/README.md`.
3. **Mở phiên đầu tiên.** Mở một tác tử ở gốc repo và bắt đầu brainstorm với LEAD: "Discuss: tôi muốn làm …". Tác tử đọc `AGENTS.md`, `CLAUDE.md` hoặc `GEMINI.md` để biết phải theo file luật nào.

## Bốn loại phiên

| Loại | Dùng khi | Vai | Câu lệnh mẫu | Kết thúc bằng |
|---|---|---|---|---|
| `ASK` | Hỏi, tra cứu; không tạo hay sửa gì | Không nhận vai | "Ask: DEC-0007 quyết định gì?" | Câu trả lời |
| `RUN` | Giao làm một task | WORKER | "Run TK-0007" | Run + PR + khối `RESULT` |
| `CHANGE` | Sửa một thứ cụ thể ngoài việc đã chốt | LEAD | "Change: thêm cột ngày vào file xuất" | `REQ-nnnn`, `DEC` và task mới |
| `DISCUSS` | Brainstorm mục tiêu, hướng làm, ý tưởng | LEAD | "Discuss: nên chia dự án thành mấy chu kỳ?" | `DSC-…`; điều đã chốt thành `DEC` |

OWNER kích hoạt thi công một chu kỳ bằng "Start CYC-01". Chỉ OWNER bấm merge.

## Cây thư mục

| Đường dẫn | Chứa gì |
|---|---|
| `harness/` | File của khung: tài liệu, luật theo vai, schema, mẫu, script, phần mở rộng |
| `harness.yaml` | Cấu hình dự án |
| `00_brief/` | Mục tiêu, phạm vi, điều không làm |
| `01_plan/` | Plan, tiêu chí nghiệm thu, đặc tả |
| `02_work/` | Task, run, chu kỳ |
| `03_output/` | Sản phẩm không phải code, bằng chứng và bản ghi kiểm định |
| `04_control/` | Trạng thái dự án, sổ quyết định, rủi ro, yêu cầu, file cổng |
| `05_memory/` | Bản ghi thảo luận, tóm tắt, thuật ngữ, tri thức cốt lõi |
| `06_sources/` | Nguồn chuẩn đã được OWNER duyệt |

Mỗi thư mục `00`–`06` có một `README.md` nêu chứa gì, ai được ghi và giới hạn số dòng.

## Tài liệu

- Tài liệu khung (nguồn chuẩn duy nhất): [`harness/HARNESS.md`](harness/HARNESS.md)
- Bảng khái niệm, Phụ lục A: `harness/HARNESS.md#CONCEPTS`
- Bảng lý thuyết nền, Phụ lục B: `harness/HARNESS.md#THEORIES`
- Luật theo vai: [`harness/rules/LEAD.md`](harness/rules/LEAD.md) · [`harness/rules/WORKER.md`](harness/rules/WORKER.md) · [`harness/rules/REVIEWER.md`](harness/rules/REVIEWER.md)
- Quy ước Git: [`harness/GIT_CONVENTIONS.md`](harness/GIT_CONVENTIONS.md)
- Workflow và CODEOWNERS: [`.github/README.md`](.github/README.md)
- Ghép với Orca và 9Router, luồng một phiên: [`harness/tools/INTEGRATION.md`](harness/tools/INTEGRATION.md)
- Kiểm tra đầu phiên: [`harness/tools/PREFLIGHT.md`](harness/tools/PREFLIGHT.md)
- Kịch bản chạy thử cho OWNER: [`harness/templates/examples/DRY_RUN.md`](harness/templates/examples/DRY_RUN.md)
- Danh mục script và đề xuất việc viết code: [`harness/tools/README.md`](harness/tools/README.md) · [`harness/tools/BUILD_TASKS.md`](harness/tools/BUILD_TASKS.md)
- Phần mở rộng: [`harness/extensions/README.md`](harness/extensions/README.md)
