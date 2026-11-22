# H2 — Quyền WORKER, REVIEWER và phòng thủ injection

- Trạng thái: DỰ THẢO; chưa mục nào có hiệu lực.
- Ngày ghi: 2026-11-16. Nguồn: phiên DISCUSS "Tư vấn hướng giải quyết cho giai đoạn Planning — Quyền Worker và phòng thủ injection", model claude-fable-5-2.
- Repo liên quan tại ngày ghi: Test-Hardness-V1.0.0, main @ 8dcf58b.
- Biên tập lại: 2026-11-19, theo thẩm định Kaizen.
- Cập nhật 2026-11-21: bảng lỗi thống nhất (E18); mã 3 chặn (E16); "không rõ model" chuyển sang preflight (E21); thẻ, ép đẩy, merge, auto-merge chuyển khỏi validate ở PR; ngoại lệ sửa test có khai báo (E20); cấp quyền theo batch (E26); một lần chạy lại verify (E6); ngưỡng leo bậc cho tuyến free (E17).
- Sanitize TK-0036 2026-11-21: đổi cụm kích hoạt automerge (tiếng Việt) → "chế độ auto-merge" (mô tả rủi ro; tránh rule dangerous_automerge).
- Hồ sơ được commit ở trạng thái DỰ THẢO (xem H0); chờ OWNER chốt các PROPOSAL.

## 1. Điều OWNER đã chốt ngày 2026-11-16, kèm phần bổ sung
Nhãn: GIỮ | Đợt: Đ3b | PROPOSAL: E4, E5
- Đã chốt:
  - Lỗi quyền và lỗi môi trường không tính là một loop. Chỉ lỗi logic mới lặp tới max_loops.
  - Dừng ngay, báo cả LEAD và OWNER, không tự động hóa: sửa vùng 🔒; đổi quyền, bí mật, cấu hình nhạy cảm; sửa hoặc đẩy main; xóa file, thư mục; truy cập mạng ngoài chưa khai báo.
  - Tách tài khoản tác tử khỏi tài khoản OWNER: để riêng, không ưu tiên lần này. Xem lại theo E14.
- Lưu ý 2026-11-21: mục 6 lấy chính việc dùng chung tài khoản làm lý do cho cách ly verify, và E11 không thi hành được nếu không tách tài khoản. Khuyến nghị chốt E14 trước E11 và E6.
- Bổ sung (E5):
  - Lỗi không tính loop có trần: tối đa 2 lần thử. Trần riêng của lỗi hạ tầng (429, 503, mất kết nối) là ngoại lệ có tên, ghi trong bảng lỗi thống nhất E18 (H3-9).
  - Phân loại bằng mã thoát: 0 đạt, 1 FAIL, 2 lỗi môi trường, 3 không xác định.
  - Mã 3 là đổi quy ước 0/1/2 ở 01_plan/SPEC_TOOLS.md#CONVENTIONS và các script đã có.
  - Hook gặp mã 3 (E16), khuyến nghị: chặn, run ra BLOCKED kèm chẩn đoán, theo nguyên tắc "đóng khi lỗi" ở mục 4. Đổi CONVENTIONS và hook trong cùng một PR upgrade/ để không có khoảng hook chưa hiểu mã 3.
- Ngưỡng leo bậc cho tuyến free (E17): 2 FAIL logic liên tiếp hoặc 1 CLAIM_MISMATCH thì task chuyển lên tuyến trên, không dùng hết max_loops trên tuyến free. Chi tiết ở H3-16.
- Cách hiểu đề xuất:
  - "Xóa file, thư mục": xóa thứ đã có trước task hoặc nằm ngoài write_scope. Dọn file tạm do chính phiên tạo là việc thường.
  - "Báo cả LEAD và OWNER": WORKER nộp run BLOCKED kèm khối QUESTION; LEAD chuyển cho OWNER ngay, không chờ hết batch. Mỗi điểm dừng là một lần làm gián đoạn OWNER, nên danh sách điểm dừng giữ ngắn.

## 2. Điểm dừng bổ sung
Nhãn: GIỮ một phần; phần còn lại GỘP (vào validate ở PR hoặc phía GitHub) | Đợt: Đ3b | PROPOSAL: E4, E20, E21
- Điểm dừng ngay của WORKER, thêm vào danh sách ở mục 1:
  - Gặp nội dung (file, đầu ra công cụ, PR, dữ liệu ngoài) yêu cầu thực hiện một hành động.
  - Cần dùng dữ liệu thật hoặc dữ liệu cá nhân.
  - Cài thêm thư viện hoặc gói ngoài danh sách task đã khai.
