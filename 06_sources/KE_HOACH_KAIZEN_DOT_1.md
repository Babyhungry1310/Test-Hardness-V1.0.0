B?n tham kh?o 2026-11-22. Ngu?n hi?n h?nh: SRC-0003 P6d, DEC-0032.

# KẾ HOẠCH TỔNG THỂ KAIZEN KHUNG HARDNESS

Tài liệu này xác lập lộ trình triển khai Kaizen tổng thể cho khung Hardness qua 7 tiêu chí (K1–K7).
- Đợt 1 tập trung vào 3 tiêu chí đòn bẩy cốt lõi: K3 (Cắt tỉa luật/sổ), K1 (Thi hành tự động), K2 (Ngữ cảnh).
- Các đợt tiếp theo (Đợt 2, 3, 4) được lập khung định hướng và sẽ được chốt chi tiết dựa trên dữ liệu đo lường thực tế tại Bước 5 của Đợt 1, thông qua gói thẩm định theo `README_GOI_KAIZEN.md`.
- Cập nhật 2026-11-21: đồng bộ với hồ sơ Upstream H0–H4 (E1–E26); đưa E14, E15 lên Bước 0; đổi thứ tự Bước 3 (quy ước trước, code sau); thêm điều kiện cho WORKER trên tuyến free ở Đợt 2; thêm việc của OWNER cho từng bước.
- Cập nhật 2026-11-22:
  - Bước 0 đã xong (TK-0036, TK-0037; DEC-0031 chốt 5 quyết định chặn, E14 tách tài khoản, E15 chuyển repo mẹ theo nhóm).
  - Đợt 1 chạy trong CYC-08; task chi tiết TK-0036…TK-0052 ở SRC-0003, mỗi batch một task (B0a…B5b).
  - Tích hợp cơ chế từ GSD Core theo `PHUONG_AN_TICH_HOP_GSD_DOT1.md` (E27–E43): thêm batch B1b (TK-0053) và B3g (TK-0054), mở rộng phạm vi một số task.
  - Ghi rõ chỗ kế hoạch này khác SRC-0003 (nơi chạy verify, Bước 3).
  - Bản trong repo có thể mang tên `KE_HOACH_KAIZEN_DOT_1.md`; LEAD đồng bộ.

## Tiến độ (2026-11-22)

| Bước | Trạng thái | Task, batch (SRC-0003) |
| --- | --- | --- |
| 0 | ĐÃ XONG | TK-0036 (B0a), TK-0037 (B0b) |
| 1 | Đang chuẩn bị | TK-0038 (B1a), O1.1–O1.4, L1.1; thêm TK-0053 (B1b) |
| 2 | Chưa | TK-0039–TK-0041 (B2a–B2c) |
| 3 | Chưa | TK-0042–TK-0047 (B3a–B3f); thêm TK-0054 (B3g) |
| 4 | Chưa | TK-0048–TK-0050 (B4a–B4c) |
| 5 | Chưa | TK-0051–TK-0052 (B5a, B5b) |

## Bảng tiêu chí và ánh xạ mã

| Tiêu chí | Nội dung | Thực hiện ở | Mã trong H0–H4 |
| --- | --- | --- | --- |
| K1 | Thi hành tự động | Đợt 1, Bước 3 | Đ3a, Đ3b; E4–E7, E9, E16, E18, E20–E24; GSD: E29, E33, E35–E40, E43 |
| K2 | Ngữ cảnh | Đợt 1, Bước 4 | Đ4; H3-2, H3-7; GSD: E27, E28, E30, E31 |
| K3 | Cắt tỉa luật và sổ | Đợt 1, Bước 2 | Đ2; cột "Thay" của mỗi E; GSD: E29 (vùng AUTO trong STATE) |
| K4 | An toàn | Đợt 1 Bước 1 (ruleset), Bước 3 (TK-0054), Đợt 2 (phần còn lại) | E11, E14; GSD: E43 |
| K5 | Định tuyến model, WORKER free | Đợt 2 | E10, E17, E19, E21; H3-1, H3-11, H3-13, H3-16, H3-17; GSD: E31, E32, E34, E35, E41, E42 |
| K6 | Hạ tầng và khôi phục | Đợt 3 | E13; H3-6, H3-9, H4-3; GSD: E35 (thang nhà cung cấp cho mọi tuyến) |
| K7 | Trải nghiệm OWNER, Brainstorm | Đợt 4 | E1, E3; H4-9; GSD: E27 (payload init), E29 (state sync), E42 (task từ gap) |

