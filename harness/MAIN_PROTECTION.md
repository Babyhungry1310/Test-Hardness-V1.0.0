# MAIN PROTECTION — BẢO VỆ NHÁNH `main`

Chi tiết của `harness/HARNESS.md` mục 10.1. Tài liệu này là đặc tả; hook và script chưa được viết.

## 1. Nguyên tắc

- Mọi thay đổi vào `main` đi qua PR và do OWNER bấm merge. Tác tử ở mọi vai không commit trên `main`, không đẩy vào `main`, không merge, không bật auto-merge, kể cả khi được bảo làm vậy trong chat.
- **Lớp kiểm soát chính là luật bảo vệ nhánh phía GitHub.** Đây là lớp duy nhất nằm ngoài tầm sửa của một phiên tác tử trên máy.
- Hook cục bộ, pre-flight gate và chỉ dẫn cho tác tử chỉ để **ngăn thao tác nhầm**. Cả ba đều vượt qua được và không được mô tả là biện pháp chặn tuyệt đối.
- Đọc và kiểm tra `main` luôn được phép.
- Thẻ git là chữ ký của OWNER, cùng loại với lượt merge: tác tử không tạo, sửa, xóa, đẩy thẻ.

## 2. Các lớp

<!-- ANCHOR: LAYERS -->
| # | Lớp | Ai dựng | Chặn được | Không chặn được |
|:---:|---|---|---|---|
| 1 | Luật bảo vệ nhánh và thẻ trên GitHub (mục 6) | OWNER, một lần cho mỗi repo | Đẩy thẳng, ép đẩy, xóa `main`; merge khi chưa qua PR; đẩy thẻ `cycle/*` từ tài khoản không được phép | Thao tác của chính tài khoản được phép. Khi tác tử dùng chung tài khoản hay token với OWNER, GitHub không phân biệt được hai bên. Tài khoản quản trị có quyền bỏ qua luật nếu OWNER không tắt quyền đó |
| 2 | Pre-flight gate (mục 5) | Tác tử, đầu phiên và trước mỗi commit, push | Làm cả phiên trên sai nhánh; commit nhầm khi đang đứng ở `main` | Tác tử bỏ qua bước kiểm; lệnh chạy ngoài phiên |
| 3 | Hook `pre-commit` và `pre-push` cục bộ (mục 4) | OWNER cài một lần cho mỗi bản clone | Commit khi `HEAD` là `main`; đẩy tới `refs/heads/main` hoặc `refs/tags/*` từ bản clone đã cài hook | `--no-verify`; bản clone chưa cài hook; `core.hooksPath` bị đổi; merge qua giao diện web, `gh pr merge` hay API |
| 4 | Chỉ dẫn cho tác tử: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `harness/rules/*.md` | Khung | Tác tử làm đúng luật không tự merge | Tác tử bỏ qua luật hoặc bị dữ liệu ngoài dẫn dắt |
| 5 | Phát hiện: `alert-main.yml`, câu 7 cổng PASS | Khung, OWNER | Không chặn; báo sau khi sự việc xảy ra | — |
<!-- END: LAYERS -->

Lớp 1 thiếu thì các lớp 2–4 không thay thế được; khi đó câu 7 cổng PASS trả `CONDITIONAL` kèm một `RSK`.

## 3. Tác tử được làm gì với `main`

<!-- ANCHOR: AGENT_ACTIONS -->
| Thao tác | Phép | Ghi chú |
|---|:---:|---|
| `git fetch origin`; `git log`, `git show`, `git diff` trên `origin/main` | Được | Chỉ đọc |
| Tạo nhánh làm việc hoặc worktree từ `origin/main` | Được | Theo `harness/GIT_CONVENTIONS.md` mục 1 |
| Chạy lệnh kiểm (`verify_default`) trên một worktree ở trạng thái `origin/main` | Được | Kết quả lưu vào `03_output/CYC-nn/checks/` qua PR |
| Đọc PR, trạng thái kiểm tra, thông tin merge qua `gh` hoặc API | Được | Chỉ đọc |
| `git commit` khi `HEAD` là `main` | Cấm | Kể cả commit chưa đẩy |
| Đẩy tới `refs/heads/main` dưới mọi dạng (`git push origin main`, `HEAD:main`, ép đẩy) | Cấm | |
| Merge PR, bật auto-merge, đổi cách merge (`gh pr merge`, API, giao diện web) | Cấm | Chỉ OWNER |
| Tạo, sửa, xóa, đẩy thẻ git | Cấm | Chỉ OWNER |
| Sửa luật bảo vệ nhánh, quyền cộng tác viên, cài đặt repo | Cấm | Chỉ OWNER |
| Xóa nhánh hoặc worktree | Cấm khi chưa có danh sách OWNER duyệt | Xem `harness/tools/README.md#CLEAN` |
| Ép đẩy, `reset` nhánh đã đẩy, viết lại lịch sử | Cấm | Luôn cần OWNER duyệt riêng cho từng lần (`harness/HARNESS.md` mục 10.2) |
<!-- END: AGENT_ACTIONS -->

