# PREFLIGHT — DANH SÁCH KIỂM TRA ĐẦU PHIÊN

Danh sách này là phần làm tay của script `doctor` (`harness/tools/README.md#DOCTOR`) và các điều kiện của luồng phiên ở `harness/tools/INTEGRATION.md` mục 4. Khi `doctor` đã có, script làm các dòng có ghi "`doctor`" ở cột cuối; các dòng còn lại vẫn kiểm tay.

Lệnh viết cho PowerShell trên Windows, chạy ở gốc worktree của phiên. `TK-0007`, `CYC-02` là ví dụ; thay bằng mã thật. Một dòng không đạt thì làm đúng cột "Khi không đạt" và không bắt đầu việc chính của phiên.

## 1. Ai kiểm gì

| Phiên | Ai kiểm | Các dòng ở mục 2 |
|---|---|---|
| `RUN` | WORKER | 1–10, 12, 14, 16 |
| `CHANGE`, `DISCUSS` | LEAD | 1–11, 14, 15, 16; `DISCUSS` thêm 17 |
| `ASK` | Không nhận vai | 1, 6, 9 |
| Kiểm định chu kỳ | REVIEWER | 1–10, 13, 14, 16 |
| Lần đầu dùng một bản cài Orca hoặc 9Router | OWNER | Mục 3 |
| Lần đầu dựng repo trên máy | OWNER | Mục 4 |

## 2. Kiểm đầu phiên