- Đ1–Đ5 trong H0 là Bước 1–5 của Đợt 1 trong tài liệu này. Đ3a, Đ3b là hai nửa của Bước 3. Không nhầm với Đợt 2, 3, 4.
- Mã sự cố theo bảng hệ mã ở `README_GOI_KAIZEN.md` mục 1.1 (S1–S8 tương ứng E1–E8 của prompt vòng 1, CHƯA XÁC MINH từng dòng).

## Nguyên tắc thực hiện chung

- Thực hiện rải rác khi rảnh. Bước sau chỉ bắt đầu khi bước trước đạt điều kiện "xong".
- Mức tốn token: **nhẹ** (đọc ít, sửa sổ), **vừa** (một task code nhỏ), **nặng** (nhiều file, chạy kiểm nhiều vòng).
- Mỗi thời điểm tối đa một PR `lead/` và một PR `upgrade/` đang mở.
- Chu kỳ sản phẩm tạm dừng tới khi xong Bước 5 của Đợt 1 (quyết định chặn 1 của DEC-0031).
- Kaizen lấy origin từ DEC (quyết định chặn 2): mọi thay đổi phạm vi task đi qua DEC. Phần GSD đi qua DEC-0032 (TK-0053). Ngoại lệ duy nhất: thêm chỉ số đo vào spec TK-0038, vì nằm trong phạm vi đo nền của DEC-0031.
- Chọn model trong Đợt 1: task code của khung là hạng T2 nên dùng tuyến trả phí. Tuyến free chưa đủ điều kiện làm WORKER (chưa có W1–W4, E10); chỉ làm việc phụ như tra cứu, tóm tắt. REVIEWER khác họ model với mọi WORKER.
- Không đổi điểm đo token, bộ phiên chuẩn, model hay tuyến dùng cho phiên chuẩn giữa L1.1 và TK-0051. Nếu buộc phải đổi, ghi lại và không so trực tiếp.
- Không đưa vào trước L1.1 bất kỳ thay đổi nào về luật, ngữ cảnh hay công cụ mà LEAD đọc.
- Khi tạm nghỉ: ghi bước đang làm và PR đang mở vào mục *Next action* của `04_control/STATE.md`.

---

# PHẦN I — KẾ HOẠCH CHI TIẾT ĐỢT KAIZEN 1 (CHIA THEO BƯỚC)

## Bước 0 — Dọn đường (ĐÃ XONG)
- **Kết quả:**
  - TK-0036: nạp hồ sơ H0–H4 vào `05_memory/upstream/` và `06_sources/`, đã sanitize.
  - TK-0037: DSC-20261121-kzn1 xử lý E1–E26; DEC-0031 ACTIVE gồm 5 quyết định chặn (tạm dừng chu kỳ sản phẩm; Kaizen lấy origin từ DEC; bật ruleset; run cũ chỉ kiểm từ mốc; trường `model` dạng danh sách).
  - E14 = tách tài khoản (thay DEC-0019; RSK-0004 mức HIGH, hạn xử lý 2026-11-26). E15 = chuyển repo mẹ theo nhóm đã thực chứng.
  - STATE chuyển sang CYC-08; PR #37 đã đóng.
- **Còn lại sau Bước 0:** trạng thái từng dòng E1–E26 chưa được ghi vào H0 (H0 mục 3).

