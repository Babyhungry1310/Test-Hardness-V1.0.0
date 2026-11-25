Bản tham khảo 2026-11-22. Nguồn hiện hành: SRC-0003 P6d, DEC-0032.

# H0 — Hồ sơ đề xuất cập nhật khung (Upstream)

- Trạng thái: DỰ THẢO cho các E chưa có trạng thái. E đã chốt ghi trạng thái ở cuối dòng (README_GOI_KAIZEN mục 4).
- Căn cứ: 04_control/decisions/DEC-0020; 04_control/requests/resolved/REQ-0007; 01_plan/SPEC_DRYRUN.md#UPSTREAM; DSC-20261121-kzn1; DEC-0031.
- Nguồn: kiểm kê đề xuất rút ra từ dry run Test-Hardness-V1.0.0; biên tập lại 2026-11-19 theo thẩm định Kaizen.
- Lộ trình thực hiện: KE_HOACH_KAIZEN.md; task chi tiết của Đợt 1 ở SRC-0003 (TK-0036…TK-0052, chạy trong CYC-08).
- Cập nhật 2026-11-21: rà xung đột logic và nút thắt giữa H0–H4, README_GOI_KAIZEN và bản tư vấn mô hình AI Lead; nới E10 cho WORKER free có điều kiện; thêm E17–E26.
- Cập nhật 2026-11-22: ghi trạng thái E14, E15 theo DEC-0031; ánh xạ lộ trình với task của SRC-0003; thêm E27–E43 (cơ chế lấy từ GSD Core, xem GSD_CORE_DE_XUAT_KAIZEN.md và PHUONG_AN_TICH_HOP_GSD_DOT1.md).
- Nơi lưu hồ sơ: 05_memory/upstream/ (nạp ở TK-0036, Bước 0); bản đối chiếu đã sanitize trong 06_sources/. File này là bản đề xuất cập nhật; LEAD đồng bộ vào bản trong repo, giữ phần đã sanitize.
- Phiên bản khung nhận thay đổi: [VERSION: OWNER chốt]. Theo SRC-0003, TK-0041 tăng VERSION lên 1.0.3.
- Trạng thái E1–E13, E16–E26: [LEAD cập nhật theo DSC-20261121-kzn1]. Bản tóm tắt hiện trạng 2026-11-22 chỉ nêu kết quả của E14, E15.

## 1. Tài liệu thành phần
- H1 — 01_brainstorm_va_tra_cuu_ngoai.md: vai ADVISOR, tra cứu ngoài, Basic Plan, bước LEAD tiếp nhận.
- H2 — 02_quyen_worker_va_phong_thu_injection.md: điểm dừng, mã thoát, nguyên tắc quyền, cách ly verify, cấp quyền theo batch.
- H3 — 03_ha_tang_context_va_dieu_phoi_loop.md: context, prefix, checkpoint, EOL, bảng lỗi thống nhất, tuyến model, WORKER trên tuyến free, Windows, quyền OWNER.
- H4 — 04_nhat_ky_kiem_toan_va_quan_tri_van_hanh.md: schema run và DEC, raw capture, token, chỉ số tuyến, sự cố, quét secret, linter.
- Tài liệu liên quan:
  - GSD_CORE_DE_XUAT_KAIZEN.md: 17 cơ chế M1–M17 trích từ GSD Core, ứng với E27–E43.
  - PHUONG_AN_TICH_HOP_GSD_DOT1.md: phân bổ E27–E43 vào task của CYC-08 và danh sách việc cần làm.

## 2. Lộ trình theo đợt Kaizen

Theo SRC-0003 (bản tóm tắt hiện trạng 2026-11-22). Mỗi dòng ghi task và các E được thi hành ở task đó. Bước 0 (TK-0036, TK-0037; batch B0a, B0b) đã xong.

