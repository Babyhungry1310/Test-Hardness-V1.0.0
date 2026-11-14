---
schema: 1
id: REQ-0004
date: 2026-11-14
title: "Lập plan triển khai và kiểm định khung V1.0.1 trên repo thử"
proposed_by: OWNER
cycle: NONE
affects: ["00_brief/BRIEF.md", "harness.yaml", "01_plan/PLAN.md", "01_plan/ACCEPTANCE.md", "04_control/MODEL_MATRIX.md", "04_control/gates/PLAN_GO.md", DEC-0015, RSK-0004]
keywords: [harness-upgrade, plan, dry-run, main-protection, scanner, model-matrix]
---
## Status (newest first)
- 2026-11-14 | RESOLVED_BY DEC-0016
- 2026-11-14 | PENDING
<!-- ANCHOR: CONTEXT -->
## Context
OWNER yêu cầu lập plan triển khai và kiểm định đủ tám nhóm cập nhật của khung V1.0.1 cùng hai điểm bổ sung (chia batch zero-overlap, mẫu `pytest.ini`), soạn cổng `PLAN_GO`, và một prompt bàn giao để một phiên Orca điều phối các task theo batch, dừng sau mỗi batch chờ OWNER squash-merge và dừng khi một task `BLOCKED`. Phân công tham khảo theo ba nhóm `9router/codex`, `9router/antigravity`, `9router/grok`. Đề bài coi repo khung gốc là nguồn V1.0.1. Đối chiếu ngày 2026-11-14: repo khung gốc `main` @ 1e1895f còn `harness/VERSION` 1.0.0, không có nhánh hay PR `upgrade/1.0.1`; V1.0.1 chỉ có ở repo này, PR #27 (đầu nhánh a63601f) do OWNER merge thành `main` @ 67a092f. OWNER đã trả lời năm câu hỏi của LEAD trong phiên: 1a, 2a, 3a, 4a, 5a.
<!-- END: CONTEXT -->
<!-- ANCHOR: IMPACT -->
## Impact
Mở rộng phạm vi dự án ngoài `BRIEF.md` hiện có; dự án rời phase `CLOSE` để thi công CYC-03 tới CYC-07. Sửa file 🔒: `00_brief/BRIEF.md`, `harness.yaml`, `01_plan/`, `04_control/MODEL_MATRIX.md`; phát hành lại file ✍ `04_control/gates/PLAN_GO.md`. Không sửa `harness/`, sản phẩm, task, run, bản ghi kiểm định, file cổng và bằng chứng của CYC-01, CYC-02. Cần ngoại lệ đối với luật 25 của LEAD để tạo task của năm chu kỳ trong một PR, và cho phép nền tích hợp tạm trong cùng một batch.
<!-- END: IMPACT -->
