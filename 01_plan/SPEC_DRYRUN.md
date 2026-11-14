# SPEC_DRYRUN — ĐIỀU PHỐI THEO BATCH QUA ORCA

Nguồn: DEC-0016 (ngoại lệ E1, E2), DEC-0017, DEC-0018, RSK-0005, RSK-0006, `harness/HARNESS.md#BATCH_RULES`. Prompt bàn giao: `01_plan/SPEC_ORCA_PROMPT.md#PROMPT`.

<!-- ANCHOR: ORDER -->
## 1. Thứ tự, song song, phụ thuộc
- Thứ tự chu kỳ: CYC-03, CYC-04, CYC-05, CYC-06, CYC-07; trong chu kỳ theo neo `CYC_nn_BATCHES` của plan. Tổng cộng 22 task, 11 batch.
- Task độc lập, nhánh dựng từ `origin/main`, chạy song song trong batch: TK-0006, TK-0007, TK-0008 (CYC-03 B1); TK-0009 (CYC-04 B1); TK-0011, TK-0012, TK-0020, TK-0021 (CYC-05 B1); TK-0013 (CYC-06 B1); TK-0016, TK-0024, TK-0025 (CYC-07 B1).
- Task cần kết quả đã merge của batch trước: TK-0018 (TK-0006, TK-0007); TK-0027 (TK-0008); TK-0010, TK-0019 (TK-0009); TK-0014, TK-0022 (TK-0013); TK-0023 (TK-0014, TK-0022); TK-0015 (TK-0009, khác chu kỳ); TK-0026 (mọi task trước); TK-0017 (mọi task trước và TK-0026).
- Số task chạy cùng lúc không vượt ba chỗ, không vượt số model đủ điều kiện còn lại sau khi để dành cho REVIEWER, không vượt giới hạn của Orca và 9Router. Mỗi chỗ một task tại một thời điểm; một chỗ có hai task trong batch thì chạy lần lượt.
- Mỗi task một worktree, một nhánh `task/TK-nnnn-Rn` dựng từ cùng một commit của `origin/main` ghi lúc mở batch, một phiên, một PR.
- Orca: khi `harness/tools/INTEGRATION.md#FEATURES` dòng 1, 2, 4, 5 đã được OWNER xác nhận trên bản đang cài thì giao task bằng `orca worktree create`; chưa xác nhận thì tạo worktree bằng `git worktree add` và OWNER mở phiên WORKER trong từng worktree.
<!-- END: ORDER -->

<!-- ANCHOR: STOPS -->
## 2. Hai điểm dừng an toàn
- Dừng 1, task `BLOCKED`: sau loop `FAIL` thứ ba, hoặc khi không có model phù hợp, không xác định được model thực tế, không có REVIEWER phù hợp (`01_plan/SPEC_MODELS.md#STOPS`). LEAD dừng điều phối batch: không giao task mới, không mở thêm lượt, không sang batch kế. LEAD thu trạng thái thật của từng WORKER còn chạy (nhánh, commit cuối, run, PR, tiến trình) trước khi báo; lệnh dừng đã gửi không phải bằng chứng WORKER đã dừng.
- Dừng 2, hết batch: khi mọi task của batch có run `DONE`, PR mở và LEAD đã rà C1–C14, LEAD xuất khối `MERGE` có dòng `order` rồi dừng. Im lặng không phải phê duyệt.
- Tiếp tục sau Dừng 2 chỉ khi OWNER viết rõ tiếp tục. Khi đó LEAD kiểm: các PR cần thiết đã merge vào `main`; ghi SHA `origin/main` mới; chạy mục 6; rồi mới mở batch kế.
- Hết batch cuối của chu kỳ: LEAD soạn gói kiểm định, REVIEWER kiểm trên `main`, PR `RVW` chờ merge; `RVW` đạt thì LEAD soạn `CYC-nn_PASS.md` trong PR đồng bộ, chờ merge. Chu kỳ sau chỉ mở khi file cổng đã ở `main`.
<!-- END: STOPS -->

<!-- ANCHOR: BASE -->
## 3. Nền tích hợp tạm (E2)
- Chỉ dùng trong cùng một batch, khi cần kiểm chung các PR chưa merge của batch đó trước Dừng 2. Không dùng để chạy task của batch sau.
- Dựng: worktree riêng ở HEAD rời tại SHA `origin/main` của batch (`git worktree add --detach`); gộp lần lượt từng SHA đầu nhánh PR bằng `git merge --no-ff --no-edit`. Không tạo nhánh, không đẩy, không mở PR, không ghi vào `main` hay nhánh của PR.
- Kiểm trên nền tạm: `python -m pytest -q --tb=line` (đúng 23 test) và `python -m pytest -q --tb=line tools/tests`.
- Ghi: SHA nền, SHA đầu nhánh từng PR theo thứ tự gộp, SHA cây kết quả, giả định "các PR này được merge nguyên nội dung".
- Worktree của nền tạm chỉ do OWNER xóa.
<!-- END: BASE -->

