---
schema: 1
id: DEC-0029
date: 2026-11-19
title: "Hủy TK-0033 và tách detector session trong ngân sách dòng"
proposed_by: LEAD
decided_by: OWNER
cycle: CYC-03
origin: REQ-0012
supersedes: ""
cancels: [TK-0033]
waives: []
affects: [TK-0018, TK-0033, TK-0034, TK-0035, "01_plan/PLAN.md", "01_plan/ACCEPTANCE.md", "01_plan/SPEC_TOOLS.md", "04_control/STATE.md"]
keywords: [preflight, hooks, crlf, line-budget]
---
## Status (newest first)
- 2026-11-24 | RETIRED
- 2026-11-19 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
REQ-0012. DEC-0028 giao toàn bộ detector session cho TK-0033. Draft khoảng 620 dòng vượt chuẩn task; TK-0033 chưa có run hay PR. Nền ghi sổ là origin/main 276d99c0b21e33ac729695866350c6eaf78980c5.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- Giữ TK-0033 và tăng line_budget: bác bỏ.
- Chia hai task cùng batch: bác bỏ vì cùng write_scope và có phụ thuộc.
- Hủy TK-0033, tạo TK-0034 rồi TK-0035, mỗi task 300 dòng: OWNER chọn.
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
- Hủy TK-0033; không supersede DEC-0028 và không có PR để đóng. TK-0034 làm resolver/detector lõi; TK-0035 làm lỗi đọc, loại file, mã hóa và dạng đường dẫn.
- Khi `core.hooksPath` có giá trị, đọc bằng `git config --get core.hooksPath` và phân giải giá trị đó; `git rev-parse --git-path hooks` chỉ là fallback khi config vắng hoặc rỗng, không thay thế việc đọc config.
- TK-0034 tạo helper byte và JSON; TK-0035 dùng lại, không viết resolver thứ hai. Mutation và bằng chứng tách theo task. Hợp đồng hook, shebang, CRLF, exit, commit/push của DEC-0028 vẫn giữ.
- Gọi preflight liên tục trong phiên worker nằm ngoài quyết định này; cần DSC mới rồi DEC riêng nếu OWNER đổi vận hành.
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
- PLAN chuyển B2 thành TK-0027, TK-0032, TK-0034; B3 chỉ TK-0035; B4 là TK-0018. TK-0018 chờ B3 và baseline main đạt.
- B2 zero-overlap: TK-0027 chỉ test audit, TK-0032 hook/test merge, TK-0034 preflight/test/evidence. TK-0035 dùng lại file TK-0034 nên chỉ chạy sau merge TK-0034.
- Chỉ thi công sau OWNER merge governance này. LEAD cập nhật ACCEPTANCE, SPEC_TOOLS và STATE; commit, push, mở PR, merge vẫn cần quyền riêng.
<!-- END: CONSEQUENCES -->
