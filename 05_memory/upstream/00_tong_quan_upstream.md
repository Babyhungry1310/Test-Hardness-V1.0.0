# H0 — Hồ sơ đề xuất cập nhật khung (Upstream)

- Trạng thái: DỰ THẢO; chưa mục nào có hiệu lực.
- Căn cứ: 04_control/decisions/DEC-0020; 04_control/requests/resolved/REQ-0007; 01_plan/SPEC_DRYRUN.md#UPSTREAM.
- Nguồn: kiểm kê đề xuất rút ra từ dry run Test-Hardness-V1.0.0; biên tập lại 2026-11-19 theo thẩm định Kaizen.
- Lộ trình thực hiện: KE_HOACH_KAIZEN.md (Đợt 1 gồm Bước 0–5, tương ứng Đ1–Đ5 dưới đây; Đợt 2–4).
- Cập nhật 2026-11-21: rà xung đột logic và nút thắt giữa H0–H4, README_GOI_KAIZEN và bản tư vấn mô hình AI Lead; nới E10 cho WORKER free có điều kiện; thêm E17–E26.
- Nơi lưu hồ sơ: [ĐƯỜNG DẪN: LEAD chốt trước gói Kaizen kế tiếp].
- Phiên bản khung nhận thay đổi: [VERSION: OWNER chốt].
- Hồ sơ được commit vào repo ở trạng thái DỰ THẢO để có SHA và đưa được vào gói Kaizen (README mục 7). DỰ THẢO nghĩa là chưa có hiệu lực; việc có mặt trong repo không làm mục nào có hiệu lực.

## 1. Tài liệu thành phần
- H1 — 01_brainstorm_va_tra_cuu_ngoai.md: vai ADVISOR, tra cứu ngoài, Basic Plan, bước LEAD tiếp nhận.
- H2 — 02_quyen_worker_va_phong_thu_injection.md: điểm dừng, mã thoát, nguyên tắc quyền, cách ly verify, cấp quyền theo batch.
- H3 — 03_ha_tang_context_va_dieu_phoi_loop.md: context, prefix, checkpoint, EOL, bảng lỗi thống nhất, tuyến model, WORKER trên tuyến free, Windows, quyền OWNER.
- H4 — 04_nhat_ky_kiem_toan_va_quan_tri_van_hanh.md: schema run và DEC, raw capture, token, chỉ số tuyến, sự cố, quét secret, linter.

## 2. Lộ trình theo đợt Kaizen
- Đ1 — đo nền và cấu hình:
  - Mô tả tối thiểu lớp hạ tầng đo token (mục 5): relay nào, 9Router, điểm đọc usage.
  - Token theo vai, task, tuyến, hạng task, đo ở một điểm cố định (H4-6, E8).
  - Tách sẵn sàng và chất lượng (H3-10).
  - EOL, -text (H3-8); bẫy Windows (H3-14); ảnh chụp môi trường (H4-5).
  - Secret scanning và push protection phía GitHub làm lớp chặn sớm; hook pre-push với detect-secrets làm ở Đ3b (H4-10, H4-11, E23).
  - Ruleset (Bước 1 của KE_HOACH_KAIZEN.md), cách đặt phụ thuộc E14.
- Đ2 — cắt tỉa luật và sổ: mỗi PROPOSAL khi chốt ghi luật bị thay hoặc xóa (cột "Thay" ở mục 3). Danh sách luật cắt: [LEAD chốt].
- Đ3a — quy ước và dữ liệu (làm trước Đ3b; Bước 3 việc 1 của KE_HOACH_KAIZEN.md):
  - Bảng lỗi thống nhất (H3-9, E18); mã 3 chặn (E16).
  - Schema run: ngữ nghĩa khóa model, khóa loại bằng chứng (H4-1, E7, E21).
  - Bổ sung DeepSeek, Nvidia Nano vào catalog ở trạng thái UNQUALIFIED, hoặc loại khỏi routing (làm sớm ở Đ2, vì SAME_MODEL cần catalog đủ).