<!-- ANCHOR: SESSION_CHECKS -->
| # | Kiểm gì | Cách kiểm bằng tay | Đạt khi | Khi không đạt |
|:---:|---|---|---|---|
| 1 | Đang ở đúng worktree của phiên, không ở bản checkout chính | `git rev-parse --show-toplevel` | Đường dẫn là thư mục worktree đã tạo cho phiên này | Dừng; không tạo hay sửa file; báo OWNER đường dẫn đang đứng |
| 2 | Đúng nhánh theo loại phiên, không phải `main` | `git branch --show-current` | `task/TK-nnnn-Rn` (`RUN`), `lead/<slug>` (LEAD), `review/CYC-nn-Rk-xxxx` (REVIEWER); `ASK` thì bất kỳ | Nhánh chưa đẩy và chỉ lệch tiền tố hay hậu tố do công cụ thêm: `git branch -m <tên đúng>`. Mọi trường hợp khác: dừng, báo OWNER tạo lại worktree |
| 3 | Nhánh dựng từ `origin/main` mới nhất | `git fetch origin` rồi `git rev-list --count HEAD..origin/main` | Kết quả `0` | Nhánh chưa có commit riêng: `git merge --ff-only origin/main`. Đã có commit riêng: dừng, báo OWNER; không rebase, không ép đẩy |
| 4 | Worktree sạch | `git status --porcelain` | Không in gì | Không xóa, không hoàn tác; báo OWNER danh sách file (có thể là việc dở của phiên trước) |
| 5 | `<project>.local` có đủ 5 thư mục, nằm ngoài worktree | `$c = Split-Path (git rev-parse --path-format=absolute --git-common-dir)`, `$l = Join-Path (Split-Path $c) ((Split-Path $c -Leaf) + '.local')` rồi `'scratch','logs','quarantine','transcripts','cache' \| ForEach-Object { Test-Path (Join-Path $l $_) }` | Năm dòng `True` | Không tạo trong worktree. OWNER tạo theo `README.md` bước 1 rồi mở lại phiên. `doctor` |
| 6 | Phiên bản khung khớp (C12) | `Get-Content harness\VERSION` và `Select-String -Path harness\HARNESS.md -Pattern 'Phiên bản' -SimpleMatch \| Select-Object -First 1` | Số ở dòng `VERSION` giống số trong dòng "Phiên bản" của bảng đầu `HARNESS.md` | Dừng; không sửa `harness/` (🔒); báo OWNER. `doctor` |
| 7 | Không có bí mật trong file theo dõi (C8) | `git grep -n -I -E "BEGIN [A-Z ]*PRIVATE KEY\|AKIA[0-9A-Z]{16}\|ghp_[A-Za-z0-9]{36}\|github_pat_[A-Za-z0-9_]{20,}\|sk-[A-Za-z0-9_-]{20,}"` và `git ls-files "*.env" "*.pem" "*.key" "*.pfx" "*.p12"` | Cả hai không in gì | Dừng mọi việc; không commit, không đẩy; không chép chuỗi nghi vấn vào chat, log hay bản ghi; báo OWNER đường dẫn file. Xóa khỏi lịch sử chỉ OWNER quyết. `doctor` |
| 8 | Không có file dữ liệu thật trong file theo dõi (C8) | `git ls-files "*.csv" "*.tsv" "*.xls" "*.xlsx" "*.xlsm" "*.parquet" "*.sqlite" "*.sqlite3" "*.db"` | Không in gì | Coi là Zone 2: không đọc nội dung, không đưa vào prompt; báo OWNER. `doctor` |
| 9 | Chỉ đọc đúng file của vai | Đối chiếu file đã đọc với `AGENTS.md` và cột "Được đọc" ở `harness/HARNESS.md` mục 6.1 | Không có file ngoài danh sách | Bỏ phần đã đọc ngoài phạm vi khỏi căn cứ làm việc; nếu đã dựa vào nó thì dừng, báo OWNER mở phiên mới |
| 10 | Đẩy bằng tài khoản GitHub riêng của model | `gh auth status` | Tài khoản đang dùng khác tài khoản OWNER ghi trong `.github/CODEOWNERS` | Không đẩy, không mở PR; báo OWNER cấp tài khoản riêng cho model |
| 11 | `STATE.md` khớp dấu hiệu file (C6) | `Get-Content 04_control\STATE.md -TotalCount 2` và `Test-Path 00_brief\BRIEF.md, 01_plan\PLAN.md, 04_control\gates\PLAN_GO.md` | Không có `BRIEF.md` → `BRAINSTORM`; có `BRIEF.md`, chưa có `PLAN_GO.md` → `PLAN`; có `PLAN_GO.md` → `EXECUTE`, `VERIFY`, `CLOSE` hoặc `CLOSED` theo file cổng chu kỳ | Bản gốc thắng: LEAD sửa `STATE.md` trong PR của phiên này và nêu trong mô tả PR. `doctor` |
| 12 | Task sẵn sàng giao và số run đúng | `git ls-tree -r --name-only origin/main 02_work/tasks \| Select-String 'TK-0007'` và `git ls-tree --name-only origin/main 02_work/runs/ \| Select-String 'TK-0007_R'`; với mỗi mã trong `depends_on`, lệnh thứ hai cho mã đó | Task có trên `main`; chưa có run `DONE` hay `CANCELLED` của task; mỗi task trong `depends_on` có run `DONE`; `n` của nhánh = 1 + số run lớn nhất (không có run thì `n` = 1) | Không xuất `CONFIRM`, không sửa file; báo OWNER điều kiện nào thiếu |
| 13 | REVIEWER khác model thực tế với các WORKER của phần được kiểm | Lấy mã task: `git ls-tree --name-only origin/main 02_work/tasks/CYC-02/`; lấy model: `git grep -h "^model:" origin/main -- "02_work/runs/TK-0007_*"` cho từng task; so với model thực tế của phiên (`INTEGRATION.md#SESSION_MODEL`, cách A) theo `harness/MODEL_POLICY.md#SAME_MODEL` | Model thực tế của phiên khác mã gốc với model của mọi run đó, không nằm trong `aliases` của chúng, và đáp ứng `DEC` phân công đang `ACTIVE` (`harness/MODEL_POLICY.md#REVIEWER_INDEPENDENCE`) | Dừng; xuất khối `QUESTION` cho OWNER (`harness/rules/REVIEWER.md` luật 2) |
| 14 | Biết model thực tế của phiên | Xem tên model công cụ tác tử hiển thị (`INTEGRATION.md#SESSION_MODEL`, cách A) | Có tên model cụ thể | Hỏi OWNER trước khi bắt đầu; không đoán, không để trống trường `model` |
| 15 | Không có phiên LEAD khác đang ghi repo | `gh pr list --state open --search "head:lead/"`; `gh pr list --state open --search "head:upgrade/"` | Không có PR mở nào từ nhánh `lead/` khác nhánh của phiên này. Một PR `upgrade/` được mở cùng lúc với một PR `lead/` khi đủ cả bốn: cùng một phiên LEAD soạn; hai PR không chạm chung file nào; mã bản ghi cấp ở PR mở sau lớn hơn mọi mã của PR mở trước; mô tả của cả hai PR ghi thứ tự merge và việc phải làm sau lượt merge đầu | Không ghi sổ, không cấp mã; báo OWNER chờ PR kia được merge hoặc đóng [THY-19] |
| 16 | Pre-flight gate cho `main`: hook cục bộ đã cài; biết quy tắc kiểm trước commit và push | `git config --get core.hooksPath` | In `harness/tools/hooks` (khi hook đã có trong khung). Hook chưa có hoặc chưa cài: vẫn làm được, nhưng trước mỗi `git commit` chạy `git branch --show-current` và trước mỗi `git push` kiểm ref đích khác `main` và không phải thẻ (`harness/MAIN_PROTECTION.md#PREFLIGHT_GATE`) | Không tự đổi cấu hình Git; báo OWNER hook chưa cài. Đang đứng ở `main`: không commit, làm theo `harness/MAIN_PROTECTION.md` mục 3 |
| 17 | Model của phiên đủ điều kiện | Đối chiếu model thực tế của phiên (dòng 14) với neo `ROUTE_CHECKS` và khóa `availability` trong `04_control/MODEL_CATALOG.md` | Thỏa `harness/MODEL_POLICY.md#ELIGIBILITY` | Dừng; xuất khối `QUESTION` cho OWNER (`harness/MODEL_POLICY.md#NO_MODEL`) |
<!-- END: SESSION_CHECKS -->

