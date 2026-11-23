---
schema: 1
id: DEC-0032
date: 2026-11-23
title: "Kaizen Dot1 P6d — E27–E43, Q-A…Q-I, supersedes thứ tự batch"
proposed_by: LEAD
decided_by: OWNER
cycle: CYC-08
origin: "DSC-20261123-gsd1"
supersedes: "B2a (P5); TK-0039.depends_on (P5); B3b (P5); B3e (P5)"
cancels: []
waives: []
affects: [DEC-0031, "06_sources/SRC-0003_kaizen-chi-tiet-dot1.md", "01_plan/PLAN.md#CYC_08"]
keywords: [kaizen, p6d, e27-e43, batch, verify]
---
## Status (newest first)
- 2026-11-23 | ACCEPTED
<!-- ANCHOR: CONTEXT -->
## Context
OWNER chấp nhận gói HANDOFF_P6D và chốt QUYET_DINH_OWNER_HANDOFF_P6D (2026-11-23). P6d là delta trên SRC-0003 P5 @ 7ad7aa6; origin thảo luận DSC-20261123-gsd1 (Q-A…Q-I và 4 SAI LỆCH).
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- Viết lại toàn bộ kế hoạch (P6c) hoặc delta trên P5: OWNER chọn delta P6d.
- B2a song song B1b hoặc chuỗi thẳng sau B1b3: OWNER chọn chuỗi thẳng (SAI LỆCH 1).
- TK-0054 làm Đợt 1 hoặc hoãn: OWNER hoãn Đợt 2 (SAI LỆCH 2).
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale

### 1. ACCEPTED (theo bảng delta)
- E33, E43 → TK-0059; E36, E37 → TK-0055; E39 → TK-0056; truy vết E27–E43 ghi trong SRC P6d qua TK-0053.
- **ACCEPTED — gán task khi viết thẻ đầu Bước:** E29, E38, E40 → Bước 3; E27, E28, E30, E31 → Bước 4 (đối chiếu bảng E27–E43 nháp P6 cũ).

### 2. DEFERRED Đợt 2
- Escalation ladder, node repair, package gate, W1–W4, script ghép log model, sửa relay ghi `model`.
- TK-0054 ruleset bằng JSON và script REST.
- Các mục đã hoãn ở nháp P6 (E32, E34, phần E33 checker PLAN_GO, …).

### 3. REJECTED
- `git.branching_strategy: none`
- `workflow.worktree_skip_hooks` (commit `--no-verify`)
- Task `checkpoint:human-verify` chen giữa lúc chạy
- PRUNE tự đóng task
- Verifier tự hoãn gap
- `ON_CRASH = allow` cho hook gác
- Bộ cài npm, `gsd-tools.cjs`, hook theo sự kiện riêng của Claude Code
- Hai bản luật độc lập

### 4. Đóng băng
- K1–K7, CS1–CS4 (TK-0038), nguyên tắc "mã đã có không đổi nghĩa" (Q-E, Q-A).
- Đổi các mục này cần DEC mới với SUPERSEDED.

### 5. Schema path `.github/`
- Schema path cho phép tiền tố `.github/`; quyền ghi vẫn theo WORKER.md luật 5 và O3.1 (Q-B).

### 6. V-RESP / SAME_MODEL
- V-RESP được chấp nhận làm bằng chứng SAME_MODEL trong CYC-08; review V1, V2 của P6c đạt V-RESP với `gpt-6-luna` (Q-G).

### 7. Kế hoạch cuốn chiếu
- Thẻ YAML Bước 3–5 viết ở đầu mỗi Bước, qua PR `lead/` riêng, sau khi có số đo L1.1 (Q-E).

### 8. Đổi thứ tự so với P5 (`supersedes`)
- B2a after B1b3; TK-0039 depends_on TK-0058; B3b after B3a2; B3e after B3d2.
- B3b/B3e theo **Q-OWNER-B3** (`QUYET_DINH_OWNER_HANDOFF_P6D` — Đồ thị Bước 3).
- Lý do: tuần tự hóa file chung (`00_tong_quan_upstream.md`), Bước 2 sau L1.1, TK-0055 trước TK-0045, baseline trước bật hook.

### 9. Marker AUTO
- Marker AUTO trong `04_control/STATE.md` và `state validate` gán vào thẻ Bước 3 (E29).
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
- SRC-0003 nâng P6d; kế hoạch hiện hành trỏ DEC-0032 ACCEPTED.
- Batch kế tiếp sau L1.1: B1b (TK-0053); không mở PR trước L1.1 (Q-H).
- Không sửa DEC-0031; E14/E15 và 5 quyết định chặn giữ nguyên.
<!-- END: CONSEQUENCES -->
