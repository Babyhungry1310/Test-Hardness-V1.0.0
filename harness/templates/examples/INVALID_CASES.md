# INVALID CASES

Mỗi file có hậu tố `.invalid` là bản sai của file cùng tên, chỉ chứa đúng một lỗi. Lời giải thích nằm ở bảng này, không nằm trong file sai. Công cụ tra con trỏ bỏ qua file `.invalid`.

| File | Loại | Trường sai | Lỗi | Kết quả | Kiểm tra |
|---|---|---|---|---|---|
| `harness.yaml.invalid` | harness | `kind` | `app` không thuộc `code`, `doc`, `research`, `mixed` | `REJECT` | Schema |
| `01_plan/PLAN.md.invalid` | plan | `based_on` | Danh sách rỗng: plan không dựa trên `DEC` nào | `REJECT` | Schema, C9 |
| `02_work/tasks/CYC-01/TK-0002.md.invalid` | task | `origin` | Thiếu trường bắt buộc: task không truy được nguồn | `REJECT` | Schema, C9 |
| `02_work/runs/TK-0002_R1_DONE.md.invalid` | run | `note` | Khóa ngoài schema, chứa lời ghi chú | `REJECT` | Schema, C13 |
| `03_output/CYC-01/checks/RVW-CYC-01.md.invalid` | review | `verdict` | `OK` không thuộc `PASS`, `FAIL` | `REJECT` | Schema |
| `04_control/decisions/DEC-0002_json-bank.md.invalid` | decision | `supersedes` | `DEC-1` sai dạng mã | `REJECT` | Schema |
| `04_control/requests/resolved/REQ-0001_duplicate-ids.md.invalid` | request | `id` | `REQ-1` sai dạng mã | `REJECT` | Schema |
| `04_control/risks/RSK-0002_real-names.md.invalid` | risk | Dòng trạng thái, `level` | `CRITICAL` không thuộc `LOW`, `MEDIUM`, `HIGH` | `REJECT` | Ngữ pháp trạng thái |
| `05_memory/discussions/2026/DSC-20261102-q7k2.md.invalid` | discussion | Dòng sự kiện `E1` | Loại `DECISION` không có; quyết định chỉ tồn tại ở `DEC` | `REJECT` | Ngữ pháp sự kiện |
| `06_sources/SRC-0001_question-format.md.invalid` | source | `decided_by` | `LEAD`; nguồn chỉ do OWNER duyệt | `REJECT` | Schema |
| `src/dupes.py.invalid` | code | Docstring, dòng `#`, `TODO` | Ghi chú trong code bàn giao | `REJECT` | C13 |
| `data/bank.json.invalid` | data | `_comment`, `note` | Trường ghi chú trong dữ liệu bàn giao | `REJECT` | C13 |
