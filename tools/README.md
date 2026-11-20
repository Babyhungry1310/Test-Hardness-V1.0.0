# TOOLS — CÔNG CỤ VÀ HOOK KIỂM SOÁT
Tài liệu kỹ thuật cho các công cụ và hook trong thư mục 	ools/.

## Cài đặt hook
OWNER chạy một lần cho mỗi bản clone: git config core.hooksPath tools/hooks. Tác tử không tự chạy lệnh này.

## Giới hạn bảo vệ và quét
- **Hook cục bộ:** Ngăn commit/merge/push nhầm vào main/thẻ. Vượt được bằng --no-verify, đổi core.hooksPath, hoặc clone chưa cài; không chặn merge web/API; không là bảo vệ tuyệt đối.
- **Pre-flight gate:** Kiểm tra trước phiên, commit, push. Chỉ có tác dụng khi tác tử gọi; không chặn lệnh ngoài phiên.
- **Phía GitHub:** Đọc cấu hình quy tắc; không chứng minh máy chủ từ chối lượt đẩy thật; dùng chung tài khoản với OWNER thì không phân biệt được hai bên.
- **Scanner:** Phân loại đúng các ca kiểm thử theo bộ luật; vượt ngưỡng luôn là QUARANTINE. Không chặn được mọi prompt injection; ALLOW không đồng nghĩa tuyệt đối an toàn.

