# MODEL POLICY — CATALOG, MA TRẬN ƯU TIÊN VÀ FALLBACK

Chi tiết của `harness/HARNESS.md` mục 3.5. Hai file dữ liệu thuộc dự án, tạo từ mẫu trong `harness/templates/`:

| File | Trả lời câu hỏi | Mẫu | Schema |
|---|---|---|---|
| `04_control/MODEL_CATALOG.md` | Model này là gì, thông tin lấy từ đâu, cập nhật khi nào | `model_catalog.md` | `model_catalog.schema.json` |
| `04_control/MODEL_MATRIX.md` | Vai nào dùng model nào, theo thứ tự nào, hết thì sao | `model_matrix.md` | `model_matrix.schema.json` |

Cả hai là nguồn **tra cứu**. Quyết định vẫn nằm ở `DEC`: một `DEC` đang `ACTIVE` mâu thuẫn với ma trận thì `DEC` thắng và LEAD sửa ma trận trong PR kế tiếp. Hai file thuộc vùng 🔒; mọi thay đổi đi qua PR do OWNER merge.

## 1. Catalog

<!-- ANCHOR: CATALOG_FIELDS -->
| Khóa | Giá trị | Quy tắc |
|---|---|---|
| `code` | Mã model cụ thể, đúng chuỗi công cụ hiển thị, kể cả hậu tố biến thể | Định danh duy nhất. Hai biến thể của một dòng là hai mục riêng |
| `provider` | Nhà cung cấp, hoặc `unverified` | Chỉ ghi tên khi có nguồn ở `provider_source` |
| `provider_source` | Con trỏ, URL, hoặc `none` | |
| `group` | Nhóm dùng để xét tính độc lập giữa REVIEWER và WORKER, hoặc `unverified` | Lấy từ một `DEC` hoặc từ nhà cung cấp đã có nguồn |
| `group_source` | Con trỏ hoặc `none` | |
| `aliases` | Danh sách bí danh: tên combo, tên rút gọn, tên hiển thị khác | Bí danh không dùng thay `code` trong bản ghi |
| `recommended_roles` | Tập con của `BRAINSTORM`, `PLANNING`, `REVIEWER`, `WORKER` | Là khuyến nghị; quyền dùng thật do ma trận quy định |
| `capability_source` | Con trỏ, URL, hoặc `none` | `none` nghĩa là chưa có căn cứ để khẳng định năng lực |
| `price_source` | URL, hoặc `none` | Không chép con số giá vào catalog; giá đổi theo thời gian, đọc ở nguồn |
| `availability` | `confirmed` · `unconfirmed` · `unavailable` | `confirmed` cần `availability_evidence` |
| `availability_evidence` | Con trỏ tới bản ghi có model này chạy thật, hoặc `none` | |
| `updated` | `YYYY-MM-DD` | Ngày kiểm lại mục này lần gần nhất |
<!-- END: CATALOG_FIELDS -->

- Không khẳng định năng lực, chi phí, cửa sổ ngữ cảnh hay thứ hạng của một model khi `capability_source` hoặc `price_source` là `none`.
- Tên dòng model ("Claude Opus", "Gemini Pro") không phải `code`. Một dòng model không tự kéo theo mọi biến thể của nó.
- Mục có `updated` cũ hơn 90 ngày được coi là cần kiểm lại trước khi dùng làm căn cứ xếp tier.
- Catalog chỉ thêm và sửa mục; model ngừng dùng thì đặt `availability: unavailable`, không xóa mục, vì bản ghi cũ còn trỏ tới `code` đó.

## 2. Tier

<!-- ANCHOR: TIERS -->
| Tier | Điều kiện | Dùng cho |
|---|---|---|
| `T1` | Đủ cả bốn: (1) là một `code` cụ thể trong catalog; (2) `availability: confirmed`; (3) `capability_source` khác `none`, hoặc OWNER ghi rõ chấp nhận không có nguồn trong `DEC` duyệt; (4) nằm trong `tier1` của ma trận, kèm `DEC` duyệt ở `tier1_approved_by` | Mọi vai; bắt buộc cho `BRAINSTORM` |
| `T2` | Điều kiện (1), (2) và nằm trong `tier2` của ma trận | `PLANNING`, `REVIEWER`, `WORKER` |
| `T3` | Điều kiện (1), (2) và nằm trong `tier3` của ma trận | `WORKER` |
| `UNRATED` | Có trong catalog nhưng không nằm trong tier nào | Không được giao vai nào theo ma trận |
<!-- END: TIERS -->

