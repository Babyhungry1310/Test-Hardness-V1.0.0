# Thông tin cần cập nhật vào khung

Danh sách các điểm OWNER và Fable đã bàn, chờ đưa vào khung qua đúng quy trình (`DSC` → `DEC` → PR). Chưa mục nào có hiệu lực.

- Ngày ghi: 2026-11-16
- Nguồn: phiên DISCUSS "Vai trò Fable trong giai đoạn Brainstorm", model `claude-fable-5-2`
- Repo liên quan: Test-Hardness-V1.0.0, `main` @ 8dcf58b, khung 1.0.1
- Lý do chưa ghi vào repo: PR #31 (`lead/model-route-clarity`) đang mở; `harness/tools/PREFLIGHT.md` dòng 15 không cho phiên LEAD khác ghi sổ hay cấp mã cho tới khi PR đó được merge hoặc đóng
- Bước tiếp theo: khi PR #31 xong, chuyển ba mục dưới thành các `PROPOSAL` trong `05_memory/discussions/2026/DSC-20261116-012x.md` để OWNER chốt từng mục

## Mục 1. Vai trò của Fable trong giai đoạn Brainstorm

Đề xuất: Fable là chuyên gia tư vấn của phiên DISCUSS, không lập plan chi tiết.

Fable làm:
- Nêu các hướng tiếp cận và phương án kiến trúc.
- Phân tích đánh đổi, phụ thuộc, rủi ro của từng hướng.
- Phản biện giả định; chỉ ra mâu thuẫn với `DEC` đang `ACTIVE` và với dữ kiện thật của repo.
- Soạn câu hỏi quyết định cho OWNER: mỗi câu một ý, có phương án và khuyến nghị.
- Xác định ranh giới phạm vi và tiêu chí "xong" ở mức hướng đi.

Giao model khác:
- Đọc và tóm tắt hiện trạng repo, sổ quyết định, rủi ro, kết quả chu kỳ trước (kèm con trỏ).
- Tra cứu bên ngoài, kiểm tuyến model. Fable tuyệt đối không trực tiếp duyệt web. Mọi nhu cầu tra cứu bên ngoài được Fable xuất thành RESEARCH_REQUEST để User chuyển sang Orca (qua copy-paste hoặc qua thư mục tạm mà claude desktop và orca có thể truy cập). Dữ liệu trả về cho Fable bắt buộc phải là bản tóm tắt kỹ thuật sạch, không mang HTML thô.
- Soạn nháp `DEC` và `BRIEF.md` từ điều OWNER đã chốt.

Giao script (khi có):
- Tạo khung `DSC`, liệt kê `PROPOSAL` còn mở, dựng nháp `DEC`, sinh `STATE.md`.
- Kiểm schema, con trỏ, giới hạn dòng.

Điều cần OWNER chốt: Fable là LEAD của phiên DISCUSS hay tư vấn đứng ngoài. Luật hiện hành ghi LEAD chủ trì DISCUSS và lập `DSC`; nếu Fable chỉ tư vấn thì phải ghi rõ ai lập `DSC` và ai soạn `DEC`.

## Mục 2. Basic Plan: sản phẩm của Brainstorm

Đề xuất: không tạo loại bản ghi mới. Nội dung Basic Plan đi vào các `PROPOSAL` của `DSC`, rồi thành `DEC` và `00_brief/BRIEF.md` sau khi OWNER chốt. Chuỗi `DSC` → `DEC` → `PLAN.md` giữ nguyên.

Mức chi tiết tối thiểu:
1. Mục tiêu và phạm vi: 3–5 dòng, kèm danh sách "không làm".
2. Hướng tiếp cận đã chọn, kèm các hướng đã loại và lý do loại.
3. Quyết định kiến trúc chính: mỗi quyết định một dòng, chuyển thẳng được thành `DEC`.
4. Các khối công việc: tên khối, kết quả cần có, phụ thuộc giữa các khối. Không chia task, không ghi `write_scope`.
5. Ràng buộc bất biến: thứ LEAD không được đổi khi lập plan.
6. Rủi ro lớn nhất và giả định: mỗi mục một dòng, kèm hậu quả nếu giả định sai.
7. Điều còn mở: câu hỏi OWNER chưa chốt; LEAD không tự chọn thay.
8. Tiêu chí "xong" ở mức hướng đi: một dòng cho mỗi khối.