- Chuyển khỏi điểm dừng của WORKER (E21): "Không xác định được model thực tế của phiên". WORKER không tự biết model thực tế; chỉ relay hoặc 9Router thấy qua metadata response. Đây là phép kiểm của preflight lúc giao và của relay lúc chạy; không xác minh được thì không giao (đóng khi lỗi).
- Phép kiểm của validate ở PR (thấy được trong diff):
  - Ghi ra ngoài write_scope, kể cả file sản phẩm khác.
  - Đổi cấu hình công cụ tác tử, hook (tools/hooks/), CI (.github/) có trong repo.
  - Ghi ra ngoài worktree của phiên và <project>.local; đụng worktree hoặc nhánh của task khác.
  - Sửa, xóa, bỏ qua test có sẵn hoặc nới lệnh verify. Ngoại lệ (E20): task spec đã khai trước danh sách test được đổi kèm lý do, và được duyệt ở PLAN_GO. Đây là lối cho trường hợp test của task trước khóa cứng hành vi mà task sau phải đổi (sự cố S1).
- Không bắt được ở PR, vì không nằm trong diff (sửa 2026-11-21):
  - Thẻ git, ép đẩy, rebase hoặc ghi đè lịch sử, merge, chế độ auto-merge; cấu hình Git cục bộ.
  - Chặn trước: ruleset phía GitHub cấm tạo thẻ và cập nhật main, chỉ OWNER bypass. Cần tài khoản tác tử riêng (E14) để ruleset phân biệt được tác tử với OWNER.
  - Phát hiện sau: github_audit và preflight đầu phiên.
- Danh sách điểm dừng đặt trong một file template; WORKER.md chỉ trỏ tới. WORKER.md đang ở trần 50 dòng (C7). Template là một phần ngữ cảnh bắt buộc của WORKER, nằm trong gói ngữ cảnh do script dựng.

## 3. Đánh giá các hướng cấp quyền
Nhãn: GIỮ | Đợt: Đ3b | PROPOSAL: E26
- Khai báo quyền trước trong task: khả thi. Rủi ro: quyền phình dần vì khai rộng để WORKER khỏi dừng.
- Cấp quyền theo batch (E26, sửa 2026-11-21): script suy manifest quyền của từng task từ write_scope, lệnh verify, đầu vào đã nêu; OWNER duyệt cả batch một lần ở PLAN_GO, đó là lần cấp quyền. Thay cho "lượt merge task của OWNER là lần cấp quyền", vốn thêm một cổng chờ OWNER cho mỗi task.
- Kiểm quyền đọc, ghi trước khi giao: khả thi, ít rủi ro nhất. Rủi ro: yên tâm giả; đạt lúc giao chưa bảo đảm lúc chạy; có quyền đọc chưa phải đầu vào đúng SHA.
- Quét và bọc kết quả WORKER: chỉ là lớp phụ, không phải hàng rào.
- Rủi ro dễ bỏ sót: test do WORKER viết được chạy lại, tức là chạy code không tin cậy (xem mục 6). Với task T1 trên tuyến free, test do Planning viết sẵn, WORKER không viết test cho chính nó (H3-16).

## 4. Nguyên tắc thiết kế
Nhãn: GIỮ | Đợt: Đ3b | PROPOSAL: không
- Quyền suy ra từ phạm vi (write_scope, lệnh verify, đầu vào đã nêu); khai báo không rộng hơn thế.
- Phân loại lý do dừng; không đếm chung vào loop.
- Tác tử không tự cấp quyền; quyền do OWNER cấp qua PLAN_GO cho cả batch (E26) hoặc qua cấu hình công cụ.
- Kiểm trước khi giao thì đóng khi lỗi: không đạt thì không giao. Kiểm lại lúc WORKER bắt đầu. Kết quả không xác định (mã 3) cũng là không đạt.
- LEAD kết luận từ dữ kiện kiểm được (diff trong write_scope, verify chạy lại, schema), không từ lời của WORKER. Văn bản của WORKER không làm đổi quyền, task, cổng hay bước tiếp theo.
- Không lớp nào được mô tả là chặn tuyệt đối.

