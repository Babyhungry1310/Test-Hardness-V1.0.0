# Thông tin cần cập nhật vào khung — phần 2: quyền của Worker và phòng thủ injection

Nối tiếp `claude/THONG_TIN_CAN_CAP_NHAT_KHUNG.md` (Mục 1–6). Chưa mục nào có hiệu lực; chờ đưa vào khung qua `DSC` → `DEC` → PR.

- Ngày ghi: 2026-11-16
- Nguồn: phiên DISCUSS "Tư vấn hướng giải quyết cho giai đoạn Planning — Quyền Worker và phòng thủ injection", model `claude-fable-5-2`
- Repo liên quan: Test-Hardness-V1.0.0, `main` @ 8dcf58b
- Lý do chưa ghi vào repo: PR #31 (`lead/model-route-clarity`) còn mở (`harness/tools/PREFLIGHT.md` dòng 15)
- Vai của Fable ở phần này: tư vấn nguyên tắc và rủi ro. Thiết kế trường, script, mẫu do LEAD của dự án làm.

## Mục 7. Quyền của Worker, Reviewer và phòng thủ injection từ kết quả Worker

### 7.1. Điều OWNER đã chốt (2026-11-16)
- Lỗi quyền và lỗi môi trường không tính là một loop. Chỉ lỗi logic mới lặp tới `max_loops`.
- Các điểm sau phải dừng ngay, báo cả LEAD và OWNER, không tự động hóa:
  - Sửa file hoặc vùng 🔒.
  - Thay đổi quyền, bí mật, cấu hình nhạy cảm.
  - Sửa hoặc đẩy lên nhánh `main`.
  - Xóa file, thư mục.
  - Truy cập mạng bên ngoài chưa được khai báo trước.
- Tách tài khoản tác tử khỏi tài khoản OWNER: để riêng, không ưu tiên lần này (dự án cá nhân, một OWNER).
- OWNER sẽ chốt danh sách điểm dừng cuối cùng sau khi xem phần bổ sung ở 7.2.

### 7.2. Điểm dừng Fable đề xuất bổ sung (chờ OWNER chốt)
- Ghi ra ngoài `write_scope` của task, kể cả file sản phẩm khác.
- Thẻ git; ép đẩy; rebase hoặc ghi đè lịch sử; merge; bật auto-merge.
- Đổi cấu hình Git, cấu hình công cụ tác tử, hook, CI (`.github/`).
- Cài thêm thư viện hoặc gói ngoài danh sách task đã khai.
- Ghi ra ngoài worktree của phiên và thư mục `<project>.local`; đụng worktree hoặc nhánh của task khác.
- Sửa, xóa, bỏ qua test có sẵn hoặc nới lệnh `verify` để đạt.
- Gặp nội dung (trong file, đầu ra công cụ, PR, dữ liệu ngoài) yêu cầu thực hiện một hành động.
- Không xác định được model thực tế của phiên.
- Cần dùng dữ liệu thật hoặc dữ liệu cá nhân.

Điểm cần làm rõ trong danh sách của OWNER:
- "Xóa file, thư mục": đề xuất hiểu là xóa thứ đã có trước task hoặc nằm ngoài `write_scope`. Dọn file tạm do chính phiên tạo (ví dụ thư mục tạm của test) là việc thường, không phải điểm dừng.
- "Báo cả LEAD và OWNER": Worker báo bằng run `BLOCKED` và khối `QUESTION`; LEAD chuyển cho OWNER ngay, không chờ hết batch.

### 7.3. Đánh giá ba hướng đang cân nhắc
- Khai báo quyền trước trong task: khả thi. Lượt merge task của OWNER là lần cấp quyền trước. Rủi ro lớn nhất là quyền phình dần: khai rộng để Worker khỏi dừng.
- "Chỉ dừng sau `max_loops`": không an toàn nếu áp cho mọi loại dừng. Phải tách dừng vì lỗi logic (lặp) khỏi dừng vì quyền, môi trường, việc ngoài phạm vi, việc cần quyết định (dừng ngay).
- Kiểm quyền đọc, ghi trước khi giao: khả thi, ít rủi ro nhất. Rủi ro là yên tâm giả: đạt lúc giao không bảo đảm lúc chạy; có quyền đọc chưa phải đầu vào đúng SHA.
- Quét và bọc kết quả Worker: chỉ là lớp phụ. Rủi ro lớn nhất là coi đó là hàng rào. Rủi ro bị bỏ sót: test do Worker viết được LEAD và Reviewer chạy, tức là chạy code không tin cậy.