Basic Plan không chứa `verify`, `done_when`, batch, phân công model hay số task. Các phần đó thuộc LEAD của dự án ở giai đoạn Planning.

## Mục 3. LEAD phân tích và phản biện kết quả Brainstorm trước khi Planning

Đề xuất: thêm một bước tiếp nhận bắt buộc giữa Brainstorm và Planning. LEAD của dự án không lập plan ngay từ Basic Plan; LEAD đọc, đối chiếu và gửi lại các yêu cầu bổ sung, làm rõ, mỗi yêu cầu kèm lý do.

LEAD phải kiểm:
- Mỗi quyết định kiến trúc có đủ rõ để ghi thành một `DEC` không.
- Mỗi khối công việc có kết quả cần đạt và phụ thuộc không.
- Tiền đề của Basic Plan có khớp dữ kiện thật không: repo, nhánh, SHA, PR, file, quyền, model đã kiểm chạy được. Không tin tiền đề khi chưa đối chiếu.
- Có mâu thuẫn với `DEC` đang `ACTIVE`, luật khung, `product_paths`, vùng 🔒 không.
- Có đủ căn cứ để viết `ACCEPTANCE.md` và `done_when` không.
- Rủi ro và giả định nào chưa có cách xử lý.

Mỗi yêu cầu LEAD gửi lại gồm:
- Loại: `BỔ SUNG` (thiếu thông tin) · `LÀM RÕ` (hiểu được nhiều cách) · `MÂU THUẪN` (trái `DEC`, luật hoặc dữ kiện) · `RỦI RO` (chưa có cách xử lý).
- Trỏ tới mục nào của Basic Plan.
- Điều cần OWNER hoặc người tư vấn trả lời.
- Tại sao: nếu không trả lời thì phần nào của plan không lập được hoặc sẽ lệch (ví dụ không xác định được `write_scope`, không viết được `done_when`, không biết thứ tự phụ thuộc).
- Mức: chặn plan · không chặn.

Quy tắc đi kèm:
- LEAD không tự chọn hướng và không tự điền chỗ trống thay OWNER.
- Yêu cầu mức "chặn plan" phải được trả lời và chốt thành `DEC`, hoặc OWNER ghi rõ miễn, trước khi LEAD lập `PLAN.md`.
- Yêu cầu "không chặn" chưa có trả lời thì vào plan dưới dạng giả định hoặc `RSK`, nêu rõ.
- Đề xuất tối đa 2 vòng hỏi đáp; còn điểm chặn sau vòng 2 thì OWNER quyết: chốt, miễn, hoặc quay lại Brainstorm.
- Người tư vấn Brainstorm và LEAD tiếp nhận nên là hai phiên khác nhau, để phản biện không do chính người đề xuất làm.

Chỗ đặt trong khung (đề xuất, không thêm loại bản ghi):
- Yêu cầu của LEAD ghi thành sự kiện `QUESTION` trong `DSC` (loại này đã có trong ngữ pháp).
- Trả lời đã chốt thành `DEC` có `origin` trỏ sự kiện đó.
- Cổng PLAN, câu 2, mở rộng: ngoài `PROPOSAL` chưa chốt, không còn `QUESTION` mức "chặn plan" nào chưa trả lời.
- Luật cần sửa khi OWNER chốt: `harness/HARNESS.md` mục 7 (phase), `harness/rules/LEAD.md` mục 4–5, `harness/templates/plan_go.md`, có thể cả `harness/schemas/STATUS_GRAMMAR.md` cho dòng trạng thái của `QUESTION`.

Điều cần OWNER chốt cho mục 3:
- Bước tiếp nhận là bắt buộc với mọi dự án, hay chỉ khi Basic Plan do một phiên khác LEAD soạn.
- Số vòng tối đa (đề xuất: 2).
- Thay đổi này đi vào bản khung nào (1.0.2 hay bản sau), và làm ở repo thử trước hay repo mẹ.
