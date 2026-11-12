# POINTER TESTS

Tám câu hỏi về dự án ví dụ (công cụ ngân hàng câu hỏi). Mỗi câu trả lời được bằng con trỏ hoặc mã vết, không quá 2 file. "Số dòng" là số dòng công cụ `get` trả về theo `harness/schemas/POINTER_GRAMMAR.md` mục 4 (YAML không tính hai dòng `---`).

| # | Câu hỏi | Con trỏ hoặc mã vết | File | Số dòng | Trả lời |
|---|---|---|:---:|:---:|---|
| 1 | Vì sao chọn JSON thay cho CSV? | `DEC-0002#RATIONALE` | 1 | 2 | Giữ nguyên câu nhiều dòng, có kiểu rõ cho từng trường |
| 2 | Rủi ro nào đang mở? | Liệt kê `04_control/risks/` (không vào `closed/`) → `RSK-0002` | 1 | 7 | `RSK-0002`: ngân hàng thật có thể chứa tên học viên; `MEDIUM`, hạn 2026-11-20 |
| 3 | Buổi thảo luận còn đề xuất nào chưa chốt? | `DSC-20261102-q7k2` (mục Status và Events) | 1 | 9 | Không còn: `E1` đã thành `DEC-0002`, `E3` bị bác; còn câu hỏi mở `E5` |
| 4 | DEC nào thay DEC-0001? | `DEC-0001` (tìm thấy ở kho lạnh) | 1 | 14 | `DEC-0002` (dòng `SUPERSEDED_BY DEC-0002`) |
| 5 | TK-0002 bắt nguồn từ quyết định và buổi thảo luận nào? | `TK-0002` (`origin: DEC-0002`) → `DEC-0002` (`origin: DSC-20261102-q7k2#E1`) | 2 | 35 | `DEC-0002`, từ đề xuất `E1` của `DSC-20261102-q7k2` |
| 6 | TK-0001 trượt ở loop nào, vì sao? | `TK-0001.L01`…`TK-0001.L03` qua run `TK-0001_R1_BLOCKED` (`loops`, `escalation`) | 1 | 25 | `L01`–`L03` đều `FAIL`; task không nói id có phân biệt hoa thường nên thiếu `Q-001` |
| 7 | Vì sao TK-0001 được mở lại, theo quyết định nào? | `TK-0001` (`constraints` có `DEC-0004`) → `DEC-0004#RATIONALE` | 2 | 26 | `DEC-0004`: so sánh id không phân biệt hoa thường vì giáo viên gõ tay id |
| 8 | Plan dựa trên quyết định nào, chu kỳ 2 làm gì? | `PLAN` (`based_on`) và `01_plan/PLAN.md#CYC_02` | 1 | 7 | `DEC-0002`, `DEC-0003`; `CYC-02` có `TK-0003` xuất handout Markdown |

Cần sâu hơn câu 6: `TK-0001.L03` trong `logs/TK-0001/index.md` cho 1 dòng (`first_error: TK-0001.L03`); tra mã vết này trong `logs/TK-0001/trace.log` cho 7 dòng của loop 3, gồm `LOOP_CLOSED` và `ESCALATE`.
