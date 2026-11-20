# Kiểm kê thay đổi Dry Run (CYC-03 – CYC-07) phục vụ xem xét chuyển về repo mẹ

- Mốc đối chiếu (Baseline SHA): `67a092fc469809d7d11c22a751bdba22f5aa9651` (PR #27, 2026-11-14T01:59:50Z)
- SHA đầu nhánh đối chiếu (Tip SHA): `c1f60821531bac9fa1c1cc8c1019b4cdeb77a888` (PR #83, 2026-11-20T13:38:47Z)
- Thời điểm đối chiếu: `2026-11-20 21:00:51 +07:00`
- Căn cứ điều phối: `DEC-0020`, `01_plan/SPEC_DRYRUN.md#UPSTREAM`, `02_work/tasks/CYC-07/TK-0028.md`
- Tổng số file khác biệt trong diff `67a092f..c1f6082`: 268 files (tất cả 268 files đều được ánh xạ trong bảng dưới)

> **Cảnh báo điều phối & chuyển giao:**
> - Bản kiểm kê này chỉ phục vụ đánh giá. Không tự ý sửa repo mẹ, không chuyển tự động, không mở PR ở repo mẹ.
> - Sau khi hoàn tất kiểm định chu kỳ CYC-07, LEAD sẽ đối chiếu lại toàn bộ diff đến commit cuối cùng và lập bản đề xuất chính thức tại `03_output/CYC-07/checks/UPSTREAM_PROPOSALS.md`.
> - Việc chuyển giao bất kỳ thành phần nào sang repo mẹ bắt buộc phải có phê duyệt (approval) rõ ràng của OWNER đối với từng đề xuất và phiên bản đích.

---

## 1. Bảng kiểm kê chi tiết các thay đổi (Diff 67a092f..c1f6082)

| STT | Nguồn (PR / Task / DEC) | Phạm vi & File trong diff | Trạng thái | Bằng chứng kiểm thử | Rủi ro | Đề xuất cho OWNER |
|---|---|---|---|---|---|---|
| 1.1 | PR #28, #29; DEC-0016, DEC-0018, REQ-0004, REQ-0005 | `harness.yaml`, `harness/` (HARNESS, MODEL_POLICY, rules/{LEAD,REVIEWER}, templates/{model_catalog,model_matrix}, tools/{INTEGRATION,PREFLIGHT}), `04_control/decisions/` (DEC-0016..0018), `04_control/requests/` (REQ-0004..0005), `04_control/risks/` (RSK-0005..0006), `00_brief/BRIEF.md`, `01_plan/` (PLAN, ACCEPTANCE, SPEC_{DRYRUN,MODELS,ORCA_PROMPT,SCAN,TOOLS}), `04_control/gates/PLAN_GO.md` [25 files] | MERGED | pytest 23 passed; gate PLAN_GO; merge PR #28, #29 | Lệch quy chuẩn nếu repo mẹ dùng cấu hình riêng hoặc schema cũ | **Điều chỉnh (Adjust)**: Chuyển các bổ sung quy tắc harness cốt lõi; giữ riêng cấu hình dry-run tại repo thử nghiệm |
| 1.2 | PR #30; DEC-0019, DEC-0020, REQ-0006, REQ-0007, RSK-0004 | `.github/README.md`, `harness/MAIN_PROTECTION.md`, `04_control/decisions/` (DEC-0019, DEC-0020), `04_control/requests/` (REQ-0006, REQ-0007), `04_control/risks/RSK-0004*.md` [7 files] | MERGED | Kiểm tra ruleset; merge PR #30 | Chính sách tài khoản chia sẻ có thể phụ thuộc hạ tầng GitHub cụ thể | **Chuyển (Transfer)**: Chuyển quy tắc MAIN_PROTECTION và hướng dẫn audit tài khoản; tinh chỉnh DEC repo mẹ |
| 1.3 | PR #31, #52, #53; DEC-0021, REQ-0008 | `04_control/MODEL_CATALOG.md`, `04_control/MODEL_MATRIX.md`, `04_control/decisions/DEC-0021*.md`, `04_control/requests/resolved/REQ-0008*.md` [4 files] | MERGED | Linter catalog/matrix; merge PR #31, #52, #53 | Danh mục model gắn với router/tài khoản môi trường thử nghiệm | **Không chuyển (Do not transfer)**: Catalog và Matrix mang tính cục bộ dự án thử nghiệm |
| 2.1 | PR #32; TK-0006 | `tools/hooks/pre-commit`, `tools/hooks/pre-push`, `tools/tests/test_hooks.py`, `02_work/tasks/CYC-03/TK-0006.md`, `02_work/runs/TK-0006_R1_DONE.md`, `03_output/CYC-03/checks/TK-0006_R1_*` (3 files) [8 files] | MERGED | `test_hooks.py` PASS; run DONE; baseline 23 passed | Hook Git phía client cần tương thích môi trường Windows & POSIX | **Chuyển (Transfer)**: Chuyển bộ hook bảo vệ nhánh main và test tương ứng sang repo mẹ |
| 2.2 | PR #33, #36, #38, #44, #45, #46; TK-0007, TK-0030, TK-0034, TK-0035; DEC-0026, DEC-0029, REQ-0009, REQ-0012 | `tools/preflight_main.py`, `tools/tests/test_preflight_main.py`, `04_control/decisions/` (DEC-0026, DEC-0029), `04_control/requests/` (REQ-0009, REQ-0012), `02_work/tasks/CYC-03/` (TK-0007, 30, 33, 34, 35), `02_work/runs/` (TK-0007, 30, 34, 35), `03_output/CYC-03/checks/` (TK-0007, 30, 34, 35: 11 files) [24 files] | MERGED (TK-0033 hủy/tách) | `test_preflight_main.py` PASS; mutation test; runs DONE | Mã hóa UTF-8 console Windows và phân giải đường dẫn hook tùy biến | **Chuyển (Transfer)**: Chuyển công cụ preflight hoàn chỉnh và test; dữ liệu runs/checks giữ tại chỗ |
| 2.3 | PR #34 (CLOSED), PR #35, PR #40; TK-0008, TK-0027 | `tools/github_audit.py`, `tools/tests/test_github_audit.py`, `tools/tests/test_shared_account_audit.py`, `02_work/tasks/CYC-03/` (TK-0008, 27), `02_work/runs/` (TK-0008 R1..R4, TK-0027), `03_output/CYC-03/checks/` (TK-0008: 5 files, TK-0027: 4 files) [17 files] | MERGED (PR #34 đóng; R1/R2 blocked) | `test_github_audit.py`, `test_shared_account_audit.py` PASS; run DONE | Quy tắc ruleset GitHub có thể khác biệt giữa tổ chức / cá nhân | **Điều chỉnh (Adjust)**: Tham số hóa repo và quy tắc trước khi áp dụng vào repo mẹ |
| 2.4 | PR #43; TK-0032 | `tools/hooks/pre-merge-commit`, `tools/tests/test_pre_merge_commit.py`, `02_work/tasks/CYC-03/TK-0032.md`, `02_work/runs/TK-0032_R1_DONE.md`, `03_output/CYC-03/checks/TK-0032_R1_*` (2 files) [6 files] | MERGED | `test_pre_merge_commit.py` PASS; tích hợp repo thật PASS; run DONE | Chặn tạo merge commit trực tiếp trên main cục bộ | **Chuyển (Transfer)**: Chuyển hook pre-merge-commit và test đi kèm |
| 2.5 | PR #41, #47; TK-0018; DEC-0028, REQ-0011 | `tools/tests/test_main_guard_edges.py`, `04_control/decisions/DEC-0028*.md`, `04_control/requests/resolved/REQ-0011*.md`, `02_work/tasks/CYC-03/TK-0018.md`, `02_work/runs/TK-0018_R1_DONE.md`, `03_output/CYC-03/checks/TK-0018_R1_*` (6 files) [11 files] | MERGED | `test_main_guard_edges.py` PASS (47 test); run DONE | Bộ test biên phức tạp, chạy tốn thời gian (~110s) | **Chuyển (Transfer)**: Chuyển test bảo vệ biên main vào bộ test công cụ của repo mẹ |
| 3.1 | PR #54; TK-0009 | `tools/model_check.py`, `tools/tests/test_model_check.py`, `02_work/tasks/CYC-04/TK-0009.md`, `02_work/runs/TK-0009_R1..R3` (3 files), `03_output/CYC-04/checks/TK-0009_*` (12 files) [17 files] | MERGED (R1/R2 blocked) | `test_model_check.py` PASS; run DONE; catalog/matrix schema PASS | Ràng buộc schema kiểm tra danh mục mô hình | **Chuyển (Transfer)**: Chuyển công cụ kiểm tra schema catalog/matrix |
| 3.2 | PR #55; TK-0010 | `tools/model_select.py`, `tools/tests/test_model_select.py`, `02_work/tasks/CYC-04/TK-0010.md`, `02_work/runs/TK-0010_R1_DONE.md`, `03_output/CYC-04/checks/TK-0010_*` (4 files) [7 files] | MERGED | `test_model_select.py` PASS; JSON output đối chiếu ma trận; run DONE | Thuật toán chọn mô hình độc lập phụ thuộc cấu hình ma trận | **Chuyển (Transfer)**: Chuyển script chọn model và kiểm định độc lập reviewer |
| 3.3 | PR #56, #57; TK-0019, TK-0029 | `tools/assign_audit.py`, `tools/tests/test_assign_audit.py`, `tools/tests/test_model_route_identity.py`, `02_work/tasks/CYC-04/` (TK-0019, 29), `02_work/runs/` (TK-0019 R1/R2, TK-0029), `03_output/CYC-04/checks/` (TK-0019: 10 files, TK-0029: 2 files) [17 files] | MERGED (TK-0019 R1 blocked) | `test_assign_audit.py`, `test_model_route_identity.py` PASS; run DONE | Định dạng log kiểm toán tuyến 9Router và tên model thực tế | **Chuyển (Transfer)**: Chuyển công cụ kiểm toán phân công và nhận dạng tuyến model |
| 4.1 | PR #62; TK-0011 | `tools/branch_names.py`, `tools/tests/test_branch_names.py`, `02_work/tasks/CYC-05/TK-0011.md`, `02_work/runs/TK-0011_R1_DONE.md`, `03_output/CYC-05/checks/TK-0011_*` (3 files) [6 files] | MERGED | `test_branch_names.py` PASS; run DONE; baseline 23 passed | Ràng buộc phân loại tên nhánh theo quy ước harness | **Chuyển (Transfer)**: Chuyển script phân loại và chuẩn hóa tên nhánh Git |
| 4.2 | PR #63; TK-0020 | `tools/tests/data/freeze_manifest.json`, `tools/tests/test_storage_freeze.py`, `tools/tests/test_trace_open.py`, `02_work/tasks/CYC-05/TK-0020.md`, `02_work/runs/TK-0020_R1_DONE.md`, `03_output/CYC-05/checks/TK-0020_*` (3 files) [7 files] | MERGED | `test_storage_freeze.py`, `test_trace_open.py` PASS; run DONE | Kiểm tra đóng băng blob và mở trace trong môi trường thực thi | **Chuyển (Transfer)**: Chuyển bộ kiểm tra bảo vệ lưu trữ và trace |
| 4.3 | PR #64; TK-0012 | `tools/chat_blocks.py`, `tools/tests/test_chat_blocks.py`, `02_work/tasks/CYC-05/TK-0012.md`, `02_work/runs/TK-0012_R1_DONE.md`, `03_output/CYC-05/checks/TK-0012_*` (2 files) [5 files] | MERGED | `test_chat_blocks.py` PASS; run DONE | Ràng buộc định dạng các khối tin nhắn trao đổi | **Chuyển (Transfer)**: Chuyển validator khối chat (CONFIRM, RESULT, v.v.) |
| 4.4 | PR #65; TK-0021 | `tools/clean_list.py`, `tools/tests/test_clean_list.py`, `02_work/tasks/CYC-05/TK-0021.md`, `02_work/runs/TK-0021_R1_DONE.md`, `03_output/CYC-05/checks/TK-0021_*` (2 files) [5 files] | MERGED | `test_clean_list.py` PASS; run DONE | Trích xuất danh sách sạch không kèm ghi chú giải thích | **Chuyển (Transfer)**: Chuyển công cụ kiểm tra danh sách sạch |
| 5.1 | PR #70, #72, #73; TK-0013, TK-0014; DEC-0030 | `tools/scan.py`, `tools/scan_rules.json`, `tools/tests/test_scan_core.py`, `tools/tests/test_scan_limits.py`, `04_control/decisions/DEC-0030*.md`, `02_work/tasks/CYC-06/` (TK-0013, 14), `02_work/runs/` (TK-0013, 14), `03_output/CYC-06/checks/` (TK-0013: 3 files, TK-0014: 2 files) [12 files] | MERGED | `test_scan_core.py`, `test_scan_limits.py` PASS; DEC-0030 PASS; runs DONE | Quét phát hiện mã độc hại / prompt injection trong dữ liệu ngoài | **Chuyển (Transfer)**: Chuyển scanner bảo mật lõi, tập luật và bộ test |
| 5.2 | PR #71; TK-0022 | `tools/scan_quarantine.py`, `tools/scan_wrap.py`, `tools/tests/test_scan_quarantine.py`, `tools/tests/test_scan_wrap.py`, `02_work/tasks/CYC-06/TK-0022.md`, `02_work/runs/TK-0022_R1_DONE.md`, `03_output/CYC-06/checks/TK-0022_*` (2 files) [7 files] | MERGED | `test_scan_quarantine.py`, `test_scan_wrap.py` PASS; run DONE | Cách ly file nguy hiểm và bọc thẻ EXTERNAL_DATA an toàn | **Chuyển (Transfer)**: Chuyển công cụ bọc dữ liệu và khu cách ly bảo mật |
| 5.3 | PR #74; TK-0023 | `tools/tests/test_scan_adversarial.py`, `02_work/tasks/CYC-06/TK-0023.md`, `02_work/runs/TK-0023_R1_DONE.md`, `03_output/CYC-06/checks/TK-0023_*` (3 files) [5 files] | MERGED | `test_scan_adversarial.py` PASS; run DONE | Test đối kháng kiểm tra độ bền vững của scanner | **Chuyển (Transfer)**: Chuyển bộ test đối kháng cho scanner |
| 6.1 | PR #79; TK-0016 | `tools/tests/test_pytest_template.py`, `02_work/tasks/CYC-07/TK-0016.md`, `02_work/runs/TK-0016_R1_DONE.md`, `03_output/CYC-07/checks/TK-0016_*` (2 files) [4 files] | MERGED | `test_pytest_template.py` PASS; run DONE; baseline 23 passed | Ngăn phát hiện nhầm các test template rỗng | **Chuyển (Transfer)**: Chuyển bộ test kiểm tra thu thập pytest template |
| 6.2 | PR #80; TK-0015 | `tools/batch_check.py`, `tools/tests/test_batch_check.py`, `02_work/tasks/CYC-07/TK-0015.md`, `02_work/runs/TK-0015_R1_DONE.md`, `03_output/CYC-07/checks/TK-0015_*` (2 files) [5 files] | MERGED | `test_batch_check.py` PASS; run DONE | Kiểm tra zero-overlap write_scope giữa các task cùng batch | **Chuyển (Transfer)**: Chuyển công cụ kiểm tra xung đột phân bổ batch |
| 6.3 | PR #81; TK-0025 | `tools/integrate_check.py`, `tools/tests/test_integrate_check.py`, `02_work/tasks/CYC-07/TK-0025.md`, `02_work/runs/TK-0025_R1_DONE.md`, `03_output/CYC-07/checks/TK-0025_*` (4 files) [7 files] | MERGED | `test_integrate_check.py` PASS; run DONE | Kiểm tra tích hợp nền tạm của batch trước khi nghiệm thu | **Chuyển (Transfer)**: Chuyển script kiểm tra tích hợp tự động |
| 6.4 | PR #82; TK-0024 | `tools/pytest_ini_check.py`, `tools/tests/test_pytest_ini_check.py`, `02_work/tasks/CYC-07/TK-0024.md`, `02_work/runs/TK-0024_R1_DONE.md`, `03_output/CYC-07/checks/TK-0024_*` (2 files) [5 files] | MERGED | `test_pytest_ini_check.py` PASS; run DONE | Tương thích cấu hình pytest giữa các phiên bản | **Chuyển (Transfer)**: Chuyển công cụ kiểm tra tương thích pytest.ini |
| 6.5 | PR #83; TK-0026 | `tools/README.md`, `tools/requirements.txt`, `02_work/tasks/CYC-07/TK-0026.md`, `02_work/runs/TK-0026_R1_DONE.md`, `03_output/CYC-07/checks/TK-0026_*` (4 files) [7 files] | MERGED | Kiểm tra tài liệu và cài đặt dependencies; run DONE | Hướng dẫn sử dụng và thư viện phụ thuộc của bộ tools | **Chuyển (Transfer)**: Chuyển tài liệu tổng hợp và requirements bộ công cụ |
| 7.1 | PR #48, #50, #58, #60, #66, #68, #75, #77, #78 | `02_work/cycles/` (CYC-03..CYC-07: 5 files), `04_control/gates/` (CYC-03..CYC-06_PASS: 4 files), `04_control/STATE.md`, `05_memory/digests/` (CYC-03..CYC-06: 4 files) [14 files] | MERGED | Ký duyệt cổng chu kỳ (PASS gates); digests đồng bộ; STATE | Dữ liệu trạng thái và sổ ghi chu kỳ riêng của dự án thử nghiệm | **Không chuyển (Do not transfer)**: Dữ liệu vận hành dry run nội bộ |
| 7.2 | PR #39, #49, #59, #67 (CLOSED), #76 | `03_output/CYC-03/checks/PR38_B2_OWNER_ACCEPTANCE.md`, `03_output/CYC-03/checks/RVW-CYC-03.md`, `03_output/CYC-04/checks/RVW-CYC-04.md`, `03_output/CYC-05/checks/RVW-CYC-05.md`, `03_output/CYC-06/checks/RVW-CYC-06.md` [5 files] | MERGED / CLOSED | Báo cáo kiểm định độc lập của REVIEWER qua từng chu kỳ | Nhật ký kiểm định chu kỳ mang tính chất lịch sử thử nghiệm | **Không chuyển (Do not transfer)**: Bằng chứng nghiệm thu chu kỳ dry run |
| 7.3 | Chưa hoàn thành / Đang thi công | `02_work/tasks/CYC-07/TK-0017.md`, `02_work/tasks/CYC-07/TK-0028.md` [2 files] | PENDING / IN PROGRESS | Chưa xác minh (chưa hoàn thành / đang thực hiện) | Task chưa đóng vòng kiểm tra | **Không chuyển (Do not transfer)**: Chờ hoàn thành và đánh giá sau |

---

## 2. Báo cáo các PR và Task chưa merge, thất bại, bị đóng hoặc dự thảo

Dưới đây là danh sách đối chiếu đầy đủ các yêu cầu/task/PR phát sinh trong quá trình dry run nhưng chưa merge vào `origin/main` hoặc có trạng thái đặc biệt:

1. **PR #34 (`task/TK-0008-R1`)**:
   - Trạng thái: **CLOSED (không merge)** ngày 2026-11-16T01:32:29Z.
   - Nguyên nhân: TK-0008 R1 và R2 gặp lỗi phân tích ruleset GitHub và quyền tài khoản (`TK-0008_R1_BLOCKED.md`, `TK-0008_R2_BLOCKED.md`).
   - Xử lý: Thay thế bởi TK-0008 R3/R4 trong PR #35 (đã MERGED).
   - Đề xuất: **Không chuyển** nhánh của PR #34; dùng kết quả đã hoàn thiện ở PR #35.

2. **PR #37 (`lead/worker-permissions`)**:
   - Trạng thái: **OPEN / DRAFT (chưa merge)**.
   - Nội dung: Dự thảo DEC-0027, REQ-0010, kế hoạch CYC-08 và task TK-0031 kiểm kê quyền WORKER sau dry run.
   - Bằng chứng: **Chưa xác minh (unverified)**; bộ test `tools/tests` khi đó có 3 test preflight thất bại; chưa được OWNER duyệt.
   - Đề xuất: **Điều chỉnh / Xem xét sau**: OWNER rà soát sau khi kết thúc CYC-07 trước khi quyết định mở CYC-08.

3. **PR #67 (`review/CYC-05-R1-7b21`)**:
   - Trạng thái: **CLOSED (không merge)** ngày 2026-11-20T08:54:28Z.
   - Nguyên nhân: Nhánh kiểm định CYC-05 mở vào nhánh `lead/cyc05-close`. LEAD đã gộp sổ CYC-05 trực tiếp qua PR #66 và mở cổng qua PR #68, đóng PR #67. Kết quả review được lưu tại `03_output/CYC-05/checks/RVW-CYC-05.md`.
   - Đề xuất: **Không chuyển** PR #67.

4. **Task TK-0033 (CYC-03)**:
   - Trạng thái: **CANCELLED / SUPERSEDED** bởi DEC-0029 (PR #42).
   - Nguyên nhân: Bản thảo task đạt ~620 dòng, vượt quá giới hạn ngân sách dòng (`line_budget: 400`).
   - Xử lý: Không tạo run/PR cho TK-0033; tách thành hai task tuần tự TK-0034 (lõi detector) và TK-0035 (lỗi đọc, mã hóa). Cả hai đã hoàn thành và merged (PR #44, #45).
   - Đề xuất: **Không chuyển** TK-0033.

5. **Các vòng chạy bị nghẽn (BLOCKED Runs)**:
   - `TK-0008 R1, R2` (CYC-03): Bế tắc do rà soát GitHub ruleset & CODEOWNERS; giải quyết ở R3/R4.
   - `TK-0009 R1, R2` (CYC-04): Bế tắc do cấu trúc schema catalog note; giải quyết ở R3.
   - `TK-0019 R1` (CYC-04): Bế tắc do thiếu dữ liệu log lịch sử để kiểm toán model thực tế; giải quyết ở R2.
   - Đề xuất: **Không chuyển** các run BLOCKED; toàn bộ đã được khắc phục ở các run DONE kế tiếp.

6. **Task TK-0017 (CYC-07)**:
   - Trạng thái: **PENDING (Chưa chạy)**.
   - Mục tiêu: Kiểm tra đối chiếu tương đương đa nền tảng Windows và Linux sau khi hoàn tất các batch CYC-07.
   - Bằng chứng: **Chưa xác minh (unverified)**.
   - Đề xuất: Đánh giá chuyển giao sau khi TK-0017 được hoàn thành và nghiệm thu ở cuối chu kỳ CYC-07.

---

## 3. Kết luận và quy trình tiếp theo

1. **Tính đầy đủ:** Toàn bộ 268 file trong diff từ `67a092f` đến tip `c1f6082` đã được phân loại và đối chiếu nguồn gốc, bằng chứng và rủi ro. Dữ liệu từ GitHub CLI (`gh`) và Git history đã được khai thác trọn vẹn. Không có nguồn ngoài nào bị bỏ sót trong phạm vi truy cập được.
2. **Không tự động chuyển:** Không thực hiện bất kỳ thao tác đẩy hoặc tạo PR sang repo mẹ.
3. **Kế hoạch tiếp theo:** Sau khi chu kỳ CYC-07 hoàn thành kiểm định độc lập, LEAD sẽ lập bảng tổng hợp cuối cùng `03_output/CYC-07/checks/UPSTREAM_PROPOSALS.md` trình OWNER phê duyệt từng mục cụ thể trước khi thực hiện chuyển giao chính thức.
