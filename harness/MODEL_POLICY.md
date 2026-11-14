# MODEL POLICY — CHỌN MODEL THEO LẦN GIAO VIỆC

Chi tiết của `harness/HARNESS.md` mục 3.5. Hai file dữ liệu thuộc dự án, tạo từ mẫu trong `harness/templates/`:

| File | Trả lời câu hỏi | Mẫu | Schema |
|---|---|---|---|
| `04_control/MODEL_CATALOG.md` | Model nào đã được kiểm chạy được, qua tuyến nào, khi nào, bằng cách kiểm nào | `model_catalog.md` | `model_catalog.schema.json` |
| `04_control/MODEL_MATRIX.md` | Lần giao nào yêu cầu model nào và model thực tế là gì | `model_matrix.md` | `model_matrix.schema.json` |

Cả hai là sổ **dữ kiện**, không cấp quyền. Hai file thuộc vùng 🔒 và chỉ đổi qua PR do OWNER merge; LEAD cập nhật chúng trong PR `lead/` kế tiếp, không cần `DEC` cho từng model và không cần chờ merge mới được dùng một model đã kiểm đạt. Một `DEC` đang `ACTIVE` về phân công thắng mọi lựa chọn của LEAD.

## 1. Catalog

<!-- ANCHOR: CATALOG_FIELDS -->
| Khóa | Giá trị | Quy tắc |
|---|---|---|
| `code` | Mã model gốc theo mục 4.1, đúng chuỗi hệ thống trả về sau khi bỏ hậu tố biến thể | Định danh duy nhất |
| `provider` | Nhà cung cấp, hoặc `unverified` | Chỉ ghi tên khi có nguồn ở `provider_source` |
| `provider_source` | Con trỏ, URL, hoặc `none` | |
| `group` | Nhóm model, hoặc `unverified` | Chỉ để tham khảo; không dùng để xét tính độc lập |
| `group_source` | Con trỏ hoặc `none` | |
| `aliases` | Tên tuyến và các chuỗi biến thể model đã ghi nhận | Tuyến chỉ gợi ý cách gọi; không chứng minh định danh model. Bí danh không dùng thay `code` trong bản ghi |
| `recommended_roles` | Tập con của `BRAINSTORM`, `PLANNING`, `REVIEWER`, `WORKER` | Là ghi nhận của LEAD; không cấp và không cấm vai nào |
| `capability_source` | Con trỏ, URL, hoặc `none` | `none` nghĩa là chưa có căn cứ để khẳng định năng lực |
| `price_source` | URL, hoặc `none` | Không chép con số giá vào catalog |
| `availability` | `confirmed` · `unconfirmed` · `unavailable` | `confirmed`: đã có phiên tác tử có công cụ chạy thật bằng model này. `unconfirmed`: mới kiểm bằng hỏi đáp ngắn hoặc chưa kiểm. `unavailable`: lần kiểm gần nhất lỗi |
| `availability_evidence` | Con trỏ tới run, `RVW`, `DSC`, hoặc tới neo `ROUTE_CHECKS` của catalog; `none` khi chưa có | Bắt buộc khác `none` khi `confirmed` |
| `updated` | `YYYY-MM-DD` | Ngày kiểm lại mục này lần gần nhất |
<!-- END: CATALOG_FIELDS -->

- Không khẳng định năng lực, chi phí, cửa sổ ngữ cảnh hay thứ hạng của một model khi `capability_source` hoặc `price_source` là `none`.
- Tên dòng model, tên tuyến, tên agent, tên combo không phải `code`.
- Khi gọi 9Router, gửi ID tuyến chính xác từ `GET /v1/models` hoặc alias đã kiểm là được chấp nhận; không gửi `code` thay tuyến nếu chưa kiểm. Danh sách ID chỉ chứng minh tuyến được liệt kê, không chứng minh gọi thành công, hỗ trợ công cụ hay model thực tế.
- Code lịch sử không có tuyến đã xác minh được giữ nguyên; không đoán tuyến hoặc thay bằng model khác trong bản ghi cũ.
- Catalog chỉ thêm và sửa mục; không xóa mục, vì bản ghi cũ còn trỏ tới `code` đó.

<!-- ANCHOR: ROUTE_CHECKS -->
Mỗi lần kiểm một tuyến, LEAD ghi một dòng vào neo `ROUTE_CHECKS` ở thân catalog, mới nhất ở trên:

`- <YYYY-MM-DDTHH:MMZ> | route: <tên tuyến đã gọi> | actual: <chuỗi model hệ thống trả về, hoặc none> | kind: chat|agent-tools | result: OK|FAIL | source: <công cụ hoặc API đã dùng> | note: <≤ 15 từ, hoặc none>`

