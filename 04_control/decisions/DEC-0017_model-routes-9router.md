---
schema: 1
id: DEC-0017
date: 2026-11-14
title: "Bổ sung catalog và ma trận model theo kết quả kiểm tuyến 9Router; phân công CYC-03 tới CYC-07 theo thế mạnh"
proposed_by: LEAD
decided_by: OWNER
cycle: NONE
origin: "REQ-0004"
supersedes: ""
cancels: []
waives: []
affects: ["04_control/MODEL_CATALOG.md", "04_control/MODEL_MATRIX.md", "01_plan/SPEC_MODELS.md", "01_plan/SPEC_TOOLS.md", "01_plan/SPEC_ORCA_PROMPT.md", "01_plan/PLAN.md", DEC-0016]
keywords: [model-catalog, model-matrix, 9router, route-probe, reviewer-independence, fallback]
---
## Status (newest first)
- 2026-11-14 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
OWNER yêu cầu tận dụng các model đã có qua 9Router cho 21 task (Claude Opus, Claude Sonnet, Grok, GPT), giữ REVIEWER độc lập và hai điểm dừng. LEAD kiểm tuyến ngày 2026-11-14 trên máy của OWNER, cổng `http://localhost:20128/v1`, từ 06:30:21Z tới 06:32:26Z: `GET /v1/models` (79 mục) và mỗi tuyến dưới đây một lượt `POST /v1/chat/completions` không luồng, 16 token. "Model thực tế" là trường `model` trong phản hồi của 9Router; đó là lời báo của cổng, chưa phải chứng cứ độc lập về model phía sau, và chưa chứng minh tuyến chạy được phiên tác tử có công cụ.

| Tuyến yêu cầu | Mã HTTP | Model thực tế trả về |
|---|:---:|---|
| `cx/gpt-5.6-luna` | 200 | `gpt-5.6-luna` |
| `cx/gpt-6.1-sol` | 200 | `gpt-6.1-sol` |
| `cx/gpt-6.1-terra` | 200 | `gpt-6.1-terra` |
| `cx/gpt-5.6-sol` | 200 | `gpt-5.6-sol` |
| `cx/gpt-5.6-terra` | 200 | `gpt-5.6-terra` |
| `ag/claude-sonnet-4-6` | 200 | `claude-sonnet-4-6` |
| `ag/claude-opus-4-6-thinking` | 200 | `claude-opus-4-6-thinking` |
| `ag/gemini-3.8-flash`, `ag/gemini-3.8-flash-high` | 200 | `gemini-3.8-flash-n` |
| `xai/grok-4.7` | 200 | `grok-4.7` |
| `xai/grok-4.6` | 200 | `grok-4.6` |
| `xai/grok-4` | 200 | `grok-4.3` (khác tên tuyến) |
| `xai/grok-code-fast-1` | 200 | `grok-build-0.1` (khác tên tuyến) |
| `Hardeness` (combo) | 200 | `gpt-5.6-luna[1m]` (không phải mã trong catalog) |
| `ag/claude-opus-5-5`, `ag/claude-opus-5-5-high`, `ag/claude-sonnet-5-5`, `ag/claude-sonnet-5-5-high` | 503 | Không có; lỗi 404 từ phía trên |
| `ag/gemini-4-carbon`, `ag/gemini-3.1-pro-high` | 503 | Không có; lỗi 404 từ phía trên |
| `cu/claude-4.6-opus-max`, `cu/claude-4.5-opus`, `cu/claude-4.5-sonnet` | 400 | Không có; lượt trả lời rỗng |

