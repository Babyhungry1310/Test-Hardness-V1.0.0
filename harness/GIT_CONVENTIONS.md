# GIT CONVENTIONS

Chắt từ `harness/HARNESS.md` mục 5.4 và 5.5. Lệnh chạy được trên Windows (PowerShell hoặc cmd) với Git và GitHub CLI.

## 1. Nhánh

| Nhánh | Ai dùng | Quy ước |
|---|---|---|
| `main` | — | Nhánh chính, luôn đạt kiểm tra; không ai đẩy thẳng |
| `task/TK-nnnn-Rn` | WORKER | Một nhánh cho một run; `n` = 1 + số run lớn nhất trên `main` |
| `lead/<slug>` | LEAD | Một nhánh cho một phiên điều phối |
| `review/CYC-nn` | REVIEWER | Một nhánh cho một lượt kiểm định chu kỳ |
| `upgrade/<version>` | LEAD | Nâng cấp khung, kèm một `DEC` |

Nhánh sống ngắn. Tên nhánh chỉ là quy ước; kiểm tra dựa vào nội dung PR.

## 2. Merge và commit

- Chỉ OWNER bấm merge. Model không merge, không đẩy thẳng vào `main`, không bật auto-merge.
- Cách merge: **squash** — mỗi PR thành đúng một commit trên `main`.
- Tiêu đề commit trên `main`: `TK-nnnn Rn: <goal>` cho PR nộp bài; `lead: <việc>` cho PR điều phối.
- Mỗi lần một PR, theo thứ tự ở dòng `order` của khối `MERGE`.

## 3. Thẻ chu kỳ

Thẻ `cycle/CYC-nn` đặt lên commit của `main` sau khi OWNER merge file cổng `CYC-nn_PASS.md`; đây là mốc quay lui.

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
