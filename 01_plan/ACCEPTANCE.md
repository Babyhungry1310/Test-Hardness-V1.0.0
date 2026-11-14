# ACCEPTANCE

<!-- ANCHOR: CYC_01 -->
## CYC-01
- `load_bank` đọc `data/bank.json` trả về đủ 5 câu, giữ thứ tự, mỗi câu có `id`, `text`, `answer` theo SRC-0001.
- `load_bank` báo lỗi khi một câu thiếu trường bắt buộc.
- `find_duplicate_ids` báo mọi id trùng theo thứ tự xuất hiện và không xóa câu hỏi nào.
- `python -m pytest -q --tb=line` đạt trên `main`.
- `data/` không chứa tên học viên thật.
<!-- END: CYC_01 -->

<!-- ANCHOR: CYC_02 -->
## CYC-02
- Công cụ xuất một file handout Markdown từ `data/bank.json`, mỗi câu một mục theo thứ tự trong ngân hàng.
- Công cụ dừng và báo id trùng trước khi xuất.
- File handout kết thúc bằng đúng một ký tự LF và không chứa ký tự CR do công cụ thêm vào, trên cả Linux và Windows.
- Không sinh file PDF.
<!-- END: CYC_02 -->

<!-- ANCHOR: CYC_03 -->
## CYC-03
- Hook `pre-commit` từ chối commit khi `HEAD` là `main`; hook `pre-push` từ chối ref đích `refs/heads/main` và `refs/tags/*`; nhánh làm việc đi qua; đúng trên Windows, trong worktree và với đường dẫn có khoảng trắng.
- Kiểm pre-flight báo đúng sai nhánh, đứng ở `main`, ref đẩy bị cấm và trạng thái cài hook, không sửa gì.
- Báo cáo kiểm phía GitHub nêu `PASS`, `FAIL` hoặc `UNKNOWN` cho từng dòng của `harness/MAIN_PROTECTION.md#GITHUB_RULES` đúng với dữ liệu đọc được.
- Bằng chứng của từng lớp nêu giới hạn và quyền cần theo `01_plan/SPEC_TOOLS.md#LAYERS`; không lớp nào được mô tả là chặn tuyệt đối.
- Bộ test ca biên phân rõ ca bị chặn và ca là giới hạn đã biết.
- Không tác tử nào đẩy thử vào `main` hay thẻ, không đổi cài đặt repo.
<!-- END: CYC_03 -->

<!-- ANCHOR: CYC_04 -->
## CYC-04
- `04_control/MODEL_CATALOG.md` và `04_control/MODEL_MATRIX.md` trên `main` đạt kiểm schema, dòng kiểm tuyến và dòng phân công; mỗi ca sai trong bộ test bị từ chối với lý do đúng.
- Danh sách model đủ điều kiện đúng `harness/MODEL_POLICY.md#ELIGIBILITY`: vai dùng công cụ không nhận model mới qua hỏi đáp ngắn; tuyến có lần kiểm mới nhất lỗi bị loại. Script không xếp hạng và không chọn thay LEAD.
- Phép so cùng model đúng `harness/MODEL_POLICY.md#SAME_MODEL`: biến thể ngoặc vuông và bí danh là cùng model; khác mã gốc là khác model dù cùng nhóm.
- REVIEWER trùng model thực tế với một WORKER của phần được kiểm bị báo dù tên agent hay tên tuyến khác nhau; REVIEWER khác mã gốc nhưng cùng nhóm thì đạt.
- Không có model phù hợp, hoặc thiếu model thực tế: mã thoát `1` kèm lý do; không suy model từ tên tuyến.
- Model yêu cầu và model thực tế được đối chiếu trên dòng `ASSIGNMENTS`, run và `RVW`.
<!-- END: CYC_04 -->

<!-- ANCHOR: CYC_05 -->
## CYC-05
- Tên nhánh theo `harness/GIT_CONVENTIONS.md` mục 1 và 7 được phân loại đúng; nhánh kiểm định theo mẫu cũ được nhận là mẫu cũ, không bị coi là lỗi.
- `clean` ở chế độ liệt kê cho đúng `SAFE`, `KEEP`, `ASK` theo `harness/tools/README.md#CLEAN_SPEC` và không xóa, không đổi ref nào; không có chế độ xóa.
- Kiểm thông điệp cuối nhận đúng thứ tự `SUMMARY`, `QUESTION`, một khối kết thúc và bắt được bảng nhiều cột.
- Mọi file sản phẩm, task, run, bản ghi kiểm định, file cổng và bằng chứng của CYC-01, CYC-02 giống từng byte với `main` @ 67a092f.
- RFC-0001 còn `OPEN`; `harness/schemas/LOG_GRAMMAR.md` không đổi.
<!-- END: CYC_05 -->

<!-- ANCHOR: CYC_06 -->
## CYC-06
- `scan`, cách ly và thẻ bọc đạt đủ 17 ca của `01_plan/SPEC_SCAN.md#CASES`; các cách lách đã biết được liệt kê trong bằng chứng của TK-0023.
- `scan` không sửa file đầu vào, không xuất đoạn trích nội dung nghi vấn, cho cùng đầu ra với cùng đầu vào và cùng bộ luật.
- Vượt giới hạn kích thước, độ sâu hoặc số lượng luôn cho `QUARANTINE`, không bao giờ `ALLOW`.
- Bằng chứng và mô tả PR chỉ kết luận trong phạm vi `01_plan/SPEC_SCAN.md#CLAIMS`.
- Repo không chứa chuỗi dạng bí mật hay dữ liệu ngoài do bộ test thêm vào.
<!-- END: CYC_06 -->

<!-- ANCHOR: CYC_07 -->
## CYC-07
- Kiểm batch bắt được: hai task cùng batch có đường dẫn trùng; một `write_scope` là thư mục phủ file của task kia; task phụ thuộc nhau cùng batch; task không thuộc hoặc thuộc hai batch. `01_plan/PLAN.md` trên `main` đạt.
- Với cấu hình mẫu `harness/templates/pytest.ini`, pytest chỉ thu thập test trong `tests/`; thiếu cấu hình thì test mẫu của khung bị thu thập (ca đối chứng).
- Kiểm thử worktree: hai nhánh có `write_scope` không giao nhau gộp sạch theo mọi thứ tự; xung đột và file ngoài `write_scope` bị báo; `main` và nhánh PR không đổi.
- `tools/README.md` có mục cho từng script, hook và giới hạn của từng lớp.
- Kiểm tương thích báo đúng khi dự án đã có `pytest.ini`, `pyproject.toml`, `tox.ini` hoặc `setup.cfg` chứa cấu hình pytest, và không ghi file nào.
- Hồi quy: `python -m pytest -q --tb=line` đạt đúng 23 test; `python -m pytest -q --tb=line tools/tests` đạt; trên Windows và Linux.
- Sản phẩm và bằng chứng của CYC-02 không đổi.
<!-- END: CYC_07 -->