Các tuyến khác trong danh sách 79 mục chưa được kiểm. Trước quyết định này catalog có 7 mã, không có mã Opus hay Grok nào; `claude-sonnet-5-5` có trong catalog nhưng tuyến 9Router của nó đang lỗi (bằng chứng cũ của nó là phiên Claude Code trực tiếp, DEC-0008).
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- (a) Thêm bốn mã đã trả lời được và có vai rõ: `claude-sonnet-4-6`, `claude-opus-4-6-thinking`, `grok-4.7`, `grok-4.6`.
- (b) Thêm mọi mã trả lời được, gồm cả `gpt-5.6-sol`, `gpt-5.6-terra`, `grok-4.3`, `grok-build-0.1`.
- (c) Không thêm; giữ phân công tạm của DEC-0016 (ba chỗ đều nhóm `codex`).
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
Chọn (a). Lượt merge PR của OWNER là chữ ký. Không thêm mã chưa có vai, và không thêm mã mà tên tuyến khác model trả về.

| # | Quyết định |
|:---:|---|
| 1 | Catalog thêm bốn mã, `availability: confirmed` với bằng chứng là bảng ở mục Context; `capability_source: none`. Nhóm do quyết định này ấn định: `claude-sonnet-4-6` và `claude-opus-4-6-thinking` thuộc nhóm `claude`; `grok-4.7` và `grok-4.6` thuộc nhóm `grok`. Ghi tên tuyến vào `aliases` của các mã đã kiểm |
| 2 | Ma trận: `tier2` thêm bốn mã trên; `tier1` vẫn rỗng. WORKER `order`: `gpt-5.6-luna`, `gpt-6.1-sol`, `claude-sonnet-4-6`, `grok-4.7`, `grok-4.6`. REVIEWER `order`: `gemini-3.8-flash-n`, `claude-opus-4-6-thinking`, `claude-sonnet-5-5`. PLANNING `fallback`: `claude-opus-4-6-thinking`, `claude-sonnet-5-5` |
| 3 | Phân công CYC-03 tới CYC-07 thay phần phân công tạm của DEC-0016 (quyết định 3): W1 `gpt-5.6-luna`, dự phòng `gpt-6.1-sol`; W2 `claude-sonnet-4-6`, dự phòng `gpt-6.1-sol`; W3 `grok-4.7`, dự phòng `grok-4.6` rồi `gpt-5.6-luna`. REVIEWER `gemini-3.8-flash-n`; dự phòng `claude-opus-4-6-thinking` chỉ trong chu kỳ không có run nào dùng model nhóm `claude`. Chi tiết theo task ở `01_plan/SPEC_MODELS.md` |
| 4 | Opus không làm WORKER trong plan này: dùng làm REVIEWER dự phòng và PLANNING dự phòng (phản biện đặc tả). Việc xếp `T1` vẫn chờ OWNER |
| 5 | Mọi phiên gọi đúng tên tuyến ở `aliases`, không gọi combo `Hardeness` và không gọi tuyến có tên khác model trả về. Model thực tế luôn lấy từ phản hồi của công cụ, không lấy từ tên tuyến |
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
- Bốn mã mới chỉ được dùng sau khi PR chứa quyết định này được OWNER merge. Trước đó phân công tạm của DEC-0016 có hiệu lực.
- Chu kỳ có W2 chạy bằng `claude-sonnet-4-6` thì REVIEWER chỉ còn một mã hợp lệ là `gemini-3.8-flash-n`; tuyến đó lỗi thì phần kiểm định `BLOCKED`.
- `claude-sonnet-5-5` giữ nguyên trong catalog; hiện chỉ chạy được ngoài 9Router. Dùng nó làm REVIEWER cần cùng điều kiện về nhóm như Opus.
- Phiên Orca kiểm lại từng tuyến lúc bắt đầu; tuyến lỗi hoặc trả về mã khác danh sách được phép thì chuyển sang dự phòng theo thứ tự, hết thì `BLOCKED`.
- Chưa kiểm: phiên tác tử có công cụ trên từng tuyến; hạn mức; các tuyến còn lại. Kết quả kiểm có thể đổi theo thời gian; mục catalog ghi ngày kiểm.
- Còn chờ OWNER: mã `T1`; có thêm `gpt-5.6-sol`, `gpt-5.6-terra` hay một mã Gemini thứ hai làm REVIEWER dự phòng hay không.
<!-- END: CONSEQUENCES -->
