# BUILD TASKS — ĐỀ XUẤT VIỆC VIẾT CODE CHO SCRIPT

Danh sách **đề xuất** để OWNER và LEAD bàn trong một phiên `DISCUSS`. Chưa có `DEC`, chưa có task: các việc dưới đây đánh số `#1`, `#2`…, không mang mã `TK`. Khi được chốt, LEAD đưa chúng vào `01_plan/PLAN.md` và cấp mã task theo `harness/rules/LEAD.md` luật 21–22.

Thứ tự theo `harness/tools/README.md#DEPENDENCIES` (Giai đoạn 3): thư viện chung → `validate` → `ledger` → `discuss` → `state` → `get` → `doctor` → `scan` → `trace` → `budget` → `context` → `loop` → `index`. Riêng kiểm tra C6 của `validate` dùng `state` (mũi tên `STATE --> VALIDATE` trong sơ đồ), nên tách thành việc `#16`, làm sau `state`.

## 1. Điều cần chốt trước khi giao việc đầu tiên

| # | Điều cần chốt | Ai quyết | Ảnh hưởng |
|:---:|---|---|---|
| 1 | Ngôn ngữ Python 3.11 trở lên; thư viện `jsonschema`, `ruamel.yaml` (đọc YAML 1.2 core như `harness/schemas/EVOLUTION.md` mục 2), `pytest` | LEAD ghi `DEC` (thêm thư viện) | Mọi việc |
| 2 | Chạy các việc ở đâu. Code script nằm ở `harness/tools/` (🔒), ngoài `product_paths` của repo mẫu (`["03_output/"]`), mà `write_scope` chỉ được gồm file trong `product_paths` (HARNESS.md mục 5.5). Không sửa `harness.yaml` của repo mẫu, vì mọi dự án tạo từ mẫu sẽ kế thừa quyền ghi `harness/tools/` cho WORKER. OWNER đã chọn (`INTEGRATION.md#OWNER_ANSWERS` câu 4): một repo phát triển riêng, không phải repo mẫu, có `product_paths: ["tools/"]`; ở đó script là sản phẩm thường, đường dẫn `harness/tools/…` trong mục 3 đọc là `tools/…`; mỗi bản phát hành chép `tools/` vào `harness/tools/` của repo mẫu bằng một PR `upgrade/<version>` kèm `DEC`, OWNER merge | OWNER (đã chốt) | Mọi việc |
| 3 | Tên tiếng Anh của ba nhãn tin cậy (`harness/tools/README.md#OWNER_ANSWERS`, câu 1) vào Phụ lục A | OWNER, trong PR nâng phiên bản khung | `#26` |
| 4 | Tính năng Orca và 9Router đã xác nhận (`harness/tools/INTEGRATION.md#FEATURES`) | OWNER kiểm theo `harness/tools/PREFLIGHT.md` mục 3 | `#22`, `#24`, `#28` |

## 2. Quy ước chung cho mọi việc