- Đ3b — thi hành tự động:
  - validate lõi, kiểm trôi; CI chạy verify trên PR; hook pre-push (E23).
  - Điểm dừng, mã thoát (H2-1, H2-2); nguyên tắc quyền, cấp quyền theo batch (H2-3 đến H2-5, H2-7, E26); ngoại lệ sửa test có khai báo (E20).
  - Cách ly verify: lần chạy trên CI là lần chạy lại chính thức duy nhất (H2-6, E6).
  - Checkpoint, phép kiểm một writer, verify chạy lại (H3-4, H3-5, H3-12); raw capture và bằng chứng (H4-4, E22); binary nền (E24).
  - Linter còn lại (H4-11). validate làm trước state.
- Đ4 — ngữ cảnh: thứ tự prefix (H3-2); nén output (H3-7).
- Đ5 — đo lại: so với số nền của Đ1, cùng công cụ đo và cùng điểm đo.
- Đợt 2 (K4 còn lại, K5): thực thi E14, E11; E10 phần P4, ELIGIBILITY; WORKER trên tuyến free (H3-1, H3-11, H3-13, H3-16, H3-17, H4-7; E17, E19); script scan (H1-2, E2); H3-1 chi tiết DeepInfra, H3-3.
- Đợt 3 (K6): H3-6, phần ngắt mạch chung của H3-9, H4-3.
- Đợt 4 (K7): Brainstorm (H1-1, H1-3, H1-4; E1 cùng E3); khối trạng thái gửi OWNER (H4-9).
- Chưa xếp đợt, LEAD chốt: H3-15, H4-2, H4-8.
- Nút thắt có hai chỗ:
  - LEAD: rà C1–C14 bằng mắt, tự soạn gói Kaizen, chạy lại verify.
  - OWNER: là cổng tuần tự của mọi merge, mọi chốt nhóm E, gói Kaizen, điểm dừng và duyệt tra cứu; chỉ một PR lead/ mở một lúc; mỗi PR upgrade/ tăng VERSION. Với thời gian OWNER có hạn, thông lượng cả hệ bằng tốc độ merge của OWNER. Xem E25, E26.

### Ánh xạ ba trục thời gian
| Mã trong H0 | KE_HOACH_KAIZEN.md | Tiêu chí K | Chu kỳ (CYC) |
| --- | --- | --- | --- |
| Đ1 | Đợt 1, Bước 1 | K4 (ruleset), đo nền | [LEAD chốt] |
| Đ2 | Đợt 1, Bước 2 | K3 | [LEAD chốt] |
| Đ3a, Đ3b | Đợt 1, Bước 3 | K1 | [LEAD chốt] |
| Đ4 | Đợt 1, Bước 4 | K2 | [LEAD chốt] |
| Đ5 | Đợt 1, Bước 5 | đo lại | [LEAD chốt] |
| Đợt 2 | Đợt 2 | K4 còn lại, K5 | [LEAD chốt] |
| Đợt 3 | Đợt 3 | K6 | [LEAD chốt] |
| Đợt 4 | Đợt 4 | K7 | [LEAD chốt] |

- Chu kỳ sản phẩm tạm dừng trong Đợt 1, nên cột CYC chỉ có nghĩa từ Đợt 2.
- Mốc theo chu kỳ đang có trong hồ sơ: scan cho 06_sources/ dự kiến CYC-06, nay đưa vào Đợt 2 (H1-2); kiểm kê cuối theo DEC-0020 sau CYC-07 (E15 đề xuất bỏ).

## 3. Đề xuất trình OWNER
Cột cuối "Thay": luật hoặc mục bị thay, xóa khi chốt; [LEAD điền] nếu chưa xác định.

