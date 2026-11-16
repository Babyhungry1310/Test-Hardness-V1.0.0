# Dự thảo plan và task — quyền WORKER theo task

Trạng thái: DỰ THẢO TRONG PHIÊN CHANGE ĐÃ ĐƯỢC OWNER CHO BẮT ĐẦU; DEC-0027, PLAN v8 và TK-0031 mới ở nhánh chờ OWNER merge, chưa có hiệu lực trên main. Mục tiêu: LEAD chuẩn bị thông tin và quyền hẹp trước giao; WORKER xử lý kỹ thuật trong scope mà không hỏi lại quyền thường lệ đã được cấp. Không hứa loại mọi prompt; ngoài quyền thì dừng. Mốc tham khảo main 3392c246, PR31 merged; STATE CYC-03 EXECUTE, B2 HOLD, TK-0030 product HOLD. Kiểm lại mốc trước ghi repo. Không đưa dự thảo này thành quyền thực thi.

## Ràng buộc và phụ thuộc quản trị

- `LEAD.md` luật 4 yêu cầu CONFIRM và OWNER gõ OK trước CHANGE; luật 14, 21–25 yêu cầu REQ/DEC, plan có nguồn, task và OWNER merge trước chạy. Mã bên dưới A–I là nhãn dự thảo, không phải mã TK đã cấp.
- `SPEC_TOOLS.md#CONVENTIONS` cấm script gọi model/mạng và task sửa `harness/`, `.github/`, ba file định tuyến. Muốn thay phải có DEC, plan và phạm vi được OWNER duyệt; không ghép vào task CYC-03 hiện có. STATE nêu DEC-0022–0025 migration ở workspace khác: rà mã và va chạm trước cấp số.
- Đề xuất tối thiểu: supervised có ghi rủi ro khi chưa có sandbox được chứng minh. Unattended chỉ trong profile có kiểm soát thực thi được kiểm; không tự bật bypass hoặc trả lời Yes hộ OWNER.
- Những lựa chọn còn chờ OWNER: profile cần hỗ trợ (giám sát/tự động); rule loop, verify gián đoạn, retry runtime và dọn tạm; phạm vi Git/network và rủi ro credential; đích repo/version và ngân sách. OWNER cho OK bắt đầu CHANGE không mặc nhiên phê duyệt các lựa chọn này.

## Chuỗi công việc

Giai đoạn 1: A kiểm kê → B thiết kế hợp đồng → C readiness và D sự kiện (sau B, không cùng file) → E thử supervised.
Giai đoạn 2: F broker/thực thi hạn chế sau quyết định OWNER và B; G sandbox verify sau F hoặc interface đã chốt; H smoke tự động sau F+G; I kiểm định độc lập và bàn giao sau E+H. Nếu OWNER chỉ chọn supervised, F–H là phần thí điểm chưa kích hoạt, I đánh giá phạm vi thực có. Task được chia lại nếu >5 file hoặc >khoảng 400 dòng.

### A — Kiểm kê và baseline
Mục tiêu: đối chiếu `doctor`, preflight, scan, model, loop, trace, launcher/runtime trên SHA nền và các task CYC-03–07; không viết lại công cụ đã có.
Phụ thuộc: SHA nền, quyền đọc, đầu vào DEC/run đã duyệt.
Đầu ra dự kiến: một báo cáo evidence và bảng chức năng tái dùng/sửa/tạo/chưa xác minh; không raw log, credential.
Verify: đối chiếu từng kết luận với SHA/path và artifact thực; test dữ liệu giả chứng minh missing là UNKNOWN; LEAD review thủ công.
Done: liệt kê rule/spec xung đột, hành vi runtime hiện tại và quyền thực tế; chưa có nguồn thì UNKNOWN. Không probe push main hay sửa config.

### B — Hợp đồng quyền, readiness và loop
Mục tiêu: đặc tả chính sách cấp theo task/dispatch, repo/worktree, SHA, thời hạn, read/write, lệnh, Git, mạng và báo cáo; mapping lỗi, dừng ngay và loop theo DEC được OWNER chốt.
Phụ thuộc: A, OWNER quyết chính sách còn mở.
Đầu ra dự kiến: SPEC giới hạn cùng mẫu task/bàn giao; chỉ đề xuất schema sau kiểm tương thích.
Verify: đối chiếu ví dụ task hợp lệ, thiếu input, phạm vi rộng, quyền bị từ chối, verify gián đoạn, thay model và policy đã hết hạn; rà schema/đường dẫn theo rule.
Done: có bảng quyền/action, ai cấp, PASS/FAIL/UNKNOWN theo profile, ranh giới dừng và phân loại facts/loop; không áp hồi tố hay xóa lịch sử.

### C — Kiểm readiness trước giao
Mục tiêu: kiểm điều kiện môi trường và task theo B; trả kết quả riêng thay vì một PASS chung.
Phụ thuộc: B; tái dùng công cụ A phát hiện.
Phạm vi dự kiến: tối đa module kiểm readiness, test tương ứng và evidence; path chính thức xác định sau inventory/product_paths.
Verify: test task đủ/thiếu read_also, SHA/depends, write_scope, verify, quyền và model; UNKNOWN bắt buộc chặn dispatch phụ thuộc, UNKNOWN không bắt buộc không ngăn lập plan.
Done: JSON hoặc interface theo contract dự án, không đổi quyền hay gửi GO; lỗi tool không thành PASS; không log bí mật.