## Bước 1 — Đo nền và cấu hình
- **Vào:** Đã xong Bước 0.
- **Việc:**
  1. **TK-0038 (B1a):** đóng băng spec 3 phiên chuẩn vào `03_output/CYC-08/checks/baseline_session_spec.md`: LEAD hỏi trạng thái; LEAD review PR; WORKER chạy task nhỏ. Task chỉ ghi spec, không chạy phiên. Ghi kèm trong spec:
     - Điểm đo cố định (H0 mục 5): bản relay đang chạy, 9Router, nơi đọc usage.
     - Model, tuyến, phiên bản model hoặc provider, đầu vào cố định cho từng phiên.
     - Bốn chỉ số thêm cho phần GSD (PHUONG_AN mục 2.2): tỷ lệ output/input theo vai; số lần đọc nguyên file (nếu có log công cụ); số dòng WORKER trả về; đỉnh `prompt_tokens` mỗi phiên.
  2. **O1.1–O1.4 (OWNER, giao diện GitHub, không tốn token):**
     - Ruleset cho `main` và cho thẻ `cycle/*`; chỉ OWNER bypass. Luật thẻ chặn tạo, sửa, xóa.
     - Tài khoản tác tử riêng (E14 đã chốt tách), quyền collaborator tối thiểu.
     - Secret scanning và push protection. Repo public nên đẩy nhánh đã là công khai; đây là lớp chặn sớm trước khi có hook pre-push ở TK-0045 (E23).
     - Làm xong trước 2026-11-26 (hạn RSK-0004).
     - Sau khi bật, OWNER xuất cấu hình ruleset (`gh api`) lưu ở `<project>.local`, làm mốc cho TK-0054.
  3. **L1.1:** chạy 3 phiên chuẩn, mỗi phiên 2 lần, theo spec TK-0038. Xuất bảng usage có nhãn vai (role), đo tại điểm đã chọn (E8).
  4. Chụp ảnh môi trường, lưu ở máy (`<project>.local`), không commit. [LEAD xác nhận việc này có trong SRC-0003; nếu không, làm cùng L1.1.]
- **OWNER:** 1 lượt merge (TK-0038); thao tác trên giao diện GitHub.
- **Xong khi:** Có bảng token nền theo vai, ghi rõ điểm đo và bốn chỉ số thêm; audit đạt 5 dòng; push protection đã bật.
- **Token:** Vừa (6 phiên chuẩn).
- **Lưu ý:** Đây là bước duy nhất phải xong trước khi đổi bất kỳ điều gì liên quan tới ngữ cảnh. Nếu chưa có nền thì sau này không thể đối chứng hiệu quả.

### Batch B1b — Nạp quyết định phần GSD (TK-0053, `lead/`)
- **Vào:** L1.1 xong, đã có bảng nền.
- **Việc:**
  1. Nạp `GSD_CORE_DE_XUAT_KAIZEN.md` và `PHUONG_AN_TICH_HOP_GSD_DOT1.md` vào `06_sources/` dạng SRC mới, qua quy trình sanitize như TK-0036.
  2. DSC mới ghi E27–E43 (H0 mục 3).
  3. DEC-0032: ACCEPTED các E áp trong Đợt 1, kèm task; hoãn các E của Đợt 2–4; REJECTED các cơ chế GSD không lấy (H0 mục 3, cuối).
  4. Sửa phạm vi task trong SRC-0003 theo PHUONG_AN mục 3; sửa cách ghi ở TK-0042 (H4 mục 1).
  5. Chốt các câu hỏi ở PHUONG_AN mục 7, trong đó có nơi chạy verify chính thức.
- **OWNER:** 1 lượt merge; trả lời câu hỏi ở PHUONG_AN mục 7.
- **Xong khi:** DEC-0032 ACTIVE đã merge; SRC-0003 cập nhật phạm vi task.
- **Token:** Nhẹ.

## Bước 2 — Cắt tỉa
- **Vào:** Đã xong Bước 1 và B1b.
- **Việc:**
  1. **TK-0039 (`lead/`):** retire 5 DEC về model (DEC-0007, 0012, 0014, 0028, 0029).
  2. **TK-0040 (`lead/`):**
     - Rút gọn mục 3 của STATE (chỉ giữ 5 DEC gần nhất).
     - Cập nhật catalog model; thêm DeepSeek, Nvidia Nano ở trạng thái UNQUALIFIED hoặc loại khỏi routing. Nếu không, phép kiểm SAME_MODEL ở TK-0043 sẽ chặn hoặc đánh giá sai các run dùng hai model này.
     - Đánh dấu vùng trong STATE mà sau này script sinh tự động (`<!-- STATE:AUTO:START -->` … `END`), chưa sinh (E29).
  3. **TK-0041 (`upgrade/`):** gộp §9 của LEAD.md thành một luật trỏ sang README; tăng VERSION lên 1.0.3.
- **OWNER:** 3 lượt merge.
- **Xong khi:** 3 PR đã merge; DEC ACTIVE còn 15; VERSION khớp; catalog có đủ model đang dùng.
- **Token:** Nhẹ.

