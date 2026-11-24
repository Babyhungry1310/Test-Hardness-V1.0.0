B?n tham kh?o 2026-11-22. Ngu?n hi?n h?nh: SRC-0003 P6d, DEC-0032.

# H1 — Brainstorm và tra cứu bên ngoài

- Trạng thái: DỰ THẢO cho các mục chưa có trạng thái. Mục đã chốt (DEC-0031, DSC-20261121-kzn1) ghi trạng thái ở H0 mục 3.
- Ngày ghi: 2026-11-16. Nguồn: phiên DISCUSS "Vai trò Fable trong giai đoạn Brainstorm", model claude-fable-5-2.
- Repo liên quan tại ngày ghi: Test-Hardness-V1.0.0, main @ 8dcf58b, khung 1.0.1.
- Biên tập lại: 2026-11-19, theo thẩm định Kaizen.
- Cập nhật 2026-11-21: điều kiện kích hoạt bước tiếp nhận; E1 gắn với E3; làm rõ "scan" của 06_sources/.
- Cập nhật 2026-11-22: nguồn mẫu quét cho 06_sources/ (E39).
- Đã nạp vào repo ở TK-0036 (05_memory/upstream/). File này là bản đề xuất cập nhật 2026-11-22; LEAD đồng bộ vào bản trong repo.

## 1. Vai ADVISOR trong phiên DISCUSS
Nhãn: GIỮ | Đợt: Đợt 4, cùng E3 | PROPOSAL: E1
- Tên vai trung tính, không gắn model. Model cho vai chọn theo harness/MODEL_POLICY.md như mọi vai khác.
- ADVISOR làm:
  - Nêu các hướng tiếp cận và phương án kiến trúc.
  - Phân tích đánh đổi, phụ thuộc, rủi ro của từng hướng.
  - Phản biện giả định; chỉ ra mâu thuẫn với DEC đang ACTIVE và với dữ kiện thật của repo.
  - Soạn câu hỏi quyết định cho OWNER: mỗi câu một ý, có phương án và khuyến nghị.
  - Xác định ranh giới phạm vi và tiêu chí "xong" ở mức hướng đi.
- ADVISOR không làm: lập plan chi tiết, lập DSC, soạn DEC.
- LEAD làm: lập DSC, ghi đề xuất của ADVISOR thành PROPOSAL, soạn DEC sau khi OWNER chốt. LEAD.md luật 17–19 giữ nguyên.
- Giao model khác:
  - Đọc và tóm tắt hiện trạng repo, sổ quyết định, rủi ro, kết quả chu kỳ trước, kèm con trỏ.
  - Kiểm tuyến model.
  - Soạn nháp DEC và BRIEF.md từ điều OWNER đã chốt.
- Giao script khi có: tạo khung DSC, liệt kê PROPOSAL còn mở, dựng nháp DEC, sinh STATE.md, kiểm schema, con trỏ, giới hạn độ dài.
- E1 chỉ có hiệu lực cùng lúc với E3 (mục 4). Nếu không, đề xuất của ADVISOR đi vào DSC mà không qua lớp kiểm nào.

## 2. Tra cứu bên ngoài
Nhãn: GỘP (vào 06_sources/ và LEAD.md luật 34) | Đợt: [ĐỢT: LEAD chốt] | PROPOSAL: E2
- ADVISOR không trực tiếp duyệt web.
- ADVISOR nêu nhu cầu tra cứu. Cách nêu: [LEAD chốt]; không thêm loại khối hay loại bản ghi.
- Kết quả trả về là bản tóm tắt kỹ thuật sạch, không mang HTML thô.
- Kết quả vào repo qua 06_sources/ sau scan.
  - Loại quét: [LEAD chốt: secret (detect-secrets, E23), nội dung yêu cầu hành động (injection), hay cả hai].
  - Bổ sung 2026-11-22 (E39): bộ mẫu injection và quét base64 có thể lấy từ GSD Core (`prompt-injection-scan.sh`, `base64-scan.sh`), chép kèm NOTICE MIT và thay phần mã thoát. Bước 3 (TK-0045) dùng ở mức cảnh báo cho PR; 06_sources/ dùng ở mức chặn từ Đợt 2.
  - Người chạy: script, không phải LEAD đọc bằng mắt.
  - Mốc: trước đây dự kiến CYC-06; nay là việc của Đợt 2 trong KE_HOACH_KAIZEN.md.
- Tới khi có scan, OWNER duyệt bằng mắt trước khi đưa vào. Đây là một cổng chờ OWNER (H0 mục 2), nên giữ số lần tra cứu ít.
- Trong DSC, dữ kiện lấy từ tra cứu ghi thành ASSUMPTION kèm nguồn.