- Đ1 — Bước 1, đo nền và cấu hình:
  - TK-0038 (B1a): đóng băng đặc tả 3 phiên chuẩn. Ghi kèm điểm đo cố định (mục 5) và các chỉ số đo cho E27, E28, E30 (E8).
  - O1.1–O1.4 (OWNER, giao diện GitHub): ruleset cho main và thẻ, quyền tối thiểu cho tài khoản tác tử, secret scanning, push protection (E11, E14, E23). Xuất cấu hình ruleset làm mốc cho TK-0054 (E43).
  - L1.1: chạy 3 phiên chuẩn × 2 lần; bảng token nền theo vai (E8).
  - TK-0053 (B1b, mới): DSC và DEC-0032 cho E27–E43; đặt sau L1.1.
  - Ảnh chụp môi trường (H4-5): [LEAD xác nhận có trong SRC-0003; nếu không, ghi cùng L1.1].
- Đ2 — Bước 2, cắt tỉa:
  - TK-0039: retire 5 DEC về model.
  - TK-0040: rút gọn mục 3 của STATE, cập nhật catalog model (thêm DeepSeek, Nvidia Nano ở trạng thái UNQUALIFIED hoặc loại khỏi routing), đánh dấu vùng AUTO trong STATE (E29).
  - TK-0041: gộp §9 của LEAD.md, tăng VERSION.
  - Mỗi PROPOSAL khi chốt ghi luật bị thay hoặc xóa (cột "Thay" ở mục 3).
- Đ3a — Bước 3, quy ước (làm trước Đ3b):
  - TK-0042: schema run MINOR (E7, E21, E40), template điểm dừng (E4), mã thoát và bảng lỗi (E5, E16, E18, E35, E36), khai báo ON_CRASH cho hook (E37).
- Đ3b — Bước 3, thi hành tự động:
  - TK-0043: validate lõi (schema run, loop, C1–C3, SAME_MODEL); thêm kiểm lời tự báo (E40), phủ DoD bằng test (E33), mã 66 và phát hiện danh sách file bị cắt (E36, E43), test đối chứng dương cho mỗi kiểm (E43).
  - TK-0044: kiểm trôi (một PR lead/ mở, DEC liên tục, VERSION, SHA của STATE); thêm `state validate` (E29), sổ chỉ thêm dòng (E38).
  - TK-0045: CI `check.yml` mức cảnh báo, hook pre-push (E23, E37), quét injection trên file `.md` thay đổi (E39), khẳng định runner do GitHub cung cấp (E43, tùy nơi chạy verify).
  - TK-0046: cách ly verify mức nhẹ (E6), bẫy Windows UTF-8 và LF (E9, H3-8, H3-14), tên file bí mật không phân biệt hoa thường (E38).
  - TK-0047: kiểm tĩnh C9 (con trỏ và origin).
  - TK-0054 (B3g, mới): ruleset thành file JSON và script áp; github_audit so khai báo với thực tế (E43).
  - Chưa thấy task trong bản tóm tắt SRC-0003: E20 (sửa test có khai báo), E22 (raw capture, bằng chứng), E24 (binary nền), E26 (cấp quyền theo batch), H3-4 (checkpoint máy), H3-5 (một writer), H4-11 (linter). [LEAD đối chiếu DSC-20261121-kzn1: ghi task hoặc ghi hoãn.]
- Đ4 — Bước 4, ngữ cảnh:
  - TK-0048: tách phụ lục HARNESS sang RATIONALE.md, tách mục lớn thành file riêng; frontmatter đủ để ra quyết định (E28).
  - TK-0049: viết lại LEAD.md ≤ 1.300 từ; luật trả về một dòng, độ sâu đọc, ba lý do tách việc, template checkpoint (E27, E28, E30, E31).
  - TK-0050: tự động hóa C5, C7 (đo theo từ), C12, C13; một hàm đo dùng chung, có đối chứng dương (E43).
  - Thứ tự prefix (H3-2), nén output (H3-7): [LEAD xác nhận nằm trong task nào].
- Đ5 — Bước 5, đo lại:
  - TK-0051: chạy lại 3 phiên chuẩn với cùng spec, cùng điểm đo.
  - TK-0052: báo cáo trước và sau; mốc ratchet (E43); cổng OWNER Đ5-C.
