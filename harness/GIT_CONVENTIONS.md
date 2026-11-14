# GIT CONVENTIONS

Chắt từ `harness/HARNESS.md` mục 5.4 và 5.5. Lệnh chạy được trên Windows (PowerShell hoặc cmd) với Git và GitHub CLI.

## 1. Nhánh

| Nhánh | Ai dùng | Quy ước |
|---|---|---|
| `main` | — | Nhánh chính, luôn đạt kiểm tra; không ai đẩy thẳng; tác tử không commit trên `main` (`harness/MAIN_PROTECTION.md`) |
| `task/TK-nnnn-Rn` | WORKER | Một nhánh cho một run; `n` = 1 + số run lớn nhất trên `main` |
| `lead/<slug>` | LEAD | Một nhánh cho một phiên điều phối |
| `review/CYC-nn-Rk-xxxx` | REVIEWER | Một nhánh cho một phiên kiểm định; chi tiết ở mục 7 |
| `upgrade/<version>` | LEAD | Nâng cấp khung, kèm một `DEC` |

Nhánh sống ngắn. Tên nhánh chỉ là quy ước; kiểm tra dựa vào nội dung PR.

## 2. Merge và commit

- Chỉ OWNER bấm merge. Model không commit trên `main`, không merge, không đẩy thẳng vào `main`, không bật auto-merge. Đọc và kiểm tra `main` thì được.
- Cách merge: **squash** — mỗi PR thành đúng một commit trên `main`.
- Tiêu đề commit trên `main`: `TK-nnnn Rn: <goal>` cho PR nộp bài; `lead: <việc>` cho PR điều phối.
- Mỗi lần một PR, theo thứ tự ở dòng `order` của khối `MERGE`.

## 3. Thẻ chu kỳ

Thẻ `cycle/CYC-nn` đặt lên commit của `main` sau khi OWNER merge file cổng `CYC-nn_PASS.md`; đây là mốc quay lui. Chỉ OWNER tạo và đẩy thẻ; tác tử ở mọi vai không chạy các lệnh dưới đây và không tạo, sửa, xóa thẻ bằng bất kỳ công cụ nào.

```text
git fetch origin
git tag -a cycle/CYC-02 origin/main -m "CYC-02 PASS"
git push origin cycle/CYC-02
```

## 4. Hoàn tác một task và quay lui về một mốc

Cả hai đều đi qua PR; không dùng `git reset --hard` hay `git push --force` trên `main` (ghi đè lịch sử luôn cần OWNER duyệt).

| Việc | Lệnh |
|---|---|
| Hoàn tác một task (một commit squash) | `git switch -c lead/revert-TK-0007 origin/main` → `git revert <SHA>` → `git push -u origin lead/revert-TK-0007` → mở PR |
| Quay lui về mốc `cycle/CYC-02` | `git switch -c lead/rollback-CYC-02 origin/main` → `git revert --no-commit cycle/CYC-02..HEAD` → `git commit -m "lead: roll back to cycle/CYC-02"` → `git push -u origin lead/rollback-CYC-02` → mở PR |

Hoàn tác hoặc quay lui kèm một `DEC`. Lỗi lộ ra sau merge mà không cần hoàn tác: LEAD lập task mới có `fixes: TK-nnnn`.

## 5. Vòng đời một nhánh task

Cột Orca: thao tác cụ thể cần kiểm trên bản đang cài. `<worktree-dir>` là nơi đặt worktree, nằm ngoài bản checkout chính.

| Bước | Trên Orca | Lệnh git tương đương |
|---|---|---|
| Tạo | Tạo worktree mới cho task từ `main`; lệnh thiết lập cài phụ thuộc | `git fetch origin` → `git worktree add <worktree-dir>\TK-0007-R1 -b task/TK-0007-R1 origin/main` |
| Làm | Tác tử WORKER làm trong worktree, chỉ ghi trong `write_scope` | `git add <file trong write_scope>` → `git commit -m "TK-0007 R1: <goal>"` |
| Mở PR | Đẩy nhánh và mở PR về `main` | `git push -u origin task/TK-0007-R1` → `gh pr create --base main --title "TK-0007 R1: <goal>" --fill` |
| Dọn | Xóa worktree sau khi OWNER merge | `git worktree remove <worktree-dir>\TK-0007-R1` → `git branch -D task/TK-0007-R1` → `git fetch --prune` |