## Bước 3 — Thi hành tự động
- **Vào:** Đã xong Bước 2.
- **Thứ tự:** quy ước và schema trước, code sau. Nếu viết `validate` và hook trước rồi mới đổi schema run và mã thoát, phải viết lại.
- **Việc** (mỗi gạch đầu dòng là một PR, làm tuần tự):
  1. **TK-0042 (`upgrade/`, quy ước, Đ3a):**
     - Schema run MINOR: khóa `model` nhận danh sách model thực tế đã xác minh (E21; không thêm khóa `actual_model`); khóa loại bằng chứng không đổi kiểu của `evidence` (H4 mục 1); thêm `files_created`, `commits`, `self_check` (E40).
     - Template điểm dừng (E4), có luật lệch kế hoạch chỉ trong write_scope và luật không thử tên gói gần giống (H2 mục 2).
     - Mã thoát 0/1/2/3 và bảng lỗi thống nhất (E5, E16, E18) trong một file nguồn duy nhất, thêm mã 66 NO_INPUT (E36); enum lớp lỗi và quy tắc đối chiếu đĩa trước khi phân loại (E35); quy ước khai báo `ON_CRASH` cho hook (E37).
     - Chỉ văn bản và schema. Nếu write_scope vượt 5 path, tách phần mã thoát sang batch B3a2 (TK-0055).
  2. **TK-0043 (`task/`):** validate lõi (schema run, loop, C1–C3, SAME_MODEL), thêm:
     - Kiểm lời tự báo cho mọi run (E40).
     - Phủ DoD bằng test (E33).
     - Phép kiểm write_scope trả 66 khi diff rỗng; phát hiện danh sách file bị `gh` cắt ở 100 (E36, E43).
     - Mỗi kiểm C có test đối chứng dương mới được đếm (E43).
     - Chạy ở chế độ cảnh báo.
  3. **TK-0044 (`task/`):** các kiểm trôi (một PR `lead/` mở, mã DEC liên tục, VERSION, SHA của STATE), thêm `state validate` trên vùng AUTO (E29) và sổ chỉ thêm dòng (E38).
  4. **TK-0045 (`task/`, chạm `.github/`, OWNER ra lệnh trực tiếp):**
     - CI `check.yml` chạy trên PR, mức cảnh báo.
     - Hook pre-push: detect-secrets (E23); hook khai `ON_CRASH = deny` và hiểu mã 66, mã 3 (E37).
     - Quét injection và base64 trên file `.md` thay đổi, mức cảnh báo (E39). Nếu write_scope vượt 5 path, tách phần này sang batch B3d2 (TK-0056).
     - Khẳng định runner do GitHub cung cấp (E43): bắt buộc nếu verify chạy trên CI, tùy chọn nếu `check.yml` chỉ chạy validate.
  5. **TK-0046 (`upgrade/`):** cách ly verify mức nhẹ (worktree riêng, không biến bí mật; E6); bẫy Windows UTF-8 và LF (E9); quét tên file bí mật không phân biệt hoa thường (E38); ghi rõ lần chạy lại verify do máy là nguồn duy nhất cho LEAD và REVIEWER.
  6. **TK-0047 (`task/`):** kiểm tĩnh C9 (con trỏ và origin), đưa lên main trước khi sang Bước 4.
  7. **TK-0054 (B3g, `task/`):** ruleset thành file JSON trong repo và script áp, viết bằng Python vì Git Bash không có `jq`; github_audit so khai báo với thực tế (E43). Luật thẻ có thêm `creation`.
- **Nơi chạy verify chính thức — cần chốt ở B1b:**
  - SRC-0003 chọn cách ly mức nhẹ trên máy (TK-0046) và CI chỉ cảnh báo (TK-0045).
  - Kế hoạch này đề xuất thêm: chạy verify trên CI (runner Windows, không cấp secret, `permissions: contents: read`). Lý do: runner của GitHub tách khỏi máy OWNER, nên code test do WORKER viết không chạy cạnh thông tin đăng nhập của OWNER. Cách này giảm rủi ro E6 mà không cần sandbox trên Windows.
  - GIẢ ĐỊNH (VỪA): runner chuẩn miễn phí cho repo public; kiểm lại trên trang thanh toán của tài khoản.
