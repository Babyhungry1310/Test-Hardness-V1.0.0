# POINTER GRAMMAR

Ngữ pháp con trỏ và mã vết, theo `harness/HARNESS.md` mục 4.2 và 7.3. Con trỏ là cách duy nhất để nhắc tới một thông tin.

## 1. Ngữ pháp

```text
pointer = code [ "#" anchor ]  |  path "#" anchor  |  trace
code    = (TK|DEC|RSK|REQ|SRC)-[0-9]{4} | CYC-[0-9]{2} | RVW-CYC-[0-9]{2}
        | DSC-[0-9]{8}-[a-z0-9]{4}
anchor  = [A-Z][A-Z0-9_]*
path    = [A-Za-z0-9_][A-Za-z0-9_./-]*
trace   = TK-[0-9]{4} ".L" [0-9]{2} [ ".S" [0-9]{2} ]
```

Biểu thức đầy đủ (giống `$defs.pointer` trong các schema):

```regex
^(?:(?:(?:TK|DEC|RSK|REQ|SRC)-\d{4}|CYC-\d{2}|RVW-CYC-\d{2}|DSC-\d{8}-[a-z0-9]{4})(?:#[A-Z][A-Z0-9_]*)?|[A-Za-z0-9_][A-Za-z0-9_./-]*#[A-Z][A-Z0-9_]*|TK-\d{4}\.L\d{2}(?:\.S\d{2})?)$
```

- Đường dẫn tính từ gốc repo, dùng `/` cả trên Windows.
- Chỉ dùng đường dẫn cho file không có mã (đặc tả, `PLAN.md`, `HARNESS.md`). Không trỏ tới sổ bằng đường dẫn, không trỏ bằng số dòng.
- `read_also` của task và `affects` của `DEC` nhận cả đường dẫn không có neo (cả file).
- Mã vết của phiên không phải `RUN` có gốc `SES-YYYYMMDD-xxxx`; chỉ dùng trong log, không phải con trỏ.

## 2. Tên neo

- Chữ in hoa, số, gạch dưới; bắt đầu bằng chữ cái. Ví dụ: `RATIONALE`, `CYC_02`.
- Mỗi neo một cặp dòng `<!-- ANCHOR: X -->` và `<!-- END: X -->`; neo không lồng nhau; trong một file không trùng tên.
- Neo là cấu trúc của file, không phải ghi chú. Không thêm neo ngoài bảng mục 3, trừ neo của đặc tả và nguồn.
- Trong `DSC`, mã sự kiện `E1`, `E2`… là neo; không cần dòng `ANCHOR`.

## 3. Neo chuẩn theo loại bản ghi

| Loại | Neo |
|---|---|
| `DEC` | `CONTEXT` · `OPTIONS` · `RATIONALE` · `CONSEQUENCES` |
| `RSK` | `IMPACT` · `RESPONSE` |
| `REQ` | `CONTEXT` · `IMPACT` |
| `SRC` | `CONTEXT`; nội dung của nguồn thêm neo riêng do LEAD đặt |
| `DSC` | `E1`, `E2`… |
| `PLAN.md` | `CYC_01`, `CYC_02`… · `RISKS` |
| `02_work/cycles/CYC-nn.md` | `TASKS` |
| `05_memory/digests/CYC-nn.md` | `RESULTS` · `DECISIONS` · `RISKS` · `LESSONS` |
| `05_memory/topics/<topic>.md` | `DECISIONS` |
| `PLAN_GO.md` | `QUESTIONS` |
| `CYC-nn_PASS.md` | `ACCEPTANCE` · `QUESTIONS` |
| `SPEC_<MODULE>.md` | Do LEAD đặt theo đặc tả |
| `harness/HARNESS.md` | `CONCEPTS` · `THEORIES` |
| Tài liệu khác của khung trong `harness/tools/`, `harness/extensions/` | Do LEAD đặt theo tài liệu, đổi qua PR như mọi file 🔒 của `harness/` |
| Task, run, `RVW` | Không có neo; thuần YAML |

## 4. Tra con trỏ

| Mã | Tìm ở (gốc trước, kho lạnh sau) |
|---|---|
| `TK-nnnn` | `02_work/tasks/CYC-*/TK-nnnn.md` |
| `DEC-nnnn` | `04_control/decisions/DEC-nnnn_*.md`, rồi `decisions/superseded/` |
| `RSK-nnnn` | `04_control/risks/RSK-nnnn_*.md`, rồi `risks/closed/` |
| `REQ-nnnn` | `04_control/requests/REQ-nnnn_*.md`, rồi `requests/resolved/` |
| `SRC-nnnn` | `06_sources/SRC-nnnn_*.md` |
| `CYC-nn` | `02_work/cycles/CYC-nn.md` |
| `RVW-CYC-nn` | `03_output/CYC-nn/checks/RVW-CYC-nn.md` |
| `DSC-YYYYMMDD-xxxx` | `05_memory/discussions/YYYY/DSC-YYYYMMDD-xxxx.md` |
| `TK-nnnn.Lnn` | Dòng `Lnn` trong `loops` của run có loop đó; rồi `<project>.local/logs/TK-nnnn/trace.log` nếu còn |
| `TK-nnnn.Lnn.Snn` | Dòng span trong `trace.log`, khi mức log là `SPAN` |

| Con trỏ | Trả về |
|---|---|
| Mã có YAML và `## Status` | YAML + dòng trạng thái mới nhất |
| Mã thuần YAML (task, run, `RVW`) | YAML |
| `<mã hoặc đường dẫn>#ANCHOR` | Riêng đoạn giữa hai dòng neo |
| `DSC-…#En` | Dòng sự kiện `En` và dòng trạng thái của `En` nếu có |
| Mã vết | Dòng tóm tắt loop, kèm các dòng log của loop hoặc span nếu log còn trên máy |

File có hậu tố `.invalid` không bao giờ được tra.

## 5. Con trỏ không tra được

Công cụ dừng, trả mã thoát khác 0 và một dòng nêu con trỏ cùng loại lỗi, không bao giờ trả nội dung đoán:

| Lỗi | Khi nào |
|---|---|
| Sai cú pháp | Không khớp biểu thức mục 1 |
| Không có mã | Không tìm thấy file ở cả gốc và kho lạnh |
| Không có neo | Có file nhưng thiếu cặp dòng neo |
| Trùng mã | Hai file cùng mã |
| Hết log | Mã vết có trong `loops` nhưng log trên máy đã bị dọn; vẫn trả dòng tóm tắt |

Con trỏ gãy trong task hoặc trong `based_on` của plan là `REJECT` (C9).
