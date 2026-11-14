# SPEC_MODELS — CHỌN MODEL CHO CYC-03 TỚI CYC-07

Nguồn: DEC-0017, DEC-0018, `harness/MODEL_POLICY.md` (bản 1.0.2). Dữ kiện khi chạy lấy từ `04_control/MODEL_CATALOG.md` (mục model và neo `ROUTE_CHECKS`) và `04_control/MODEL_MATRIX.md#ASSIGNMENTS` trên `origin/main`, cộng các dòng kiểm LEAD ghi trong phiên. File này không gắn model cố định cho chỗ hay task.

<!-- ANCHOR: SLOTS -->
## 1. Chỗ và loại việc
- W1, W2, W3 ở trường `assignee` của task là chỗ chạy song song. Mỗi chỗ một task tại một thời điểm.
- W1: logic, thuật toán, công cụ, unit test. Task: TK-0006, TK-0009, TK-0010, TK-0011, TK-0013, TK-0014, TK-0015.
- W2: triển khai, tích hợp, tài liệu. Task: TK-0007, TK-0012, TK-0016, TK-0021, TK-0022, TK-0025, TK-0026, TK-0027, TK-0028, TK-0029.
- W3: ca biên, stress, bảo mật, phản biện. Task: TK-0008, TK-0017, TK-0018, TK-0019, TK-0020, TK-0023, TK-0024.
- REVIEWER: kiểm định từng chu kỳ và hồi quy toàn bộ sau CYC-07. LEAD: điều phối, phản biện đặc tả.
<!-- END: SLOTS -->

<!-- ANCHOR: RULES -->
## 2. Quy tắc chọn
- Mỗi lần giao một task hay một lượt kiểm định, LEAD chọn một model thỏa `harness/MODEL_POLICY.md#ELIGIBILITY`, theo yêu cầu của việc, khả năng thực tế đã thấy trong bản ghi, và hạn mức. Không có thứ tự hay dự phòng cố định.
- Mọi vai ở đây đều dùng công cụ: model chỉ được giao khi đã có dòng `ROUTE_CHECKS` loại `agent-tools` đạt cho đúng tuyến sẽ gọi, hoặc mục catalog đã `availability: confirmed` và dòng kiểm mới nhất của tuyến không lỗi. Hỏi đáp ngắn chưa đủ.
- Đầu phiên điều phối, LEAD kiểm lại các tuyến định dùng và ghi dòng `ROUTE_CHECKS`: tuyến đã gọi, chuỗi model hệ thống trả về, loại kiểm, kết quả, nguồn, thời điểm.
- Trước khi phiên bắt đầu, LEAD ghi dòng phân công: model yêu cầu, tuyến, lý do chọn, hạn mức (số liệu hoặc `chưa xác minh`). Cuối phiên ghi model thực tế và `match`.
- Hạn mức hoặc khả năng thực tế chưa xác minh: ghi `chưa xác minh`, không ước đoán. Nếu điều đó ảnh hưởng tới việc chọn (ví dụ tuyến vừa báo lỗi hạn mức, hoặc chỉ còn một model cho REVIEWER): hỏi OWNER trước khi giao.
- Gọi tuyến của một model cụ thể; không giao việc qua combo. So sánh và ghi theo model thực tế, không theo tên tuyến, tên agent hay model yêu cầu.
- `aliases` có thể chứa ID tuyến; tuyến chỉ là đầu vào API, không chứng minh định danh model. `actual` phải lấy từ công cụ hoặc phản hồi; giữ nguyên cả dấu `/` nếu hệ thống trả về và đối chiếu bằng chứng.
- ID gửi 9Router phải khớp danh sách `/v1/models` hoặc là alias đã kiểm được chấp nhận. Tuyến được liệt kê chưa chứng minh gọi thành công hoặc hỗ trợ công cụ; code lịch sử không có tuyến đã xác minh không được tự gán tuyến thay thế.
- Model thực tế khác model yêu cầu: nếu vẫn đủ điều kiện (và với REVIEWER vẫn thỏa mục 4) thì tiếp tục, ghi `match: no`; không thì dừng phiên đó, không dùng kết quả.
- Phiên lỗi vì model hoặc tuyến: LEAD được chọn model đủ điều kiện khác cho loop kế. Đổi model không cấp thêm loop: mỗi task vẫn tối đa 3 loop, tính cả loop đầu.
<!-- END: RULES -->

<!-- ANCHOR: HINTS -->
## 3. Gợi ý theo loại việc (không ràng buộc)
- Dòng GPT qua tuyến `cx/`: logic, thuật toán, công cụ, unit test. `gpt-5.6-luna`, `gpt-6.1-sol`, `gpt-6.1-terra` đã có run thật trong dự án.
- Claude Sonnet (`claude-sonnet-4-6`): triển khai, tích hợp, tài liệu; kiểm định khi thỏa mục 4.
- Claude Opus (`claude-opus-4-6-thinking`): phản biện đặc tả, kiểm định khi thỏa mục 4.
- Grok (`grok-4.7`, `grok-4.6`): ca biên, stress, phản biện bảo mật.
- Gemini (`gemini-3.8-flash-n`): kiểm định; đã có bản kiểm định thật ở CYC-02.
- Các model Claude, Grok và hai mã `gpt-5.6-sol`, `gpt-5.6-terra` mới qua hỏi đáp ngắn ngày 2026-11-14: cần kiểm bằng phiên tác tử có công cụ trước lần giao đầu tiên. Không ép dùng đủ mọi model.
<!-- END: HINTS -->

<!-- ANCHOR: REVIEW -->
## 4. REVIEWER
- Model thực tế của REVIEWER khác, theo `harness/MODEL_POLICY.md#SAME_MODEL`, với model thực tế của mọi run có sản phẩm trong chu kỳ được kiểm, kể cả run chạy lại bằng model khác. Không bắt buộc khác nhóm hay nhà cung cấp.
- Biến thể cùng mã gốc là cùng model: `gpt-5.6-luna` và `gpt-5.6-luna[1m]`. Khác mã gốc là khác model: `gpt-5.6-luna` kiểm được `gpt-6.1-terra`.
- LEAD kiểm điều này ba lần: khi chọn, khi REVIEWER báo model thực tế lúc bắt đầu, và khi review PR `RVW`.
- Để còn REVIEWER, LEAD không dùng hết mọi model đủ điều kiện làm WORKER trong cùng một chu kỳ.
<!-- END: REVIEW -->

<!-- ANCHOR: STOPS -->
## 5. Dừng và báo OWNER
- Không có model đủ điều kiện cho một task: task `BLOCKED`.
- Không xác định được model thực tế của một phiên: không dùng kết quả của phiên; task hoặc lượt kiểm định `BLOCKED`.
- Không có REVIEWER thỏa mục 4, hoặc một run của chu kỳ không ghi được model thực tế: phần kiểm định `BLOCKED`.
- Mọi trường hợp trên áp điểm dừng 1 của `01_plan/SPEC_DRYRUN.md#STOPS`; báo cáo nêu các model đã xét và lý do từng model không dùng được.
<!-- END: STOPS -->