- Cây file: script `harness/tools/<tên>.py`; thư viện chung `harness/tools/lib/`; test `harness/tools/tests/`; thư viện cần cài ghi ở `harness/tools/requirements.txt`.
- Dữ liệu thử: dự án ví dụ `harness/templates/examples/` (file hợp lệ và file `.invalid`, `INVALID_CASES.md`, `POINTER_TESTS.md`); dữ liệu tạm của test ghi vào thư mục tạm của hệ điều hành, không ghi vào repo.
- Chạy được trên Windows: đường dẫn qua `pathlib`, chấp nhận khoảng trắng và `\`; gọi Git bằng danh sách tham số, không qua shell.
- Mỗi script: tham số dòng lệnh, cờ `--json`, mã thoát `0` đạt · `1` không đạt · `2` lỗi dùng hoặc lỗi nội bộ (ghi `TOOL_ERROR`). Không script nào gọi model.
- Code tuân mục 8.4: không dòng ghi chú, không docstring, không `TODO`.
- Mỗi việc: một phiên, `write_scope` ≤ 5 file, ≤ khoảng 400 dòng thay đổi, `max_loops: 3`.

## 3. Danh sách việc

<!-- ANCHOR: TASK_LIST -->
### Nhóm 0. Thư viện chung

**#1. Đọc bản ghi**
- goal: Tách YAML đầu file theo YAML 1.2 core, dòng trạng thái và đoạn theo neo của một bản ghi
- write_scope: `harness/tools/requirements.txt`, `harness/tools/lib/__init__.py`, `harness/tools/lib/record.py`, `harness/tools/tests/test_record.py`
- verify: `python -m pytest -q harness/tools/tests/test_record.py`
- done_when: đọc được mọi bản ghi `.md` có YAML trong dự án ví dụ · `escalate: no` đọc ra chuỗi `"no"`, ngày đọc ra chuỗi · tách đúng các dòng dưới `## Status (newest first)` · trả đúng đoạn giữa `ANCHOR` và `END` · đạt mọi kiểm tra trong file test
- size: 1 phiên · 4 file · ~200 dòng · phụ thuộc: không

**#2. Vị trí repo và cấu hình**
- goal: Tìm gốc worktree, bản checkout chính, thư mục `<project>.local`; đọc `harness.yaml`
- write_scope: `harness/tools/lib/repo.py`, `harness/tools/tests/conftest.py`, `harness/tools/tests/test_repo.py`
- verify: `python -m pytest -q harness/tools/tests/test_repo.py`
- done_when: từ một worktree tìm ra `<project>.local` cạnh bản checkout chính · đúng với đường dẫn có khoảng trắng · đọc `harness.yaml` của dự án ví dụ ra `max_loops: 3` · đạt mọi kiểm tra
- size: 1 phiên · 3 file · ~150 dòng · phụ thuộc: #1

**#3. Kiểm theo schema**
- goal: Chọn schema theo đường dẫn bản ghi và trả danh sách trường lỗi
- write_scope: `harness/tools/lib/schema.py`, `harness/tools/tests/test_schema.py`
- verify: `python -m pytest -q harness/tools/tests/test_schema.py`
- done_when: 17 bản ghi hợp lệ của dự án ví dụ đạt · 8 file `.invalid` loại schema trong `INVALID_CASES.md` bị loại đúng trường · đạt mọi kiểm tra
- size: 1 phiên · 2 file · ~150 dòng · phụ thuộc: #1

**#4. Ngữ pháp dòng**
- goal: Kiểm dòng trạng thái, dòng có cấu trúc, dòng log và dòng chỉ mục log
- write_scope: `harness/tools/lib/grammar.py`, `harness/tools/tests/test_grammar.py`
- verify: `python -m pytest -q harness/tools/tests/test_grammar.py`
- done_when: mọi ví dụ "Đúng" trong `STATUS_GRAMMAR.md`, `LOG_GRAMMAR.md` đạt và mọi ví dụ "Sai" bị loại · `RSK-0002….md.invalid` và `DSC-….md.invalid` bị loại · đạt mọi kiểm tra
- size: 1 phiên · 2 file · ~200 dòng · phụ thuộc: #1

**#5. Con trỏ**
- goal: Phân tích và tra con trỏ, tìm thư mục gốc rồi kho lạnh, trả năm loại lỗi
- write_scope: `harness/tools/lib/pointer.py`, `harness/tools/tests/test_pointer.py`
- verify: `python -m pytest -q harness/tools/tests/test_pointer.py`
- done_when: mọi dòng trong `POINTER_TESTS.md` cho đúng kết quả · không bao giờ tra file `.invalid` · con trỏ gãy trả lỗi, không trả nội dung · đạt mọi kiểm tra
- size: 1 phiên · 2 file · ~200 dòng · phụ thuộc: #1, #2

### Nhóm 1. `validate`

