---
schema: 1
id: CYC-nn_PASS
cycle: CYC-nn
date: YYYY-MM-DD
---
<!-- ANCHOR: ACCEPTANCE -->
## Acceptance
| task | outcome | run | done | loops | review | deviations |
|---|---|---|---|---|---|---|
| TK-nnnn | DONE | R1 | 0/0 | 1 · last PASS | PASS | 0 |
<!-- END: ACCEPTANCE -->
<!-- ANCHOR: QUESTIONS -->
## Questions
| # | Câu hỏi | Kết quả | Bằng chứng |
|---|---|---|---|
| 1 | Mọi task đã DONE hoặc CANCELLED có DEC chưa? | PASS | TK-nnnn |
| 2 | RVW của người kiểm định độc lập, dùng model khác người làm, có verdict: PASS chưa? | PASS | RVW-CYC-nn |
| 3 | Sản phẩm có đạt đúng "xong" đã thống nhất không? | PASS | RVW-CYC-nn |
| 4 | Có sai biệt nào so với điều đã chốt mà OWNER cần biết không? | PASS | DEC-nnnn |
| 5 | Rủi ro nào chuyển sang chu kỳ sau? | PASS | RSK-nnnn |
| 6 | OWNER đã tự xem sản phẩm chưa? | PASS | 03_output/CYC-nn/checks |
| 7 | Mọi thay đổi vào nhánh chính đều do OWNER merge chứ? | PASS | TK-nnnn |
| 8 | Một model mới, chỉ đọc rules/LEAD.md và STATE.md, có trả lời đúng 5 câu không? | PASS | 04_control/STATE.md |
<!-- END: QUESTIONS -->
