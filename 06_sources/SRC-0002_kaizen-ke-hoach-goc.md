---
schema: 1
id: SRC-0002
date: 2026-11-22
title: "Kế hoạch Kaizen gốc 4 đợt (bản OWNER cung cấp)"
decided_by: OWNER
related: []
keywords: [kaizen, plan]
---
<!-- ANCHOR: CONTEXT -->
## Context
Nguồn: OWNER cung cấp/duyệt trong phiên lập kế hoạch Kaizen, 2026-11-21–22; thư mục làm việc ngoài repo ghi là `<SHARED>`. scan: ALLOW (`tools/scan.py`, scan-core-1).

# KẾ HOẠCH TỔNG THỂ KAIZEN KHUNG HARDNESS

Tài liệu này xác lập lộ trình triển khai Kaizen tổng thể cho khung Hardness qua 7 tiêu chí (K1–K7).
- Đợt 1 tập trung vào 3 tiêu chí đòn bẩy cốt lõi: K3 (Cắt tỉa luật/sổ), K1 (Thi hành tự động), K2 (Ngữ cảnh).
- Các đợt tiếp theo (Đợt 2, 3, 4) được lập khung định hướng và sẽ được chốt chi tiết dựa trên dữ liệu đo lường thực tế tại Bước 5 của Đợt 1, thông qua gói thẩm định theo `README_GOI_KAIZEN.md`.
- Cập nhật 2026-11-21: đồng bộ với hồ sơ Upstream H0–H4 (E1–E26); đưa E14, E15 lên Bước 0; đổi thứ tự Bước 3 (quy ước trước, code sau); verify chính thức chạy trên CI; thêm điều kiện cho WORKER trên tuyến free ở Đợt 2; thêm việc của OWNER cho từng bước.

## Bảng tiêu chí và ánh xạ mã

| Tiêu chí | Nội dung | Thực hiện ở | Mã trong H0–H4 |
| --- | --- | --- | --- |
| K1 | Thi hành tự động | Đợt 1, Bước 3 | Đ3a, Đ3b; E4–E7, E9, E16, E18, E20–E24 |
| K2 | Ngữ cảnh | Đợt 1, Bước 4 | Đ4; H3-2, H3-7 |
| K3 | Cắt tỉa luật và sổ | Đợt 1, Bước 2 | Đ2; cột "Thay" của mỗi E |
| K4 | An toàn | Đợt 1 Bước 1 (ruleset), Đợt 2 (phần còn lại) | E11, E14 |
| K5 | Định tuyến model, WORKER free | Đợt 2 | E10, E17, E19, E21; H3-1, H3-11, H3-13, H3-16, H3-17 |
| K6 | Hạ tầng và khôi phục | Đợt 3 | E13; H3-6, H3-9, H4-3 |
| K7 | Trải nghiệm OWNER, Brainstorm | Đợt 4 | E1, E3; H4-9 |

- Đ1–Đ5 trong H0 là Bước 1–5 của Đợt 1 trong tài liệu này. Đ3a, Đ3b là hai nửa của Bước 3. Không nhầm với Đợt 2, 3, 4.
- Mã sự cố theo bảng hệ mã ở `README_GOI_KAIZEN.md` mục 1.1 (S1–S8 tương ứng E1–E8 của prompt vòng 1, CHƯA XÁC MINH từng dòng).

## Nguyên tắc thực hiện chung

- Thực hiện rải rác khi rảnh. Bước sau chỉ bắt đầu khi bước trước đạt điều kiện "xong".
- Mức tốn token: **nhẹ** (đọc ít, sửa sổ), **vừa** (một task code nhỏ), **nặng** (nhiều file, chạy kiểm nhiều vòng).
- Mỗi thời điểm tối đa một PR `lead/` và một PR `upgrade/` đang mở.
- Chu kỳ sản phẩm tạm dừng tới khi xong Bước 5 của Đợt 1.
- Chọn model trong Đợt 1: task code của khung là hạng T2 nên dùng tuyến trả phí. Tuyến free chưa đủ điều kiện làm WORKER (chưa có W1–W4, E10); chỉ làm việc phụ như tra cứu, tóm tắt. REVIEWER khác họ model với mọi WORKER.
- Không đổi điểm đo token, bộ phiên chuẩn, model hay tuyến dùng cho phiên chuẩn giữa Bước 1 và Bước 5. Nếu buộc phải đổi, ghi lại và không so trực tiếp.
- Khi tạm nghỉ: ghi bước đang làm và PR đang mở vào mục *Next action* của `04_control/STATE.md`.

