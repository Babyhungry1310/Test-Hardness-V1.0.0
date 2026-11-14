---
schema: 1
id: DEC-0016
date: 2026-11-14
title: "Thử khung V1.0.1 trên repo này: nguồn chuẩn, nơi đặt code, duyệt ma trận model, ngoại lệ tạo task và nền tích hợp tạm"
proposed_by: LEAD
decided_by: OWNER
cycle: NONE
origin: "REQ-0004"
supersedes: ""
cancels: []
waives: []
affects: ["00_brief/BRIEF.md", "harness.yaml", "01_plan/PLAN.md", "01_plan/ACCEPTANCE.md", "01_plan/SPEC_TOOLS.md", "01_plan/SPEC_SCAN.md", "01_plan/SPEC_DRYRUN.md", "01_plan/SPEC_ORCA_PROMPT.md", "04_control/MODEL_MATRIX.md", "04_control/gates/PLAN_GO.md", DEC-0015, RSK-0004, RSK-0005]
keywords: [harness-upgrade, plan, dry-run, product-paths, model-matrix, integration-base, provisional]
---
## Status (newest first)
- 2026-11-14 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
REQ-0004. DEC-0015 đưa V1.0.1 vào repo này ở mức đặc tả, chưa có script, plan hay task. Năm điểm chặn việc lập plan: nguồn chuẩn không nằm ở repo khung gốc; code của hook và script theo đặc tả nằm ở `harness/tools/` (🔒), ngoài `product_paths`; `04_control/MODEL_MATRIX.md` còn `PROPOSED`; `00_brief/BRIEF.md` không gồm việc thử khung; tạo task của năm chu kỳ trong một PR trái luật 25 của LEAD, và nền tích hợp tạm chưa có trong luật. OWNER chọn 1a, 2a, 3a, 4a, 5a trong phiên ngày 2026-11-14, sau đó yêu cầu thêm: phân công tham khảo theo ba nhóm 9Router (W2, W3 tạm dùng model đã hợp lệ trong catalog), dừng sau mỗi batch chờ squash-merge, dừng điều phối khi một task `BLOCKED`. Không còn `PROPOSAL` nào treo; RFC-0001 giữ `OPEN`.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- Nguồn chuẩn: (a) `main` @ 67a092f của repo này · (b) chờ V1.0.1 vào repo khung gốc
- Nơi đặt code: (a) thêm `tools/` vào `product_paths` của repo này · (b) repo phát triển riêng
- Ma trận model: (a) duyệt `tier2` như đề xuất, `tier1` rỗng · (b) chờ OWNER chốt mã `T1`
- Phạm vi: (a) mở rộng dự án hiện tại · (b) đóng dự án, lập dự án mới
- Ngoại lệ vận hành: (a) cấp ngoại lệ, có nền tích hợp tạm · (b) không ngoại lệ. Yêu cầu tiếp theo của OWNER trong ngày thu hẹp (a): batch sau chờ merge, nền tạm chỉ dùng trong cùng batch
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
Chọn (a) ở cả năm điểm. Lượt merge PR của OWNER là chữ ký.