Dòng 5 dùng `--path-format=absolute`, có từ Git 2.31. Bản Git cũ hơn: chạy `git rev-parse --git-common-dir`, tự nối thành đường dẫn đầy đủ rồi dùng `Test-Path`.

## 3. Kiểm tính năng Orca và 9Router trên bản đang cài

<!-- ANCHOR: TOOL_CHECKS -->
**Nhận diện đúng phần mềm (làm trước mọi dòng dưới).** Tài liệu ở bảng 1 của `INTEGRATION.md` là của Orca do Stably AI phát hành và của 9Router do decolua phát hành. Nếu một dòng dưới đây không đạt, mọi dòng của phần mềm đó giữ "chưa" và LEAD tra lại tài liệu của đúng phần mềm OWNER dùng.

| Phần mềm | Cách kiểm bằng tay | Đạt khi |
|---|---|---|
| Orca | Mở mục giới thiệu (About) hoặc trang tải về đã dùng để cài; ghi số phiên bản | Nhà phát hành là Stably AI, trang chủ `onorca.dev`, mã nguồn `github.com/stablyai/orca` |
| 9Router | `npm ls -g 9router` (nếu cài bằng npm); mở `http://localhost:20128/dashboard`; ghi số phiên bản | Gói `9router` từ `github.com/decolua/9router`, không phải bản fork khác tên; Dashboard có các trang Providers, Combos, Usage |

OWNER làm trên một repo thử (ví dụ repo chạy thử của `harness/templates/examples/DRY_RUN.md`), không làm trên repo dự án thật. Mỗi dòng ứng với cùng số dòng ở bảng 1 của `harness/tools/INTEGRATION.md`. Đạt thì báo LEAD đổi dòng đó sang "đã xác nhận", kèm số phiên bản Orca hoặc 9Router.

