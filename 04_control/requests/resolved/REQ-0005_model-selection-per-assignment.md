---
schema: 1
id: REQ-0005
date: 2026-11-14
title: "Đổi quy định phân công model: LEAD chọn theo từng lần giao, REVIEWER khác model thực tế với WORKER"
proposed_by: OWNER
cycle: NONE
affects: ["harness/MODEL_POLICY.md", "harness/HARNESS.md", "harness/rules/LEAD.md", "harness/rules/REVIEWER.md", "harness/tools/PREFLIGHT.md", "harness/tools/INTEGRATION.md", "harness/VERSION", DEC-0015]
keywords: [model-policy, model-selection, reviewer-independence, route-check, harness-upgrade]
---
## Status (newest first)
- 2026-11-14 | RESOLVED_BY DEC-0018
- 2026-11-14 | PENDING
<!-- ANCHOR: CONTEXT -->
## Context
OWNER yêu cầu quy định mới: "Mỗi lần giao task, LEAD chọn bất kỳ model nào đã kiểm tra chạy được qua 9Router, dựa trên yêu cầu công việc và hạn mức. REVIEWER phải dùng model khác các WORKER đã thực hiện phần việc được kiểm định. Nếu không có model phù hợp, dừng và báo OWNER." Mục tiêu là để LEAD chạy dry run hơn 20 task và tự cập nhật phân công. Khung 1.0.1 (DEC-0015) quy định ngược lại ở ba điểm: quyền dùng model theo tier và thứ tự do OWNER duyệt bằng `DEC`; REVIEWER khác mã và khác nhóm với mọi WORKER của chu kỳ; model mới chỉ dùng sau khi PR catalog được merge. OWNER đã trả lời năm câu hỏi của LEAD ngày 2026-11-14: 1b, 2a, 3a, 4a, 5a.
<!-- END: CONTEXT -->
<!-- ANCHOR: IMPACT -->
## Impact
Sửa luật khung trong `harness/` và giữ `harness/VERSION` là 1.0.1 theo yêu cầu OWNER qua nhánh `upgrade/1.0.2`. Không đổi schema; bản ghi cũ vẫn hợp lệ. Không sửa `harness.yaml`, sản phẩm, plan, task hay bản ghi của các chu kỳ. PR #28 (plan version 4) phải được sửa cho khớp và merge sau PR này. Các quyết định phân công cũ (DEC-0007, DEC-0012, DEC-0014) giữ nguyên cho các chu kỳ đã xong.
<!-- END: IMPACT -->