**#6. `validate` cho từng file**
- goal: Lệnh `validate` kiểm một hay nhiều file, trả `PASS`, `REJECT` hoặc `AUTOFIX` theo mục 8.2
- write_scope: `harness/tools/validate.py`, `harness/tools/lib/autofix.py`, `harness/tools/tests/test_validate_file.py`
- verify: `python -m pytest -q harness/tools/tests/test_validate_file.py`
- done_when: 10 file `.invalid` loại bản ghi bị `REJECT` · giá trị liệt kê viết thường và ngày sai dạng được `AUTOFIX` kèm báo đã sửa gì · không bao giờ đổi nội dung văn bản · mã thoát đúng · đạt mọi kiểm tra
- size: 1 phiên · 3 file · ~250 dòng · phụ thuộc: #3, #4, #5

**#7. C1, C2, C3**
- goal: Kiểm run của một PR: tên, số run, số loop, `DONE`/`BLOCKED`, phạm vi ghi
- write_scope: `harness/tools/lib/changes.py`, `harness/tools/lib/checks_runs.py`, `harness/tools/tests/test_checks_runs.py`
- verify: `python -m pytest -q harness/tools/tests/test_checks_runs.py`
- done_when: run của dự án ví dụ đạt · các ca dựng sẵn bị loại: số run nhảy cóc, loop thứ tư trong một run, run `DONE` có `unverified`, đủ `max_loops` loop `FAIL` mà không `BLOCKED`, PR chạm file ngoài `write_scope` · đạt mọi kiểm tra
- size: 1 phiên · 3 file · ~300 dòng · phụ thuộc: #6

**#8. C4, C5, C7, C8, C14**
- goal: Đánh dấu vùng 🔒 và ✍, kiểm sổ chỉ-thêm, giới hạn dòng, bí mật, test bị xóa hay nới
- write_scope: `harness/tools/lib/checks_files.py`, `harness/tools/lib/patterns.py`, `harness/tools/tests/test_checks_files.py`
- verify: `python -m pytest -q harness/tools/tests/test_checks_files.py`
- done_when: sửa một dòng trạng thái cũ bị loại · run 46 dòng bị loại · chuỗi dạng khóa riêng PEM bị loại · xóa một file test được đánh dấu · mẫu Zone 3 nằm ở `patterns.py` để `scan` dùng chung · đạt mọi kiểm tra
- size: 1 phiên · 3 file · ~300 dòng · phụ thuộc: #6, #7

**#9. C9, C10, C11, C12, C13**
- goal: Kiểm truy nguồn, khớp `DSC`–`DEC`, file cổng `PLAN_GO`, phiên bản khung, không ghi chú
- write_scope: `harness/tools/lib/checks_refs.py`, `harness/tools/tests/test_checks_refs.py`
- verify: `python -m pytest -q harness/tools/tests/test_checks_refs.py`
- done_when: dự án ví dụ đạt · `TK-0002.md.invalid`, `src/dupes.py.invalid`, `data/bank.json.invalid` bị loại · C11 chỉ xét đường dẫn mục 5.1, bỏ qua `harness/` · đạt mọi kiểm tra
- size: 1 phiên · 2 file · ~300 dòng · phụ thuộc: #6

**#10. Bật `check.yml`**
- goal: Workflow `check` chạy `validate` trên mọi PR vào `main`, lấy bộ kiểm tra từ `main`, không chạy code của PR
- write_scope: `.github/workflows/check.yml`, `.github/README.md`, `harness/tools/tests/test_check_workflow.py`
- verify: `python -m pytest -q harness/tools/tests/test_check_workflow.py`
- done_when: trigger `pull_request` vào `main` · `permissions: contents: read` · script lấy từ commit `main`, nội dung PR chỉ được đọc · `.github/README.md` ghi `check.yml` đã kích hoạt · đạt mọi kiểm tra
- size: 1 phiên · 3 file · ~120 dòng · phụ thuộc: #7, #8, #9

### Nhóm 2. `ledger`