- Đợt 2 (K4 còn lại, K5):
  - E10 phần P4, ELIGIBILITY; WORKER trên tuyến free (H3-1, H3-11, H3-13, H3-16, H3-17, H4-7; E17, E19).
  - Phần còn lại của cơ chế GSD: E30 (script giám sát ngữ cảnh), E31 (ngưỡng cỡ task), E32, E33 (phủ yêu cầu, checker ngữ nghĩa), E34, E35 (script phân loại lỗi, thang nhà cung cấp cho tuyến free), E38 (đọc trước khi sửa), E39 (quét 06_sources/ mức chặn), E41, E42.
  - Script scan (H1-2, E2); H3-1 chi tiết DeepInfra; H3-3.
- Đợt 3 (K6): H3-6, phần ngắt mạch chung của H3-9, H4-3; E35 thang nhà cung cấp cho mọi tuyến.
- Đợt 4 (K7): Brainstorm (H1-1, H1-3, H1-4; E1 cùng E3); khối trạng thái gửi OWNER (H4-9); E27 (payload `init`), E29 (`state sync`), E42 (sinh task sửa từ gap).
- Chưa xếp đợt, LEAD chốt: H3-15, H4-2, H4-8.
- Nút thắt có hai chỗ:
  - LEAD: rà C1–C14 bằng mắt, tự soạn gói Kaizen, chạy lại verify.
  - OWNER: là cổng tuần tự của mọi merge, mọi chốt nhóm E, gói Kaizen, điểm dừng và duyệt tra cứu; chỉ một PR lead/ mở một lúc; mỗi PR upgrade/ tăng VERSION. Với thời gian OWNER có hạn, thông lượng cả hệ bằng tốc độ merge của OWNER. Xem E25, E26.

### Ánh xạ ba trục thời gian
| Mã trong H0 | KE_HOACH_KAIZEN.md | Task, batch (SRC-0003) | Tiêu chí K | Chu kỳ |
| --- | --- | --- | --- | --- |
| — | Đợt 1, Bước 0 | TK-0036, TK-0037 (B0a, B0b) — đã xong | — | CYC-08 |
| Đ1 | Đợt 1, Bước 1 | TK-0038 (B1a), O1.1–O1.4, L1.1, TK-0053 (B1b) | K4 (ruleset), đo nền | CYC-08 |
| Đ2 | Đợt 1, Bước 2 | TK-0039–TK-0041 (B2a–B2c) | K3 | CYC-08 |
| Đ3a, Đ3b | Đợt 1, Bước 3 | TK-0042–TK-0047 (B3a–B3f), TK-0054 (B3g) | K1 | CYC-08 |
| Đ4 | Đợt 1, Bước 4 | TK-0048–TK-0050 (B4a–B4c) | K2 | CYC-08 |
| Đ5 | Đợt 1, Bước 5 | TK-0051–TK-0052 (B5a, B5b) | đo lại | CYC-08 |
| Đợt 2 | Đợt 2 | [LEAD lập] | K4 còn lại, K5 | [LEAD chốt] |
| Đợt 3 | Đợt 3 | [LEAD lập] | K6 | [LEAD chốt] |
| Đợt 4 | Đợt 4 | [LEAD lập] | K7 | [LEAD chốt] |

- Chu kỳ sản phẩm tạm dừng trong CYC-08 (quyết định chặn 1 của DEC-0031).
- Nếu phải tách TK-0042 hoặc TK-0045 vì write_scope vượt 5 path, batch tách ra đặt tên B3a2, B3d2 (PHUONG_AN_TICH_HOP_GSD_DOT1.md mục 3).
- Mốc theo chu kỳ cũ trong hồ sơ: scan cho 06_sources/ dự kiến CYC-06, nay đưa vào Đợt 2 (H1-2); kiểm kê cuối theo DEC-0020 sau CYC-07, nay bỏ theo E15.

## 3. Đề xuất trình OWNER
Cột cuối "Thay": luật hoặc mục bị thay, xóa khi chốt; [LEAD điền] nếu chưa xác định. Trạng thái ghi sau dấu → theo README_GOI_KAIZEN mục 4.