---

# PHẦN I — KẾ HOẠCH CHI TIẾT ĐỢT KAIZEN 1 (CHIA THEO BƯỚC)

## Bước 0 — Dọn đường
- **Vào:** Không cần điều kiện gì.
- **Việc:**
  1. Đóng hoặc merge PR #37.
  2. PR `lead/`: commit H0–H4 ở trạng thái DỰ THẢO vào nơi lưu đã chốt, và DSC chứa E1–E26. Mục đích: hồ sơ có SHA, đưa được vào gói Kaizen.
  3. OWNER chốt riêng E15 (cách chuyển giao về repo mẹ), vì E15 quy định cách chốt các mục còn lại.
  4. OWNER chốt 5 quyết định chặn:
     - Tạm dừng chu kỳ sản phẩm.
     - Kaizen lấy origin từ DEC.
     - Bật ruleset Nhánh 1.
     - Dữ liệu run cũ chỉ kiểm từ mốc.
     - Trường `model` dạng danh sách, mỗi phần tử là model thực tế đã xác minh, không ghi tên tuyến (E21).
  5. OWNER chốt E14: giữ hay tách tài khoản GitHub của tác tử. Quyết định này đổi cách đặt ruleset ở Bước 1 và liên quan RSK-0004 (mức HIGH, có hạn trong sổ).
  6. LEAD ra DEC Kaizen.
- **OWNER:** 1 lượt merge; chốt E15, E14 và 5 quyết định chặn.
- **Xong khi:** DSC và DEC Kaizen đã merge; E15 và E14 có trạng thái trong H0.
- **Token:** Nhẹ.

## Bước 1 — Đo nền và cấu hình
- **Vào:** Đã xong Bước 0.
- **Việc:**
  1. OWNER bật trên giao diện GitHub, không tốn token:
     - Ruleset dòng 1, 2, 3, 6 và luật thẻ.
     - Secret scanning và push protection. Repo public nên đẩy nhánh đã là công khai; đây là lớp chặn sớm trước khi có hook pre-push ở Bước 3 (E23).
     - Nếu E14 là giữ chung tài khoản: ruleset không phân biệt được tác tử với OWNER. Luật thẻ đặt không bypass; khi cần tạo thẻ, OWNER tạm tắt luật, tạo thẻ, bật lại và ghi vào log. Nếu E14 là tách: làm tài khoản máy ở bước này luôn và đặt bypass chỉ cho OWNER.
  2. Ghi mô tả tối thiểu lớp hạ tầng đo token (H0 mục 5): bản relay đang chạy, 9Router, điểm đọc usage được chọn. Một đoạn ngắn trong STATE hoặc nơi LEAD chốt.
  3. Đóng băng bộ 3 phiên chuẩn: đầu vào cố định, model và tuyến cố định, ghi phiên bản model hoặc provider.
  4. Chạy 3 phiên chuẩn, mỗi phiên 2 lần. Xuất bảng usage có nhãn vai (role), đo tại điểm đã chọn (E8).
  5. Chụp ảnh môi trường, lưu ở máy (`<project>.local`), không commit.
- **OWNER:** thao tác trên giao diện GitHub (ruleset, secret scanning, push protection, tài khoản máy nếu tách).
- **Xong khi:** Có bảng token nền theo vai, ghi rõ điểm đo; audit đạt 5 dòng; push protection đã bật.
- **Token:** Vừa (6 phiên chuẩn).
- **Lưu ý:** Đây là bước duy nhất phải xong trước khi đổi bất kỳ điều gì liên quan tới ngữ cảnh. Nếu chưa có nền thì sau này không thể đối chứng hiệu quả.

## Bước 2 — Cắt tỉa
- **Vào:** Đã xong Bước 1.
- **Việc:**
  1. PR `lead/`:
     - Retire 5 DEC.
     - Rút gọn mục 3 của STATE.
     - Bổ sung DeepSeek, Nvidia Nano vào MODEL_CATALOG ở trạng thái UNQUALIFIED, hoặc loại khỏi routing. Nếu không, phép kiểm SAME_MODEL ở Bước 3 sẽ chặn hoặc đánh giá sai các run dùng hai model này.
  2. PR `upgrade/`: gộp §9 của LEAD.md, sửa VERSION.
  3. Trong lúc làm bước này, OWNER chốt nhóm E cho Bước 3: E4, E5, E6, E7, E9, E16, E18, E20, E21, E22, E23, E24. Mỗi E được chấp nhận ghi luật bị thay hoặc xóa (cột "Thay" ở H0).
