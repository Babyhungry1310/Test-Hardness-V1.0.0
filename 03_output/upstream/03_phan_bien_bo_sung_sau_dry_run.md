# Phần 3 — Phản biện và bổ sung cho tổng hợp sau dry run

Dự thảo từ nội dung OWNER cung cấp ngày 2026-11-16, gắn nguồn tư vấn Fable. Là đề xuất, không phải quyết định hay kiểm kê chính thức DEC-0020. Mốc trạng thái PR/SHA trong nguồn là ảnh chụp, cần kiểm lại trước khi dùng.

## A. Bổ sung xuyên suốt
- A1: Một bảng bảy loại lỗi: logic, quyền, môi trường, hạn mức, an toàn, vượt phạm vi, thiếu thông tin chặn. Với mỗi loại nêu người phân loại, tính loop, trần thử, người nhận báo cáo và bằng chứng tối thiểu.
- A2: Một bảng thẩm quyền: WORKER tự xử lý; hỏi LEAD; dừng báo LEAD và OWNER. Các mục khác trỏ về bảng.
- A3: Mỗi đề xuất có số lần quan sát trong dry run, con trỏ bằng chứng và nhãn đã quan sát hoặc ý tưởng; chuẩn hóa dữ liệu và checkpoint hiện là ý tưởng.
- A4: Ghi tầng đích (luật/script/cấu hình/RSK), chi phí, phụ thuộc và khả năng đảo ngược.
- A5: Đo số lần OWNER được hỏi/task, loop mất vì lỗi không phải logic và số phiên phải làm lại; đo trước và sau.
- A6: Chốt phạm vi không làm; ví dụ sandbox, tài khoản riêng, schema MAJOR.

## B1. Brainstorm và Planning
- Bất đồng về hướng đưa OWNER quyết; LEAD không tự sửa DEC, tư vấn không sửa plan. Đề xuất tiêu chí LEAD quyết kỹ thuật: đảo ngược, trong product_paths, không thêm phụ thuộc, không đổi luật/phạm vi. Cần đối chiếu thẩm quyền LEAD hiện hành trước khi chốt.
- Hết hai vòng còn điểm chặn: OWNER chốt, miễn có lý do hoặc quay lại Brainstorm. Hai vòng là đề xuất.
- Yêu cầu tra cứu nêu quyết định phục vụ; kết quả gồm tóm tắt, nguồn, ngày truy cập, mức chắc chắn và hạn dùng; tư vấn không nhận dữ liệu thô. Chốt người lập DSC nếu tư vấn không ghi repo.

## B2. Task và preflight
- Điều kiện bắt buộc UNKNOWN xử lý như FAIL; điều kiện tùy chọn thành giả định có tên. Gắn kết quả với SHA, tuyến, phiên; kiểm lại khi đổi hoặc xuất hiện prompt quyền.
- Smoke không ghi repo hoặc write_scope, theo cặp máy/tuyến. Các inputs/read_also phải giải được trong worktree tại SHA nền; bản chưa merge không là đầu vào task.
- Đưa kiểm task sẵn sàng vào PLAN_GO câu 4 cho chu kỳ đầu và bước mở batch cho chu kỳ sau.

## B3. Điều phối, loop và làm rõ task
- Đề xuất định nghĩa loop là lần verify thực sự chạy trên sản phẩm đã đổi; lần bị chặn trước chạy không tính nhưng phải ghi bằng chứng. LEAD phân loại từ bằng chứng; WORKER chỉ đề xuất.
- Quy định trần retry riêng cho lỗi không tính loop; hết trần thì dừng. Chỉ LEAD xác nhận worker đã dừng khi có bằng chứng tiến trình kết thúc hoặc quyền ghi bị thu hồi; quá hạn là UNKNOWN.
- LEAD được làm rõ không đổi scope/acceptance và ghi vào run; thay đổi phạm vi hoặc nghiệm thu cần task mới hoặc DEC. LEAD được giao lại, đổi model, không nới scope, cấp quyền hoặc thêm loop.
- Chỉ chuẩn hóa trạng thái dispatch Orca thực sự cung cấp; mỗi GO có mã để phát hiện lặp.

## B4. Quyền và cách ly
- Phân biệt prompt tác tử, quyền OS và policy repo. Bổ sung trạng thái chạy không giám sát đã/chưa kiểm; không giao batch tự động cho tuyến chưa đạt.
- Cho phép lệnh theo task/verify, mặc định từ chối mạng, cài gói, đẩy ref ngoài nhánh task. Không đổi PowerShell execution policy để chạy; ghi cách gọi phù hợp.
- Đề xuất ngưỡng xem lại broker/sandbox: có sự cố đầu tiên hoặc trước người thứ hai dùng repo; OWNER chốt RSK phần cách ly nhẹ không che được mạng và credential manager.