- E1 | PROPOSAL | Vai tư vấn Brainstorm đặt tên ADVISOR, không gắn model; ADVISOR chỉ đề xuất, LEAD lập DSC và soạn DEC. Chỉ áp dụng cùng lúc với E3. | Thay: [LEAD điền]
- E2 | PROPOSAL | Kết quả tra cứu ngoài vào qua 06_sources/ sau scan; DSC ghi ASSUMPTION có nguồn; bỏ kênh clipboard, thư mục tạm. | Thay: [LEAD điền]
- E3 | PROPOSAL | Basic Plan 8 trường và bước LEAD tiếp nhận (QUESTION trong DSC, tối đa 2 vòng) áp dụng ở Đợt 4; bước tiếp nhận kích hoạt theo người đề xuất nội dung, không theo người ghi vào DSC (sửa 2026-11-21). | Thay: [LEAD điền]
- E4 | PROPOSAL | WORKER dừng ngay ở mục 7.1 và khi gặp lệnh nhúng, dữ liệu thật, cài gói; điểm khác do validate bắt. "Không rõ model" chuyển sang E21 (sửa 2026-11-21). Bổ sung 2026-11-22: template ghi luật lệch kế hoạch chỉ trong write_scope và luật "không thử tên gói gần giống" (H2 mục 2). | Thay: danh sách điểm dừng trong WORKER.md, chuyển sang file template
- E5 | PROPOSAL | Lỗi quyền, môi trường không tính loop, tối đa 2 lần thử; mã thoát 0 đạt, 1 FAIL, 2 môi trường, 3 không rõ. Trần chi tiết theo bảng lỗi E18 (bổ sung 2026-11-21). Thêm mã 66 theo E36 (2026-11-22). | Thay: quy ước 0/1/2 ở SPEC_TOOLS#CONVENTIONS
- E6 | PROPOSAL | Mọi lần chạy verify chạy cách ly mức nhẹ; mở RSK cho cách ly đầy đủ. Bổ sung 2026-11-21: chỉ một lần chạy lại do máy, LEAD và REVIEWER đọc raw capture kèm hash, không tự chạy lại trừ khi chẩn đoán. Bổ sung 2026-11-22: nơi chạy lần đó cần chốt — cách ly trên máy (SRC-0003, TK-0046) hay trên CI (KE_HOACH). | Thay: [LEAD điền]
- E7 | PROPOSAL | trace ghi raw capture (argv, cwd, exit, stdout, stderr, phiên bản, hash); khóa model nhận danh sách; thêm khóa loại bằng chứng. Nơi lưu và che dữ liệu theo E22; ngữ nghĩa khóa model theo E21. Lưu ý 2026-11-22: cách ghi "actual_model" và "evidence.kind" ở TK-0042 cần kiểm theo H4 mục 1. | Thay: [LEAD điền]
- E8 | PROPOSAL | Ghi token theo session, task, tuyến; chỉ số Cost per Accepted Task; báo cáo tách độ sẵn sàng và chất lượng. Bổ sung 2026-11-21: thêm nhãn vai và hạng task; đo ở một điểm cố định; giữ nguyên công cụ đo từ Đ1 tới Đ5. | Thay: [LEAD điền]
- E9 | PROPOSAL | Kiểm nền Windows (UTF-8 không BOM, LF cho file khung tự viết, -text cho checks/, cấm Out-File PS5.1); detect-secrets gọi từ tools/hooks; công cụ mới cài qua pip, binary theo E24. | Thay: [LEAD điền]
- E10 | PROPOSAL | Gộp tuyến đã chứng minh và sổ kiểm định tuyến vào ELIGIBILITY, ROUTE_CHECKS. Sửa 2026-11-21: tuyến miễn phí được làm WORKER cho task hạng T0, T1 khi đạt W1–W4 cho hạng đó và có tuyến trả phí dự phòng; không làm task T2, không làm REVIEWER chính, không đứng ở bước chặn xuất bản (thu hẹp DEC-0018). | Thay: câu "tuyến miễn phí không làm WORKER" của bản 2026-11-19
- E11 | PROPOSAL | Quyền riêng OWNER: merge, đẩy hoặc sửa main, thẻ git, cấu hình nhạy cảm, miễn trừ; tác tử vẫn đẩy nhánh, mở PR. Chỉ thi hành được khi có E14 và ruleset phía GitHub; E14 đã chốt (DEC-0031), ruleset bật ở O1.1–O1.4. | Thay: [LEAD điền]
- E12 | PROPOSAL | Không áp dụng chuỗi băm bản ghi, INDEX.jsonl, sổ quyết định OWNER riêng, mã OWNER-DEC; quyết định lâu dài thành DEC có thời hạn. Bổ sung 2026-11-21: DEC có hiệu lực khi Status là ACTIVE và chưa hết hạn; validate tính, LEAD thêm dòng RETIRED khi hết hạn. | Thay: [LEAD điền]
- E13 | PROPOSAL | Hoãn sau Kaizen: ngắt mạch tuyến chung, thống nhất relay, chuyển phiên 4 bước, nhật ký phê duyệt lệnh. Ma trận lỗi 402/429/503 chuyển vào bảng lỗi E18 (Đ3a); ngắt mạch cho riêng tuyến free làm ở Đợt 2, cùng việc đưa tuyến free làm WORKER (sửa 2026-11-21). | Thay: [LEAD điền]
- E14 | QUESTION | Xét lại DEC-0019, tách tài khoản máy, vì verify chạy code WORKER cạnh thông tin đăng nhập của OWNER? Khuyến nghị của LEAD: chốt trước E11 và E6, vì validate ở PR không bắt được thẻ, ép đẩy, merge, auto-merge. Repo dry run là public nên ruleset dùng được ở gói GitHub Free (CHƯA XÁC MINH với repo mẹ). | Thay: DEC-0019 → ACCEPTED (tách tài khoản) → DEC-0031; RSK-0004 hạn xử lý 2026-11-26
- E15 | PROPOSAL | Sửa DEC-0020: chuyển về repo mẹ theo từng nhóm PROPOSAL đã chốt, không chờ kiểm kê cuối sau CYC-07. Chốt riêng, trước mọi nhóm khác. | Thay: DEC-0020, SPEC_DRYRUN#UPSTREAM → ACCEPTED → DEC-0031
- E16 | QUESTION | Hook gặp mã thoát 3 (không xác định) thì chặn hay cho qua, và có đổi SPEC_TOOLS#CONVENTIONS không? Khuyến nghị của LEAD: chặn, ra BLOCKED kèm chẩn đoán, theo nguyên tắc "đóng khi lỗi" (H2-4); đổi CONVENTIONS và hook trong cùng một PR upgrade/. Bổ sung 2026-11-22: cụ thể hóa thành E36 (mã 66) và E37 (khai báo ON_CRASH theo từng hook). | Thay: SPEC_TOOLS#CONVENTIONS
- E17 | PROPOSAL | Phân hạng task T0 (cơ học), T1 (logic nhỏ, test có sẵn), T2 (thiết kế, nhiều file) trong task spec; thang leo tuyến free → trả phí rẻ → mạnh; leo bậc khi 2 FAIL logic liên tiếp, 1 CLAIM_MISMATCH, hoặc quá khung thời gian (H3-16, H3-17). Bổ sung 2026-11-22: CLAIM_MISMATCH áp cho mọi run từ Bước 3 (E40); tách hai thang leo (E34, E35); thử tách task trước khi leo (E42). | Thay: [LEAD điền]
- E18 | PROPOSAL | Bảng lỗi thống nhất đặt ở SPEC_TOOLS#CONVENTIONS: loại lỗi → mã thoát → có tính loop → trần thử → xử lý khi chạm trần (H3-9). E5 là mặc định; trần của lỗi hạ tầng là ngoại lệ có tên. | Thay: phần trần thử rời rạc ở H2-1 và H3-9
- E19 | PROPOSAL | Định nghĩa W1–W4; ROUTE_CHECKS ghi chỉ số theo hạng task (đạt lần đầu, CLAIM_MISMATCH, độ trễ, lỗi hạ tầng, Cost per Accepted Task tính cả lần thử hỏng và token LEAD); tuyến vượt ngưỡng tự về UNQUALIFIED cho hạng đó (H3-13, H4-7). | Thay: "[CẦN ĐỊNH NGHĨA]" của W1–W4
- E20 | PROPOSAL | validate cho phép sửa test có sẵn khi task spec đã khai trước danh sách test được đổi và lý do, được duyệt ở PLAN_GO (H2-2). | Thay: [LEAD điền] | Trạng thái 2026-11-25 (O2.1, DEC-0034): ACCEPTED → TK-0043
- E21 | PROPOSAL | Model thực tế do preflight hoặc relay xác minh từ metadata response, không phải điểm dừng của WORKER; mỗi phần tử của khóa model là mã catalog của một model thực tế đã xác minh trong run (H2-2, H4-1). | Thay: điểm dừng "không xác định được model thực tế" | Trạng thái 2026-11-25 (O2.1, DEC-0034): ACCEPTED (DEC-0033 A, V-RESP do LEAD)
- E22 | PROPOSAL | Bằng chứng: bản thô kèm hash ở <project>.local; commit bản đã che kèm hash của cả hai; end-of-file-fixer, mixed-line-ending loại 03_output/**/checks/; quy tắc LF chỉ áp file khung tự viết, raw capture lưu nguyên byte (H3-8, H4-4, H4-10, H4-11). | Thay: [LEAD điền] | Trạng thái 2026-11-25 (O2.1, DEC-0034): HOÃN Đợt 2 (cần hạ tầng .local)
- E23 | PROPOSAL | Quét secret ở pre-push vì repo public: đẩy nhánh đã là công khai; preflight hoặc github_audit kiểm lại phòng hook bị bỏ qua (H4-10). | Thay: mốc "trước khi mở PR" ở H4-10 | Trạng thái 2026-11-25 (O2.1, DEC-0034): ACCEPTED → TK-0045, TK-0056
- E24 | PROPOSAL | Danh sách binary nền đã duyệt (Git, Python, pwsh 7.4, 9Router, Codex CLI, [LEAD bổ sung]); binary mới cần DEC; công cụ Python mới cài qua pip (H3-14). | Thay: câu "cần binary ngoài, trái H3 mục 14" ở H4 | Trạng thái 2026-11-25 (O2.1, DEC-0034): ACCEPTED → TK-0046
- E25 | QUESTION | Cho một PR upgrade/ gom nhiều DEC đã chốt và chỉ tăng harness/VERSION khi phát hành, thay vì mỗi PR một lần? Đây là đổi ràng buộc cố định ở README mục 6. | Thay: ràng buộc "mỗi PR upgrade/ tăng VERSION" | Trạng thái 2026-11-25 (O2.1, DEC-0034): REJECTED: giữ "mỗi PR upgrade/ tăng VERSION một lần"
- E26 | PROPOSAL | Lượt duyệt PLAN_GO là lần cấp quyền cho cả batch; manifest quyền mỗi task do script suy từ write_scope, lệnh verify, đầu vào đã nêu (H2-3, H2-4). | Thay: "lượt merge task của OWNER là lần cấp quyền" | Trạng thái 2026-11-25 (O2.1, DEC-0034): ACCEPTED một phần (đã áp qua Q5/D6); manifest bằng script hoãn Đợt 2