- `kind: chat`: một lượt hỏi đáp ngắn. `kind: agent-tools`: một phiên tác tử gọi được ít nhất một công cụ đọc và trả về model thực tế.
- `actual` chép nguyên chuỗi nhận được, kể cả hậu tố. Không lấy từ tên tuyến. Không nhận được thì `none` và `result: FAIL`.
- `route` là ID gửi tới API; `code` là model kỳ vọng; `actual` là chuỗi phản hồi. Một route trong `aliases` không chứng minh model nó trả về ở lần gọi khác.
- Dòng kiểm không chứa khóa API, tiêu đề xác thực, nội dung prompt hay câu trả lời.
- Dòng kiểm được dùng ngay; nó vào `main` cùng PR `lead/` kế tiếp. Trước lúc đó LEAD giữ bản sao ở `<project>.local/logs/` và nêu trong báo cáo cho OWNER.
<!-- END: ROUTE_CHECKS -->

## 2. Model đủ điều kiện

<!-- ANCHOR: ELIGIBILITY -->
Một model được giao một vai khi đủ cả ba:

1. Có dòng `ROUTE_CHECKS` với `result: OK` cho đúng tuyến sẽ gọi, và dòng mới nhất của tuyến đó không phải `FAIL`.
2. Vai cần dùng công cụ (WORKER, REVIEWER, LEAD ở mọi loại phiên) thì dòng đó phải có `kind: agent-tools`, hoặc mục catalog đã `availability: confirmed`. Hỏi đáp ngắn không đủ.
3. `actual` của dòng đó quy về đúng `code` của mục catalog theo mục 4.1.

Tuyến trả về model khác với lần kiểm trước, hoặc tên tuyến khác model trả về: ghi dòng mới; model đủ điều kiện là model **thực tế trả về**, không phải model theo tên tuyến. Combo trên cổng model không được dùng để giao việc, trừ khi mọi thành phần của nó đều đủ điều kiện cho vai đó và đều thỏa mục 4.2 nếu là REVIEWER.
<!-- END: ELIGIBILITY -->

<!-- ANCHOR: TIERS -->
Tier (`T1`, `T2`, `T3`, `UNRATED`) không còn là điều kiện giao việc từ DEC-0018. Các khóa `status`, `tier1`, `tier2`, `tier3`, `tier1_candidate_families`, `tier1_approved_by`, `roles` trong `04_control/MODEL_MATRIX.md` giữ lại để bản ghi cũ còn hợp schema; chúng không có hiệu lực.
<!-- END: TIERS -->

## 3. Chọn model

<!-- ANCHOR: ROLE_ORDER -->
- Mỗi lần giao một task, một lượt kiểm định, hoặc mở một phiên LEAD, LEAD chọn một model đủ điều kiện theo mục 2. Không có thứ tự chọn cố định và không có danh sách fallback cố định; áp cho mọi vai, kể cả phiên `DISCUSS`.
- Căn cứ chọn: yêu cầu của công việc; khả năng thực tế đã thấy ở bản ghi của dự án; hạn mức còn lại. Căn cứ nào chưa xác minh được thì ghi `chưa xác minh`, không ước đoán; nếu điều chưa xác minh ảnh hưởng tới việc chọn thì báo OWNER bằng khối `QUESTION` trước khi giao.
- LEAD ghi lựa chọn và lý do ngắn ở dòng phân công (mục 5) trước khi phiên bắt đầu.
- Phiên lỗi vì model hoặc tuyến: LEAD được chọn model đủ điều kiện khác cho lần chạy tiếp. Đổi model không cấp thêm loop hay thêm vòng kiểm định.
- Một `DEC` đang `ACTIVE` chỉ định hoặc cấm model cho một phạm vi thì LEAD chọn trong giới hạn đó.
<!-- END: ROLE_ORDER -->

## 4. Tính độc lập của REVIEWER

### 4.1. Thế nào là cùng một model

<!-- ANCHOR: SAME_MODEL -->
- So sánh trên **model thực tế** hệ thống trả về cho từng phiên, không trên tên tuyến, tên agent, tên combo hay model yêu cầu.
- Mã gốc của một chuỗi model là chuỗi đó sau khi bỏ phần trong ngoặc vuông ở cuối. Ví dụ `gpt-5.6-luna[1m]` có mã gốc `gpt-5.6-luna`.
- Hai chuỗi model thực tế là cùng một model khi cùng mã gốc, hoặc có bằng chứng độc lập rằng hai chuỗi model thực tế là bí danh cùng model. Tên tuyến trong `aliases` hoặc `ROUTE_CHECKS` không tự chứng minh hai model là cùng hay khác.
- Hai chuỗi khác mã gốc là hai model khác nhau, kể cả khi cùng nhà cung cấp hay cùng dòng. Ví dụ `gpt-5.6-luna` và `gpt-5.6-terra` là hai model.
- Không chắc hai chuỗi có phải cùng một model hay không: coi là cùng, và hỏi OWNER.
- Khi đầu vào chỉ là tên tuyến, tên agent hoặc combo mà không có model thực tế do hệ thống trả về: không suy ra định danh; coi là chưa xác minh, không kết luận `different` hay cho qua kiểm độc lập. Nếu hệ thống thực sự trả một chuỗi có dấu `/`, giữ nguyên và xác minh bằng chứng; không tự loại hoặc bỏ tiền tố.
<!-- END: SAME_MODEL -->

