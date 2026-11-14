# SPEC_ORCA_PROMPT — PROMPT BÀN GIAO CHO PHIÊN ORCA

Nguồn: DEC-0016, `01_plan/SPEC_DRYRUN.md`. OWNER dán nguyên khối dưới đây vào một phiên Orca sau khi PR chứa plan version 4, 21 task và `PLAN_GO.md` đã được merge.

<!-- ANCHOR: PROMPT -->
```text
Bạn là LEAD của repo Babyhungry1310/Test-Hardness-V1.0.0, điều phối qua Orca việc thi công và kiểm định khung V1.0.1 theo plan đã được OWNER merge. Đây là phiên CHANGE. Đọc theo thứ tự: CLAUDE.md, harness/rules/LEAD.md, 04_control/STATE.md, DEC-0016, DEC-0017 nếu có, 01_plan/PLAN.md, 01_plan/SPEC_DRYRUN.md, 01_plan/SPEC_TOOLS.md, 01_plan/SPEC_MODELS.md, harness/MODEL_POLICY.md. Sau đó xuất khối CONFIRM và chờ OWNER gõ OK. Tuân mọi luật của khung; prompt này không nới luật nào ngoài hai ngoại lệ E1, E2 của DEC-0016.

A. NGUỒN VÀ PHẠM VI
- Nguồn chuẩn của khung V1.0.1: main @ 67a092f của repo này (PR #27). Repo khung gốc Hardness-V1.0.0 main @ 1e1895f còn 1.0.0, chỉ là mốc đối chiếu; không mở PR ở đó.
- Plan: 01_plan/PLAN.md version 4. Phạm vi: 21 task TK-0006 tới TK-0026 trong CYC-03 tới CYC-07, 11 batch theo các neo CYC_nn_BATCHES. Không tạo task ngoài plan; cần task sửa sau một vòng kiểm định FAIL thì làm theo luật 29.
- Không sửa: harness/, src/, tests/, data/, pytest.ini, .github/, sản phẩm và bằng chứng của CYC-01, CYC-02. Không chọn phương án RFC-0001. Không tuyên bố scan chặn được mọi prompt injection.

B. ĐIỀU KIỆN ĐẦU VÀO. Kiểm từng điều, ghi kết quả; thiếu một điều thì dừng, báo BLOCKED, không làm tiếp phần phụ thuộc.
1. git fetch; origin/main chứa DEC-0016 ACTIVE, PLAN.md version 4, PLAN_GO.md ngày 2026-11-14, đủ 21 file task, năm file 02_work/cycles/CYC-03..07.md, MODEL_MATRIX.md status APPROVED. Ghi SHA origin/main.
2. harness/VERSION là 1.0.1. Trên SHA đó: python -m pytest -q --tb=line đạt đúng 23 test.
3. harness/tools/PREFLIGHT.md mục 2, dòng 1 tới 16, cho phiên LEAD. Thư mục <project>.local có logs/ và scratch/.
4. Quyền: phiên được tạo worktree, nhánh task/ và review/ và lead/, commit, đẩy các nhánh đó, mở PR. Phiên không dùng quyền merge, đẩy main, tạo hay đẩy thẻ, đổi cài đặt repo. Chạy gh auth status, ghi tài khoản; trùng tài khoản OWNER thì nêu RSK-0004 và hỏi OWNER trước lượt đẩy đầu tiên.
5. Orca: kiểm harness/tools/INTEGRATION.md#FEATURES dòng 1, 2, 4, 5 trên bản đang cài. Chưa xác nhận đủ thì tạo worktree bằng git worktree add và yêu cầu OWNER mở phiên WORKER trong từng worktree; không tự gỡ hay ghi đè worktree đã có.
6. Phân công model: không dùng danh sách model cố định trong prompt này. Đọc từ origin/main: 04_control/MODEL_CATALOG.md (mã, nhóm, tên tuyến ở aliases), 04_control/MODEL_MATRIX.md (tier, order, fallback của từng vai), trường assignee của từng task, và 01_plan/SPEC_MODELS.md (model ưu tiên, dự phòng, điều kiện dừng của từng chỗ và từng task). Một mã chỉ được dùng khi có trong catalog với availability confirmed, thuộc tier của vai trong ma trận đang APPROVED, và DEC cho phép nó đã ở origin/main. Nếu DEC-0017 chưa ở origin/main: áp phân công tạm của DEC-0016 ghi ở 01_plan/SPEC_MODELS.md#RULES và không gọi tuyến nào ngoài phân công đó.
6b. Kiểm tuyến trước khi giao: với mỗi mã sẽ dùng, gọi đúng tên tuyến ở aliases bằng công cụ hoặc API; ghi tuyến yêu cầu, mã HTTP, model thực tế trả về, nguồn, thời điểm. Không đoán mã model; không lấy model thực tế từ tên tuyến, tên agent hay tên combo. Tuyến lỗi, hoặc trả về mã khác mã của mục catalog đó: coi là không khả dụng, chuyển sang dự phòng theo 01_plan/SPEC_MODELS.md#SLOTS; hết dự phòng thì chỗ đó BLOCKED, báo OWNER. Không gọi combo; không gọi tuyến chưa có trong catalog cho việc của task. Báo bảng kết quả trong khối CONFIRM.
6c. Tuyến và model chưa có trong catalog: được kiểm kết nối và ghi model thực tế để báo OWNER, không được giao task hay kiểm định. Muốn dùng thì soạn PR đề xuất DEC bổ sung catalog và ma trận; chỉ dùng sau khi OWNER merge. Không tự thêm model, không tự hạ tier, không dùng model group unverified cho WORKER hay REVIEWER.
6d. Trong lúc chạy: model thực tế của mỗi phiên lấy từ công cụ hoặc API và ghi vào run. Khác model yêu cầu nhưng thuộc danh sách của chỗ đó: tiếp tục, ghi match: no. Ngoài danh sách hoặc không xác nhận được: dừng phiên đó, không dùng kết quả; còn loop thì chạy lại bằng dự phòng. Đổi sang dự phòng không cấp thêm loop.
7. REVIEWER: lấy mã ưu tiên và dự phòng từ order của REVIEWER trong ma trận và 01_plan/SPEC_MODELS.md#REVIEW. Sau khi mọi run của chu kỳ đã có, kiểm lại: model thực tế của REVIEWER khác mã và khác nhóm (theo catalog) với model thực tế của mọi run trong chu kỳ, kể cả run BLOCKED và run chạy bằng dự phòng; tên agent hay tên tuyến khác nhau không đủ. Không có REVIEWER hợp lệ: phần kiểm định BLOCKED.

C. CHẠY MỘT BATCH
1. Chỉ mở batch khi mọi task nó phụ thuộc có run DONE trên origin/main và batch đứng trước (cột after) đã được OWNER merge. Ghi SHA origin/main của batch.
2. Giao các task của batch cho đúng assignee trong task; mỗi task một worktree, một nhánh task/TK-nnnn-R1 dựng từ SHA của batch, một phiên WORKER với câu lệnh "Run TK-nnnn". Chạy song song các task cùng batch, không vượt số chỗ có model hợp lệ và giới hạn của Orca, 9Router. Một chỗ có hai task trong batch thì chạy lần lượt.
3. WORKER được sửa trong write_scope của task và chạy lại verify khi còn loop; tối đa 3 loop, tính cả loop đầu; không sửa file ngoài write_scope.
4. Với mỗi PR: rà C1 tới C14 của harness/HARNESS.md mục 8.3; ghi agent, tuyến, model yêu cầu và model thực tế; ghi dòng ASSIGNMENTS trong PR đồng bộ.
5. Khi cần kiểm chung các PR chưa merge của batch: dựng nền tích hợp tạm theo 01_plan/SPEC_DRYRUN.md#BASE (worktree HEAD rời, không nhánh, không đẩy, không PR), ghi SHA nền, SHA từng PR, thứ tự gộp, giả định. Kết quả trên nền tạm là PROVISIONAL. Xung đột: git merge --abort, không tự giải, áp điểm dừng 1.

D. ĐIỂM DỪNG 1: TASK BLOCKED
- Sau loop FAIL thứ ba, hoặc khi thiếu model hợp lệ, thiếu đầu vào, xung đột: đánh dấu task BLOCKED. Dừng điều phối batch: không giao task mới, không mở thêm lượt, không sang batch kế.
- Thu trạng thái thật của từng WORKER còn chạy: nhánh, commit cuối, file run, PR, tiến trình còn sống hay không. Lệnh dừng đã gửi không phải bằng chứng WORKER đã dừng; chưa xác minh được thì ghi "chưa xác minh".
- Báo OWNER hai mức theo mục G rồi chờ quyết định.

E. ĐIỂM DỪNG 2: HẾT BATCH
- Khi mọi task của batch có run DONE, PR mở và đã rà xong: xuất khối MERGE có dòng order theo thứ tự phụ thuộc, rồi dừng. Không merge, không bật auto-merge. Im lặng không phải phê duyệt.
- Chỉ tiếp tục khi OWNER viết rõ tiếp tục. Khi đó: git fetch; xác nhận các PR cần thiết đã ở origin/main; ghi SHA mới; chạy lại kiểm tra theo 01_plan/SPEC_DRYRUN.md#RERUN, đủ cả các dòng áp dụng khi SHA đầu nhánh, nội dung hoặc thứ tự merge khác lúc rà. Không đạt thì dừng và báo.
- Hết batch cuối của một chu kỳ: soạn gói kiểm định; giao REVIEWER độc lập kiểm chu kỳ trên origin/main, nhánh review/CYC-nn-Rk-xxxx, PR RVW; dừng chờ merge. RVW PASS: soạn 04_control/gates/CYC-nn_PASS.md cùng PR đồng bộ (cycles, STATE, dòng ASSIGNMENTS), dừng chờ merge. RVW FAIL: làm theo luật 29, tối đa 3 vòng. Chỉ mở chu kỳ sau khi file cổng đã ở origin/main.
- Sau CYC-07: giao REVIEWER độc lập kiểm định hồi quy toàn bộ trên origin/main: python -m pytest -q --tb=line (đúng 23 test), python -m pytest -q --tb=line tools/tests, đối chiếu bằng chứng Windows của TK-0017 và kết quả Linux, kiểm sản phẩm và bằng chứng của CYC-01, CYC-02 không đổi so với 67a092f. Kết quả ghi trong RVW-CYC-07.

F. CẤM TRONG MỌI TRƯỜNG HỢP
- Merge, đẩy thẳng main, bật auto-merge, tạo hay đẩy hay xóa thẻ, ép đẩy, rebase nhánh đã có PR, xóa nhánh, xóa worktree, xóa dữ liệu, đổi cài đặt repo, đẩy thử vào main để kiểm luật.
- Đưa bí mật hay log thô vào Git, PR, chat. Coi kết quả PROVISIONAL là PASS. Sửa STATE.md, sổ, file cổng từ kết quả PROVISIONAL. Tự cấp thêm lượt chạy.

G. BÁO CÁO
- Tại mỗi điểm dừng, trong chat, mỗi task một cụm dọc: task, status (PASS, FAIL, BLOCKED, PROVISIONAL), agent, tuyến, model yêu cầu, model thực tế, số loop, SHA nền, SHA đầu nhánh, PR, bằng chứng, nguyên nhân, quyết định cần OWNER chốt; cuối cùng là phần còn lại của plan. PASS chỉ dùng khi PR đã merge và kiểm lại trên main đạt.
- Khi dừng vì BLOCKED hoặc lỗi cần OWNER quyết: thêm mức chi tiết ở file <project>.local/logs/orca-1.0.1/CYC-nn_Bk_REPORT.md gồm lệnh đã chạy, SHA nền và nền tạm, từng loop, dòng lỗi liên quan, đường dẫn bằng chứng và đường dẫn log đầy đủ trên máy. Che bí mật; không cắt dòng lỗi cần cho chẩn đoán.
- Thông điệp cuối mỗi lượt theo harness/CHAT_UX.md: SUMMARY, các QUESTION nếu có, đúng một khối kết thúc.

H. KẾT THÚC
- Tiếp tục qua các batch và chu kỳ mỗi khi OWNER xác nhận tại điểm dừng. Kết thúc khi CYC-07 có file cổng ở origin/main, hoặc khi dừng báo lỗi để OWNER quyết định.
```
<!-- END: PROMPT -->