### Cơ chế lấy từ GSD Core (thêm 2026-11-22)
Nguồn: GSD_CORE_DE_XUAT_KAIZEN.md (M1–M17). Task theo PHUONG_AN_TICH_HOP_GSD_DOT1.md. Chốt ở TK-0053 (B1b), DEC-0032.

- E27 | PROPOSAL | Vai con ghi kết quả ra file, trả một dòng xác nhận kèm đường dẫn và hash (TK-0049); payload `init` gọn cho từng vai ở Đợt 4 (M1). | Thay: [LEAD điền]
- E28 | PROPOSAL | Độ sâu đọc: LEAD đọc frontmatter của sổ và đặc tả, thân chỉ đọc khi chẩn đoán; không nhét file lớn vào prompt của vai khác, chỉ trỏ đường dẫn (TK-0048, TK-0049; M2). | Thay: [LEAD điền]
- E29 | PROPOSAL | Vùng AUTO trong STATE.md (TK-0040); `state validate` so vùng AUTO với sổ gốc (TK-0044); `state sync` dựng lại STATE ở Đợt 4 (M3). | Thay: phần STATE do LEAD sửa tay
- E30 | PROPOSAL | Luật dừng ở ranh giới batch khi ngữ cảnh nặng và template checkpoint kiểu continue-here, mỗi mục "đã xong" trỏ SHA hoặc hash (TK-0049); đo đỉnh prompt_tokens ở TK-0038; script giám sát ngưỡng 50% và 70% ở Đợt 2 (M4). | Thay: [LEAD điền]
- E31 | PROPOSAL | Chỉ tách hoặc bỏ việc vì ba lý do: quá ngân sách ngữ cảnh, thiếu thông tin, xung đột phụ thuộc (TK-0049); ngưỡng cỡ task cho tuyến free khoảng 50% ngân sách, task TDD khoảng 40%, ở Đợt 2 (M5). | Thay: GIẢ ĐỊNH "5 file hoặc 200 dòng" ở tiêu chí tách Cấp 3 (Đợt 2)
- E32 | PROPOSAL | Ước lượng token có hiệu chỉnh: trung vị tỷ lệ thực tế/ước, kẹp trong [0.5, 3.0], cần ít nhất 3 mẫu, độ tin cậy suy từ số mẫu; dùng cho thẻ khởi chạy batch (Đợt 2; M6). | Thay: [LEAD điền]
- E33 | PROPOSAL | Phủ DoD bằng test trong validate (TK-0043); phủ yêu cầu và checker ngữ nghĩa trước PLAN_GO ở Đợt 2; vòng sửa kế hoạch tối đa 3, dừng sớm khi số lỗi không giảm (M7). | Thay: [LEAD điền]
- E34 | PROPOSAL | Thang năng lực: tier mặc định theo vai, leo khi lỗi năng lực, trần 1 bậc mỗi task (`max_escalations`), lỗi crash không leo (Đợt 2; M8). | Thay: phần thang leo trong E17
- E35 | PROPOSAL | Enum lớp lỗi một nguồn và quy tắc đối chiếu sản phẩm trên đĩa trước khi phân loại lỗi (TK-0042); script phân loại theo mã HTTP và chuỗi nhận diện, thang đổi nhà cung cấp khi hết hạn mức (Đợt 2 cho tuyến free, Đợt 3 cho mọi tuyến) (M9). | Thay: [LEAD điền]
- E36 | PROPOSAL | Sổ mã thoát một nguồn (`exit_codes.json`), thêm mã 66 NO_INPUT; phép kiểm trên phạm vi rỗng trả 66, không trả 0 (TK-0042, TK-0043; M10). | Thay: phần mã thoát của câu hỏi E16
- E37 | PROPOSAL | Mỗi hook khai `ON_CRASH`: hook gác chặn, hook quan sát cho qua; thiếu khai báo là lỗi (TK-0042, TK-0045; M11). | Thay: phần "chặn hay cho qua" của câu hỏi E16
- E38 | PROPOSAL | Rào máy thay luật văn xuôi: tên file bí mật không phân biệt hoa thường (TK-0046); sổ chỉ thêm dòng, kiểm bằng diff (TK-0044); luật đọc trước khi sửa cho tuyến free (Đợt 2) (M12). | Thay: [LEAD điền]
- E39 | PROPOSAL | Quét injection và base64 trên file `.md` thay đổi trong PR, mức cảnh báo (TK-0045); quét 06_sources/ mức chặn ở Đợt 2; script chép từ GSD kèm NOTICE MIT và thay phần mã thoát (M13). | Thay: [LEAD điền]
- E40 | PROPOSAL | Kiểm lời tự báo cho mọi run: schema run có `files_created`, `commits`, `self_check` (TK-0042); script kiểm lại trên đúng nhánh, lệch là CLAIM_MISMATCH (TK-0043) (M14). | Thay: mốc Đợt 2 của CLAIM_MISMATCH trong E17
- E41 | PROPOSAL | REVIEWER kiểm ngược từ mục tiêu: bốn mức artifact (tồn tại, có thực chất, được nối, có dữ liệu chảy qua); trạng thái đóng passed / gaps_found / human_needed (Đợt 2; M15). | Thay: [LEAD điền]
- E42 | PROPOSAL | Sửa khi task FAIL: thử lại có điều chỉnh, tách tối đa 3 bước con, hoặc báo BLOCK; ngân sách 2 lần; không bỏ task mà không có BLOCK; báo cáo REVIEWER xuất gap dạng YAML (Đợt 2; sinh task sửa từ gap ở Đợt 4) (M16). | Thay: "chỉ thử lại tới max_loops" của loop hiện tại
- E43 | PROPOSAL | Ruleset bằng file JSON và script, github_audit so khai báo với thực tế (TK-0054); test đối chứng dương cho mọi cổng (TK-0043, TK-0044, TK-0050); phát hiện danh sách file bị cắt (TK-0043); khẳng định runner (TK-0045); ratchet chỉ số sau Đợt 1 (TK-0052) (M17). | Thay: ruleset chỉ cấu hình trên giao diện

