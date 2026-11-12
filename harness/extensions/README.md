# EXTENSIONS — CẮM THÊM CHỨC NĂNG MÀ KHÔNG SỬA LÕI

Theo `harness/HARNESS.md` mục 11 [THY-44, THY-45, DC-06]. Lõi là mọi file khác trong `harness/` cùng các file định tuyến và thư mục `00`–`06`. Một phần mở rộng là một thư mục `harness/extensions/<name>/`; thêm phần mở rộng chỉ là thêm thư mục đó, không sửa file nào của lõi. Phần mở rộng mẫu: [`example-skill/`](example-skill/README.md).

**Hai loại phần mở rộng.** *Đi kèm khung*: do repo mẫu phát hành, nằm trong `harness/extensions/`, được thay cùng `harness/` khi nâng cấp; `example-skill` thuộc loại này. *Riêng của dự án*: do một dự án tự thêm. Mục 11 đặt mọi phần mở rộng trong `harness/`, mà nâng cấp lại thay nguyên khối `harness/`, nên phần mở rộng riêng sẽ mất nếu người nâng cấp quên chép. Ở V1.0, `harness/extensions/` chỉ chứa phần mở rộng đi kèm khung; dự án chưa thêm phần mở rộng riêng cho tới khi bản khung 1.1.0 có chỗ đặt riêng ngoài `harness/` (mục 6).

## 1. Bốn loại

| `kind` | Dùng để | Ví dụ |
|---|---|---|
| `skill` | Thêm cách làm một loại việc cho tác tử, kích hoạt theo từ khóa hoặc loại phiên | Đối chiếu thuật ngữ trong prompt với `GLOSSARY.md` |
| `loop` | Thêm cách điều khiển loop ngoài script `loop` của lõi, trong giới hạn `max_loops` | Chạy lại `verify` trên nhiều phiên bản ngôn ngữ |
| `routing` | Gợi ý model hay nhóm model cho phiên | Chọn nhóm model của REVIEWER theo loại sản phẩm |
| `monitor` | Theo dõi và báo, không sửa gì | Đếm số run `BLOCKED` theo chu kỳ |

## 2. Thư mục

```text
harness/extensions/<name>/
├── manifest.yaml     Bắt buộc: khai báo ở mục 3
├── README.md         Bắt buộc: phần mở rộng làm gì, khi nào, các bước, đầu ra
└── <file khác>       Tùy chọn: script, dữ liệu cấu hình của chính phần mở rộng
```

`<name>` trùng trường `name` của manifest. Code trong thư mục tuân mục 8.4 như code bàn giao; `README.md` là tài liệu, được viết văn xuôi.

## 3. Đặc tả `manifest.yaml`

<!-- ANCHOR: MANIFEST -->
YAML đọc theo 1.2 core schema như bản ghi (`harness/schemas/EVOLUTION.md` mục 2). Đúng tám khóa dưới đây, theo đúng thứ tự này; không khóa nào khác; không dòng chú thích `#`; không khóa kiểu `note`, `comment`.

| Khóa | Kiểu | Bắt buộc | Giá trị cho phép | Ví dụ |
|---|---|:---:|---|---|
| `name` | Chuỗi | Có | `^[a-z0-9]+(?:-[a-z0-9]+)*$`; trùng tên thư mục | `example-skill` |
| `version` | Chuỗi | Có | Semantic Versioning `MAJOR.MINOR.PATCH` [THY-26], đặt trong ngoặc kép | `"1.0.0"` |
| `kind` | Chuỗi liệt kê | Có | `skill` · `loop` · `routing` · `monitor` | `skill` |
| `triggers` | Danh sách chuỗi | Có, ≥ 1 mục | Mỗi mục là một trong ba dạng: mã loại phiên (`ASK`, `RUN`, `CHANGE`, `DISCUSS`); mã sự kiện log của `harness/HARNESS.md` mục 7.3 (`LOOP_CLOSED`, `ESCALATE`…); từ khóa chữ thường theo mẫu `^[a-z0-9]+(?:-[a-z0-9]+)*$`, khớp khi từ đó có trong prompt | `["DISCUSS", "CHANGE", "glossary"]` |
| `reads` | Danh sách chuỗi | Có, được rỗng | Con trỏ hoặc đường dẫn theo `harness/schemas/POINTER_GRAMMAR.md`; đường dẫn kết thúc bằng `/` là cả thư mục | `["05_memory/GLOSSARY.md", "harness/HARNESS.md#CONCEPTS"]` |
| `writes` | Danh sách chuỗi | Có, được rỗng | Chỉ thư mục con của `.local/` (viết tắt của `<project>.local/`) mang tên phần mở rộng: `.local/scratch/<name>/`, `.local/logs/<name>/`, `.local/cache/<name>/` | `[".local/scratch/example-skill/"]` |
| `hook` | Chuỗi liệt kê | Có | `pre_session` · `pre_context` · `post_run` · `post_session` (mục 4) | `pre_context` |
| `requires` | Chuỗi | Có | Phiên bản khung tối thiểu, dạng `MAJOR.MINOR.PATCH`; không lớn hơn `harness/VERSION` | `"1.0.0"` |