**#11. Tạo bản ghi và cấp mã**
- goal: `ledger` tạo `DEC`, `RSK`, `REQ`, task, chu kỳ, `SRC` từ mẫu; mã = 1 + số lớn nhất ở gốc và kho lạnh
- write_scope: `harness/tools/ledger.py`, `harness/tools/lib/ledger_ops.py`, `harness/tools/tests/test_ledger_new.py`
- verify: `python -m pytest -q harness/tools/tests/test_ledger_new.py`
- done_when: trên dự án ví dụ mã `DEC` kế tiếp là `DEC-0005`, `RSK` kế tiếp là `RSK-0003` · file tạo ra qua được `validate` · không ghi thân văn bản · đạt mọi kiểm tra
- size: 1 phiên · 3 file · ~250 dòng · phụ thuộc: #6

**#12. Trạng thái, kho lạnh, liệt kê**
- goal: `ledger` chèn dòng trạng thái, chuyển kho lạnh, liệt kê theo từ khóa, truy chuỗi `supersedes`, báo chủ đề quá 10 `DEC`
- write_scope: `harness/tools/ledger.py`, `harness/tools/lib/ledger_ops.py`, `harness/tools/tests/test_ledger_status.py`
- verify: `python -m pytest -q harness/tools/tests/test_ledger_status.py`
- done_when: dòng mới nằm ngay dưới `## Status` · `SUPERSEDED_BY` chuyển file vào `superseded/` · không chuyển ngược · chuỗi `DEC-0002` trả `DEC-0001` · đạt mọi kiểm tra
- size: 1 phiên · 3 file · ~250 dòng · phụ thuộc: #11

### Nhóm 3. `discuss`

**#13. Bản ghi thảo luận**
- goal: `discuss` tạo `DSC`, thêm sự kiện, ghi `ACCEPTED`/`REJECTED`, liệt kê `PROPOSAL` mở, sinh nháp `DEC` qua `ledger`
- write_scope: `harness/tools/discuss.py`, `harness/tools/lib/discuss_ops.py`, `harness/tools/tests/test_discuss.py`
- verify: `python -m pytest -q harness/tools/tests/test_discuss.py`
- done_when: sự kiện quá 25 từ hoặc `DSC` quá 40 dòng bị từ chối · `ACCEPTED` sinh nháp `DEC` có `origin` đúng (C10) · trên `DSC` ví dụ, `PROPOSAL` mở là rỗng · đạt mọi kiểm tra
- size: 1 phiên · 3 file · ~250 dòng · phụ thuộc: #12

### Nhóm 4. `state`

**#14. Sinh `STATE.md`**
- goal: `state` sinh lại mục 1, 2, 3, 5 và ba dòng đầu, giữ nguyên mục 4
- write_scope: `harness/tools/state.py`, `harness/tools/lib/projection.py`, `harness/tools/tests/test_state.py`
- verify: `python -m pytest -q harness/tools/tests/test_state.py`
- done_when: chạy trên dự án ví dụ cho mục 1, 2, 3, 5 giống `04_control/STATE.md` ví dụ · mục 4 không đổi · đạt mọi kiểm tra
- size: 1 phiên · 3 file · ~300 dòng · phụ thuộc: #12

**#15. Bảng nghiệm thu và các khung**
- goal: `state` sinh bảng nghiệm thu cổng PASS, khung digest chu kỳ, trang chủ đề, khung `CORE.md`
- write_scope: `harness/tools/state.py`, `harness/tools/lib/projection.py`, `harness/tools/tests/test_state_tables.py`
- verify: `python -m pytest -q harness/tools/tests/test_state_tables.py`
- done_when: bảng của `CYC-01` giống neo `ACCEPTANCE` của `CYC-01_PASS.md` ví dụ · khung tạo ra qua `validate` · đạt mọi kiểm tra
- size: 1 phiên · 3 file · ~200 dòng · phụ thuộc: #14