- E1 | PROPOSAL | Vai tư vấn Brainstorm đặt tên ADVISOR, không gắn model; ADVISOR chỉ đề xuất, LEAD lập DSC và soạn DEC. Chỉ áp dụng cùng lúc với E3. | Thay: [LEAD điền]
- E2 | PROPOSAL | Kết quả tra cứu ngoài vào qua 06_sources/ sau scan; DSC ghi ASSUMPTION có nguồn; bỏ kênh clipboard, thư mục tạm. | Thay: [LEAD điền]
- E3 | PROPOSAL | Basic Plan 8 trường và bước LEAD tiếp nhận (QUESTION trong DSC, tối đa 2 vòng) áp dụng ở Đợt 4; bước tiếp nhận kích hoạt theo người đề xuất nội dung, không theo người ghi vào DSC (sửa 2026-11-21). | Thay: [LEAD điền]
- E4 | PROPOSAL | WORKER dừng ngay ở mục 7.1 và khi gặp lệnh nhúng, dữ liệu thật, cài gói; điểm khác do validate bắt. "Không rõ model" chuyển sang E21 (sửa 2026-11-21). | Thay: danh sách điểm dừng trong WORKER.md, chuyển sang file template
- E5 | PROPOSAL | Lỗi quyền, môi trường không tính loop, tối đa 2 lần thử; mã thoát 0 đạt, 1 FAIL, 2 môi trường, 3 không rõ. Trần chi tiết theo bảng lỗi E18 (bổ sung 2026-11-21). | Thay: quy ước 0/1/2 ở SPEC_TOOLS#CONVENTIONS
- E6 | PROPOSAL | Mọi lần chạy verify chạy cách ly mức nhẹ; mở RSK cho cách ly đầy đủ. Bổ sung 2026-11-21: chỉ một lần chạy lại do máy, LEAD và REVIEWER đọc raw capture kèm hash, không tự chạy lại trừ khi chẩn đoán. | Thay: [LEAD điền]
- E7 | PROPOSAL | trace ghi raw capture (argv, cwd, exit, stdout, stderr, phiên bản, hash); khóa model nhận danh sách; thêm khóa loại bằng chứng. Nơi lưu và che dữ liệu theo E22; ngữ nghĩa khóa model theo E21. | Thay: [LEAD điền]
- E8 | PROPOSAL | Ghi token theo session, task, tuyến; chỉ số Cost per Accepted Task; báo cáo tách độ sẵn sàng và chất lượng. Bổ sung 2026-11-21: thêm nhãn vai và hạng task; đo ở một điểm cố định; giữ nguyên công cụ đo từ Đ1 tới Đ5. | Thay: [LEAD điền]
- E9 | PROPOSAL | Kiểm nền Windows (UTF-8 không BOM, LF cho file khung tự viết, -text cho checks/, cấm Out-File PS5.1); detect-secrets gọi từ tools/hooks; công cụ mới cài qua pip, binary theo E24. | Thay: [LEAD điền]
- E10 | PROPOSAL | Gộp tuyến đã chứng minh và sổ kiểm định tuyến vào ELIGIBILITY, ROUTE_CHECKS. Sửa 2026-11-21: tuyến miễn phí được làm WORKER cho task hạng T0, T1 khi đạt W1–W4 cho hạng đó và có tuyến trả phí dự phòng; không làm task T2, không làm REVIEWER chính, không đứng ở bước chặn xuất bản (thu hẹp DEC-0018). | Thay: câu "tuyến miễn phí không làm WORKER" của bản 2026-11-19
- E11 | PROPOSAL | Quyền riêng OWNER: merge, đẩy hoặc sửa main, thẻ git, cấu hình nhạy cảm, miễn trừ; tác tử vẫn đẩy nhánh, mở PR. Chỉ thi hành được khi có E14 và ruleset phía GitHub. | Thay: [LEAD điền]
- E12 | PROPOSAL | Không áp dụng chuỗi băm bản ghi, INDEX.jsonl, sổ quyết định OWNER riêng, mã OWNER-DEC; quyết định lâu dài thành DEC có thời hạn. Bổ sung 2026-11-21: DEC có hiệu lực khi Status là ACTIVE và chưa hết hạn; validate tính, LEAD thêm dòng RETIRED khi hết hạn. | Thay: [LEAD điền]
- E13 | PROPOSAL | Hoãn sau Kaizen: ngắt mạch tuyến chung, thống nhất relay, chuyển phiên 4 bước, nhật ký phê duyệt lệnh. Ma trận lỗi 402/429/503 chuyển vào bảng lỗi E18 (Đ3a); ngắt mạch cho riêng tuyến free làm ở Đợt 2, cùng việc đưa tuyến free làm WORKER (sửa 2026-11-21). | Thay: [LEAD điền]
- E14 | QUESTION | Xét lại DEC-0019, tách tài khoản máy, vì verify chạy code WORKER cạnh thông tin đăng nhập của OWNER? Khuyến nghị của LEAD: chốt trước E11 và E6, vì validate ở PR không bắt được thẻ, ép đẩy, merge, auto-merge. Repo dry run là public nên ruleset dùng được ở gói GitHub Free (CHƯA XÁC MINH với repo mẹ). | Thay: DEC-0019
- E15 | PROPOSAL | Sửa DEC-0020: chuyển về repo mẹ theo từng nhóm PROPOSAL đã chốt, không chờ kiểm kê cuối sau CYC-07. Chốt riêng, trước mọi nhóm khác. | Thay: DEC-0020, SPEC_DRYRUN#UPSTREAM
- E16 | QUESTION | Hook gặp mã thoát 3 (không xác định) thì chặn hay cho qua, và có đổi SPEC_TOOLS#CONVENTIONS không? Khuyến nghị của LEAD: chặn, ra BLOCKED kèm chẩn đoán, theo nguyên tắc "đóng khi lỗi" (H2-4); đổi CONVENTIONS và hook trong cùng một PR upgrade/. | Thay: SPEC_TOOLS#CONVENTIONS
- E17 | PROPOSAL | Phân hạng task T0 (cơ học), T1 (logic nhỏ, test có sẵn), T2 (thiết kế, nhiều file) trong task spec; thang leo tuyến free → trả phí rẻ → mạnh; leo bậc khi 2 FAIL logic liên tiếp, 1 CLAIM_MISMATCH, hoặc quá khung thời gian (H3-16, H3-17). | Thay: [LEAD điền]
- E18 | PROPOSAL | Bảng lỗi thống nhất đặt ở SPEC_TOOLS#CONVENTIONS: loại lỗi → mã thoát → có tính loop → trần thử → xử lý khi chạm trần (H3-9). E5 là mặc định; trần của lỗi hạ tầng là ngoại lệ có tên. | Thay: phần trần thử rời rạc ở H2-1 và H3-9
- E19 | PROPOSAL | Định nghĩa W1–W4; ROUTE_CHECKS ghi chỉ số theo hạng task (đạt lần đầu, CLAIM_MISMATCH, độ trễ, lỗi hạ tầng, Cost per Accepted Task tính cả lần thử hỏng và token LEAD); tuyến vượt ngưỡng tự về UNQUALIFIED cho hạng đó (H3-13, H4-7). | Thay: "[CẦN ĐỊNH NGHĨA]" của W1–W4
- E20 | PROPOSAL | validate cho phép sửa test có sẵn khi task spec đã khai trước danh sách test được đổi và lý do, được duyệt ở PLAN_GO (H2-2). | Thay: [LEAD điền]
- E21 | PROPOSAL | Model thực tế do preflight hoặc relay xác minh từ metadata response, không phải điểm dừng của WORKER; mỗi phần tử của khóa model là mã catalog của một model thực tế đã xác minh trong run (H2-2, H4-1). | Thay: điểm dừng "không xác định được model thực tế"
- E22 | PROPOSAL | Bằng chứng: bản thô kèm hash ở <project>.local; commit bản đã che kèm hash của cả hai; end-of-file-fixer, mixed-line-ending loại 03_output/**/checks/; quy tắc LF chỉ áp file khung tự viết, raw capture lưu nguyên byte (H3-8, H4-4, H4-10, H4-11). | Thay: [LEAD điền]
- E23 | PROPOSAL | Quét secret ở pre-push vì repo public: đẩy nhánh đã là công khai; preflight hoặc github_audit kiểm lại phòng hook bị bỏ qua (H4-10). | Thay: mốc "trước khi mở PR" ở H4-10
- E24 | PROPOSAL | Danh sách binary nền đã duyệt (Git, Python, pwsh 7.4, 9Router, Codex CLI, [LEAD bổ sung]); binary mới cần DEC; công cụ Python mới cài qua pip (H3-14). | Thay: câu "cần binary ngoài, trái H3 mục 14" ở H4
- E25 | QUESTION | Cho một PR upgrade/ gom nhiều DEC đã chốt và chỉ tăng harness/VERSION khi phát hành, thay vì mỗi PR một lần? Đây là đổi ràng buộc cố định ở README mục 6. | Thay: ràng buộc "mỗi PR upgrade/ tăng VERSION"
- E26 | PROPOSAL | Lượt duyệt PLAN_GO là lần cấp quyền cho cả batch; manifest quyền mỗi task do script suy từ write_scope, lệnh verify, đầu vào đã nêu (H2-3, H2-4). | Thay: "lượt merge task của OWNER là lần cấp quyền"