## B5. Model và phân bổ
- Ưu tiên Grok/GPT/Opus chỉ để phân xử model đủ điều kiện, hợp việc; đề xuất DEC phạm vi dry run và ghi lý do bỏ qua model ưu tiên.
- Dành reviewer trước khi phân bổ worker; kiểm tra chéo không thay review vòng/cổng, có chi phí riêng và đầu ra không tin cậy.
- Hết quota dừng, không mua; route khác model dùng actual; thiếu metadata UNKNOWN; SSE lỗi dù HTTP 200 là lỗi. OWNER chốt trần phiên/thời gian batch khi quota chưa đọc được.

## B6. Injection
- Đề xuất danh sách nguồn chỉ dẫn: task và luật tại SHA đã merge, cùng lời OWNER trong phiên; cần thiết kế xác thực coordinator và xử lý xung đột phân cấp trước khi biến thành luật.
- Giao việc trỏ task/SHA, worker đối chiếu, không nhận phạm vi vượt task. LEAD dùng con trỏ thay sao chép output worker vào prompt phiên khác; kết luận MERGE/PASS dựa trên kiểm tra, không chép từ worker.
- Bản phân tích chuẩn hóa do script tạo là ý tưởng; giữ nguyên gốc, đánh giá sau kết quả scanner CYC-06. Thẻ bọc và scan không thay ranh giới quyền.

## B7. Checkpoint và token
- Tách khôi phục bắt buộc, cơ học do coordinator và giải trình dự định tùy chọn do worker. Đề xuất checkpoint ngoài write_scope, không vào Git; cần thiết kế để không chặn ghi hợp lệ hoặc vi phạm C3.
- Quy định khi nào cùng run/mở run mới, ai quyết, loop mang theo. Đo chi phí checkpoint tùy chọn trên một số task trước khi đưa vào luật.

## B8. Kiểm định và repo mẹ
- Tái hiện lỗi trên main sạch trong môi trường đích; Windows mặc định là môi trường đích thì UnicodeEncodeError là lỗi sản phẩm, trừ khi UTF-8 là yêu cầu môi trường chính thức đã chốt.
- Bằng chứng chỉ ở .local: tạo trích gọn đã che bí mật vào repo thông qua task hoặc ghi chưa xác minh. Mỗi mục kiểm kê có ID, trạng thái đề xuất/đã chốt/đã merge/bị loại/thất bại/chưa xác minh và SHA phạm vi.
- Đối chiếu dữ kiện lịch sử: PR31/36, DEC21–26, upstream path và trạng thái CYC-03. Không tự kết luận bỏ mã hay đảo ngược quyết định; đề xuất 'mã chỉ cấp khi mở PR' cần OWNER chốt và kiểm tương thích quy tắc mã bất biến.

## B9–B10. Quyết định và nguồn
- Cần chốt: người phân loại và trần retry; làm rõ task bất biến; UNKNOWN; readiness không giám sát; chi phí batch; giữ bằng chứng local; thước đo; phạm vi không làm; Unicode là lỗi sản phẩm hay yêu cầu môi trường.
- Mỗi nguồn local kèm ngày và mã băm khi tổng hợp; không coi source snapshot là trạng thái hiện tại.

## C. Thứ tự đề xuất
0. Đối chiếu sổ, PR lead, mã quyết định, đường dẫn upstream, trạng thái chu kỳ.
1. Luật: phân loại lỗi, thẩm quyền, loop, dừng, làm rõ task, nguồn chỉ dẫn, bàn giao đủ nguồn, tiếp nhận Basic Plan.
2. Script: kiểm môi trường hai lần, smoke, kiểm cơ học, verify cách ly nhẹ và snapshot; triển khai theo các quyết định/bằng chứng và kiểm định tương ứng.
3. Xem xét sau hoặc RSK: broker/sandbox, bản phân tích chuẩn hóa, checkpoint tùy chọn, tài khoản riêng; cần số đo hoặc lý do đã chốt.

## Lưu ý kiểm chứng
- PR #31 còn OPEN tại lượt kiểm hiện tại; PR #36 đã MERGED. Nhận định nguồn nói cả hai đang mở chỉ là lịch sử.
- Nội dung trên là bản tổng hợp dự thảo từ lời OWNER và nội dung gán cho Fable trong chat, không xác minh độc lập mọi tuyên bố 'đã chốt'. So bản gốc trong hội thoại trước khi đưa vào PR; không tự chuyển đề xuất thành quyết định.