**#16. C6 của `validate`**
- goal: `validate` kiểm `STATE.md` khớp dấu hiệu file và bản gốc bằng `state`
- write_scope: `harness/tools/validate.py`, `harness/tools/lib/checks_state.py`, `harness/tools/tests/test_check_c6.py`
- verify: `python -m pytest -q harness/tools/tests/test_check_c6.py`
- done_when: `STATE.md` ví dụ đạt · `PHASE: EXECUTE` khi chưa có `PLAN_GO.md` ở gốc bị loại · file trong `harness/` không được tính là dấu hiệu · đạt mọi kiểm tra
- size: 1 phiên · 3 file · ~150 dòng · phụ thuộc: #14

### Nhóm 5. `get`

**#17. Tra con trỏ và mã vết**
- goal: `get` trả đúng đoạn cho con trỏ và dòng tóm tắt loop cho mã vết
- write_scope: `harness/tools/get.py`, `harness/tools/tests/test_get.py`
- verify: `python -m pytest -q harness/tools/tests/test_get.py`
- done_when: `DEC-0004#RATIONALE` trả đúng đoạn · `DEC-0001` tìm được trong kho lạnh · `TK-0001.L03` trả dòng `loops` và dòng log ví dụ · log đã dọn vẫn trả dòng tóm tắt · đạt mọi kiểm tra
- size: 1 phiên · 2 file · ~200 dòng · phụ thuộc: #5

### Nhóm 6. `doctor`

**#18. Kiểm đầu phiên**
- goal: `doctor` làm các dòng có ghi "`doctor`" của `PREFLIGHT.md` mục 2, gọi C6, C8, C12 của `validate`
- write_scope: `harness/tools/doctor.py`, `harness/tools/tests/test_doctor.py`
- verify: `python -m pytest -q harness/tools/tests/test_doctor.py`
- done_when: mỗi điều kiện sai cho mã thoát `1` và nêu số dòng `PREFLIGHT.md` · không sửa file nào · chạy được làm lệnh thiết lập ở `INTEGRATION.md#ORCA_SETUP` · đạt mọi kiểm tra
- size: 1 phiên · 2 file · ~200 dòng · phụ thuộc: #8, #9, #16

### Nhóm 7. `scan`

**#19. Quét dữ liệu ngoài**
- goal: `scan` xếp một file vào `ALLOW`, `WARN`, `QUARANTINE`, `BLOCK` theo bộ luật, ghi `SCAN_HIT`
- write_scope: `harness/tools/scan.py`, `harness/tools/scan_rules.yaml`, `harness/tools/lib/patterns.py`, `harness/tools/tests/test_scan.py`
- verify: `python -m pytest -q harness/tools/tests/test_scan.py`
- done_when: cột "Ví dụ lành" của `README.md#SCAN_SIGNALS` cho `ALLOW` hoặc `WARN`, cột "Ví dụ độc" cho `QUARANTINE` hoặc `BLOCK` · `mau-a.txt` của `DRY_RUN.md` bị chuyển vào `.local/quarantine/` · `BLOCK` chỉ lưu đường dẫn và giá trị băm · dòng `SCAN_HIT` đúng `LOG_GRAMMAR.md` · đạt mọi kiểm tra
- size: 1 phiên · 4 file · ~300 dòng · phụ thuộc: #8

### Nhóm 8. `trace`

**#20. Chạy `verify` và đếm loop**
- goal: `trace` chạy lệnh `verify` lấy từ task, khép loop, đếm loop liên tục qua các run, từ chối khi đủ `max_loops`, ghi log và `index.md`
- write_scope: `harness/tools/trace.py`, `harness/tools/lib/tracelog.py`, `harness/tools/tests/test_trace_loop.py`
- verify: `python -m pytest -q harness/tools/tests/test_trace_loop.py`
- done_when: lần chạy đầu của run `R2` ra `L04` · lần thứ tư trong một run bị từ chối với mã thoát riêng · dòng log và `index.md` đúng `LOG_GRAMMAR.md` · không nhận lệnh kiểm qua tham số · đạt mọi kiểm tra
- size: 1 phiên · 3 file · ~300 dòng · phụ thuộc: #2, #4