### 4.2. Điều kiện

<!-- ANCHOR: REVIEWER_INDEPENDENCE -->
1. Model thực tế của REVIEWER khác, theo mục 4.1, với model thực tế của mọi run có sản phẩm nằm trong phần được kiểm định. Không bắt buộc khác nhóm hay khác nhà cung cấp.
2. Run không ghi được model thực tế thì không kiểm định được phần việc đó: dừng, báo OWNER.
3. REVIEWER đáp ứng mọi `DEC` đang `ACTIVE` về phân công model của phần được kiểm định.
4. Kiểm cả ba điều trước khi giao kiểm định (`PREFLIGHT.md` mục 2, dòng 13), lúc REVIEWER bắt đầu, và khi LEAD review PR của REVIEWER, mỗi lần đều theo model thực tế. Bản kiểm định vi phạm thì không được merge; có tính là một vòng hay không do OWNER quyết bằng `DEC`.
<!-- END: REVIEWER_INDEPENDENCE -->

## 5. Model yêu cầu và model thực tế

<!-- ANCHOR: REQUESTED_ACTUAL -->
| Thứ | Ghi ở đâu | Ai ghi | Khi nào |
|---|---|---|---|
| Model yêu cầu, tuyến, lý do chọn | Neo `ASSIGNMENTS` của `04_control/MODEL_MATRIX.md` | LEAD | Khi giao việc |
| Model thực tế | `model` của run và `DSC`, `reviewer_model` của `RVW`; lấy từ công cụ hoặc API của phiên | Phiên làm việc | Cuối phiên |
| Đối chiếu | Neo `ASSIGNMENTS`, khóa `actual` và `match` | LEAD | Khi review PR của phiên |
<!-- END: REQUESTED_ACTUAL -->

Dòng phân công: `- CYC-nn | <ROLE> | requested: <code> | actual: <chuỗi thực tế hoặc pending> | record: <con trỏ tới task, run hoặc RVW> | match: yes|no|pending | route: <tên tuyến> | basis: <lý do ≤ 15 từ; hạn mức: số liệu hoặc chưa xác minh>`. Hai khóa `route` và `basis` là tùy chọn với dòng lập trước DEC-0018.

- `match` so theo mục 4.1. `match: no` chưa phải lỗi: cổng model có thể tự chuyển model. LEAD kiểm model thực tế có đủ điều kiện theo mục 2 và, với REVIEWER, mục 4.2. Đạt thì tiếp tục. Không đạt thì LEAD không xuất khối `MERGE` cho PR đó và đưa về OWNER bằng khối `QUESTION`.
- Không xác định được model thực tế của một phiên: kết quả của phiên đó không được dùng; dừng và báo OWNER.

## 6. Khi không có model phù hợp

<!-- ANCHOR: NO_MODEL -->
- Dừng. Xuất khối `QUESTION` nêu vai, việc cần giao, các model đã xét và lý do từng model không dùng được.
- Không dùng model chưa đủ điều kiện ở mục 2, không nới mục 4.2, không dùng kết quả của phiên không rõ model thực tế.
- Không có REVIEWER thỏa mục 4.2: dừng phần kiểm định, báo OWNER; không để WORKER tự kiểm.
<!-- END: NO_MODEL -->

## 7. Điều còn mở

| # | Điều | Trạng thái |
|:---:|---|---|
| 1 | Thêm trường tùy chọn `requested_model` vào schema của run, `DSC`, `RVW` | Chờ OWNER quyết; hiện ghi ở neo `ASSIGNMENTS` |
| 2 | Nguồn đọc hạn mức trên cổng model | Chưa xác nhận (`harness/tools/INTEGRATION.md#FEATURES` dòng 9); tới khi có thì ghi `chưa xác minh` |
| 3 | Thời hạn hiệu lực của một dòng kiểm tuyến | Đề xuất: kiểm lại ở đầu mỗi phiên điều phối; OWNER đổi được |
| 4 | Bỏ hẳn các khóa tier khỏi schema của ma trận | Mức MAJOR theo `harness/schemas/EVOLUTION.md`; chưa làm |
