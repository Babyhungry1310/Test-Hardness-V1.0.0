# SPEC_TOOLS — QUY ƯỚC CHUNG CHO CYC-03 TỚI CYC-07

Nguồn: DEC-0015, DEC-0016. Nền: `main` @ 67a092f.

<!-- ANCHOR: CONVENTIONS -->
## 1. Quy ước
- Cây file: script `tools/<tên>.py`; hook `tools/hooks/`; test `tools/tests/test_<tên>.py`; dữ liệu test cố định `tools/tests/data/`; thư viện cần cài `tools/requirements.txt`. Đường dẫn `harness/tools/…` trong đặc tả của khung đọc là `tools/…`.
- Python 3.11 trở lên. Thư viện ngoài chuẩn chỉ gồm `jsonschema`, `ruamel.yaml`, `pytest`. Không script nào gọi model hay gọi mạng.
- Mỗi script: tham số dòng lệnh, cờ `--json`, mã thoát `0` đạt · `1` không đạt · `2` lỗi dùng hoặc lỗi nội bộ.
- Windows: đường dẫn qua `pathlib`, chấp nhận khoảng trắng và `\`; gọi Git bằng danh sách tham số, không qua shell; file văn bản ghi với newline LF.
- Test chạy từ gốc repo bằng `python -m pytest -q --tb=line tools/tests/<file>`; import theo dạng `tools.<module>`. Dữ liệu tạm ghi vào `tmp_path`, không ghi vào repo. Repo Git dùng cho test là repo tạm trong `tmp_path` với remote là thư mục bare cục bộ.
- Test không đổi cấu hình Git, nhánh, thẻ hay remote của bản clone đang làm việc.
- `pytest.ini` của dự án không bị sửa. Lệnh `python -m pytest -q --tb=line` vẫn chỉ thu thập `tests/` và đạt đúng 23 test; test trong `tools/tests/` chỉ chạy khi nêu đường dẫn.
- Code tuân `harness/HARNESS.md` mục 8.4: không dòng ghi chú, không docstring, không `TODO`. Dòng khai báo trình thông dịch của hook được phép.
- Không lưu vào repo: chuỗi có dạng bí mật, dữ liệu thật, log thô. Đầu ra kiểm đã cắt gọn nằm ở `03_output/CYC-nn/checks/`, tên bắt đầu bằng mã task; log đầy đủ ở `<project>.local/logs/`.
- Không task nào sửa `src/`, `tests/`, `data/`, `pytest.ini`, `harness/`, `.github/`, ba file định tuyến.
<!-- END: CONVENTIONS -->

<!-- ANCHOR: MODELS -->
## 2. Model
- LEAD chọn model cho từng lần giao theo `harness/MODEL_POLICY.md` (bản 1.0.2) và `01_plan/SPEC_MODELS.md`; không có model gắn cố định cho chỗ hay task.
- W1, W2, W3 là chỗ chạy song song và loại việc: W1 logic, thuật toán, công cụ, unit test; W2 triển khai, tích hợp, tài liệu; W3 ca biên, stress, bảo mật, phản biện.
- Ghi model yêu cầu, tuyến, lý do và hạn mức ở neo `ASSIGNMENTS` trước khi phiên bắt đầu; ghi model thực tế vào `model` của run và `reviewer_model` của `RVW`. Điều chưa xác minh ghi `chưa xác minh`.
- REVIEWER khác mã model thực tế với các WORKER đã làm phần được kiểm; biến thể cùng mã gốc là cùng model; tên agent hay tên tuyến khác nhau không đủ.
- Không có model phù hợp, không xác định được model thực tế, hoặc không có REVIEWER phù hợp: `BLOCKED`, báo OWNER.
<!-- END: MODELS -->

<!-- ANCHOR: CLASSIFICATION -->
## 3. Đã là quy tắc, còn cần làm
| Nhóm | Đã là quy tắc trong khung | Còn cần code, cấu hình, tài liệu, kiểm thử | Task |
|---|---|---|---|
| 1. Bảo vệ `main` | `harness/MAIN_PROTECTION.md`; luật 33 của LEAD; ba file định tuyến; `PREFLIGHT.md` dòng 16 | Code hook; code kiểm pre-flight; kiểm chỉ đọc cài đặt GitHub. Cấu hình phía GitHub và cài hook: OWNER làm | TK-0006, TK-0007, TK-0008, TK-0018, TK-0027 |
| 2. Chọn model | `harness/MODEL_POLICY.md` mục 2–6 (bản 1.0.2, DEC-0018); DEC-0017 | Code liệt kê model đủ điều kiện, so cùng model, kiểm REVIEWER; test dừng khi không có model; đối chiếu yêu cầu và thực tế trên bản ghi | TK-0009, TK-0010, TK-0019 |
| 3. Catalog model | `harness/MODEL_POLICY.md` mục 1; schema và mẫu; dòng kiểm tuyến trong catalog | Code kiểm schema, dòng kiểm tuyến, dòng phân công. Kiểm bằng phiên tác tử có công cụ và nguồn hạn mức: LEAD làm khi vận hành | TK-0009 |
| 4. Trace log | RFC-0001 `OPEN`; `LOG_GRAMMAR.md` không đổi | Test giữ nguyên ngữ pháp log. Chọn phương án: OWNER | TK-0020 |
| 5. Chat | `harness/CHAT_UX.md` mục 1–2; `BLOCKS.md` | Code kiểm thông điệp cuối | TK-0012 |
| 6. Storage | `harness/CHAT_UX.md` mục 3 | Test bất biến từng file của CYC-01, CYC-02 | TK-0020 |
| 7. Git và cleanup | `harness/GIT_CONVENTIONS.md` mục 7–10; `README.md#CLEAN_SPEC` | Code phân loại tên nhánh; `clean` chế độ liệt kê. Chế độ xóa: chưa làm. Tự xóa nhánh nguồn: OWNER quyết | TK-0011, TK-0021 |
| 8. Scanner | `harness/HARNESS.md` mục 10.2; `README.md#SCAN_SPEC` | Code `scan`, bộ luật, cách ly, thẻ bọc; bộ test ở `01_plan/SPEC_SCAN.md`; bộ test phản biện | TK-0013, TK-0014, TK-0022, TK-0023 |
| 9. Chia batch | `harness/HARNESS.md#BATCH_RULES`; luật 21, 26 của LEAD; mẫu plan | Code kiểm zero-overlap; kiểm thử worktree và nền tích hợp tạm. Cách Orca mở nhiều worktree: OWNER kiểm `PREFLIGHT.md` mục 3 | TK-0015, TK-0025 |
| 10. Mẫu `pytest.ini` | `harness/templates/pytest.ini`; `harness/HARNESS.md` mục 5.5 | Test thu thập; code kiểm tương thích, không ghi đè | TK-0016, TK-0024 |
| Tài liệu và hồi quy | `verify_default` | `tools/README.md`; chạy toàn bộ trên Windows; Linux do LEAD chạy khi review. CI cho `tools/tests` trong `.github/`: chưa làm, ngoài `product_paths` | TK-0026, TK-0017 |
<!-- END: CLASSIFICATION -->