**#21. Đóng loop và khung run**
- goal: `trace` tính số run, sinh khung file run, điền `loops`, khi loop đóng thì gom bằng chứng và ghi `LOOP_CLOSED`, `ESCALATE`
- write_scope: `harness/tools/trace.py`, `harness/tools/lib/tracelog.py`, `harness/tools/tests/test_trace_close.py`
- verify: `python -m pytest -q harness/tools/tests/test_trace_close.py`
- done_when: dựng lại được `TK-0001_R1_BLOCKED.md` ví dụ ở các trường `loops`, `evidence` · số run đúng 1 + lớn nhất trên `main` · khung run qua `validate` · đạt mọi kiểm tra
- size: 1 phiên · 3 file · ~250 dòng · phụ thuộc: #20

**#22. Dòng span**
- goal: Ở mức `SPAN`, `trace` rút các bước từ nhật ký phiên của công cụ tác tử thành dòng `SPAN`
- write_scope: `harness/tools/trace.py`, `harness/tools/lib/tracelog.py`, `harness/tools/tests/test_trace_span.py`
- verify: `python -m pytest -q harness/tools/tests/test_trace_span.py`
- done_when: dòng `SPAN` có mã vết `.Snn`, đếm lại từ `S01` mỗi loop, đúng `LOG_GRAMMAR.md` · đọc log ở mức `LOOP` cho cùng kết quả như trước khi có span · đạt mọi kiểm tra
- size: 1 phiên · 3 file · ~200 dòng · phụ thuộc: #21
- điều kiện giao: OWNER đã kiểm định dạng nhật ký phiên của công cụ tác tử đang dùng; chưa có thì chưa giao

### Nhóm 9. `budget`

**#23. Đếm ngữ cảnh và ghi model**
- goal: `budget` đếm dòng, ước tính token phần ngữ cảnh đã nạp; ghi `model` (cách A ở `INTEGRATION.md#SESSION_MODEL`) và `usage` vào run
- write_scope: `harness/tools/budget.py`, `harness/tools/tests/test_budget.py`
- verify: `python -m pytest -q harness/tools/tests/test_budget.py`
- done_when: đếm đúng số dòng của danh sách file và con trỏ cho trước · điền `model`, `usage` mà run vẫn qua `validate` · không gửi gì ra ngoài máy · đạt mọi kiểm tra
- size: 1 phiên · 2 file · ~150 dòng · phụ thuộc: #5, #6

**#24. Đọc số liệu 9Router**
- goal: `budget` lấy model thực tế và số token của phiên từ 9Router (cách D ở `INTEGRATION.md#SESSION_MODEL`)
- write_scope: `harness/tools/budget.py`, `harness/tools/tests/test_budget_router.py`
- verify: `python -m pytest -q harness/tools/tests/test_budget_router.py`
- done_when: với dữ liệu mẫu chép từ một phiên thử, model đọc ra khớp model công cụ hiển thị · khi 9Router không trả lời thì giữ cách A và báo, không đoán · đạt mọi kiểm tra
- size: 1 phiên · 2 file · ~150 dòng · phụ thuộc: #23
- điều kiện giao: `INTEGRATION.md#FEATURES` dòng 9 đã xác nhận

### Nhóm 10. `context`

**#25. Kế hoạch nạp**
- goal: `context` ở chế độ kế hoạch: từ prompt ra danh sách con trỏ và số dòng theo `README.md#CONTEXT_SIGNALS`
- write_scope: `harness/tools/context.py`, `harness/tools/lib/context_rules.py`, `harness/tools/tests/test_context_plan.py`
- verify: `python -m pytest -q harness/tools/tests/test_context_plan.py`
- done_when: mỗi dòng của bảng 2.9.1 có một ca thử cho đúng dữ liệu cần nạp · vượt ngân sách thì bỏ nguyên đoạn và liệt kê con trỏ bị bỏ · không khớp gì thì nạp mặc định và báo rõ · đạt mọi kiểm tra
- size: 1 phiên · 3 file · ~300 dòng · phụ thuộc: #13, #17, #19

