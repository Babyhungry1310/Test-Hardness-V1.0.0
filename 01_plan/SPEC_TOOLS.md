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
- Phân công theo chỗ, theo task, dự phòng và điều kiện dừng: `01_plan/SPEC_MODELS.md`. Quyền dùng một mã do `04_control/MODEL_CATALOG.md` và `04_control/MODEL_MATRIX.md` trên `origin/main` quy định.
- Ba chỗ: W1 logic, thuật toán, công cụ, unit test; W2 triển khai, tích hợp, tài liệu; W3 ca biên, stress, bảo mật, phản biện.
- Model thực tế ghi vào `model` của run và `reviewer_model` của `RVW`; LEAD ghi dòng `ASSIGNMENTS` khi giao việc và khi review PR. Không xác nhận được model thực tế: `BLOCKED`.
- REVIEWER khác mã và khác nhóm với model thực tế của mọi WORKER trong chu kỳ. Tên agent khác nhau không chứng minh model khác nhau.
- Không có model hợp lệ: dừng phần đó, trạng thái `BLOCKED`, xuất `QUESTION`. Không tự hạ tier, không dùng model `group: unverified`, không tự thêm model vào catalog hay ma trận.
<!-- END: MODELS -->

<!-- ANCHOR: CLASSIFICATION -->
## 3. Đã là quy tắc, còn cần làm
| Nhóm | Đã là quy tắc trong khung | Còn cần code, cấu hình, tài liệu, kiểm thử | Task |
|---|---|---|---|
| 1. Bảo vệ `main` | `harness/MAIN_PROTECTION.md`; luật 33 của LEAD; ba file định tuyến; `PREFLIGHT.md` dòng 16 | Code hook; code kiểm pre-flight; kiểm chỉ đọc cài đặt GitHub. Cấu hình phía GitHub và cài hook: OWNER làm | TK-0006, TK-0007, TK-0008, TK-0018 |
| 2. Ma trận model | `harness/MODEL_POLICY.md` mục 2–6; ma trận `APPROVED` theo DEC-0016 | Code chọn model, fallback, tính độc lập; test dừng khi hết model; đối chiếu yêu cầu và thực tế trên bản ghi | TK-0009, TK-0010, TK-0019 |
| 3. Catalog model | `harness/MODEL_POLICY.md` mục 1; schema và mẫu | Code kiểm schema và ràng buộc chéo. Nguồn `provider`, `capability_source`: OWNER bổ sung | TK-0009 |
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