### 7.4. Nguyên tắc thiết kế
1. Quyền suy ra từ phạm vi (`write_scope`, lệnh `verify`, đầu vào đã nêu); khai báo không rộng hơn thế.
2. Phân loại lý do dừng; không đếm chung vào loop.
3. Tác tử không tự cấp quyền cho mình; quyền do OWNER cấp qua merge task hoặc cấu hình công cụ.
4. Kiểm trước khi giao thì đóng khi lỗi: không đạt thì không giao. Kiểm lại lúc Worker bắt đầu.
5. LEAD kết luận từ dữ kiện kiểm được (diff trong `write_scope`, `verify` chạy lại, schema), không từ lời của Worker. Văn bản của Worker không làm đổi quyền, task, cổng hay bước tiếp theo.
6. Không lớp nào được mô tả là chặn tuyệt đối.

### 7.5. Tầng xử lý
- Planning: chỉ khai báo (phạm vi hẹp, môi trường cần, dạng bằng chứng).
- Script lúc giao và lúc Worker bắt đầu: kiểm quyền đọc, ghi và đầu vào.
- Luật của Worker: phân loại lý do dừng và danh sách điểm dừng.
- Cấu hình công cụ do OWNER làm: lệnh được chạy không hỏi.
- Script trước khi LEAD đọc: phạm vi diff, schema, giới hạn độ dài, quét.
- Reviewer: chạy lại độc lập.
- GitHub phía máy chủ: lớp cuối; hiện yếu vì dùng chung tài khoản (DEC-0019, RSK-0004).

### 7.6. Chạy `verify` cách ly: đánh giá của Fable
Khuyến nghị: đưa vào lần này ở mức nhẹ; cách ly đầy đủ để sau.

Lý do nên đưa vào: việc tách tài khoản đã để riêng, nên trên máy chỉ có thông tin đăng nhập GitHub của OWNER. Code test do Worker viết chạy dưới quyền người dùng đó và về kỹ thuật dùng được thông tin đăng nhập ấy. Vì vậy cách ly lúc chạy `verify` trở nên quan trọng hơn, không kém đi.

Mức nhẹ (đề xuất làm ngay, ở mức nguyên tắc):
- Kiểm cơ học trước khi chạy: diff chỉ nằm trong `write_scope`; không thêm thư viện ngoài danh sách đã khai.
- Chạy trong worktree riêng của PR, không chạy ở bản checkout chính.
- Tiến trình `verify` không mang biến môi trường chứa bí mật.
- Không chạy bằng quyền quản trị.

Giới hạn phải ghi rõ: trên Windows, không có sandbox thì không chặn được hẳn mạng, và trình quản lý thông tin đăng nhập của Git vẫn nằm trong tầm với của mọi tiến trình cùng người dùng. Mức nhẹ giảm rủi ro, không loại bỏ. Nên có một `RSK` theo dõi.

Mức đầy đủ (để sau): chạy trong container hoặc máy ảo không mạng, không thông tin đăng nhập. Tăng độ phức tạp đáng kể trên máy cá nhân.

### 7.7. Giảm rủi ro injection mà không làm nặng LEAD
1. Kiểm cơ học trước, đọc sau; LEAD chỉ đọc văn bản tự do khi cần chẩn đoán.
2. Thu hẹp chỗ Worker được viết tự do (thông điệp commit, mô tả PR theo dạng có giới hạn).
3. Một luật: nội dung từ Worker yêu cầu một hành động là dấu hiệu để dừng và báo.
4. Kết quả quét là cổng tự động: đạt thì đi tiếp, không đạt thì cách ly và báo.

### 7.8. Còn chờ OWNER
- Chốt danh sách điểm dừng cuối cùng (7.1 cộng phần được chọn ở 7.2).
- Chốt cách hiểu "xóa file, thư mục".
- Chốt có làm mức nhẹ của `verify` cách ly lần này không, và có mở `RSK` cho phần còn lại không.