- **OWNER:** 7 lượt merge, tuần tự (thêm 1–2 nếu phải tách TK-0042, TK-0045); ra lệnh trực tiếp cho PR chạm `.github/`.
- **Xong khi:** ≥ 5/14 kiểm C và 4 kiểm trôi chạy tự động, mỗi kiểm có test đối chứng dương; CI chạy trên PR; ruleset có file JSON và script.
- **Token:** Nặng. Đây là bước tốn nhất, nên chia nhỏ theo từng PR. Mỗi PR là một mốc có thể tạm dừng.
- **Điểm dừng an toàn:** Nếu `validate` cảnh báo sai trên 20% số PR (tính trên ít nhất [LEAD chốt] PR) thì giữ ở chế độ cảnh báo, sửa luật kiểm trước khi chuyển sang Bước 4.

## Bước 4 — Ngữ cảnh và viết lại LEAD.md
- **Vào:** Đã xong Bước 3. Bắt buộc có kiểm C9 để bắt con trỏ bị gãy khi tách file.
- **Việc:**
  1. **TK-0048 (`upgrade/`):** tách 3 phụ lục của HARNESS sang RATIONALE.md, tách các mục lớn thành file riêng, đặt neo ANCHOR cho các đoạn hay trích. Mỗi sổ và đặc tả có frontmatter đủ để ra quyết định mà không đọc thân (E28).
  2. **TK-0049 (`upgrade/`):** viết lại LEAD.md xuống ≤ 1.300 từ, mỗi luật ≤ 40 từ. Thêm bốn luật ngắn từ GSD:
     - Chỉ đọc frontmatter; đọc thân khi chẩn đoán (E28).
     - Không nhét file lớn vào prompt của vai khác, chỉ trỏ đường dẫn (E28).
     - Vai con ghi kết quả ra file, trả một dòng (E27).
     - Chỉ tách hoặc bỏ việc vì ba lý do: quá ngân sách ngữ cảnh, thiếu thông tin, xung đột phụ thuộc (E31).
     - Kèm template checkpoint kiểu continue-here; mỗi mục "đã xong" trỏ SHA hoặc hash (E30).
     - Cố định thứ tự prefix giữa các phiên (H3-2) [LEAD xác nhận nằm trong task này].
  3. **TK-0050 (`task/`):** tự động hóa C5, C7 (đo theo từ), C12, C13; một hàm đo dùng chung cho test và báo cáo, có test đối chứng dương (E43). Nén output công cụ theo H3-7 [LEAD xác nhận task].
- **OWNER:** 3 lượt merge.
- **Xong khi:** ≥ 8/14 kiểm C; LEAD.md ≤ 1.300 từ.
- **Token:** Vừa đến nặng.
- **Lưu ý:** Không đổi model, tuyến hay điểm đo của phiên chuẩn trong bước này, để Bước 5 so được với nền.

## Bước 5 — Đo lại và đóng đợt
- **Vào:** Đã xong Bước 4.
- **Việc:**
  1. **TK-0051 (`lead/`):** chạy lại 3 phiên chuẩn với cùng đầu vào, cùng model và tuyến, cùng điểm đo. Model hoặc provider đổi phiên bản thì ghi lại và không kết luận trực tiếp.
  2. **TK-0052 (`lead/`):**
     - Báo cáo so sánh token theo vai giữa nền và sau Đợt 1, gồm bốn chỉ số thêm cho phần GSD.
     - Ghi mốc ratchet (chỉ được đi một chiều, lùi phải có DEC): số từ LEAD.md, số luật, số DEC ACTIVE, token LEAD phiên chuẩn (E43).
     - Cập nhật trạng thái các dòng E trong H0, gồm E27–E43.
     - Chuẩn bị gói Kaizen 2 theo `README_GOI_KAIZEN.md`, đổi mã theo bảng hệ mã mục 1.1.
  3. **Cổng Đ5-C (OWNER):** quyết định bật CI thành check bắt buộc; chọn nhóm E đầu tiên chuyển về repo mẹ theo E15. Nhóm E27–E43 chỉ chuyển sau cổng này.
- **OWNER:** 2 lượt merge; duyệt gói Kaizen 2; cổng Đ5-C.
- **Xong khi:** Có bảng so sánh token theo vai giữa nền và sau Đợt 1; H0 đã cập nhật trạng thái; gói Kaizen 2 đã gửi.
- **Token:** Vừa.
- **Điểm dừng an toàn:** Nếu phiên chuẩn của LEAD giảm dưới 15% token thì không đi tiếp hướng tách ngữ cảnh động, mà điều tra lại nguyên nhân gốc rễ tiêu tốn token.

---

# PHẦN II — KHUNG ĐỊNH HƯỚNG CÁC ĐỢT TIẾP THEO

