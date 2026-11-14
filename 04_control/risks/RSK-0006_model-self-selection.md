---
schema: 1
id: RSK-0006
opened: 2026-11-14
title: "LEAD tự chọn model: REVIEWER cùng dòng với WORKER, model thực tế khác tên tuyến, hạn mức chưa xác minh"
related: [DEC-0017, DEC-0018, RSK-0005]
keywords: [model-selection, reviewer-independence, route-check, quota]
---
## Status (newest first)
- 2026-11-14 | OPEN | level: MEDIUM | due: 2026-12-12 | owner: LEAD
<!-- ANCHOR: IMPACT -->
## Impact
Theo DEC-0018, OWNER không duyệt trước từng model và REVIEWER chỉ cần khác mã model thực tế với WORKER. Ba điều có thể làm kết quả kiểm định yếu đi: REVIEWER cùng dòng, cùng nhà cung cấp với WORKER nên dễ có cùng thiên lệch; cổng 9Router trả về model khác tên tuyến (đã thấy ngày 2026-11-14), nên một phiên có thể chạy bằng model LEAD không định chọn; hạn mức chưa đọc được từ nguồn đã xác nhận, nên một tuyến có thể hết hạn mức giữa batch. "Model thực tế" hiện là lời báo của cổng, chưa có nguồn đối chiếu độc lập.
<!-- END: IMPACT -->
<!-- ANCHOR: RESPONSE -->
## Response
Mọi phép so và bản ghi dùng model thực tế hệ thống trả về (`harness/MODEL_POLICY.md#SAME_MODEL`); không xác định được thì dừng. LEAD kiểm REVIEWER ba lần: khi chọn, khi REVIEWER bắt đầu, khi review PR `RVW`. LEAD nêu trong báo cáo mỗi điểm dừng: model yêu cầu, model thực tế, tuyến, và mọi lần REVIEWER cùng `group` với WORKER. Hạn mức ghi `chưa xác minh` tới khi `harness/tools/INTEGRATION.md#FEATURES` dòng 9 được OWNER xác nhận. TK-0010 và TK-0019 đưa các phép kiểm này vào script. OWNER siết bằng một `DEC` nếu muốn buộc khác nhóm cho một phạm vi. Đóng rủi ro khi CYC-07 có file cổng và không bản kiểm định nào bị loại vì model.
<!-- END: RESPONSE -->