## 3. Basic Plan: sản phẩm của Brainstorm
Nhãn: HOÃN (Brainstorm) | Đợt: Đợt 4 (KE_HOACH_KAIZEN.md) | PROPOSAL: E3
- Không tạo loại bản ghi mới. Nội dung Basic Plan đi vào các PROPOSAL của DSC, rồi thành DEC và 00_brief/BRIEF.md sau khi OWNER chốt.
- Chuỗi DSC → DEC → PLAN.md giữ nguyên.
- Mức chi tiết tối thiểu:
  - Mục tiêu và phạm vi: 3–5 dòng, kèm danh sách "không làm".
  - Hướng tiếp cận đã chọn, các hướng đã loại và lý do loại.
  - Quyết định kiến trúc chính: mỗi quyết định một dòng, chuyển thẳng được thành DEC.
  - Khối công việc: tên khối, kết quả cần có, phụ thuộc giữa các khối. Không chia task, không ghi write_scope.
  - Ràng buộc bất biến: thứ LEAD không được đổi khi lập plan.
  - Rủi ro lớn nhất và giả định: mỗi mục một dòng, kèm hậu quả nếu giả định sai.
  - Điều còn mở: câu hỏi OWNER chưa chốt; LEAD không tự chọn thay.
  - Tiêu chí "xong" ở mức hướng đi: một dòng cho mỗi khối.
- Basic Plan không chứa verify, done_when, batch, phân công model, hạng task (E17) hay số task. Các phần đó thuộc LEAD ở giai đoạn Planning.

## 4. Bước LEAD tiếp nhận Basic Plan trước Planning
Nhãn: HOÃN (Brainstorm) | Đợt: Đợt 4 (KE_HOACH_KAIZEN.md) | PROPOSAL: E3
- Bắt buộc khi nội dung Basic Plan do ADVISOR hoặc một phiên khác đề xuất, kể cả khi chính LEAD là người ghi nội dung đó vào DSC (sửa 2026-11-21). Điều kiện cũ "do một phiên khác LEAD soạn" không bao giờ đúng, vì theo mục 1 LEAD luôn là người ghi PROPOSAL.
- Tối đa 2 vòng hỏi đáp.
- LEAD kiểm:
  - Mỗi quyết định kiến trúc đủ rõ để ghi thành một DEC.
  - Mỗi khối công việc có kết quả cần đạt và phụ thuộc.
  - Tiền đề khớp dữ kiện thật: repo, nhánh, SHA, PR, file, quyền, model đã kiểm chạy được.
  - Không mâu thuẫn với DEC đang ACTIVE, luật khung, product_paths, vùng 🔒.
  - Đủ căn cứ để viết ACCEPTANCE.md và done_when.
  - Rủi ro và giả định đều có cách xử lý.
- Phần kiểm cơ học (SHA, nhánh, PR, file tồn tại, DEC đang ACTIVE, model trong catalog) do script chạy trước; LEAD chỉ xét phần ngữ nghĩa.
- Mỗi yêu cầu LEAD gửi lại gồm:
  - Loại: BỔ SUNG · LÀM RÕ · MÂU THUẪN · RỦI RO.
  - Mục của Basic Plan được trỏ tới.
  - Điều cần OWNER hoặc ADVISOR trả lời.
  - Tại sao: phần nào của plan không lập được hoặc sẽ lệch nếu không trả lời.
  - Mức: chặn plan · không chặn.
- Quy tắc:
  - LEAD không tự chọn hướng, không tự điền chỗ trống thay OWNER.
  - Yêu cầu "chặn plan" phải được chốt thành DEC, hoặc OWNER ghi rõ miễn, trước khi lập PLAN.md.
  - Yêu cầu "không chặn" chưa có trả lời thì vào plan dưới dạng giả định hoặc RSK.
  - Còn điểm chặn sau vòng 2 thì OWNER quyết: chốt, miễn, hoặc quay lại Brainstorm.
  - ADVISOR và LEAD tiếp nhận là hai phiên khác nhau, chạy nối tiếp; quy tắc một phiên LEAD tại một thời điểm (PREFLIGHT) vẫn giữ.
- Chỗ đặt, không thêm loại bản ghi:
  - Yêu cầu của LEAD ghi thành sự kiện QUESTION trong DSC.
  - Trả lời đã chốt thành DEC có origin trỏ sự kiện đó.
  - Cổng PLAN câu 2 mở rộng: không còn QUESTION mức "chặn plan" chưa trả lời.
- Luật cần sửa khi OWNER chốt: harness/HARNESS.md mục 7; harness/rules/LEAD.md mục 4–5; harness/templates/plan_go.md; có thể cả harness/schemas/STATUS_GRAMMAR.md.
- Phiên bản khung nhận thay đổi: [VERSION: OWNER chốt].

## Đã loại
- Định nghĩa vai bằng tên model → trái DEC-0012, DEC-0018; vai phải trung tính.
- Chuyển kết quả tra cứu qua clipboard hoặc thư mục tạm dùng chung → bỏ qua 06_sources/ và scan, trái LEAD.md luật 34.
- Khối RESEARCH_REQUEST riêng → thêm loại khối; cách nêu nhu cầu tra cứu do LEAD chốt.
- Kích hoạt bước tiếp nhận theo người ghi vào DSC → không bao giờ kích hoạt, vì LEAD luôn là người ghi (2026-11-21).