Sau Đợt 1, thứ tự và cách làm của các đợt tiếp theo căn cứ vào số liệu thực tế tại Bước 5. Mỗi đợt được chốt lại bằng gói thẩm định mới.

## Đợt 2 — An toàn, định tuyến model và WORKER trên tuyến free (K4 còn lại, K5)
- **Vào khi:** Đợt 1 đã đóng.
- **Việc chính:**
  - An toàn: phần K4 còn lại sau O1.x và TK-0054, ví dụ duyệt code owner (E11).
  - Định tuyến:
    - Gộp "tuyến đã chứng minh" vào ELIGIBILITY và ROUTE_CHECKS; định nghĩa P4 (E10).
    - Kiểm tuyến bằng máy trước khi giao việc; preflight xác minh model thực tế (E21).
  - WORKER trên tuyến free (H3 mục 11, 13, 16, 17):
    1. Định nghĩa W1–W4, ngưỡng đạt và bộ task mẫu cho hạng T0, T1 (E19).
    2. Hạng task trong task spec, thang leo tuyến (E17). Tách hai thang: năng lực (E34) và nhà cung cấp (E35); trần 1 bậc; thử tách task trước khi leo (E42).
    3. Ngân sách context và hạn mức (request mỗi phút, mỗi ngày, đồng thời) của từng tuyến trong MODEL_CATALOG; chặn giao khi vượt (H3-1). Gói task khoảng 50% ngân sách tuyến (E31).
    4. Khung thời gian, hạn mức và ngắt mạch cho riêng tuyến free (H3-17); script phân loại lỗi theo mã HTTP (E35).
    5. Luật đọc trước khi sửa cho tuyến free (E38).
    6. Chạy W1–W4 cho các tuyến free định dùng; tuyến đạt mới được nhận task T0, T1.
  - Kiểm định và sửa lỗi: REVIEWER kiểm ngược từ mục tiêu (E41); phủ yêu cầu và checker ngữ nghĩa trước PLAN_GO (E33); ước lượng token có hiệu chỉnh cho thẻ khởi chạy batch (E32); script giám sát ngữ cảnh LEAD (E30).
  - Viết script `scan` cho 06_sources/ (trước đây dự kiến ở CYC-06; E2), dùng bộ mẫu injection ở mức chặn (E39).
- **Chỉ số đo lường:**
  - Số lượt giao việc hoặc kiểm định hỏng vì model (nền: 3/5 lượt kiểm định hỏng).
  - Theo tuyến và hạng task: tỷ lệ đạt lần đầu, tỷ lệ CLAIM_MISMATCH, Cost per Accepted Task của tuyến free so với tuyến trả phí (H4-7).
- **Lưu ý:** Chu kỳ sản phẩm mở lại sau Đợt 1. Tới khi tuyến free đạt W1–W4, task sản phẩm dùng tuyến trả phí.

## Đợt 3 — Hạ tầng và khôi phục (K6)
- **Vào khi:** Đợt 1 đã có số đo tách bạch độ sẵn sàng và chất lượng (E8).
- **Việc chính:**
  - Ngắt mạch chung cho mọi tuyến (E13), dùng bảng lỗi thống nhất đã có từ TK-0042 (E18); thang nhà cung cấp cho mọi tuyến (E35).
  - Thống nhất relay; chuyển phiên có chặn triệt để phiên cũ. Nếu điểm đo token nằm ở relay, đo song song bản cũ và bản mới ít nhất một lần để nối số liệu.
  - Mô tả đầy đủ lớp hạ tầng thực thi (relay, Codex CLI, pwsh) vào khung quy ước.
  - Xử lý kịch bản khi token GitHub hết hạn. Theo bảng hệ mã đây là S6; CHƯA XÁC MINH.
  - Nhật ký phê duyệt lệnh, nếu công cụ tác tử chưa tự ghi (H4-3).
- **Chỉ số đo lường:** Số lần quy trình bị tắc nghẽn chờ OWNER xử lý vì lỗi hạ tầng.
- **Lưu ý:** Nếu số đo của Đợt 1 cho thấy lỗi hạ tầng rất hiếm, đợt này có thể thu nhỏ hoặc gộp vào Đợt 2.

