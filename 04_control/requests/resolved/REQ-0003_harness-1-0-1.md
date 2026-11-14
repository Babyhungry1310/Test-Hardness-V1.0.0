---
schema: 1
id: REQ-0003
date: 2026-11-14
title: "Nâng khung lên V1.0.1 theo tám nhóm yêu cầu"
proposed_by: OWNER
cycle: NONE
affects: ["harness/HARNESS.md", "harness/rules/LEAD.md", "harness/rules/WORKER.md", "harness/rules/REVIEWER.md", "harness/GIT_CONVENTIONS.md", "harness/tools/README.md", "harness/tools/PREFLIGHT.md", "AGENTS.md", "CLAUDE.md", "GEMINI.md", DEC-0011, DEC-0012, RSK-0004]
keywords: [harness-upgrade, main-protection, model-matrix, chat-ux, git-cleanup, scanner]
---
## Status (newest first)
- 2026-11-14 | RESOLVED_BY DEC-0015
- 2026-11-14 | PENDING
<!-- ANCHOR: CONTEXT -->
## Context
Sau khi CYC-02 đạt cổng PASS, OWNER yêu cầu cập nhật khung lên V1.0.1 theo tám nhóm: bảo vệ `main`; ma trận ưu tiên model; catalog model; trace log (giữ ba phương án mở); vertical-first cho chat; tách Chat UX và Storage; Git và cleanup; scanner dữ liệu ngoài. OWNER bổ sung hai điểm trong cùng phiên: quy tắc chia task song song (zero-overlap `write_scope`) kèm mẫu chia batch trong plan, và file mẫu `pytest.ini`. Phiên chỉ thiết kế và cập nhật khung: không lập plan thi công, không tạo task, không chạy loop. OWNER sẽ thử bản này trên repo thử rồi mới đưa sang repo khung gốc.
<!-- END: CONTEXT -->
<!-- ANCHOR: IMPACT -->
## Impact
Sửa file trong `harness/`, ba file định tuyến và `.github/` (vùng 🔒). Thêm hai file dữ liệu dự án `04_control/MODEL_CATALOG.md`, `04_control/MODEL_MATRIX.md`. Không sửa sản phẩm, task, run, bản ghi kiểm định, file cổng và bằng chứng của CYC-01, CYC-02. Không thay đổi verdict của CYC-02; bản kiểm định ở PR #20 vẫn không tính là một vòng theo DEC-0014. Không sửa DEC nào đang có; các điểm lệch với DEC-0012 được nêu ở DEC-0015 để OWNER quyết sau.
<!-- END: IMPACT -->
