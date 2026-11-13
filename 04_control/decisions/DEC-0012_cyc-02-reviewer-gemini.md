---
schema: 1
id: DEC-0012
date: 2026-11-13
title: "Phân công model CYC-02: WORKER dùng Codex, REVIEWER dùng nhóm Gemini; không gắn cứng Claude"
proposed_by: OWNER
decided_by: OWNER
cycle: CYC-02
origin: "REQ-0002"
supersedes: "DEC-0009"
cancels: []
waives: []
affects: [TK-0003]
keywords: [model-assignment, worker, reviewer]
---
## Status (newest first)
- 2026-11-13 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
DEC-0009 giao REVIEWER của CYC-02 cho `claude-sonnet-5-5` chạy Claude Code trực tiếp, vì khi đó các tuyến Gemini văn bản và code chưa hoạt động. Ở CYC-02, tuyến Gemini đã chạy được: bằng chứng kiểm tra cấp task của TK-0003 R1 ghi `gemini-3.8-flash-n`. Run TK-0003 R1 ghi `model: gpt-5.6-luna`, thuộc nhóm Codex.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- Giữ REVIEWER là `claude-sonnet-5-5` theo DEC-0009
- Đổi REVIEWER của CYC-02 sang nhóm Gemini; không gắn cứng Claude cho các bước sau
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
OWNER chọn phương án sau: dự án không cần gắn cứng model Claude cho bước kiểm định và các bước tiếp theo.

| Vai | Model | Công cụ chạy |
|---|---|---|
| W1 | Nhóm Codex | Orca qua 9Router |
| REVIEWER của CYC-02 | Nhóm Gemini | 9Router hoặc công cụ hỗ trợ Gemini |

Điều kiện độc lập giữ nguyên: `reviewer_model` lấy từ nhật ký công cụ và phải khác mọi giá trị `model` của các run trong chu kỳ. Nhóm Gemini dùng để kiểm định không được có model dự phòng thuộc nhóm Codex.
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
OWNER mở phiên kiểm định CYC-02 bằng nhóm Gemini sau khi quyết định này vào `main`. Trước khi nhận một bản ghi `RVW-CYC-02`, LEAD đối chiếu `reviewer_model` với quyết định này và với `model` của mọi run trong CYC-02; không khớp thì đưa về OWNER. Các bước sau của dự án chọn model theo tuyến đang chạy được và điều kiện độc lập trên. DEC-0008 chỉ áp dụng cho CYC-01 và giữ nguyên.
<!-- END: CONSEQUENCES -->