- **OWNER:** 2 lượt merge; chốt nhóm E của Bước 3.
- **Xong khi:** 2 PR đã merge; DEC ACTIVE còn 15; VERSION khớp; catalog có đủ model đang dùng; nhóm E của Bước 3 đã có trạng thái.
- **Token:** Nhẹ.

## Bước 3 — Thi hành tự động
- **Vào:** Đã xong Bước 2.
- **Thứ tự:** quy ước và schema trước, code sau. Nếu viết `validate` và hook trước rồi mới đổi schema run và mã thoát, phải viết lại.
- **Việc** (mỗi gạch đầu dòng là một PR, làm tuần tự):
  1. `upgrade/` — quy ước (Đ3a): schema run MINOR (E7, ngữ nghĩa khóa `model` theo E21, khóa loại bằng chứng); mã thoát 0/1/2/3 và bảng lỗi thống nhất trong SPEC_TOOLS#CONVENTIONS (E5, E16, E18). Chỉ văn bản và schema.
  2. `task/` — validate lõi: schema run mới, C1–C3, SAME_MODEL (danh sách model của REVIEWER không giao với của WORKER). Nếu có kiểm C bắt việc sửa test cũ, áp ngoại lệ có khai báo (E20). Chạy ở chế độ cảnh báo.
  3. `task/` — các kiểm trôi: một PR `lead/` mở, mã DEC liên tục, VERSION, SHA của STATE.
  4. `task/` có chạm `.github/` (OWNER ra lệnh trực tiếp):
     - CI chạy verify trên PR, dùng runner Windows để bắt lỗi cp1252 và CRLF. Đặt `permissions: contents: read`, không cấp secret cho job.
     - Hook pre-push: detect-secrets (E23); hook hiểu mã thoát 3 và chặn khi gặp (E16).
  5. `upgrade/` — thi hành (Đ3b):
     - Template điểm dừng (E4; bỏ "không rõ model", chuyển sang preflight theo E21).
     - Cách ly verify (E6): lần chạy trên CI là lần chạy lại chính thức duy nhất; LEAD và REVIEWER đọc kết quả CI, không tự chạy lại trừ khi chẩn đoán.
     - Kiểm nền Windows, quy tắc LF cho file khung tự viết, raw capture lưu nguyên byte (E9, E22).
     - Danh sách binary nền đã duyệt (E24).
- **Vì sao verify chạy trên CI:** runner của GitHub là môi trường tách khỏi máy OWNER. Code test do WORKER viết không còn chạy cạnh thông tin đăng nhập của OWNER. Điều này giảm rủi ro mà E6 và E14 nêu, mà không cần cài sandbox trên Windows. GIẢ ĐỊNH (VỪA): runner chuẩn miễn phí cho repo public; kiểm lại trên trang thanh toán của tài khoản.
- **OWNER:** 5 lượt merge (tuần tự); ra lệnh trực tiếp cho PR chạm `.github/`.
- **Xong khi:** ≥ 5/14 kiểm C và 4 kiểm trôi chạy tự động; CI chạy verify trên PR.
- **Token:** Nặng. Đây là bước tốn nhất, nên chia nhỏ theo từng PR. Mỗi PR là một mốc có thể tạm dừng.
- **Điểm dừng an toàn:** Nếu `validate` cảnh báo sai trên 20% số PR (tính trên ít nhất [LEAD chốt] PR) thì giữ ở chế độ cảnh báo, sửa luật kiểm trước khi chuyển sang Bước 4.

## Bước 4 — Ngữ cảnh và viết lại LEAD.md
- **Vào:** Đã xong Bước 3. Bắt buộc có kiểm C9 để bắt con trỏ bị gãy khi tách file.
- **Việc:**
  1. `upgrade/`: tách phụ lục HARNESS sang RATIONALE.md, tách các mục lớn thành file riêng, đặt neo ANCHOR cho các đoạn hay trích.
  2. `upgrade/`: viết lại LEAD.md xuống ≤ 1.300 từ; cố định thứ tự prefix giữa các phiên (H3-2).
  3. `task/`: C5, C7 (đo theo từ), C9, C12, C13; nén output công cụ theo H3-7 (bản đủ lưu file kèm hash, ngữ cảnh chỉ giữ tóm tắt và đường dẫn).