## Đợt 4 — Trải nghiệm OWNER và Brainstorm (K7, E1, E3)
- **Vào khi:** Đã có script `state` (sinh STATE tự động); công cụ `validate` đã hoạt động ổn định.
- **Việc chính:**
  - File STATE được sinh tự động từ sổ gốc (`state sync`, E29), cấu trúc để đọc hiểu nhanh trong 30 giây.
  - Khối STATUS chuẩn 4 dòng (H4-9); báo cáo PR cô đọng dưới 30 dòng.
  - Triển khai vai ADVISOR (E1) cùng lúc với Basic Plan và bước LEAD tiếp nhận (E3); bước tiếp nhận kích hoạt theo người đề xuất nội dung. Áp dụng cho dự án mới.
  - Script dựng phần cơ học của gói Kaizen từ neo ANCHOR (README "Người chuẩn bị").
  - Triển khai script `get` và payload `init` gọn cho từng vai (E27), cơ chế cắt ngữ cảnh động nếu Đợt 1 cho thấy việc tách file tĩnh chưa đủ.
  - Sinh nháp task sửa từ gap của REVIEWER (E42).

## Quy trình sau mỗi đợt
1. **Đo lại:** Đánh giá số liệu thực nghiệm theo chỉ số mục tiêu của đợt, cùng điểm đo với lần trước.
2. **Cập nhật hồ sơ:** Cập nhật trạng thái các dòng E trong H0 (`ACCEPTED` / `REJECTED`); ghi nhận dữ kiện mới (N11, N12…).
3. **Thẩm định độc lập:** Gửi gói thẩm định mới theo `README_GOI_KAIZEN.md` để chốt nội dung đợt kế tiếp. Thứ tự Đợt 2, 3, 4 có thể linh hoạt điều chỉnh theo dữ liệu đo lường.
4. **Chuyển giao:** Chuyển giao các nhóm PROPOSAL đã ổn định về repo mẹ theo E15.

---

# PHẦN III — LƯU Ý KHI THỰC HIỆN RẢI RÁC

- **Hạn RSK-0004 (2026-11-26):** O1.1–O1.4 làm ngay trên giao diện, không chờ phần GSD. Nếu chưa kịp, cập nhật dòng trạng thái mới cho RSK để dời hạn, tuyệt đối không để quá hạn vô thừa nhận.
- **Ghi điểm dừng vào STATE khi tạm nghỉ:** Mục *Next action* trong `04_control/STATE.md` ghi rõ đang ở bước nào, PR nào đang mở. Lần sau mở phiên mới, LEAD chỉ cần đọc STATE là nắm ngữ cảnh, không tốn token quét lại nhiều file.
- **Kiểm soát song song PR:** Tại mỗi thời điểm chỉ mở tối đa một PR `lead/` và một PR `upgrade/`. Mỗi PR `upgrade/` tăng VERSION, nên hai PR `upgrade/` cùng mở sẽ đụng nhau ở file VERSION (E25 đang xét).
- **Dồn tài nguyên:** Chu kỳ sản phẩm tạm dừng cho tới khi hoàn tất Bước 5 của Đợt 1.
- **Thời gian OWNER là nút thắt:** OWNER là cổng tuần tự của mọi merge và mọi quyết định. Gom quyết định theo bước như bảng dưới, không để rải rác giữa chừng.
- **Đồng bộ tài liệu:** các file trong bộ cập nhật 2026-11-22 là bản đề xuất; bản trong repo (đã sanitize) có thể khác. LEAD đồng bộ ở TK-0053.

## Việc của OWNER theo bước (Đợt 1)

| Bước | Quyết định | Thao tác |
| --- | --- | --- |
| 0 | E15; E14; 5 quyết định chặn — ĐÃ XONG | 1 merge — ĐÃ XONG |
| 1 | — | 1 merge (TK-0038); ruleset, quyền tài khoản tác tử, secret scanning, push protection trên giao diện; xuất cấu hình ruleset |
| B1b | DEC-0032; câu hỏi ở PHUONG_AN mục 7, gồm nơi chạy verify | 1 merge (TK-0053) |
| 2 | — | 3 merge (TK-0039–TK-0041) |
| 3 | Ra lệnh cho PR chạm `.github/` | 7 merge tuần tự (TK-0042–TK-0047, TK-0054); thêm 1–2 nếu tách TK-0042, TK-0045 |
| 4 | — | 3 merge (TK-0048–TK-0050) |
| 5 | CI bắt buộc; nhóm E đầu tiên về repo mẹ (cổng Đ5-C) | 2 merge (TK-0051, TK-0052); duyệt gói Kaizen 2 |
