---
schema: 1
id: DEC-0017
date: 2026-11-14
title: "Phân công model của CYC-03 tới CYC-07 theo luật khung 1.0.2: dữ kiện kiểm tuyến 9Router và giới hạn khi chọn"
proposed_by: LEAD
decided_by: OWNER
cycle: NONE
origin: "REQ-0004"
supersedes: ""
cancels: []
waives: []
affects: ["04_control/MODEL_CATALOG.md", "01_plan/SPEC_MODELS.md", "01_plan/SPEC_TOOLS.md", "01_plan/SPEC_ORCA_PROMPT.md", "01_plan/PLAN.md", DEC-0016, DEC-0018, RSK-0006]
keywords: [model-selection, 9router, route-check, reviewer-independence, quota]
---
## Status (newest first)
- 2026-11-14 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
DEC-0018 (khung 1.0.2) cho LEAD chọn model theo từng lần giao việc trong số model đã kiểm chạy được. LEAD kiểm tuyến ngày 2026-11-14 trên máy của OWNER, cổng `http://localhost:20128/v1`, từ 06:30Z tới 06:32Z: `GET /v1/models` (79 mục) và 23 tuyến, mỗi tuyến một lượt hỏi đáp ngắn. Từng dòng kiểm nằm ở `04_control/MODEL_CATALOG.md#ROUTE_CHECKS`. "Model thực tế" là trường `model` trong phản hồi của 9Router: lời báo của cổng, chưa phải chứng cứ độc lập về model phía sau.

- Trả lời được, model trả về trùng tên tuyến: `gpt-5.6-luna`, `gpt-6.1-sol`, `gpt-6.1-terra`, `gpt-5.6-sol`, `gpt-5.6-terra`, `claude-sonnet-4-6`, `claude-opus-4-6-thinking`, `grok-4.7`, `grok-4.6`.
- Trả lời được, model trả về khác tên tuyến: `ag/gemini-3.8-flash` và `ag/gemini-3.8-flash-high` trả `gemini-3.8-flash-n`; `xai/grok-4` trả `grok-4.3`; `xai/grok-code-fast-1` trả `grok-build-0.1`; combo `Hardeness` trả `gpt-5.6-luna[1m]`.
- Lỗi: `ag/claude-opus-5-5`, `ag/claude-sonnet-5-5` và biến thể `-high`; `ag/gemini-4-carbon`; `ag/gemini-3.1-pro-high`; ba tuyến `cu/claude-*`.
- Chưa kiểm: 56 tuyến còn lại; phiên tác tử có công cụ trên mọi tuyến; hạn mức của mọi tuyến.
- Model đã có phiên tác tử thật trong bản ghi của dự án: `gpt-5.6-luna`, `gpt-6.1-sol`, `gpt-6.1-terra` (run), `gemini-3.8-flash-n` (RVW-CYC-02), `claude-sonnet-5-5` (RVW-CYC-01, ngoài 9Router), `claude-fable-5-2` (DSC).
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- (a) Không gắn model cố định cho chỗ hay task; LEAD chọn mỗi lần giao theo DEC-0018, plan chỉ ghi loại việc và gợi ý.
- (b) Giữ bảng gắn cố định W1, W2, W3 với một model và danh sách dự phòng.
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
Chọn (a), theo yêu cầu của OWNER ngày 2026-11-14. Lượt merge PR của OWNER là chữ ký.

| # | Quyết định |
|:---:|---|
| 1 | `assignee` W1, W2, W3 trong task là chỗ chạy song song và loại việc, không phải model. Model của mỗi lần giao do LEAD chọn theo `harness/MODEL_POLICY.md` và `01_plan/SPEC_MODELS.md`; phần phân công tạm của DEC-0016 hết áp dụng |
| 2 | Catalog ghi tám model mới thấy ở lần kiểm với `availability: unconfirmed`. Chúng chỉ được giao vai có dùng công cụ sau khi LEAD kiểm bằng một phiên tác tử có công cụ và ghi dòng `ROUTE_CHECKS` loại `agent-tools` |
| 3 | Mỗi phiên gọi tuyến của một model cụ thể. Không giao việc qua combo `Hardeness`. Tuyến có tên khác model trả về vẫn dùng được; bản ghi và phép so luôn theo model thực tế |
| 4 | REVIEWER của một chu kỳ có model thực tế khác model thực tế của mọi run có sản phẩm trong chu kỳ đó; `gpt-5.6-luna` và `gpt-5.6-luna[1m]` là cùng model |
| 5 | Hạn mức chưa đọc được từ nguồn nào đã xác nhận: LEAD ghi `chưa xác minh` ở dòng phân công, và hỏi OWNER trước khi giao nếu một tuyến đã báo lỗi hạn mức trong phiên |
| 6 | Không có model phù hợp, không xác định được model thực tế, hoặc không có REVIEWER phù hợp: dừng theo điểm dừng 1 của `01_plan/SPEC_DRYRUN.md#STOPS` và báo OWNER |
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
- Quyết định này cần DEC-0018 ở `main` trước; PR chứa nó merge sau PR `upgrade/1.0.2`.
- `04_control/MODEL_MATRIX.md` không đổi so với `main` @ 67a092f; các khóa tier trong đó không có hiệu lực. Dòng phân công được thêm vào neo `ASSIGNMENTS` khi giao việc.
- OWNER không duyệt trước từng model. OWNER thấy lựa chọn của LEAD ở khối `CONFIRM` đầu phiên điều phối, ở báo cáo mỗi điểm dừng và ở PR đồng bộ.
- REVIEWER có thể cùng dòng model với WORKER; RSK-0006 theo dõi rủi ro này và rủi ro hạn mức chưa xác minh.
- `claude-sonnet-5-5` còn trong catalog nhưng tuyến 9Router của nó đang lỗi; chỉ dùng lại sau một lần kiểm đạt.
- OWNER có thể chỉ định hoặc cấm model cho một task, một chu kỳ bằng một `DEC`; LEAD chọn trong giới hạn đó.
<!-- END: CONSEQUENCES -->