Dữ liệu tạm và log nằm ở `<project>.local\`, ngoài mọi worktree, nên dọn worktree không làm mất.

## 6. Dự án code

Áp dụng khi `harness.yaml` ghi `kind: code` hoặc `mixed`.

| Mục | Quy ước |
|---|---|
| Vị trí mã nguồn | Theo chuẩn của ngôn ngữ, ở gốc repo (ví dụ `src/`, `tests/`, file khai báo gói); liệt kê trong `product_paths`. Không lồng `00`–`06` hay `harness/` vào mã nguồn |
| Test | Nằm cạnh mã nguồn, thuộc `product_paths`; lệnh `verify` của task là lệnh chạy test. PR xóa test hoặc nới điều kiện test bị đánh dấu (C14) |
| Kích cỡ | Mỗi task ≤ khoảng 400 dòng thay đổi |
| Phụ thuộc | Lockfile được commit. Thêm hoặc nâng thư viện cần một `DEC`. File khai báo gói và lockfile thuộc vùng 🔒 |
| Thẻ phát hành | `v<MAJOR>.<MINOR>.<PATCH>` cho sản phẩm, độc lập với `harness/VERSION` |
| Nhánh release | `release/<x.y>`, chỉ tạo khi phải bảo trì một bản đã phát hành |
| Không commit | Sản phẩm build, thư mục gói tải về, file môi trường. Chỉ commit file mẫu môi trường không chứa giá trị thật |
| Ghi chú trong code | Cấm (`harness/HARNESS.md` mục 8.4) |

## 7. Nhánh kiểm định

<!-- ANCHOR: REVIEW_BRANCH -->
Mẫu: `review/CYC-nn-Rk-xxxx`.

| Phần | Nghĩa | Lấy từ đâu |
|---|---|---|
| `CYC-nn` | Chu kỳ được kiểm định | Câu giao việc |
| `Rk` | Vòng kiểm định đang làm, `k` = 1 + số vòng đã được tính của chu kỳ | LEAD ghi trong câu giao việc; một bản kiểm định bị loại bằng `DEC` không làm tăng `k` |
| `xxxx` | 4 ký tự đầu mã phiên, chữ thường và số | Công cụ tác tử; cùng quy ước với `DSC-YYYYMMDD-xxxx` |

- Tên nhánh là duy nhất cho mỗi phiên: hai phiên kiểm định cùng chu kỳ, cùng vòng (ví dụ một phiên bị loại và một phiên thay thế) vẫn có hai nhánh khác nhau.
- Model không nằm trong tên nhánh. Model yêu cầu ghi ở neo `ASSIGNMENTS` của `04_control/MODEL_MATRIX.md`; model thực tế ghi ở `reviewer_model` của `RVW`. Lý do: model có thể đổi giữa phiên, và hai phiên khác nhau có thể dùng cùng một model.
- Tên file bản ghi không đổi: `03_output/CYC-nn/checks/RVW-CYC-nn.md`.
- Nhánh đã có theo mẫu cũ (`review/CYC-nn`, `review/CYC-nn-Rk`) giữ nguyên tên; không đổi tên nhánh cũ.
<!-- END: REVIEW_BRANCH -->

## 8. Tự xóa nhánh nguồn sau merge

<!-- ANCHOR: AUTO_DELETE -->
Cài đặt "Automatically delete head branches" của GitHub xóa nhánh nguồn trên máy chủ ngay khi PR được merge. Bật hay không do OWNER quyết; tác tử không đổi cài đặt này.

| Khía cạnh | Khi bật |
|---|---|
| Nhánh trên máy chủ | Bị xóa ngay sau merge; khôi phục được từ trang PR chừng nào GitHub còn giữ |
| Commit gốc của nhánh | Không nằm trên `main` (merge kiểu squash); còn tra được qua trang PR |
| Nhánh cục bộ và worktree | Không bị đụng tới. Nhánh cục bộ mất nhánh theo dõi; `git pull` trong worktree báo lỗi; worktree vẫn phải dọn tay hoặc bằng `clean` |
| Sau `git fetch --prune` | Nhánh theo dõi từ xa biến mất; `git branch -d` từ chối vì commit squash không chứa commit gốc, nên bước dọn dùng `git branch -D` sau khi đã đối chiếu SHA với PR |
| PR khác dựng trên nhánh bị xóa | GitHub chuyển nhánh đích của PR đó; cần kiểm trên bản GitHub đang dùng |
| PR đóng mà không merge | Nhánh không bị xóa; vẫn phải qua `clean` |
| Orca | Cách Orca xử lý worktree có nhánh từ xa đã mất: cần kiểm trên bản đang cài |
| Trường `branch` của run | Vẫn là tên nhánh lúc nộp; là dữ liệu lịch sử, không cần nhánh còn tồn tại |

Đẩy thêm commit lên một nhánh đã merge sẽ tạo lại nhánh trên máy chủ; quy ước "một nhánh cho một phiên" tránh việc này. Bật cài đặt này không thay cho `clean`: nó không dọn nhánh cục bộ, worktree, và nhánh của PR đóng không merge.
<!-- END: AUTO_DELETE -->

## 9. Dọn nhánh và worktree

Đặc tả: `harness/tools/README.md#CLEAN`. Hai bước tách rời: liệt kê (chỉ đọc), rồi xóa đúng danh sách OWNER đã duyệt. Không bao giờ dọn `main`, thẻ, nhánh có PR đang mở, nhánh có commit chưa merge, worktree còn thay đổi chưa commit. Không `reset`, không ép đẩy, không sửa lịch sử.

## 10. Nội dung PR

- Mô tả PR chứa: tóm tắt nghiệm thu, danh sách file 🔒 và ✍ cần OWNER đọc kỹ, kết quả kiểm và test, điểm cần OWNER chốt.
- Không dán log thô, hội thoại thô hay đầu ra lệnh đầy đủ vào PR hay vào repo. Đầu ra kiểm đã cắt gọn nằm ở `03_output/CYC-nn/checks/`; log đầy đủ ở `<project>.local/logs/`.