**#26. Ghép prompt**
- goal: `context` ghép prompt theo thứ tự 2.9.3, gắn nhãn tin cậy, bọc dữ liệu ngoài
- write_scope: `harness/tools/context.py`, `harness/tools/lib/context_rules.py`, `harness/tools/tests/test_context_build.py`
- verify: `python -m pytest -q harness/tools/tests/test_context_build.py`
- done_when: hai lần chạy cùng prompt cho cùng kết quả · phần đầu giống nhau giữa các phiên cùng vai · đoạn ngoài chưa qua `scan` không được ghép · đạt mọi kiểm tra
- size: 1 phiên · 3 file · ~250 dòng · phụ thuộc: #25 và điều cần chốt số 3

### Nhóm 11. `loop`

**#27. Kích hoạt bằng Git**
- goal: `loop` kiểm điều kiện, tính số run, tạo worktree bằng `git worktree add`, chạy lệnh thiết lập, in câu `Run TK-nnnn` cho OWNER
- write_scope: `harness/tools/loop.py`, `harness/tools/tests/test_loop_git.py`
- verify: `python -m pytest -q harness/tools/tests/test_loop_git.py`
- done_when: từ chối khi chưa có `PLAN_GO.md` trên `main` hoặc `depends_on` chưa `DONE` · không chạy song song hai task có `write_scope` chồng nhau · không merge, không gọi model · đạt mọi kiểm tra
- size: 1 phiên · 2 file · ~250 dòng · phụ thuộc: #18, #21, #26

**#28. Kích hoạt qua Orca**
- goal: `loop` tạo worktree và giao task qua lệnh `orca worktree create`, chờ tác tử xong
- write_scope: `harness/tools/loop.py`, `harness/tools/tests/test_loop_orca.py`
- verify: `python -m pytest -q harness/tools/tests/test_loop_orca.py`
- done_when: lệnh gửi cho Orca có tên workspace, nhánh và prompt đúng `INTEGRATION.md#ORCA_ASSIGN` · Orca không trả lời thì quay về đường Git của `#27` · đạt mọi kiểm tra
- size: 1 phiên · 2 file · ~200 dòng · phụ thuộc: #27
- điều kiện giao: `INTEGRATION.md#FEATURES` dòng 1, 2, 4, 5, 6 đã xác nhận

### Nhóm 12. `index`

**#29. Chỉ mục tùy chọn**
- goal: `index` sinh chỉ mục mã, neo, từ khóa vào `.local/cache/`; `get` và `context` dùng khi chỉ mục còn mới
- write_scope: `harness/tools/index.py`, `harness/tools/get.py`, `harness/tools/context.py`, `harness/tools/tests/test_index.py`
- verify: `python -m pytest -q harness/tools/tests/test_index.py`
- done_when: `get` và `context` cho cùng kết quả khi có và khi không có chỉ mục · chỉ mục cũ hơn commit hiện tại thì được dựng lại · không ghi gì vào repo · đạt mọi kiểm tra
- size: 1 phiên · 4 file · ~200 dòng · phụ thuộc: #17, #26
<!-- END: TASK_LIST -->

## 4. Kiểm cỡ việc theo mục 7.1

| Tiêu chí | Kết quả |
|---|---|
| Một phiên | Cả 29 việc; ước lượng 120–300 dòng mỗi việc |
| `write_scope` ≤ 5 file | Nhiều nhất 4 file (`#1`, `#19`, `#29`) |
| Có `verify` và `done_when` | Cả 29 việc; mỗi `verify` là một lệnh `pytest` chạy một file test |
| ≤ khoảng 400 dòng thay đổi | Ước lượng lớn nhất 300 dòng |
| Có điều kiện giao | `#22`, `#24`, `#28` chỉ giao khi OWNER đã xác nhận tính năng tương ứng |