## 4. Quy trình chuyển giao về repo mẹ
- Bước 0: commit H0–H4 ở trạng thái DỰ THẢO vào [ĐƯỜNG DẪN: LEAD chốt] để hồ sơ có SHA.
- Bước 1: OWNER chốt riêng E15, vì E15 quy định cách chốt các mục còn lại. Tới khi E15 được chốt, DEC-0020 hiện hành vẫn áp dụng.
- Bước 2: LEAD đưa các mục còn lại vào một DSC khi không còn PR lead/ nào khác đang mở (harness/tools/PREFLIGHT.md dòng 15).
- Bước 3: OWNER chốt theo nhóm; mỗi nhóm được chốt thành một DEC. Thứ tự khuyến nghị: E14 trước E11; E18 trước E5, E16; E19 trước E10, E17; E1 cùng E3.
- Bước 4: mỗi nhóm đã chốt có một PR upgrade/ ở repo thử; sau khi merge, một PR tương ứng sang repo mẹ Hardness-V1.0.0. Nếu E25 được chấp nhận, một PR upgrade/ có thể gom nhiều nhóm và VERSION chỉ tăng khi phát hành.
- Mọi đổi schema (run, decision) ghi mức MINOR, đi qua upgrade/, chỉ áp từ mốc kiểm.

## 5. Điểm mù: hạ tầng thực thi chưa được khung mô tả
Nhãn: GIỮ (phần đo token) | Đợt: Đ1 (mô tả tối thiểu), K6 (phần còn lại) | PROPOSAL: không
- Hồ sơ nhắc tới các thành phần khung chưa ghi nhận: relay_p4, Codex CLI, DeepInfra, Nvidia Nano, pwsh 7.4.
- DeepSeek và Nvidia Nano đã được dùng nhưng không có trong MODEL_CATALOG. Phải bổ sung ở trạng thái UNQUALIFIED hoặc loại khỏi routing trước Đ3b, nếu không run dùng chúng sẽ bị validate chặn.
- Đ1 ghi token qua relay (H4-6), mà relay đang có nhiều bản (H3-6). Cần mô tả tối thiểu trước Đ1: bản relay nào đang chạy, 9Router, điểm đọc usage cố định. Nếu điểm đo đổi giữa Đ1 và Đ5, hai số không so được.
- Phần mô tả đầy đủ và thống nhất relay vẫn thuộc K6.
