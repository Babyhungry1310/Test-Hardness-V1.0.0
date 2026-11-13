---
schema: 1
id: RSK-0004
opened: 2026-11-13
title: "Tác tử có shell trên máy OWNER có thể tự đẩy thẻ git hoặc merge"
related: [DEC-0011, CYC-01]
keywords: [git-tag, credentials, owner-signature, agent-permissions]
---
## Status (newest first)
- 2026-11-13 | OPEN | level: HIGH | due: 2026-11-26 | owner: OWNER
<!-- ANCHOR: IMPACT -->
## Impact
Thẻ `cycle/CYC-nn` và lượt merge là chữ ký nghiệm thu của OWNER. Khi đặt thẻ `cycle/CYC-01`, phiên LEAD chạy Claude Code trên cloud bị chặn đẩy thẻ (HTTP 403) nên OWNER tự đặt. Việc chặn đó đến từ quyền của môi trường chạy, không đến từ khung. Tác tử chạy trên máy OWNER có quyền terminal (ví dụ Gemini trong Antigravity) kế thừa keyring và credentials của máy, nên có thể dùng `git` hoặc `gh` để đẩy thẻ hoặc merge. Khi đó chữ ký nghiệm thu mất tính toàn vẹn và không còn phân biệt được với thao tác của OWNER.
<!-- END: IMPACT -->
<!-- ANCHOR: RESPONSE -->
## Response
Quy trình: DEC-0011 cấm mọi tác tử tạo, sửa, xóa, đẩy thẻ git; chỉ OWNER đặt thẻ.
Kỹ thuật, do OWNER làm trên GitHub: đặt luật bảo vệ thẻ để chỉ tài khoản OWNER đẩy được `cycle/*`, chặn token của app và bot; bảo vệ nhánh `main` để chỉ OWNER merge.
Khung: bản khung sau đưa điều cấm này vào `harness/rules/` và thêm kiểm tra thẻ vào bộ C1–C14. Đóng rủi ro khi luật bảo vệ thẻ đã bật và bản khung mới đã vào repo này.
<!-- END: RESPONSE -->