| # | Quyết định |
|:---:|---|
| 1 | Nguồn chuẩn của plan là `main` @ 67a092f (PR #27, đầu nhánh a63601f). Repo khung gốc `main` @ 1e1895f (1.0.0) chỉ là mốc đối chiếu; PR `upgrade/1.0.1` ở đó mở sau khi kiểm định đạt và không thuộc plan này |
| 2 | `harness.yaml`: thêm `tools/` vào `product_paths`. Code và test của hook, script nằm ở `tools/`, `tools/hooks/`, `tools/tests/`; đường dẫn `harness/tools/…` trong đặc tả đọc là `tools/…`. WORKER không ghi vào `harness/`. Thư viện được thêm: `jsonschema`, `ruamel.yaml`, ghi ở `tools/requirements.txt` |
| 3 | `04_control/MODEL_MATRIX.md` chuyển `APPROVED`, `tier1_approved_by: DEC-0016`, `tier1` rỗng, `tier2` giữ như đề xuất. Model có `group: unverified` không được giao vai WORKER hay REVIEWER: bỏ `gpt-6.1-terra` khỏi `order` của WORKER. Phân công CYC-03 tới CYC-07, theo lựa chọn của OWNER ngày 2026-11-14: W1 yêu cầu `gpt-5.6-luna`, W2 yêu cầu `gpt-6.1-sol`, W3 yêu cầu `gpt-5.6-luna`; dự phòng của mỗi chỗ là mã còn lại trong `order` của WORKER. Phân công W2, W3 là tạm thời. Hai tuyến `9router/antigravity` và `9router/grok` chưa được dùng cho vai nào: phiên Orca chỉ kiểm khả năng kết nối và báo mã model thực tế của hai tuyến; LEAD sau đó đề xuất một `DEC` bổ sung catalog và ma trận để OWNER duyệt. Không phiên nào được ghi nhãn Antigravity hay Grok khi tuyến và model thực tế chưa được xác nhận. Model thực tế của mọi phiên phải có trong catalog và hợp lệ theo `harness/MODEL_POLICY.md`, nếu không thì chỗ đó `BLOCKED`. REVIEWER yêu cầu `gemini-3.8-flash-n`, dự phòng `claude-sonnet-5-5`, và phải khác mã, khác nhóm với mọi WORKER của chu kỳ. Phiên `DISCUSS` vẫn chưa mở được |
| 4 | Dự án mở rộng: `BRIEF.md` thêm việc thử khung V1.0.1; `PLAN.md` lên version 4 với CYC-03 tới CYC-07; `PLAN_GO.md` được phát hành lại cho version 4, bản ngày 2026-11-12 còn trong lịch sử Git tại 67a092f. CYC-01, CYC-02 không đổi |
| 5 | Hai ngoại lệ, chi tiết ở `01_plan/SPEC_DRYRUN.md`: (E1) task của CYC-03 tới CYC-07 được tạo trong một PR, trái luật 25 của LEAD; (E2) trong cùng một batch, LEAD được dựng nền tích hợp tạm ở HEAD rời trong một worktree riêng để kiểm chung các PR chưa merge của batch đó; nền tạm không có nhánh, không đẩy lên máy chủ, không mở PR |

Không ngoại lệ nào khác. Batch sau chỉ bắt đầu khi OWNER đã squash-merge các PR cần thiết của batch trước và kiểm trên `main` đạt (luật 26 của LEAD, `harness/HARNESS.md#BATCH_RULES` quy tắc 6). Chu kỳ sau chỉ bắt đầu khi file cổng của chu kỳ trước đã ở `main`. Vẫn cấm merge, đẩy `main`, thẻ, bật auto-merge, xóa nhánh; `max_loops: 3`; tối đa 3 vòng kiểm định. Kết quả dựa vào PR chưa merge mang nhãn `PROVISIONAL`: không thay lượt merge của OWNER, không đổi `STATE.md`, sổ hay file cổng. E2 hết hiệu lực khi CYC-07 có file cổng hoặc sau ngày 2026-12-12, tùy điều nào tới trước.
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
- Dự án rời `CLOSE`, về `EXECUTE` với CYC-03. Việc đóng dự án (`CORE.md`, `CLOSED.md`) lùi sau CYC-07.
- Lớp bảo vệ `main` phía GitHub vẫn do OWNER dựng; plan chỉ kiểm chỉ đọc. RSK-0004 giữ `OPEN`. Tác tử không thử đẩy vào `main` hay thẻ để kiểm luật.
- RSK-0005 mở cho rủi ro kết quả `PROVISIONAL` bị hiểu là nghiệm thu hoặc lệch `main` thực tế.
- Cả ba chỗ WORKER dùng model nhóm `codex` cho tới khi có `DEC` bổ sung hai tuyến 9Router; khi đó phân công theo nhóm việc (tích hợp và tài liệu cho W2; ca biên, stress, bảo mật cho W3) mới áp được. Đổi model của một chỗ giữa chừng không cần sửa task, vì task chỉ ghi chỗ.
- `gpt-6.1-terra` và `claude-fable-5-2` còn `group: unverified`; muốn giao vai WORKER hay REVIEWER cần cập nhật catalog kèm một `DEC`.
- Dữ liệu thử của `scan` được dựng lúc chạy test; không có dữ liệu ngoài hay chuỗi dạng bí mật nào được lưu vào repo.
- Code ở `tools/` chưa phải là một phần của khung. Việc đưa sang `harness/tools/` và sang repo khung gốc cần PR `upgrade/` riêng.
- Còn chờ OWNER: mã `T1`; `DEC` bổ sung hai tuyến 9Router sau khi phiên Orca báo model thực tế; phương án RFC-0001; bật luật bảo vệ `main` và thẻ; tài khoản riêng cho tác tử; tự xóa nhánh nguồn; danh sách nhánh cũ được dọn; trường `requested_model`.
<!-- END: CONSEQUENCES -->
