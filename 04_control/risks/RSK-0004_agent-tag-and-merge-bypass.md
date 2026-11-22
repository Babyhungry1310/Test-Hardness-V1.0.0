---
schema: 1
id: RSK-0004
opened: 2026-11-13
title: "Tác tử có shell trên máy OWNER có thể tự đẩy thẻ git hoặc merge"
related: [DEC-0011, CYC-01]
keywords: [git-tag, credentials, owner-signature, agent-permissions]
---
## Status (newest first)
- 2026-11-22 | OPEN | level: HIGH | due: 2026-11-26 | owner: OWNER | E14=tách; agent GitHub `conchonomoconmeo-AIAIAI`; OWNER `Babyhungry1310`; chờ xác nhận ruleset/luật thẻ/bypass và quyền collaborator (O1.1–O1.3)
- 2026-11-14 | OPEN | level: HIGH | due: 2026-11-26 | owner: OWNER
- 2026-11-13 | OPEN | level: HIGH | due: 2026-11-26 | owner: OWNER
<!-- ANCHOR: IMPACT -->
## Impact
Thẻ `cycle/CYC-nn` và lượt merge là chữ ký nghiệm thu của OWNER. Khi đặt thẻ `cycle/CYC-01`, phiên LEAD chạy Claude Code trên cloud bị chặn đẩy thẻ (HTTP 403) nên OWNER tự đặt. Việc chặn đó đến từ quyền của môi trường chạy, không đến từ khung. Tác tử chạy trên máy OWNER có quyền terminal (ví dụ Gemini trong Antigravity) kế thừa keyring và credentials của máy, nên có thể dùng `git` hoặc `gh` để đẩy thẻ hoặc merge. Khi đó chữ ký nghiệm thu mất tính toàn vẹn và không còn phân biệt được với thao tác của OWNER. Sau DEC-0031 (E14=tách), danh tính GitHub của tác tử và OWNER khác nhau, nhưng rủi ro shell/keyring trên máy OWNER và quyền collaborator thực tế của tài khoản agent vẫn còn tới khi O1.1–O1.3 xong.
<!-- END: IMPACT -->
<!-- ANCHOR: RESPONSE -->
## Response
Quy trình: DEC-0011 cấm mọi tác tử tạo, sửa, xóa, đẩy thẻ git; chỉ OWNER đặt thẻ.
Kỹ thuật, do OWNER làm trên GitHub: bảo vệ `main` và thẻ `cycle/*`, chặn đẩy trái phép; với E14=tách đặt bypass ruleset/luật thẻ chỉ cho OWNER (`Babyhungry1310`), không cho tài khoản agent (`conchonomoconmeo-AIAIAI`); O1.3 kiểm quyền collaborator/token của tài khoản agent, không tạo tài khoản mới.
Khung: bản khung sau đưa điều cấm này vào `harness/rules/` và thêm kiểm tra thẻ vào bộ C1–C14. Chỉ đóng rủi ro khi OWNER xác nhận ruleset, luật thẻ và quyền thực tế đã phân biệt; chỉ có quyết định E14=tách trên giấy chưa đủ.
<!-- END: RESPONSE -->