## Đối chiếu nhóm chức năng (SPEC_TOOLS.md#CLASSIFICATION)
| Nhóm | Đường dẫn trong repo | Trạng thái / Phần chưa làm |
|---|---|---|
| 1. Bảo vệ main | 	ools/hooks/*, 	ools/preflight_main.py, 	ools/github_audit.py | Lớp phía GitHub: chưa thử nghiệm đẩy thật, cấu hình do OWNER làm |
| 2. Chọn model | 	ools/model_select.py, 	ools/assign_audit.py | Hoàn thành |
| 3. Catalog model | 	ools/model_check.py | Hoàn thành |
| 4. Trace log | 	ools/tests/test_trace_open.py | Chưa làm: chọn phương án trace A/B/C (RFC-0001 OPEN) |
| 5. Chat | 	ools/chat_blocks.py | Hoàn thành |
| 6. Storage | 	ools/tests/test_storage_freeze.py | Hoàn thành |
| 7. Git và cleanup | 	ools/branch_names.py, 	ools/clean_list.py | Chế độ xóa của clean: chưa làm (--delete bị chặn) |
| 8. Scanner | 	ools/scan.py, 	ools/scan_rules.json, 	ools/scan_wrap.py, 	ools/scan_quarantine.py | Dòng log SCAN_HIT: chưa làm |
| 9. Chia batch | 	ools/batch_check.py, 	ools/integrate_check.py | Hoàn thành |
| 10. Mẫu pytest.ini | 	ools/pytest_ini_check.py | Hoàn thành |

## Danh mục công cụ và hook
### 	ools/assign_audit.py
- Mục đích: Đối chiếu phân công model giữa MODEL_MATRIX.md, MODEL_CATALOG.md, run và RVW; kiểm tra tính độc lập REVIEWER.
- Lệnh mẫu: python tools/assign_audit.py --root . --cycle CYC-01 (mã thoát: 0). Mã thoát: 0 đạt, 1 sai lệch, 2 lỗi đối số/file.
- Đầu vào / Đầu ra: Vào --root <dir>, --cycle <CYC-nn>, --json. Ra văn bản/JSON danh sách sai lệch và ghi chú.
- Không làm: Không chọn hay xếp hạng model thay LEAD, không sửa file bản ghi, không gọi mạng.
### 	ools/batch_check.py
- Mục đích: Kiểm tra batch song song trong PLAN.md và task: zero-overlap write_scope, không phụ thuộc nội batch, không trùng lock.
- Lệnh mẫu: python tools/batch_check.py --plan 01_plan/PLAN.md --tasks 02_work/tasks --cycle CYC-07 (mã thoát: 0). Mã thoát: 0 đạt, 1 vi phạm, 2 lỗi đối số/file.
- Đầu vào / Đầu ra: Vào --plan <file>, --tasks <dir>, --cycle <CYC>, --json. Ra vi phạm quy tắc hoặc JSON.
- Không làm: Không tự sửa PLAN/task, không chia lại batch, không khởi chạy task.
### 	ools/branch_names.py
- Mục đích: Phân loại tên nhánh Git theo quy ước khung (main, 	ask, lead, 
eview, upgrade, legacy-review, unknown).
- Lệnh mẫu: python tools/branch_names.py main task/TK-0026-R1 (mã thoát: 0). Mã thoát: 0 hợp lệ, 1 có unknown, 2 thiếu đối số.
- Đầu vào / Đầu ra: Vào danh sách tên nhánh qua đối số vị trí, tùy chọn --json. Ra dòng <nhánh>: <loại> hoặc JSON.
- Không làm: Không kiểm tra nhánh tồn tại trong Git, không tạo hay đổi tên nhánh.
### 	ools/chat_blocks.py
- Mục đích: Kiểm tra định dạng thông điệp cuối phiên: khối kết thúc duy nhất, SUMMARY đầu tiên, thứ tự khóa, không có bảng markdown ngoài code block.
- Lệnh mẫu: python tools/chat_blocks.py --help (mã thoát: 2). Mã thoát: 0 hợp lệ, 1 sai định dạng thông điệp, 2 lỗi đọc file/đối số.
- Đầu vào / Đầu ra: Vào đường dẫn file văn bản, tùy chọn --json. Ra mã lỗi kèm PASS hoặc JSON (ok, issues).
- Không làm: Không sửa định dạng văn bản, không phân tích hội thoại nhiều lượt.
### 	ools/clean_list.py
- Mục đích: Liệt kê và phân loại nhánh Git thành SAFE, KEEP, ASK dựa trên PR, trạng thái merge vào main và độ sạch worktree.
- Lệnh mẫu: python tools/clean_list.py --help (mã thoát: 0). Mã thoát: 0 thành công, 2 lỗi đối số/repo hoặc yêu cầu --delete.
- Đầu vào / Đầu ra: Vào --repo <dir>, --prs <json>, --out <file> (ngoài repo), --json. Ra báo cáo phân loại kèm mã hash hoặc JSON.
- Không làm: Không xóa nhánh/worktree (chế độ xóa chưa làm / trả mã 2), không sửa ref Git.
### 	ools/github_audit.py
- Mục đích: Đối chiếu cấu hình bảo vệ nhánh/thẻ phía GitHub từ dữ liệu dump JSON với MAIN_PROTECTION.md#GITHUB_RULES.
- Lệnh mẫu: python tools/github_audit.py --help (mã thoát: 0). Mã thoát: 0 tất cả 9 quy tắc PASS, 1 có FAIL/UNKNOWN, 2 lỗi thư mục/dữ liệu.
- Đầu vào / Đầu ra: Vào thư mục chứa JSON từ GitHub API, --json, --report <file>. Ra dòng kết quả 1-9 hoặc JSON/file báo cáo.
- Không làm: Không gọi mạng tới GitHub API, không thay đổi thiết lập repo trên GitHub.
### 	ools/integrate_check.py
- Mục đích: Thử nghiệm merge nhiều nhánh trên worktree tạm detached; phát hiện xung đột và file ngoài phạm vi.
- Lệnh mẫu: python tools/integrate_check.py --help (mã thoát: 0). Mã thoát: 0 tích hợp sạch, 1 xung đột/out-of-scope, 2 lỗi đối số/repo.
- Đầu vào / Đầu ra: Vào --repo <dir>, --base <ref>, --heads <ref>..., --scopes <json>, --json. Ra kết quả tích hợp hoặc JSON.
- Không làm: Không commit/push vào main, không đổi trạng thái nhánh làm việc.
### 	ools/model_check.py
- Mục đích: Kiểm tra schema và quy tắc của MODEL_CATALOG.md (route checks, aliases) hoặc MODEL_MATRIX.md (assignments match).
- Lệnh mẫu: python tools/model_check.py catalog 04_control/MODEL_CATALOG.md (mã thoát: 0). Mã thoát: 0 đạt, 1 lỗi schema/quy tắc, 2 lỗi file/đối số.
- Đầu vào / Đầu ra: Vào loại file (catalog/matrix), đường dẫn file, --json. Ra danh sách lỗi kèm PASS/FAIL hoặc JSON.
- Không làm: Không sửa file catalog/matrix, không truy vấn mạng.
### 	ools/model_select.py
- Mục đích: Lọc model đủ điều kiện (eligible), so hai model (same), hoặc kiểm tra tính độc lập REVIEWER (
eviewer).
- Lệnh mẫu: python -m tools.model_select --catalog 04_control/MODEL_CATALOG.md eligible (mã thoát: 0). Mã thoát: 0 hợp lệ, 1 không đạt/UNKNOWN, 2 lỗi cú pháp.
- Đầu vào / Đầu ra: Vào --catalog <file>, lệnh con (eligible, same, 
eviewer), bằng chứng, --json. Ra mã model/kết quả hoặc JSON.
- Không làm: Không chọn model thay LEAD; không tự nạp repo root (cần gọi qua -m hoặc đặt PYTHONPATH).
### 	ools/preflight_main.py
- Mục đích: Kiểm tra điều kiện tiên quyết trước phiên, trước commit, trước push (ngăn thao tác trên main, kiểm tra hook, worktree).
- Lệnh mẫu: python tools/preflight_main.py --role worker --stage session (mã thoát: 0). Mã thoát: 0 đạt preflight, 1 không đạt, 2 lỗi ngoài git/đối số.
- Đầu vào / Đầu ra: Vào --role {worker,lead,reviewer}, --stage {session,commit,push}, --ref <ref>, --json. Ra chi tiết kiểm tra hoặc JSON.
- Không làm: Không tự cài hook, không sửa tên nhánh, không chặn lệnh Git ngoài phiên.
### 	ools/pytest_ini_check.py
- Mục đích: Đối chiếu cấu hình pytest của dự án với mẫu khung harness/templates/pytest.ini; phát hiện khác biệt hoặc bị che bóng.
- Lệnh mẫu: python tools/pytest_ini_check.py . --template harness/templates/pytest.ini (mã thoát: 0). Mã thoát: 0 bsent/same, 1 differs/shadowed, 2 lỗi đọc/cú pháp.
- Đầu vào / Đầu ra: Vào thư mục dự án, --template <path>, --json. Ra trạng thái (status), tùy chọn cấu hình, khác biệt hoặc JSON.
- Không làm: Không ghi đè hay sửa file cấu hình pytest của dự án.
### 	ools/scan.py
- Mục đích: Quét văn bản phát hiện dấu hiệu prompt injection, ký tự ẩn, đồng hình, che giấu HTML và base64 lồng nhau theo bộ luật.
- Lệnh mẫu: python tools/scan.py tools/scan_rules.json (mã thoát: 0). Mã thoát: 0 cho ALLOW/WARN, 1 cho QUARANTINE/BLOCK, 2 lỗi đối số/luật/file.
- Đầu vào / Đầu ra: Vào đường dẫn file cần quét, --rules <json>, --json. Ra một dòng JSON chứa level, 
uleset, sha256, 
easons, decoded_skipped.
- Không làm: Không sửa đổi hay chuyển file, không xuất nội dung độc hại ra log, không bảo đảm chặn 100% injection.
### 	ools/scan_quarantine.py
- Mục đích: Di chuyển file vào thư mục cách ly khi kết quả scan là QUARANTINE, đối chiếu SHA-256 trước và sau khi chuyển.
- Lệnh mẫu: python tools/scan_quarantine.py --help (mã thoát: 2). Mã thoát: 0 hoàn thành (cách ly hoặc bỏ qua), 2 lỗi file/hash/đích đến.
- Đầu vào / Đầu ra: Vào file gốc, file JSON scan, thư mục cách ly, --json. Ra dòng trạng thái hoặc JSON.
- Không làm: Không tự quét file, không xóa file gốc khi mức BLOCK/ALLOW, không sửa nội dung file.
### 	ools/scan_wrap.py
- Mục đích: Bọc dữ liệu ngoại vi vào thẻ <EXTERNAL_DATA> kèm thuộc tính nguồn, hash SHA-256, mức scan và số thẻ đóng xuất hiện.
- Lệnh mẫu: python tools/scan_wrap.py tools/scan_rules.json --scan ALLOW --json (mã thoát: 0). Mã thoát: 0 thành công, 2 lỗi đọc/ghi.
- Đầu vào / Đầu ra: Vào file hoặc stdin, --source, --scan, --ruleset, --scan-json, --out, --json. Ra dữ liệu đã bọc hoặc JSON.
- Không làm: Không thanh lọc payload độc hại; chỉ bao bọc dữ liệu và gắn metadata.
### 	ools/hooks/pre-commit
- Mục đích: Chặn thao tác commit trực tiếp khi nhánh hiện tại (HEAD) là main.
- Lệnh mẫu: sh tools/hooks/pre-commit (mã thoát: 0). Mã thoát: 0 cho phép commit (HEAD khác main), 1 từ chối commit trên main.
- Đầu vào / Đầu ra: Vào trạng thái nhánh HEAD từ Git. Ra thông báo từ chối commit nếu ở main.
- Không làm: Không kiểm tra nội dung staged file/commit message; vượt được bằng --no-verify.
### 	ools/hooks/pre-merge-commit
- Mục đích: Chặn thao tác merge commit (git merge --no-ff) trực tiếp trên nhánh main.
- Lệnh mẫu: sh tools/hooks/pre-merge-commit (mã thoát: 0). Mã thoát: 0 cho phép merge (HEAD khác main), 1 từ chối merge trên main.
- Đầu vào / Đầu ra: Vào trạng thái nhánh HEAD từ Git. Ra thông báo từ chối merge commit nếu ở main.
- Không làm: Không chặn fast-forward merge không tạo commit; vượt được bằng --no-verify.
### 	ools/hooks/pre-push
- Mục đích: Chặn thao tác push ref đích vào 
efs/heads/main hoặc 
efs/tags/*.
- Lệnh mẫu: sh tools/hooks/pre-push (mã thoát: 0 khi không có dòng ref từ chối). Mã thoát: 0 cho phép push ref hợp lệ, 1 từ chối khi đích là main/thẻ.
- Đầu vào / Đầu ra: Vào các dòng ref từ stdin của git push. Ra thông báo từ chối nếu ref đích bị cấm.
- Không làm: Không xác thực quyền hạn trên máy chủ GitHub; vượt được bằng --no-verify.