Một phần mở rộng có đúng một `hook`. Cần cắm ở hai điểm thì tách thành hai phần mở rộng.

`writes` hẹp hơn mục 11 (mục 11 chỉ cấm vùng 🔒 và ✍): ở V1.0 phần mở rộng không ghi vào repo. Lý do: thư mục `02_work/`, `04_control/`, `05_memory/` chỉ một người ghi theo vai [THY-19], còn sản phẩm chỉ WORKER ghi trong `write_scope` của task (C3). Đầu ra của phần mở rộng là dữ liệu trên máy; tác tử đọc rồi ghi vào repo theo luật của vai mình.
<!-- END: MANIFEST -->

## 4. Bốn điểm cắm

<!-- ANCHOR: HOOKS -->
Thời điểm tính theo luồng phiên ở `harness/tools/INTEGRATION.md` mục 4. Tại mỗi điểm, phần mở rộng có `hook` đó chỉ chạy khi ít nhất một mục trong `triggers` khớp với phiên đang chạy.

| `hook` | Thời điểm | Phần mở rộng được làm | Ví dụ dùng |
|---|---|---|---|
| `pre_session` | Ngay sau kiểm tra đầu phiên (`harness/tools/PREFLIGHT.md` mục 2, hoặc `doctor`), trước khi đọc bất kỳ file nào ngoài file luật của vai | Kiểm thêm điều kiện riêng của dự án và báo đạt hoặc không đạt; không chặn thay `doctor` | Kiểm phiên bản trình biên dịch trong worktree |
| `pre_context` | Sau khi xếp loại phiên, trước khi ghép ngữ cảnh (`context`, hoặc tự chọn theo `harness/tools/README.md#CONTEXT_SIGNALS`) | Đề xuất thêm con trỏ nằm trong `reads`; đoạn được xếp sau đoạn trích của lõi và vẫn trong ngân sách dòng của vai | Đối chiếu thuật ngữ trong prompt |
| `post_run` | Sau khi WORKER ghi xong file run và tự soát (hoặc `validate`), trước khi commit và mở PR | Đọc run và `.local/logs/TK-nnnn/`, ghi kết quả vào `writes`; không sửa run hay sản phẩm | Thống kê thời gian từng loop |
| `post_session` | Sau `budget`, trước thông điệp cuối của phiên | Ghi tổng kết của phiên vào `writes`; không thêm gì vào thông điệp cuối | Ghi số dòng ngữ cảnh đã nạp vào bảng theo dõi trên máy |

**Ai chạy phần mở rộng.** Khi các script `doctor`, `context`, `trace`, `budget` đã có, script ở điểm cắm tương ứng đọc mọi `harness/extensions/*/manifest.yaml`. Khi chưa có script, tác tử tự làm ở đúng điểm cắm, theo góc nhìn của vai [HARNESS.md mục 6.1]:

- LEAD: đọc các `manifest.yaml`, chọn phần mở rộng có `triggers` khớp, đọc `README.md` của nó rồi làm theo.
- WORKER: chỉ dùng phần mở rộng khi LEAD đưa đường dẫn `harness/extensions/<name>/README.md` vào `read_also` của task. WORKER không tự đọc thư mục `harness/extensions/`.
- REVIEWER: không dùng phần mở rộng ở V1.0; gói kiểm định giữ đúng `harness/rules/REVIEWER.md` luật 1.
<!-- END: HOOKS -->

## 5. Điều phần mở rộng không được làm