- **OWNER:** 3 lượt merge.
- **Xong khi:** ≥ 8/14 kiểm C; LEAD.md ≤ 1.300 từ.
- **Token:** Vừa đến nặng.
- **Lưu ý:** Không đổi model, tuyến hay điểm đo của phiên chuẩn trong bước này, để Bước 5 so được với nền.

## Bước 5 — Đo lại và đóng đợt
- **Vào:** Đã xong Bước 4.
- **Việc:**
  1. Chạy lại 3 phiên chuẩn với cùng đầu vào, cùng model và tuyến, cùng điểm đo. So sánh đối chứng với số liệu nền. Model hoặc provider đổi phiên bản thì ghi lại và không kết luận trực tiếp.
  2. Cập nhật trạng thái các dòng E trong H0.
  3. Chuẩn bị gói Kaizen 2 theo `README_GOI_KAIZEN.md`, đổi mã theo bảng hệ mã mục 1.1.
  4. OWNER quyết định bật CI thành check bắt buộc, và chọn nhóm E đầu tiên chuyển về repo mẹ theo E15.
- **OWNER:** duyệt gói Kaizen 2; hai quyết định ở việc 4.
- **Xong khi:** Có bảng so sánh token theo vai giữa nền và sau Đợt 1; H0 đã cập nhật trạng thái; gói Kaizen 2 đã gửi.
- **Token:** Vừa.
- **Điểm dừng an toàn:** Nếu phiên chuẩn của LEAD giảm dưới 15% token thì không đi tiếp hướng tách ngữ cảnh động, mà điều tra lại nguyên nhân gốc rễ tiêu tốn token.

---

# PHẦN II — KHUNG ĐỊNH HƯỚNG CÁC ĐỢT TIẾP THEO

Sau Đợt 1, thứ tự và cách làm của các đợt tiếp theo căn cứ vào số liệu thực tế tại Bước 5. Mỗi đợt được chốt lại bằng gói thẩm định mới.

## Đợt 2 — An toàn, định tuyến model và WORKER trên tuyến free (K4 còn lại, K5)
- **Vào khi:** Đợt 1 đã đóng; E14 đã chốt ở Bước 0.
- **Việc chính:**
  - An toàn: nếu tách tài khoản mà chưa làm ở Bước 1, tạo tài khoản máy, bật ruleset có duyệt code owner và luật thẻ chỉ OWNER bypass (E11, E14).
  - Định tuyến:
    - Gộp "tuyến đã chứng minh" vào ELIGIBILITY và ROUTE_CHECKS; định nghĩa P4 (E10).
    - Kiểm tuyến bằng máy trước khi giao việc; preflight xác minh model thực tế (E21).
  - WORKER trên tuyến free (H3 mục 11, 13, 16, 17):
    1. Định nghĩa W1–W4, ngưỡng đạt và bộ task mẫu cho hạng T0, T1 (E19).
    2. Hạng task trong task spec, thang leo tuyến, phép kiểm CLAIM_MISMATCH trong loop (E17).
    3. Ngân sách context và hạn mức (request mỗi phút, mỗi ngày, đồng thời) của từng tuyến trong MODEL_CATALOG; chặn giao khi vượt (H3-1).
    4. Khung thời gian, hạn mức và ngắt mạch cho riêng tuyến free (H3-17).
    5. Chạy W1–W4 cho các tuyến free định dùng; tuyến đạt mới được nhận task T0, T1.
  - Viết script `scan` cho 06_sources/ (trước đây dự kiến ở CYC-06; E2).
- **Chỉ số đo lường:**
  - Số lượt giao việc hoặc kiểm định hỏng vì model (nền: 3/5 lượt kiểm định hỏng).
  - Theo tuyến và hạng task: tỷ lệ đạt lần đầu, tỷ lệ CLAIM_MISMATCH, Cost per Accepted Task của tuyến free so với tuyến trả phí (H4-7).
- **Lưu ý:** Chu kỳ sản phẩm mở lại sau Đợt 1. Tới khi tuyến free đạt W1–W4, task sản phẩm dùng tuyến trả phí.

## Đợt 3 — Hạ tầng và khôi phục (K6)
- **Vào khi:** Đợt 1 đã có số đo tách bạch độ sẵn sàng và chất lượng (E8).
- **Việc chính:**
  - Ngắt mạch chung cho mọi tuyến (E13), dùng bảng lỗi thống nhất đã có từ Bước 3 (E18).
  - Thống nhất relay; chuyển phiên có chặn triệt để phiên cũ. Nếu điểm đo token nằm ở relay, đo song song bản cũ và bản mới ít nhất một lần để nối số liệu.
  - Mô tả đầy đủ lớp hạ tầng thực thi (relay, Codex CLI, pwsh) vào khung quy ước.
  - Xử lý kịch bản khi token GitHub hết hạn. Theo bảng hệ mã đây là S6 (bản trước ghi S8, mà S8 là trôi trạng thái); CHƯA XÁC MINH.
  - Nhật ký phê duyệt lệnh, nếu công cụ tác tử chưa tự ghi (H4-3).