### D — Facts dispatch và loop
Mục tiêu: ghi sự kiện sent/queued/acknowledged, quyền, verify started/finished, liveness và settlement khi runtime cung cấp; phân loại theo rule version.
Phụ thuộc: B; chỉ phát triển sự kiện thực sự có nguồn xác minh.
Phạm vi dự kiến: module sự kiện, test và evidence; tách khỏi C khi có thể bảo đảm zero-overlap.
Verify: fixture duplicate GO, queued không chứng minh chạy, timeout/liveness UNKNOWN, verify gián đoạn, đổi model, policy thiếu; không tạo writer thứ hai hay tự cấp loop.
Done: lịch sử append-only và output trạng thái rõ; không thêm khóa vào schema hiện tại khi chưa duyệt, không ghi credential; retry runtime có trần theo quyết định.

### E — Pilot supervised và bàn giao
Mục tiêu: chạy một task giả trong repo thử trên Windows với quyền OWNER cấp theo B; LEAD quan sát và ghi rủi ro còn lại.
Phụ thuộc: C, D, profile và quyền đã được OWNER duyệt; không dùng B2 đang HOLD.
Verify: đọc nguồn SHA, ghi trong scope, chạy test mẫu, báo LEAD; thiếu quyền hoặc ngoài scope dừng; đo prompt thường lệ, retry và thời gian chờ, xác nhận không ghi secret.
Done: báo cáo số liệu và giới hạn (credential manager, mạng, git-common-dir); không khẳng định đã sandbox hoặc auto-ready. OWNER quyết có chấp nhận profile cho batch liên quan.

### F — Broker quyền cho hành động thường lệ
Mục tiêu: PoC broker giữ policy ngoài vùng WORKER ghi; xử lý yêu cầu có cấu trúc theo task/dispatch/SHA/scope; không trao shell toàn quyền.
Phụ thuộc: B, OWNER chọn auto và quyền; A xác minh runtime/cách tích hợp; script mạng phải được ngoại lệ SPEC_TOOLS hoặc đặt đúng sản phẩm được duyệt.
Phạm vi dự kiến: module policy/ủy quyền, test, evidence; chia task để ≤5 file.
Verify: hành động trong scope thành công; ngoài scope, traversal, junction, hard link, thay đích sau kiểm, giả sender, policy hết hạn và broker hỏng bị từ chối; thử repo và remote giả. Nếu Windows chưa cưỡng chế được, trả NOT_READY.
Done: chính sách thực thi được kiểm trên Windows; không tự mở rộng quyền, không lộ credential, không đụng main/tag thật. Không công bố an toàn chỉ từ prompt hoặc unit test.

### G — Cách ly verify và Git
Mục tiêu: PoC chạy code test không tin cậy với giới hạn OS theo profile, không thấy credential, Git admin thật hay mạng ngoài quyền; broker xử lý Git thật theo phạm vi nếu được duyệt.
Phụ thuộc: B/F và lựa chọn runtime OWNER; chia tiếp theo OS/cơ chế nếu vượt scope.
Verify: test giả cố đọc credential/home, ghi task khác/git-common-dir và truy cập mạng; kiểm thao tác hợp lệ hoạt động, bypass bị chặn; repo tạm riêng, không probe phá hủy repo thật.
Done: có evidence Windows, nêu giới hạn và lỗ chưa xử lý; fail closed khi cách ly không dựng được. Không tự khẳng định worktree là sandbox.

### H — Smoke end-to-end và lỗi runtime
Mục tiêu: kiểm model/runner/gateway/policy thực tế, quyền và IPC theo profile; auto phải chạy thao tác đã cấp không có prompt thường lệ nhưng ngăn thao tác cấm.
Phụ thuộc: F+G, và model đủ điều kiện theo policy hiện hành.
Verify: đọc/ghi trong scope, test sandbox, gửi/nhận đúng dispatch, Git giả; mất classifier/broker, timeout, GO trùng, metadata model thiếu; chứng minh không fail-open. Không thử ref cấm trên GitHub thật.
Done: evidence hành động đúng lẫn bị chặn, actual model của phiên, policy hash, runtime, thời điểm và rủi ro; không tính smoke là loop task sản phẩm theo policy mới nếu được OWNER chốt. Không tự cấp ngoại lệ.

### I — Kiểm định và bàn giao
Mục tiêu: REVIEWER độc lập kiểm toàn bộ phạm vi và bằng chứng, đối chiếu diff/rule/schema, trạng thái source và rủi ro; chuẩn bị đề xuất upstream.
Phụ thuộc: E và, nếu profile auto trong phạm vi đã duyệt, H; REVIEWER khác actual model của mọi WORKER trong phần kiểm theo policy.
Verify: chạy lại kiểm phù hợp trên main SHA chốt, test escape, recovery, model mismatch và injection; rà C1–C14, protected paths, không có secret.
Done: verdict có evidence, UNKNOWN không biến PASS; OWNER merge cổng theo rule. Kiểm kê cuối sau CYC-07 theo DEC-0020, OWNER duyệt từng mục trước repo mẹ.

## Giới hạn xác nhận

Đây là bản nháp review trước CHANGE, path sản phẩm, số lượng task cuối, schema và lệnh verify cụ thể cần kiểm template, product_paths, tool thực tế và DEC; không giả lập TK ID hoặc hứa hoàn thành trong một phiên. REQ-0010 được đề xuất RESOLVED_BY DEC-0027 trong nhánh; DEC và task chỉ có hiệu lực sau OWNER merge. Các task sau kiểm kê vẫn là dự thảo. Không giao WORKER hay chạy loop; không merge/đẩy main/auto-merge.



## Cập nhật lựa chọn OWNER 2026-11-16

OWNER chọn supervised trước, thử tự động trong sandbox sau; giữ rule loop hiện hành trong lúc kiểm kê, trình rule mới sau. DEC-0027 và TK-0031 trong nhánh chờ OWNER review/merge; A–I còn lại là dự thảo.
