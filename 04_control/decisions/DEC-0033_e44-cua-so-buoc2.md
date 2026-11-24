---
schema: 1
id: DEC-0033
date: 2026-11-24
title: "Cửa sổ trước Bước 2 — E44 linh hoạt model/review, V-RESP, quy tắc vận hành Đợt 1"
proposed_by: LEAD
decided_by: OWNER
cycle: CYC-08
origin: "DSC-20261121-kzn1#E44"
supersedes: "DEC-0018"
cancels: []
waives: []
affects: [DEC-0032, DEC-0008, "06_sources/SRC-0003_kaizen-chi-tiet-dot1.md", "01_plan/PLAN.md", "harness/MODEL_POLICY.md", "harness/rules/LEAD.md", "harness/rules/REVIEWER.md", "harness/rules/WORKER.md", "03_output/CYC-08/checks/baseline_session_spec.md", "04_control/STATE.md"]
keywords: [e44, model-flex, review-class, v-resp, cua-so-thay-doi]
---
## Status (newest first)
- 2026-11-24 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
- L1.1 xong, OWNER duyệt O1.5 (2026-11-23); điểm đo chuyển sang bảng `usageHistory` của 9Router (F06).
- E44 (DSC-20261121-kzn1) áp vận hành từ 2026-11-23; luật khung và DEC-0018 chưa đổi theo (F12).
- Cửa sổ thay đổi sau TK-0058 (#101), trước Bước 2: gom các phát hiện loại BƯỚC KẾ của sổ phát hiện Kaizen Đợt 1 (mã F, sổ giữ ngoài repo; bản chụp vào `03_output/CYC-08/checks/` ở PR kế tiếp).
- Bước 2 vướng: lệnh verify trỏ script chưa có trong repo (F47); model thực tế đang dùng không hợp lệ theo `MODEL_POLICY` (F46).
- OWNER trả lời Q1–Q8 ngày 2026-11-24: đồng ý khuyến nghị Q1–Q5, Q7, Q8; Q6 chốt Loại F43, F45–F47 = BƯỚC KẾ, F44 = ĐỢT SAU.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- A: mỗi nhóm phát hiện một DEC. Loại: trái quy tắc "một DEC cho cả lô" của cửa sổ thay đổi.
- B: một DEC chép đủ văn luật mới. Loại: quá dài, lặp nội dung với luật (F30).
- C (chọn): một DEC, sáu nhóm, mỗi quy tắc một dòng kèm mã F; văn luật sửa ở task sau.
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale

### A. Model và review (F05, F11, F12, F25, F42, F43, F46)
- Giữ điểm 1, 3, 5 của DEC-0018 (xem `04_control/decisions/superseded/DEC-0018_model-selection-per-assignment.md`, mục RATIONALE). Điểm 2 và 4 bị thay bởi các dòng dưới.
- Ba loại review theo E44: Brainstorm và Planning bắt buộc review, OWNER chọn REVIEWER khác họ, hoặc MERGE, hoặc tự review; phiếu WORKER qua cổng máy 4 điểm do LEAD tự chạy.
- Phiếu WORKER chạm vùng 🔒 hoặc sổ (DEC, RSK, REQ) tính là review bắt buộc, báo OWNER bằng mẫu CẦN REVIEW.
- Nguồn model thực tế hợp lệ: nhật ký công cụ của phiên, hoặc `usageHistory` của 9Router đọc bằng `usage_9router.py` đúng khung giờ dispatch (V-RESP).
- Chuỗi `<tuyến>/<model>` bỏ tiền tố tuyến rồi so mã; quy tắc "có / thì UNKNOWN" không áp cho V-RESP.
- Khai V-RESP phải kèm CSV và khung giờ, do LEAD chạy. Tự khai không có CSV tính là CHƯA XÁC MINH (F43).
- CHƯA XÁC MINH: dùng được cho phiếu WORKER đạt cổng máy; không dùng cho vai bắt buộc review hay vai được đo.
- Vai cần xác minh model chỉ giao cho tuyến mà `usage_9router.py` đã trả dòng khớp model ở lần kiểm agent-tools gần nhất; lần kiểm ghi vào ROUTE_CHECKS với `source: usageHistory`. Quy tắc theo bằng chứng log, không theo tên họ model (F25 là một trường hợp).
- Họ = khóa `group` của catalog (grok, gpt, gemini, claude…). REVIEWER khác họ với người soạn. `group` là `unverified` thì hỏi OWNER.
- SRC-0005 là danh sách ưu tiên; MODEL_CATALOG là sổ dữ kiện quyết định đủ điều kiện. Tuyến không có log không đủ điều kiện cho vai cần xác minh.
- REVIEWER chấm theo checklist đóng băng lúc giao; lỗi ngoài checklist ghi WARN (F05). REVIEWER tự lấy nguồn chuẩn từ mục lục, không dùng nguồn người làm đưa (F42).

### B. Đo (F09)
- L5.1 đo theo cặp: khung @ `7ad7aa6` và khung sau TK-0050, cùng cặp model có sẵn lúc đó, 3 phiên × 2 lần mỗi khung (12 lượt); không so trực tiếp L1.1 với L5.1.
- Quyết định OWNER 2026-11-23: WORKER Session 3 của L1.1 đổi từ gemini sang grok vì tuyến gemini không có log 9Router.
- Phần còn lại của spec đo (F06, F08, F31) làm ở cửa sổ trước Bước 4.

### C. Nguồn và quét (F20, F33, F38, F39)
- Nguồn bị QUARANTINE do câu cấm hoặc câu mô tả: sanitize theo tiền lệ TK-0036, trên bản sao; bản cách ly giữ nguyên.
- Mỗi lần sanitize ghi cụm cần tránh vào danh sách cụm của thư mục làm việc để trả về người soạn; người soạn chạy `tools/scan.py` trước khi nộp.
- Hash chỉ dùng cho đầu vào đóng băng, bằng chứng đo, file chép nguyên văn; ghi 12 ký tự đầu.
- File vào repo phải qua kiểm đường dẫn máy (`verify_doc_artifact.py`, kiểm mặc định).

### D. Thẻ task và preflight (F15, F40, F47)
- `line_budget` chỉ tính dòng tự viết; task chép nguyên văn ghi riêng kích thước nguồn.
- PREFLIGHT 5 mục là điều kiện giao phiếu; thêm điều kiện: lệnh verify chạy được trên checkout sạch @ `origin/main`.
- "Kế hoạch sẵn sàng" phải có danh sách giả định đã thăm dò, mỗi giả định kèm bằng chứng; áp từ thẻ đầu Bước 3.
- Đồ thị batch: thêm B1b3a (TK-0060) và B1b4 (TK-0059 thu hẹp, trước B2a); phần `--base-ref` tách thành TK-0061 ở B3a1.

### E. Vận hành tác tử (F10, F19, F21, F34, F35)
- `git fetch` và ghi SHA `origin/main` đầu mỗi phiên LEAD và mỗi lượt đo.
- "commit" chỉ dùng cho git commit; file làm việc ngoài repo liệt kê trong mục lục thư mục làm việc.
- Mỗi lúc một việc chính. Tin nhắn giữa tác tử theo khung TỪ/ĐẾN/LOẠI/MÃ/REF/CẦN LÀM/ĐẦU VÀO/ĐẦU RA/DỪNG KHI/TRẢ LỜI.
- Vòng tự động: OWNER merge PR thẻ đầu Bước được coi là `Go` cho các phiếu WORKER không chạm 🔒 của Bước đó; phiếu chạm 🔒 vẫn chờ lệnh OWNER.
- Một lần đổi tên file (git rename) tính là 1 path trong write_scope.

### F. STATE và sổ (F28, F32, F36, F37, F45)
- STATE chỉ ghi hiện tại, ≤ 300 từ, không BOM, ghi đè; lịch sử trỏ tới thẻ cycle; mục 4 lấy từ đồ thị batch.
- DEC và DSC theo `harness/schemas/` và STATUS_GRAMMAR. Khóa `supersedes` chỉ ghi mã DEC; dòng kế hoạch bị thay ghi ở mục "Thay thế" và `affects`.

### Thay thế
- DEC-0018 (khóa `supersedes`): điểm 2 (REVIEWER cho mọi phần, chỉ khác mã model) và điểm 4 (không rõ model thực tế thì dừng).
- Dòng L5.1 của P5 trong SRC-0003 (so trực tiếp với L1.1): thay bằng mục B.
- `harness/rules/LEAD.md` luật 27, 30; `harness/rules/REVIEWER.md` luật 2 (phần ai chỉ định REVIEWER); `harness/rules/WORKER.md` luật 2 (phần `Go` từng task).
- `harness/MODEL_POLICY.md` mục SAME_MODEL, ELIGIBILITY, ROUTE_CHECKS, REQUESTED_ACTUAL, NO_MODEL, REVIEWER_INDEPENDENCE ở các điểm trái mục A.
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
- Có hiệu lực khi TK-0060 merge. Văn luật sửa ở TK-0049 (LEAD.md) và thẻ Bước 4 cho REVIEWER.md, WORKER.md, MODEL_POLICY.md. Tới lúc đó, chỗ luật cũ trái DEC-0033 thì DEC-0033 thắng.
- DEC-0018 chuyển vào `superseded/` với dòng `SUPERSEDED_BY DEC-0033`.
- TK-0040 thêm code `grok-4.5`, `gpt-6-luna` kèm `group` vào catalog; ROUTE_CHECKS ghi `source: usageHistory`.
- DEC-0008 hết căn cứ: retire cùng DEC-0007 ở TK-0039; OWNER cập nhật danh sách O2.2.
- PR kế tiếp (`lead/`, nhỏ): sửa khuôn DEC-0032 (thêm dòng ACTIVE, `supersedes` về rỗng) và bản chụp sổ phát hiện đã sanitize.
- Hoãn: tái cấu trúc SRC (F30) tới cửa sổ trước Bước 3; spec đo tới cửa sổ trước Bước 4; khuôn dòng E44 cũ trong DSC (F44) để Đợt sau.
<!-- END: CONSEQUENCES -->