- **Chỉ số đo lường:** Số lần quy trình bị tắc nghẽn chờ OWNER xử lý vì lỗi hạ tầng.
- **Lưu ý:** Nếu số đo của Đợt 1 cho thấy lỗi hạ tầng rất hiếm, đợt này có thể thu nhỏ hoặc gộp vào Đợt 2.

## Đợt 4 — Trải nghiệm OWNER và Brainstorm (K7, E1, E3)
- **Vào khi:** Đã có script `state` (sinh STATE tự động); công cụ `validate` đã hoạt động ổn định.
- **Việc chính:**
  - File STATE được sinh tự động, cấu trúc để đọc hiểu nhanh trong 30 giây.
  - Khối STATUS chuẩn 4 dòng (H4-9); báo cáo PR cô đọng dưới 30 dòng.
  - Triển khai vai ADVISOR (E1) cùng lúc với Basic Plan và bước LEAD tiếp nhận (E3); bước tiếp nhận kích hoạt theo người đề xuất nội dung. Áp dụng cho dự án mới.
  - Script dựng phần cơ học của gói Kaizen từ neo ANCHOR (README "Người chuẩn bị").
  - Triển khai script `get` và cơ chế cắt ngữ cảnh động nếu Đợt 1 cho thấy việc tách file tĩnh chưa đủ.

## Quy trình sau mỗi đợt
1. **Đo lại:** Đánh giá số liệu thực nghiệm theo chỉ số mục tiêu của đợt, cùng điểm đo với lần trước.
2. **Cập nhật hồ sơ:** Cập nhật trạng thái các dòng E trong H0 (`ACCEPTED` / `REJECTED`); ghi nhận dữ kiện mới (N11, N12…).
3. **Thẩm định độc lập:** Gửi gói thẩm định mới theo `README_GOI_KAIZEN.md` để chốt nội dung đợt kế tiếp. Thứ tự Đợt 2, 3, 4 có thể linh hoạt điều chỉnh theo dữ liệu đo lường.
4. **Chuyển giao:** Chuyển giao các nhóm PROPOSAL đã ổn định về repo mẹ theo E15.

---

# PHẦN III — LƯU Ý KHI THỰC HIỆN RẢI RÁC

- **E14 chốt ở Bước 0:** RSK-0004 là rủi ro mức HIGH và có hạn định trong sổ. Nếu chưa chốt kịp, cập nhật dòng trạng thái mới cho RSK để dời hạn, tuyệt đối không để quá hạn vô thừa nhận.
- **Ghi điểm dừng vào STATE khi tạm nghỉ:** Mục *Next action* trong `04_control/STATE.md` ghi rõ đang ở bước nào, PR nào đang mở. Lần sau mở phiên mới, LEAD chỉ cần đọc STATE là nắm ngữ cảnh, không tốn token quét lại nhiều file.
- **Kiểm soát song song PR:** Tại mỗi thời điểm chỉ mở tối đa một PR `lead/` và một PR `upgrade/`. Mỗi PR `upgrade/` tăng VERSION, nên hai PR `upgrade/` cùng mở sẽ đụng nhau ở file VERSION (E25 đang xét).
- **Dồn tài nguyên:** Chu kỳ sản phẩm tạm dừng cho tới khi hoàn tất Bước 5 của Đợt 1.
- **Thời gian OWNER là nút thắt:** OWNER là cổng tuần tự của mọi merge và mọi quyết định. Gom quyết định theo bước như bảng dưới, không để rải rác giữa chừng.

## Việc của OWNER theo bước (Đợt 1)

| Bước | Quyết định | Thao tác |
| --- | --- | --- |
| 0 | E15; E14; 5 quyết định chặn | 1 merge |
| 1 | — | Ruleset, secret scanning, push protection trên giao diện GitHub |
| 2 | Nhóm E của Bước 3 | 2 merge |
| 3 | Ra lệnh cho PR chạm `.github/` | 5 merge, tuần tự |
| 4 | — | 3 merge |
| 5 | CI bắt buộc; nhóm E đầu tiên về repo mẹ | Duyệt gói Kaizen 2 |