<!-- ANCHOR: FORBIDDEN -->
1. Sửa, xóa hay đổi tên bất kỳ file nào ngoài thư mục của chính nó; nhất là `harness/HARNESS.md`, `rules/`, `schemas/`, `templates/`, `tools/`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `harness.yaml`, `.github/`.
2. Ghi vào repo; ghi vùng 🔒 hay file ✍; ghi sổ, task, run, `RVW`, `DSC`, `STATE.md`. Mọi thứ ghi ra nằm trong `writes`.
3. Thêm khóa vào bản ghi, thêm loại bản ghi, cấp mã, thêm giá trị liệt kê, thêm sự kiện log, thêm neo vào file của lõi. Cần thuật ngữ mới thì LEAD đề xuất với OWNER và ghi `DEC`.
4. Đổi hay nới luật của vai: không tăng `max_loops`, không vượt ngân sách dòng, không mở rộng `write_scope`, không bỏ khối `CONFIRM` hay bước chờ `OK`/`Go`.
5. Merge, đẩy thẳng vào `main`, bật auto-merge, ép đẩy, xóa nhánh hay worktree.
6. Gọi model từ script của phần mở rộng (`harness/HARNESS.md` mục 9).
7. Đọc ngoài `reads`; đọc dữ liệu Zone 2, Zone 3; đọc log thô ngoài `.local/logs/` của task đang chạy; gửi dữ liệu ra khỏi máy.
8. Đưa dữ liệu ngoài vào prompt mà không qua `scan` và phần bọc ở `harness/HARNESS.md` mục 10.2.
9. Xuất khối chuẩn hay thông điệp cuối riêng; thêm ghi chú vào manifest, dữ liệu hay code của nó (mục 8.4).
10. Dựa vào tính năng Orca hay 9Router chưa xác nhận ở `harness/tools/INTEGRATION.md#FEATURES`.
<!-- END: FORBIDDEN -->

## 6. Thêm, gỡ và nâng cấp

| Việc | Cách làm |
|---|---|
| Thêm | PR `lead: add extension <name>` chỉ thêm thư mục `harness/extensions/<name>/`. PR chạm `harness/` (🔒) nên C4 đánh dấu "OWNER cần đọc kỹ". LEAD rà bảng kiểm mục 7 và ghi kết quả vào khối `MERGE`. OWNER merge |
| Gỡ | PR `lead: remove extension <name>` chỉ xóa thư mục đó |
| Đổi phiên bản | Sửa file trong thư mục và tăng `version` theo Semantic Versioning |
| Nâng cấp khung | `harness/` được thay nguyên khối (mục 11), kể cả `harness/extensions/`. Trước khi merge PR `upgrade/<version>`, LEAD chạy `git diff --name-status origin/main...HEAD -- harness/extensions` và liệt kê mọi dòng `D` trong khối `MERGE`; có thư mục bị xóa mà không có trong bản khung mới thì dừng, đưa về OWNER bằng khối `QUESTION` |

**Điểm nâng cấp cho bản khung 1.1.0** (OWNER đã chốt hướng, `harness/tools/INTEGRATION.md#OWNER_ANSWERS` câu 3): tách chỗ đặt phần mở rộng riêng của dự án ra một thư mục thuộc dự án, ngoài `harness/`, để nâng cấp không chạm tới; sửa `harness/HARNESS.md` mục 5.1 và 11 kèm một `DEC`. Tên thư mục do OWNER chọn trong PR nâng cấp đó.

## 7. Bảng kiểm một phần mở rộng

| # | Kiểm | Đạt khi |
|:---:|---|---|
| 1 | Chỉ thêm file | `git diff --name-status origin/main...HEAD` chỉ có dòng `A` dưới `harness/extensions/<name>/` |
| 2 | Đủ hai file bắt buộc | Có `manifest.yaml` và `README.md` |
| 3 | Manifest đúng đặc tả | Đúng tám khóa, đúng thứ tự, đúng kiểu và giá trị ở mục 3; `name` trùng tên thư mục |
| 4 | Không ghi chú | `Select-String -Path harness\extensions\<name>\manifest.yaml -Pattern '(^\|\s)#'` không in gì (dấu `#` dính liền trong con trỏ như `HARNESS.md#CONCEPTS` không phải chú thích); code không có dòng ghi chú (C13) |
| 5 | Ghi đúng chỗ | Mọi mục trong `writes` nằm dưới `.local/` và mang tên phần mở rộng |
| 6 | Đọc đúng chỗ | Mọi mục trong `reads` tra được (C9); không trỏ tới `.local/`, dữ liệu Zone 2, Zone 3 |
| 7 | Tương thích khung | `requires` ≤ `harness/VERSION` |
| 8 | Không vi phạm mục 5 | `README.md` không có bước nào thuộc danh sách cấm |