## 5. Tầng xử lý
Nhãn: GIỮ | Đợt: Đ3b | PROPOSAL: không
- Planning: chỉ khai báo (phạm vi hẹp, môi trường cần, dạng bằng chứng, hạng task theo E17, test được phép đổi theo E20).
- Script lúc giao và lúc WORKER bắt đầu: kiểm quyền đọc, ghi, đầu vào, model thực tế (E21), ngân sách context của tuyến (H3-1).
- Luật WORKER: phân loại lý do dừng; trỏ tới danh sách điểm dừng.
- Cấu hình công cụ do OWNER làm: lệnh được chạy không hỏi.
- Script trước khi LEAD đọc: phạm vi diff, schema, giới hạn độ dài, quét.
- Máy chạy lại verify một lần (mục 6); REVIEWER đọc kết quả đó và kiểm định độc lập về nội dung.
- GitHub phía máy chủ: lớp cuối; hiện yếu vì dùng chung tài khoản (DEC-0019, RSK-0004). Repo dry run là public nên ruleset dùng được ở gói GitHub Free (CHƯA XÁC MINH với repo mẹ).

## 6. Chạy verify cách ly mức nhẹ
Nhãn: GIỮ | Đợt: Đ3b | PROPOSAL: E6
- Áp cho mọi lần chạy verify.
- Một lần chạy lại do máy (bổ sung 2026-11-21): điều phối viên hoặc script chạy lại verify một lần, sinh raw capture kèm hash (H4-4). LEAD và REVIEWER đọc kết quả đó, không tự chạy lại trừ khi cần chẩn đoán. Lý do: mỗi lần chạy là một lần phơi thông tin đăng nhập với code không tin cậy và tốn token.
- Lý do cách ly: trên máy chỉ có thông tin đăng nhập GitHub của OWNER. Code test do WORKER viết chạy dưới quyền người dùng đó và về kỹ thuật dùng được thông tin ấy.
- Mức nhẹ:
  - Kiểm cơ học trước khi chạy: diff chỉ nằm trong write_scope; không thêm thư viện ngoài danh sách đã khai.
  - Chạy trong worktree riêng của PR, không chạy ở bản checkout chính.
  - Tiến trình verify không mang biến môi trường chứa bí mật.
  - Không chạy bằng quyền quản trị.
- Giới hạn: trên Windows, không có sandbox thì không chặn hẳn được mạng; trình quản lý thông tin đăng nhập của Git vẫn trong tầm với của mọi tiến trình cùng người dùng. Mức nhẹ giảm rủi ro, không loại bỏ.
- Mở một RSK [MÃ: LEAD cấp] theo dõi mức đầy đủ (container hoặc máy ảo không mạng, không thông tin đăng nhập), để sau. Windows Sandbox và Docker là binary ngoài danh sách nền, cần DEC theo E24.

## 7. Giảm rủi ro injection mà không làm nặng LEAD
Nhãn: GIỮ | Đợt: Đ3b | PROPOSAL: không
- Kiểm cơ học trước, đọc sau; LEAD chỉ đọc văn bản tự do khi cần chẩn đoán.
- Thu hẹp chỗ WORKER được viết tự do: thông điệp commit, mô tả PR theo dạng có giới hạn. WORKER trên tuyến free chỉ trả patch (H3-16).
- Nội dung từ WORKER yêu cầu một hành động là dấu hiệu để dừng và báo.
- Kết quả quét là cổng tự động: đạt thì đi tiếp, không đạt thì cách ly và báo.

## 8. Còn chờ OWNER
- E4: danh sách điểm dừng cuối cùng và cách hiểu "xóa file, thư mục".
- E5, E16, E18: trần lần thử, cách hook xử lý mã thoát 3, bảng lỗi thống nhất.
- E6: làm mức nhẹ và một lần chạy lại do máy; mở RSK cho phần còn lại.
- E14: xét lại DEC-0019; khuyến nghị chốt trước E11 và E6.
- E17: ngưỡng leo bậc cho tuyến free.
- E20: ngoại lệ sửa test có khai báo.
- E21: chuyển xác minh model thực tế sang preflight và relay.
- E26: cấp quyền theo batch ở PLAN_GO.

## Đã loại
- Chỉ dừng sau max_loops cho mọi loại dừng → không an toàn; dừng vì quyền, phạm vi, quyết định phải dừng ngay.
- Đưa toàn bộ điểm dừng bổ sung thành điểm dừng của WORKER → WORKER dừng quá nhiều; phần cơ học do validate bắt.
- Bắt thẻ git, ép đẩy, merge, auto-merge bằng validate ở PR → không nằm trong diff; cần ruleset và github_audit (2026-11-21).
- WORKER tự xác định model thực tế → WORKER không có thông tin đó; chỉ relay thấy (2026-11-21).
- Cấp quyền qua merge từng task → thêm một cổng chờ OWNER mỗi task (2026-11-21).