- Xếp tier là quyết định của OWNER, ghi bằng `DEC`. LEAD chỉ đề xuất.
- Ma trận có `status: PROPOSED` là đề xuất của LEAD: các danh sách tier và `order` trong đó chưa có hiệu lực, kể cả khi file đã ở trên `main`. Ma trận có hiệu lực khi `status: APPROVED` và `tier1_approved_by` trỏ một `DEC` do OWNER quyết.
- Không mặc định mọi biến thể của một dòng là tương đương: biến thể nhỏ, nhanh, rẻ hoặc đời cũ của một dòng `T1` là `UNRATED` cho tới khi được duyệt riêng.
- Các dòng OWNER nêu làm ứng viên `T1` (ghi ở `tier1_candidate_families` của ma trận) chỉ là định hướng tìm `code`; chúng không cấp tier.

## 3. Thứ tự ưu tiên theo vai

<!-- ANCHOR: ROLE_ORDER -->
| Vai | Phiên | Tier tối thiểu | Thứ tự | Fallback |
|---|---|---|---|---|
| `BRAINSTORM` | `DISCUSS`, phase `BRAINSTORM` | `T1` | Theo `order` của vai trong ma trận | Chỉ trong `T1`. Hết `T1` thì dừng |
| `PLANNING` | LEAD lập plan, `CHANGE`, điều phối | `T2` | `T1` trước, rồi `T2` | Xuống `T2` được phép; LEAD nêu model thực tế trong khối cuối |
| `REVIEWER` | Kiểm định chu kỳ, kiểm thử độc lập | `T2` | `T1` trước, rồi `T2`, sau khi loại các model vi phạm mục 4 | Chỉ sang model vẫn đạt mục 4. Hết thì dừng |
| `WORKER` | `RUN` | `T3` | `T2` trước, rồi `T3` | Xuống `T3` được phép |
<!-- END: ROLE_ORDER -->

`order` và `fallback` trong ma trận là danh sách `code` cụ thể. Combo trên cổng model (`harness/tools/INTEGRATION.md#MODEL_GROUPS`) chỉ được chứa các `code` mà ma trận cho phép đối với vai đó.

## 4. Tính độc lập của REVIEWER

1. `reviewer_model` khác mọi giá trị `model` của các run trong chu kỳ, kể cả run `BLOCKED`.
2. `group` của REVIEWER khác `group` của mọi WORKER đó. `group: unverified` được coi là trùng.
3. REVIEWER đáp ứng mọi `DEC` đang `ACTIVE` về phân công model của chu kỳ.
4. Kiểm cả ba điều trước khi giao kiểm định (`PREFLIGHT.md` mục 2, dòng 13) và khi LEAD review PR của REVIEWER. Bản kiểm định vi phạm thì không được merge; có tính là một vòng hay không do OWNER quyết bằng `DEC`.

## 5. Model yêu cầu và model thực tế

<!-- ANCHOR: REQUESTED_ACTUAL -->
| Thứ | Ghi ở đâu | Ai ghi | Khi nào |
|---|---|---|---|
| Model yêu cầu | Neo `ASSIGNMENTS` của ma trận, khóa `requested` | LEAD | Khi giao việc |
| Model thực tế | `model` của run và `DSC`, `reviewer_model` của `RVW`; lấy từ nhật ký công cụ | Phiên làm việc | Cuối phiên |
| Đối chiếu | Neo `ASSIGNMENTS` của ma trận, khóa `actual` và `match` | LEAD | Khi review PR của phiên |
<!-- END: REQUESTED_ACTUAL -->

Dòng phân công: `- CYC-nn | <ROLE> | requested: <code hoặc nhóm> | actual: <code> | record: <con trỏ> | match: yes|no`.

`match: no` chưa phải lỗi: cổng model có thể tự chuyển model. LEAD kiểm model thực tế có hợp lệ với vai theo mục 3 và mục 4 không. Hợp lệ thì tiếp tục. Không hợp lệ thì LEAD không xuất khối `MERGE` cho PR đó và đưa về OWNER bằng khối `QUESTION`.

## 6. Khi không có model hợp lệ

- Dừng. Xuất khối `QUESTION` nêu vai, tier yêu cầu, danh sách đã thử và lý do từng model không hợp lệ.
- Không tự hạ tier, không tự dùng model `UNRATED`, không tự nới mục 4.
- Danh sách fallback không bảo đảm hệ thống luôn vận hành được; nó chỉ nêu thứ tự thử. Hết danh sách là một blocker cần OWNER xử lý.
- `tier1` rỗng thì chưa mở được phiên `BRAINSTORM` mới theo chính sách này; OWNER duyệt ít nhất một `code` trước.

## 7. Điều còn mở

| # | Điều | Trạng thái |
|:---:|---|---|
| 1 | Thêm trường tùy chọn `requested_model` vào schema của run, `DSC`, `RVW` (schema 2, mức MINOR theo `harness/schemas/EVOLUTION.md`) để model yêu cầu nằm ngay trong bản ghi | Chờ OWNER quyết; hiện ghi ở neo `ASSIGNMENTS` |
| 2 | Ngưỡng 90 ngày ở mục 1 | Đề xuất; OWNER đổi được |