<!-- ANCHOR: CONFLICT -->
## 4. Xung đột và thiếu đầu vào
- Gộp vào nền tạm báo xung đột: `git merge --abort`; không tự giải; các task liên quan là `BLOCKED`; áp Dừng 1. Hai task cùng batch ghi chung một file là lỗi của plan, sửa bằng một PR kèm `DEC`.
- Kiểm trên nền tạm không đạt: tính một loop `FAIL` cho task gây lỗi; WORKER sửa trong `write_scope`, cùng PR, cùng số run, nếu còn loop.
- Thiếu run `DONE` trên `main` của task phụ thuộc: không mở task; trạng thái `BLOCKED`; không giả định `PASS`.
- PR của một task xung đột với `main` sau khi PR khác merge: WORKER không rebase, không ép đẩy; báo OWNER.
<!-- END: CONFLICT -->

<!-- ANCHOR: LIMITS -->
## 5. Giới hạn lượt chạy
- Mỗi task tối đa 3 loop, tính cả loop đầu (`max_loops: 3`). Mỗi loop chạy đủ lệnh `verify` và mọi `done_when`; đầu vào, điều kiện đạt và bằng chứng của từng bài test ghi ở task.
- Mỗi chu kỳ tối đa 3 vòng kiểm định. Vòng `FAIL` sinh task sửa mới qua PR của LEAD; không sửa task cũ.
<!-- END: LIMITS -->

<!-- ANCHOR: PROVISIONAL -->
## 6. Nhãn `PROVISIONAL` và kiểm lại trên `main`
- `PROVISIONAL`: kết quả đạt nhưng dựa vào ít nhất một PR chưa merge (mọi kết quả trên nền tạm). Không thay lượt merge, không đổi `STATE.md`, sổ, file cổng, `02_work/cycles/`.
- `PASS` của một task: run `DONE`, PR đã merge, và kiểm ở neo `RERUN` đạt trên `main`.
<!-- END: PROVISIONAL -->

<!-- ANCHOR: RERUN -->
## 6b. Kiểm lại sau merge
| Khi | LEAD chạy lại trên `origin/main` | Kết quả cũ còn dùng được khi |
|---|---|---|
| Sau khi OWNER merge các PR của một batch | `python -m pytest -q --tb=line`; `python -m pytest -q --tb=line tools/tests` | Cả hai đạt |
| SHA đầu nhánh của một PR đổi sau khi LEAD rà | `verify` của task đó; rà lại C1–C14 | Đạt trên SHA mới |
| Thứ tự merge khác dòng `order`, hoặc một PR bị bỏ | `verify` của mọi task trong batch và của task phụ thuộc PR bị ảnh hưởng | Đạt trên `main` mới; PR bị bỏ thì task phụ thuộc `BLOCKED` |
| Cây `tools/` trên `main` khác SHA cây đã kiểm trên nền tạm | Toàn bộ kiểm của batch | Đạt; kết quả `PROVISIONAL` cũ bị bỏ |
| Sau lượt merge cuối của CYC-07 | Hồi quy trên Linux: hai lệnh pytest trên; đối chiếu với bằng chứng Windows của TK-0017 | Đạt; khi có file cổng CYC-07 thì đóng RSK-0005 |
<!-- END: RERUN -->

<!-- ANCHOR: REPORT -->
## 7. Báo cáo cho OWNER
- Mức ngắn, trong chat, mỗi task một cụm dọc: `task`, `status` (`PASS` · `FAIL` · `BLOCKED` · `PROVISIONAL`), `agent`, `model` (yêu cầu và thực tế), `loops`, `sha`, `pr`, `evidence`, `cause`, `decide`.
- Mức chi tiết, file `<project>.local/logs/orca-1.0.1/CYC-nn_Bk_REPORT.md`: lệnh đã chạy, SHA nền và nền tạm, từng loop, dòng lỗi liên quan, đường dẫn bằng chứng, đường dẫn log đầy đủ trên máy, phần còn lại.
- Không đưa bí mật hay log thô vào Git, PR, chat; che bí mật khi trích. Không cắt dòng lỗi cần cho chẩn đoán.
<!-- END: REPORT -->
