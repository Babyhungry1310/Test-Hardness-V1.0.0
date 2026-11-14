---
schema: 1
id: RSK-0005
opened: 2026-11-14
title: "Kết quả PROVISIONAL trên nền tích hợp tạm bị hiểu là nghiệm thu hoặc lệch với main thực tế"
related: [DEC-0016, RSK-0004]
keywords: [dry-run, provisional, integration-base, merge-order]
---
## Status (newest first)
- 2026-11-14 | OPEN | level: MEDIUM | due: 2026-12-12 | owner: LEAD
<!-- ANCHOR: IMPACT -->
## Impact
Theo DEC-0016 (E2), LEAD được kiểm chung các PR chưa merge của một batch trên một nền tích hợp tạm. Nếu OWNER merge theo thứ tự khác, sửa nội dung PR, hoặc bỏ một PR, `main` thực tế khác nền đã kiểm; khi đó kết quả đạt trên nền tạm không còn chứng minh gì cho `main`. Kết quả `PROVISIONAL` có thể bị đọc nhầm là batch đã đạt, kéo theo việc bắt đầu batch sau khi PR của batch trước chưa merge.
<!-- END: IMPACT -->
<!-- ANCHOR: RESPONSE -->
## Response
Mọi kết quả trên nền tạm mang nhãn `PROVISIONAL` kèm SHA nền, SHA từng PR và thứ tự gộp (`01_plan/SPEC_DRYRUN.md#PROVISIONAL`). Nền tạm không có nhánh, không đẩy, không mở PR. Phiên điều phối dừng sau mỗi batch; batch sau chỉ bắt đầu khi OWNER đã merge và xác nhận, và LEAD đã chạy lại kiểm tra ở `01_plan/SPEC_DRYRUN.md#RERUN` trên `main` thực tế. File cổng `CYC-nn_PASS.md` chỉ soạn từ kết quả trên `main`. Đóng rủi ro khi CYC-07 có file cổng.
<!-- END: RESPONSE -->