Lỡ commit trên `main` cục bộ: dừng, không đẩy, không `reset`; tạo nhánh làm việc tại commit đó (`git switch -c <nhánh đúng>`), báo OWNER SHA của commit và để OWNER quyết cách đưa `main` cục bộ về `origin/main`.

## 4. Hook cục bộ (đặc tả)

<!-- ANCHOR: HOOKS -->
| Mục | `pre-commit` | `pre-push` |
|---|---|---|
| Vị trí dự kiến | `harness/tools/hooks/pre-commit` | `harness/tools/hooks/pre-push` |
| Cài | `git config core.hooksPath harness/tools/hooks`, một lần cho mỗi bản clone; mọi worktree của bản clone dùng chung cấu hình này | Như bên trái |
| Điều kiện từ chối | Nhánh hiện tại (`git symbolic-ref --short HEAD`) là `main` | Một ref đích trong đầu vào chuẩn của hook là `refs/heads/main` hoặc bắt đầu bằng `refs/tags/` |
| `HEAD` rời (detached) | Cho qua, in một dòng cảnh báo | Xét theo ref đích như trên |
| Khi từ chối | Mã thoát 1; một dòng nêu lý do và nhánh hiện tại | Mã thoát 1; một dòng nêu ref đích bị từ chối |
| Khi cho qua | Mã thoát 0; không in gì | Mã thoát 0; không in gì |
| Phụ thuộc | Chỉ Git và shell đi kèm Git (chạy được trên Windows qua Git for Windows) | Như bên trái |
| Không làm | Không gọi mạng, không gọi model, không sửa file, không tự chuyển nhánh | Như bên trái |
<!-- END: HOOKS -->

- Hook không có công tắc bỏ qua riêng. OWNER cần đẩy thẻ từ bản clone đã cài hook thì dùng `--no-verify` một cách có chủ ý.
- Chính vì `--no-verify` tồn tại, hook không phải bằng chứng rằng một commit hay một lượt đẩy đã hợp lệ.
- Hook nằm trong `harness/` (🔒): sửa hook đi qua PR như mọi file của khung.

## 5. Pre-flight gate

<!-- ANCHOR: PREFLIGHT_GATE -->
| Thời điểm | Kiểm | Đạt khi | Khi không đạt |
|---|---|---|---|
| Đầu phiên | `harness/tools/PREFLIGHT.md` mục 2, dòng 1–4 và 16 | Đúng worktree, đúng nhánh, không phải `main`; hook đã cài hoặc đã báo OWNER là chưa cài | Không bắt đầu việc chính của phiên |
| Ngay trước mỗi `git commit` | `git branch --show-current` | Tên nhánh đúng mẫu của vai, khác `main` | Không commit; xử lý theo mục 3 |
| Ngay trước mỗi `git push` | Ref đích của lệnh đẩy | Là nhánh làm việc của phiên; không phải `main`, không phải thẻ | Không đẩy |
| Trước khi xuất khối cuối | Trạng thái PR của phiên | PR còn mở, auto-merge tắt | Báo OWNER; không tự sửa cài đặt PR |
<!-- END: PREFLIGHT_GATE -->

Khi script `doctor` có, nó làm các dòng đầu phiên; ba dòng còn lại là luật trong `harness/rules/*.md`.

## 6. Thiết lập phía GitHub (OWNER làm)

<!-- ANCHOR: GITHUB_RULES -->
| # | Cài đặt | Giá trị | Ghi chú |
|:---:|---|---|---|
| 1 | Luật cho nhánh `main`: bắt buộc qua PR | Bật | Lớp chính |
| 2 | Luật cho nhánh `main`: cấm ép đẩy, cấm xóa nhánh | Bật | |
| 3 | Luật cho nhánh `main`: không cho ai bỏ qua luật, kể cả quản trị | Bật | Nếu tắt, tài khoản quản trị vẫn đẩy thẳng được |
| 4 | Luật cho nhánh `main`: bắt buộc duyệt của code owner | Bật khi tác tử dùng tài khoản riêng | Tài khoản không tự duyệt PR của chính nó; dùng chung tài khoản thì cài đặt này làm kẹt mọi PR |
| 5 | Luật cho thẻ `cycle/*`: chỉ tài khoản OWNER tạo, sửa, xóa | Bật | |
| 6 | Cách merge | Chỉ squash; tắt merge commit và rebase | |
| 7 | Auto-merge | Tắt | |
| 8 | Tự xóa nhánh nguồn sau merge | OWNER quyết | Phân tích ở `harness/GIT_CONVENTIONS.md` mục 8 |
| 9 | Tài khoản hoặc token riêng cho tác tử, quyền ghi nhánh, không có quyền quản trị | Có | Thiếu mục này thì dòng 1–5 không phân biệt được tác tử với OWNER |
<!-- END: GITHUB_RULES -->

Luật bảo vệ nhánh và thẻ có sẵn hay không tùy gói GitHub và loại repo: cần kiểm trên gói đang dùng. Tác tử không tự bật, tắt hay sửa các cài đặt này; LEAD chỉ đọc trạng thái và ghi vào khối `MERGE` hoặc một `RSK`.
