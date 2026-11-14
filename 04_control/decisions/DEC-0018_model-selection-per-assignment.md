---
schema: 1
id: DEC-0018
date: 2026-11-14
title: "Khung 1.0.2: LEAD chọn model theo từng lần giao việc; REVIEWER khác model thực tế với WORKER của phần được kiểm"
proposed_by: LEAD
decided_by: OWNER
cycle: NONE
origin: "REQ-0005"
supersedes: ""
cancels: []
waives: []
affects: ["harness/MODEL_POLICY.md", "harness/HARNESS.md", "harness/rules/LEAD.md", "harness/rules/REVIEWER.md", "harness/tools/PREFLIGHT.md", "harness/tools/INTEGRATION.md", "harness/templates/model_catalog.md", "harness/templates/model_matrix.md", "harness/VERSION", "04_control/MODEL_CATALOG.md", "04_control/MODEL_MATRIX.md", DEC-0015]
keywords: [model-policy, model-selection, reviewer-independence, route-check, same-model, harness-upgrade]
---
## Status (newest first)
- 2026-11-14 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
REQ-0005. Lần kiểm tuyến 9Router ngày 2026-11-14 cho thấy: nhiều model chạy được nhưng chưa có trong catalog; tên tuyến có khi khác model trả về (`xai/grok-4` trả `grok-4.3`; một combo trả `gpt-5.6-luna[1m]`); một số tuyến có trong danh sách nhưng lỗi. Chính sách tier của bản 1.0.1 buộc mỗi model mới phải qua một `DEC` và một PR trước khi dùng, và buộc REVIEWER khác nhóm với mọi WORKER của chu kỳ.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- Phạm vi: (a) chỉ WORKER và REVIEWER · (b) mọi vai, bỏ tier và thứ tự cố định. OWNER chọn (b).
- "Model khác" của REVIEWER: (a) khác mã model thực tế, biến thể cùng mã gốc coi là cùng · (b) khác mã và khác nhóm. OWNER chọn (a).
- Xác lập "đã kiểm chạy được": (a) LEAD tự kiểm và ghi bằng chứng · (b) qua PR catalog trước khi dùng. OWNER chọn (a), kèm điều kiện vai cần công cụ phải kiểm bằng phiên tác tử có công cụ.
- Nơi đặt quy định: (a) sửa khung qua PR `upgrade/` · (b) một `DEC` của dự án ghi đè. OWNER chọn (a).
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
Lượt merge PR của OWNER là chữ ký. LEAD soạn câu chữ của luật; năm điểm dưới là nội dung OWNER đã chọn.

| # | Quyết định | Nằm ở |
|:---:|---|---|
| 1 | Mỗi lần giao việc, LEAD chọn một model đã kiểm chạy được, theo yêu cầu công việc, khả năng thực tế và hạn mức. Áp cho mọi vai. Tier, thứ tự chọn và fallback cố định không còn hiệu lực | `harness/MODEL_POLICY.md` mục 2, 3; `harness/HARNESS.md` mục 3.5; `harness/rules/LEAD.md` luật 17, 30 |
| 2 | REVIEWER khác mã model thực tế với các WORKER đã làm phần được kiểm định; không bắt buộc khác nhóm. Biến thể của cùng model gốc (ví dụ `gpt-5.6-luna` và `gpt-5.6-luna[1m]`) là cùng model. So trên model thực tế nhận được, không trên tên tuyến | `harness/MODEL_POLICY.md` mục 4; `harness/rules/REVIEWER.md` luật 2; `harness/tools/PREFLIGHT.md` dòng 13 |
| 3 | LEAD tự kiểm tuyến và ghi dòng `ROUTE_CHECKS` trong catalog; không cần PR hay `DEC` trước từng model. Vai cần dùng công cụ phải có lần kiểm bằng phiên tác tử có công cụ. Ghi cả model yêu cầu và model thực tế | `harness/MODEL_POLICY.md` mục 1, 2, 5; mẫu catalog và mẫu ma trận |
| 4 | Không có model phù hợp, không xác định được model thực tế, hoặc không có REVIEWER phù hợp: dừng và báo OWNER. Hạn mức hay model thực tế chưa xác minh được thì ghi `chưa xác minh`, và báo OWNER khi điều đó ảnh hưởng việc giao | `harness/MODEL_POLICY.md` mục 3, 6 |
| 5 | Một PR `upgrade/` được mở cùng lúc với một PR `lead/` khi cùng phiên LEAD soạn, không chạm chung file, mã bản ghi không đụng nhau và cả hai PR ghi thứ tự merge | `harness/tools/PREFLIGHT.md` dòng 15 |

Không đổi schema: các khóa tier của ma trận giữ lại nhưng không có hiệu lực; `availability: confirmed` nay nghĩa là đã có phiên tác tử có công cụ. Số phiên bản 1.0.2 theo cách OWNER đã đặt cho bản 1.0.1; theo bảng ở `harness/HARNESS.md` mục 11 thay đổi này ở mức MINOR.
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
- DEC-0015 không bị sửa; phần chính sách tier và tính độc lập theo nhóm mà nó đưa vào khung được thay bằng quyết định này. Bảy nhóm còn lại của DEC-0015 không đổi.
- DEC-0007, DEC-0012, DEC-0014 không đổi; kết quả và vòng kiểm định của CYC-01, CYC-02 không bị xét lại theo luật mới.
- REVIEWER nay có thể cùng nhà cung cấp, cùng dòng với WORKER. Rủi ro thiên lệch cùng dòng model tăng; LEAD nêu điều này khi chọn và OWNER có thể siết bằng một `DEC` cho từng phạm vi.
- OWNER không còn duyệt trước từng model. Thứ OWNER thấy là dòng kiểm tuyến, dòng phân công và báo cáo của LEAD ở mỗi điểm dừng; hai file model vẫn vào `main` qua PR do OWNER merge.
- `04_control/MODEL_CATALOG.md` và `04_control/MODEL_MATRIX.md` của dự án được cập nhật trong PR #28, không trong PR này. Phiên `DISCUSS` không còn bị chặn vì `tier1` rỗng.
- Thứ tự merge: PR `upgrade/1.0.2` trước; sau đó LEAD đưa `main` vào nhánh của PR #28 bằng `git merge` (không rebase, không ép đẩy), kiểm lại, rồi OWNER merge PR #28. `04_control/STATE.md` được cập nhật ở PR #28 để hai PR không chạm chung file.
- Chưa có nguồn đọc hạn mức được xác nhận; chưa có script nào thi hành các kiểm tra này. Việc đưa bản 1.0.2 sang repo khung gốc cần PR riêng.
<!-- END: CONSEQUENCES -->