<!-- ANCHOR: LAYERS -->
## 4. Bảo vệ `main`: ba lớp kiểm riêng
| Lớp | Kiểm bằng | Quyền cần | Giới hạn phải nêu trong bằng chứng |
|---|---|---|---|
| Hook cục bộ | TK-0006, TK-0018, repo tạm | Không cần quyền trên GitHub. OWNER cài một lần cho mỗi bản clone bằng `git config core.hooksPath tools/hooks` | Vượt được bằng `--no-verify`, bản clone chưa cài, đổi `core.hooksPath`; không chặn merge qua web, `gh` hay API |
| Pre-flight | TK-0007, TK-0018, repo tạm | Quyền đọc repo cục bộ | Chỉ có tác dụng khi tác tử gọi; không chặn lệnh chạy ngoài phiên |
| Phía GitHub | TK-0008, dữ liệu đọc bằng `gh api` kiểu `GET` | Quyền đọc repo; đọc chi tiết luật nhánh có thể cần quyền quản trị, thiếu thì dòng đó là `UNKNOWN`. Bật luật: quyền quản trị, chỉ OWNER | Chỉ đọc cấu hình, không chứng minh máy chủ từ chối một lượt đẩy thật. Tác tử không đẩy thử vào `main` hay thẻ. Dùng chung tài khoản với OWNER thì luật không phân biệt được hai bên |
<!-- END: LAYERS -->

