---
schema: 1
id: DEC-0028
date: 2026-11-19
title: "Hai task nguồn và bàn giao theo snapshot trước khi tiếp tục TK-0018"
proposed_by: LEAD
decided_by: OWNER
cycle: CYC-03
origin: REQ-0011
supersedes: ""
cancels: []
waives: []
affects: [TK-0018, TK-0032, TK-0033, "01_plan/PLAN.md", "01_plan/ACCEPTANCE.md", "01_plan/SPEC_TOOLS.md", "04_control/STATE.md"]
keywords: [hooks, crlf, source-tasks, handoff, immutable-evidence]
---
## Status (newest first)
- 2026-11-24 | RETIRED
- 2026-11-19 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
REQ-0011. TK-0018 R1 L01 ghi 44 passed/3 failed: merge tạo commit không gọi pre-commit, và Git for Windows chạy được bản hook CRLF. Task chỉ được sửa test nên không tự sửa hai lỗi nguồn. Nền governance là main 9a841076706dcd4ed34856ca111cd818b82cbfb5. Draft code do Grok làm, Gemini review qua route ag/gemini-3.8-flash-high; response.model là gemini-3.8-flash-n. PASS draft không phải PASS sản phẩm hoặc hoàn tất TK-0018; log scratch và mutation giữ ngoài repo.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- Nới assert hoặc đổi ca phải chặn thành test_limit_: bác bỏ.
- Sửa hook/preflight trong phạm vi test-only của TK-0018: bác bỏ.
- Hai task nguồn có write_scope rời nhau, rồi nghiệm thu TK-0018 trên base đã tích hợp: OWNER chọn.
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
- TK-0032 thêm pre-merge-commit LF, mode 100755, cùng chính sách main; test dùng merge --no-ff thật, HEAD/main không đổi, abort xong status sạch, nhánh hợp lệ merge được.
- TK-0033 nhận diện hook bằng tên githooks(5) phân biệt hoa thường hoặc shebang; bỏ .md/.sample không phân biệt hoa thường. Không có hook phù hợp: missing và warning Hook chưa cài. Hook LF: installed. CR byte: crlf, tên file, session exit 1. Lỗi đọc/duyệt: error, JSON có cấu trúc, exit 1; giữ cả bằng chứng CRLF và lỗi đọc theo thứ tự xác định. Commit/push stage và lỗi dùng exit 2 giữ nguyên.
- CRLF fixture sinh bằng write_bytes trong tmp_path, assert byte CRLF trước khi gọi sản phẩm. Không thay .gitattributes hoặc config. Kiểm Git blob/mode và mutation trên bản sao của cây commit ở task nguồn; không cho EOL/filter làm mất fixture.
- Sau cả hai nguồn và batch trước đã merge, cập nhật TK-0018 lên SHA main mới, kiểm diff/base trước khi sửa và verify. Rebase chỉ khi thích hợp với lịch sử local chưa publish; không rewrite nhánh đã publish, amend hay force push. Snapshot PASS cũ không tự chuyển sang base mới.
- TK-0018 giữ merge --no-ff phải chặn; ca CRLF chuyển sang kiểm detector session trên bản sao hook. Mỗi ca vẫn có assert thực; không skip/xfail để giấu lỗi. L01 bất biến; tiếp tục R1 chỉ còn L02/L03, không reset max_loops.
- Số 3 failed/39 passed chỉ là mutation bỏ hai dòng cách ly Git của bộ scratch 42 ca. Mutation trên nguồn/main mới có kỳ vọng theo ca bị tác động, không ép số tổng cũ.
- Writer ưu tiên Grok native; model thực tế phải được xác minh trong phiên thi công. Reviewer Gemini qua 9Router, actual khác writer. PASS đọc code dùng log được cấp không được ghi là reviewer tự chạy test.
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
- Ghi task/plan/spec trong PR governance này; chỉ thi công sau khi OWNER merge. B2 gồm TK-0027, TK-0032, TK-0033 độc lập, write_scope rời nhau; B3 chỉ TK-0018, sau toàn B2 và baseline main đạt. TK-0030 đã merge là đầu vào TK-0033, không mở lại.
- Áp dụng SPEC_TOOLS#HANDOFF cho các task này: checklist đóng băng, bundle rN, manifest hash cả SUMMARY, verdict gắn bundle ID, kiểm blob/base trước publication. LEAD chịu bước chuyển từ PASS sang gói diff/commit chờ duyệt; worker thiếu Git giao patch cho committer script, không tự cài công cụ.
- OWNER duyệt riêng commit, push nhánh task và mở PR, gắn SHA/phạm vi; chỉ OWNER merge. Không thay quyền bằng SLA, không tự bật CI/branch protection, không sửa harness hay tài khoản. Không có check thì ghi không có, không ghi xanh.
- Theo DEC-0019 và RSK-0004, tài khoản chung chưa tách tác tử/OWNER bằng kỹ thuật; giữ verdict và dấu vết phiên độc lập. GitHub App/tài khoản riêng là ưu tiên đề xuất, không được tự tạo hoặc cấu hình trong task này.
- BLOCKED ghi loại/chủ/điều kiện mở kiểm chứng được/thời điểm. Tra quyết định đã có trước DECISION_OWNER; việc LEAD chưa làm là ACTION_LEAD. Hai vòng review là ngưỡng tái cấu trúc, không miễn lỗi đúng đắn. Không đoán thời gian chưa ghi nhận.
<!-- END: CONSEQUENCES -->