**Cơ chế GSD không lấy** (đề xuất ghi REJECTED trong DEC-0032 để không đề xuất lại):
- `git.branching_strategy: none` (làm tiếp trên nhánh hiện tại): trái luật mỗi task một nhánh, cấm sửa main.
- Commit `--no-verify` theo `workflow.worktree_skip_hooks`: Hardness giữ hook ở mọi lần đẩy.
- Task `checkpoint:human-verify` chen giữa lúc chạy: trái nguyên tắc WORKER không dừng hỏi; thay bằng BLOCK kèm QUESTION.
- PRUNE tự đóng task; verifier tự hoãn gap: quyết định phạm vi thuộc LEAD và OWNER.
- Hook gác cho qua khi tự lỗi (`ON_CRASH = allow`): WORKER chạy không giám sát.
- Bộ cài npm và hook theo sự kiện riêng của Claude Code: ngoài danh sách binary nền; WORKER chạy qua Orca, Codex CLI.

## 4. Quy trình chuyển giao về repo mẹ
- Bước 0 — ĐÃ XONG: H0–H4 nạp vào repo ở TK-0036.
- Bước 1 — ĐÃ XONG: E15 chốt ở DEC-0031; DEC-0020 hiện hành được thay theo E15.
- Bước 2 — ĐÃ XONG: DSC-20261121-kzn1 xử lý E1–E26 (TK-0037).
- Bước 3: OWNER chốt theo nhóm; mỗi nhóm một DEC. DEC-0031 cho nhóm đầu; DEC-0032 cho E27–E43 ở TK-0053. Thứ tự khuyến nghị: E14 trước E11 (đã đạt); E18 trước E5, E16; E19 trước E10, E17; E1 cùng E3.
- Bước 4: mỗi nhóm đã chốt có một PR upgrade/ ở repo thử; sau khi merge, một PR tương ứng sang repo mẹ Hardness-V1.0.0. Nếu E25 được chấp nhận, một PR upgrade/ có thể gom nhiều nhóm và VERSION chỉ tăng khi phát hành.
- Nhóm E27–E43 chỉ chuyển về repo mẹ sau khi qua Bước 5 và cổng Đ5-C, theo E15 (chỉ chuyển công cụ đã được thực chứng).
- Mọi đổi schema (run, decision) ghi mức MINOR, đi qua upgrade/, chỉ áp từ mốc kiểm.

## 5. Điểm mù: hạ tầng thực thi chưa được khung mô tả
Nhãn: GIỮ (phần đo token) | Đợt: Đ1 (mô tả tối thiểu, ghi trong spec TK-0038), Đợt 3 (phần còn lại) | PROPOSAL: không
- Hồ sơ nhắc tới các thành phần khung chưa ghi nhận: relay_p4, Codex CLI, DeepInfra, Nvidia Nano, pwsh 7.4.
- DeepSeek và Nvidia Nano đã được dùng nhưng không có trong MODEL_CATALOG. Bổ sung ở trạng thái UNQUALIFIED hoặc loại khỏi routing ở TK-0040, trước khi validate kiểm SAME_MODEL (TK-0043).
- Đ1 ghi token qua relay (H4-6), mà relay đang có nhiều bản (H3-6). Spec TK-0038 phải ghi trước L1.1: bản relay nào đang chạy, 9Router, điểm đọc usage cố định. Nếu điểm đo đổi giữa L1.1 và TK-0051, hai số không so được.
- Phần mô tả đầy đủ và thống nhất relay vẫn thuộc Đợt 3 (K6).