| # | Tính năng | Cách kiểm bằng tay | Đạt khi | Khi không đạt |
|:---:|---|---|---|---|
| 1 | Orca: mỗi task một worktree | Tạo một workspace mới trên Orca cho repo thử, rồi chạy `git worktree list` ở bản checkout chính | Có thêm một dòng worktree với thư mục riêng | Giữ "chưa"; tạo worktree bằng `git worktree add` |
| 2 | Orca: lệnh thiết lập | Đặt lệnh `git status --short --branch` vào "Auto-run commands on worktree create" của repo thử; tạo một workspace | Terminal thiết lập in đúng tên nhánh mới, không báo lỗi | Giữ "chưa"; chạy tay lệnh ở `INTEGRATION.md#ORCA_SETUP` |
| 3 | Orca: nơi đặt worktree | Xem cột đường dẫn của `git worktree list` sau dòng 1; tìm cài đặt thư mục workspace trong Settings | Thư mục nằm ngoài bản checkout chính và ngoài `<project>.local\`; ghi lại đường dẫn và tên cài đặt | Đổi cài đặt nếu có; không có thì giữ "chưa" và tạo worktree bằng Git |
| 4 | Orca: đúng tên nhánh | Tạo workspace với Branch name `task/TK-9999-R1`, rồi `git -C <worktree> branch --show-current` | In đúng `task/TK-9999-R1`, không tiền tố, không hậu tố | Xóa tiền tố mặc định trong Settings nếu có rồi thử lại; vẫn sai thì giữ "chưa" |
| 5 | Orca: giao task bằng một lệnh | `orca status --json`; rồi `orca worktree create --name TK-9999-R2 --branch task/TK-9999-R2 --agent <agent-id> --prompt "Ask: PHASE hiện tại là gì?" --setup run --json`; rồi `git -C <worktree> rev-list --count HEAD..origin/main` | Tác tử mở trong worktree mới và nhận đúng prompt; tên nhánh đúng; lệnh cuối in `0` | Giữ "chưa"; giao task bằng cách gõ `Run TK-nnnn` |
| 6 | Orca: biết tác tử đã xong | Trong phiên của dòng 5: `orca terminal wait --terminal <handle> --for tui-idle --timeout-ms 600000 --json` | Lệnh trả về đúng lúc tác tử in xong câu trả lời | Giữ "chưa"; OWNER đọc khối cuối của phiên |
| 7 | 9Router: nhóm model | Dashboard → Combos: tạo ba combo theo `INTEGRATION.md#MODEL_GROUPS`, đặt tên OWNER đã duyệt; gọi thử một phiên `ASK` với từng combo | Mỗi combo trả lời được; danh sách model của combo WORKER và combo REVIEWER không có model chung | Giữ "chưa"; chọn model cố định cho từng phiên theo bảng tay |
| 8 | 9Router: chuyển model dự phòng | Tạo combo thử gồm hai model; tạm tắt kết nối của model đầu; gửi một câu hỏi qua combo đó | Câu trả lời vẫn về, Usage Analytics ghi model thứ hai | Giữ "chưa"; không dùng combo nhiều model |
| 9 | 9Router: ghi model thực tế | Sau phiên của dòng 8, mở Usage Analytics, lọc theo thời gian phiên | Thấy được model đã phục vụ từng request trong phiên | Giữ "chưa"; chỉ dùng cách A ở `INTEGRATION.md#SESSION_MODEL` |
| 10 | 9Router: liệt kê model và combo | `Invoke-RestMethod http://localhost:20128/v1/models -Headers @{ Authorization = "Bearer <khóa API>" }` với khóa lấy từ trình quản lý bí mật | Danh sách có đủ ba combo của mục 7 | Giữ "chưa"; xem trang Combos trên Dashboard |
<!-- END: TOOL_CHECKS -->

## 4. Thiết lập một lần

| # | Việc | Ai | Cách kiểm | Khi không đạt |
|:---:|---|---|---|---|
| 1 | Bảo vệ `main` và thẻ `cycle/*` theo `harness/MAIN_PROTECTION.md#GITHUB_RULES`; đây là lớp kiểm soát chính | OWNER | GitHub → Settings → Rules hoặc Branches (`.github/README.md`) | Chưa có thì hook và luật chỉ chống nhầm; câu 7 cổng PASS trả `CONDITIONAL` kèm một `RSK` |
| 2 | Chỉ squash merge; tắt auto-merge | OWNER | GitHub → Settings → General → Pull Requests | Bật lại đúng cài đặt trước phiên đầu tiên |
| 3 | `<project>.local` cạnh bản checkout chính | OWNER | Mục 2, dòng 5 | Tạo theo `README.md` bước 1 |
| 4 | Bộ nhớ đệm gói dùng chung | OWNER | `echo $env:PIP_CACHE_DIR` (dự án Python) trỏ vào `<project>.local\cache\` | Đặt theo `INTEGRATION.md#ORCA_SETUP` |
| 5 | Tài khoản GitHub riêng cho model | OWNER | Mục 2, dòng 10 | Không giao phiên có đẩy nhánh cho model tới khi có tài khoản riêng |
| 6 | Cài hook cục bộ cho bản clone (khi hook đã có trong khung) | OWNER | `git config --get core.hooksPath` in `harness/tools/hooks` | Chạy `git config core.hooksPath harness/tools/hooks` ở bản checkout chính |
| 7 | Quyết định tự xóa nhánh nguồn sau merge | OWNER | GitHub → Settings → General → Pull Requests | Đọc `harness/GIT_CONVENTIONS.md#AUTO_DELETE` rồi chọn |
| 8 | Catalog model và sổ phân công | LEAD kiểm tuyến và ghi; OWNER merge | `04_control/MODEL_CATALOG.md` có ít nhất một model thỏa `harness/MODEL_POLICY.md#ELIGIBILITY` | Chưa có thì chưa giao được phiên nào cho model |