<!-- ANCHOR: HANDOFF -->
## 5. Bàn giao TK-0032, TK-0034, TK-0035 và TK-0018 (DEC-0028, DEC-0029)
- Checklist là task và ACCEPTANCE#CYC_03 đã merge; thay checklist phải ghi quyết định. Hai vòng review là ngưỡng tái cấu trúc, không tự miễn lỗi đúng đắn.
- LEAD chịu bước từ draft PASS sang diff/commit message chờ duyệt; WORKER giao code/bằng chứng/patch; REVIEWER chỉ đọc. Chỉ OWNER merge; commit, push và mở PR cần quyền riêng theo task/nhánh/SHA. PR mở và checks đạt là hai trạng thái khác nhau; không có check phải ghi không có.
- Bundle ngoài repo theo task/rN, không ghi đè. MANIFEST sinh cuối: base SHA, file SHA256, Git blob OID/SHA256 và mode, attr/filter liên quan, Python/pytest, lệnh/cwd/env/exit/thời gian, log thô và kết quả từng ca. Hash cả SUMMARY; SUMMARY không chứa hash của nó hay manifest. Verdict ngoài bundle ghi hash MANIFEST làm bundle ID.
- CRLF fixture sinh bằng byte lúc chạy; assert CRLF trước khi kiểm. Không đổi attributes/config. Mutation chỉ trên bản sao, giữ blob trước/sau, patch, hash, kỳ vọng/thực tế và log; số 3 fail/39 pass chỉ thuộc đối chứng cách ly Git cũ, không cố định số ca sau đổi base.
- Trước publication so cây commit với allowlist, blob/hash/mode dự đoán theo EOL/filter được duyệt, base và bundle. Hash code giống không miễn kiểm khi base/phụ thuộc/môi trường thay đổi. Dùng script committer nếu worker thiếu Git; không tự cài hay mở quyền.
- Sau TK-0032, TK-0034, TK-0035 merge, xác nhận main SHA, cập nhật base TK-0018 và review delta; không rewrite lịch sử đã publish, force push hay reset loop. Chạy verify toàn tools/tests và baseline23; ghi L02/L03 trên R1, giữ L01. Mutation mới theo hành vi bị tác động, không ép tổng test cũ.
- BLOCKED ghi loại DECISION_OWNER/ACTION_LEAD/OUTPUT_WORKER/TOOLING/DEPENDENCY, chủ, điều kiện mở và thời điểm; tra quyết định cũ trước khi chờ OWNER. Event ngoài repo ghi từ/đến, task, chủ, thời điểm; đo PASS đến PR, review vòng, thời gian chờ và lỗi công cụ. SLA không tạo thêm quyền.
- Tài khoản GitHub chung chưa tách OWNER/tác tử bằng kỹ thuật (DEC-0019, RSK-0004); giữ verdict/phiên riêng. Ưu tiên đề xuất GitHub App/tài khoản riêng, chưa tự thay cấu hình. Không nhận hai approval cùng tài khoản là chứng minh hai chủ thể độc lập.
<!-- END: HANDOFF -->
