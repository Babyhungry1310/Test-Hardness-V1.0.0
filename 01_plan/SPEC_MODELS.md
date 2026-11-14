# SPEC_MODELS — PHÂN CÔNG MODEL CHO CYC-03 TỚI CYC-07

Nguồn: DEC-0016, DEC-0017, `harness/MODEL_POLICY.md`. Nguồn tra cứu khi chạy: `04_control/MODEL_CATALOG.md`, `04_control/MODEL_MATRIX.md`, trường `assignee` của task, và file này. File này không cấp quyền: mã nào không còn hợp lệ theo catalog và ma trận trên `origin/main` thì không được dùng, dù có tên ở đây.

<!-- ANCHOR: SLOTS -->
## 1. Chỗ WORKER và REVIEWER
| Chỗ | Loại việc | Model ưu tiên · tuyến | Dự phòng theo thứ tự · tuyến | Dừng khi |
|---|---|---|---|---|
| W1 | Logic, thuật toán, công cụ, unit test | `gpt-5.6-luna` · `cx/gpt-5.6-luna` | `gpt-6.1-sol` · `cx/gpt-6.1-sol` | Cả hai tuyến lỗi hoặc trả về mã ngoài danh sách |
| W2 | Triển khai, tích hợp, tài liệu | `claude-sonnet-4-6` · `ag/claude-sonnet-4-6` | `gpt-6.1-sol` · `cx/gpt-6.1-sol` | Cả hai tuyến lỗi hoặc trả về mã ngoài danh sách |
| W3 | Ca biên, stress, bảo mật, phản biện | `grok-4.7` · `xai/grok-4.7` | `grok-4.6` · `xai/grok-4.6`; rồi `gpt-5.6-luna` · `cx/gpt-5.6-luna` | Cả ba tuyến lỗi hoặc trả về mã ngoài danh sách |
| REVIEWER | Kiểm định chu kỳ, hồi quy toàn bộ | `gemini-3.8-flash-n` · `ag/gemini-3.8-flash` | `claude-opus-4-6-thinking` · `ag/claude-opus-4-6-thinking`, chỉ khi không run nào của chu kỳ có model nhóm `claude` | Không còn mã nào khác mã và khác nhóm với mọi WORKER của chu kỳ |
| LEAD | Điều phối, phản biện đặc tả | Theo `order` của PLANNING trong ma trận | `claude-opus-4-6-thinking`, rồi `claude-sonnet-5-5` | Không có mã PLANNING hợp lệ |
<!-- END: SLOTS -->

<!-- ANCHOR: RULES -->
## 2. Quy tắc
- Trước DEC-0017 ở `origin/main`: W2 dùng `gpt-6.1-sol`, W3 dùng `gpt-5.6-luna` (phân công tạm của DEC-0016); không gọi tuyến `ag/claude-*` hay `xai/*` cho bất kỳ vai nào.
- Mỗi phiên gọi đúng tên tuyến ghi ở `aliases` của catalog. Không gọi combo, không gọi tuyến mà tên khác model trả về.
- Model thực tế lấy từ phản hồi của công cụ hoặc API, ghi vào `model` của run và `reviewer_model` của `RVW`. Không xác nhận được: `BLOCKED`. Không ghi nhãn Antigravity, Grok, Opus hay Sonnet cho một phiên khi model thực tế chưa được xác nhận.
- Model thực tế khác model yêu cầu nhưng nằm trong danh sách của chỗ đó: tiếp tục, LEAD ghi `match: no`. Nằm ngoài danh sách, không có trong catalog, không thuộc tier của vai, hoặc `group: unverified`: dừng phiên đó, không dùng kết quả, chuyển sang dự phòng nếu còn loop.
- Đổi sang dự phòng không cấp thêm loop: mỗi task vẫn tối đa 3 loop, tính cả loop đầu. Hết dự phòng: task `BLOCKED`, áp điểm dừng 1 của `01_plan/SPEC_DRYRUN.md#STOPS`.
- REVIEWER khác mã và khác nhóm với model thực tế của mọi run trong chu kỳ, kể cả run `BLOCKED` và run chạy bằng dự phòng. Tên agent hay tên tuyến khác nhau không đủ. LEAD kiểm lại điều này sau khi mọi run của chu kỳ đã có, trước khi giao kiểm định.
- Không tự thêm model vào catalog hay ma trận, không tự hạ tier, không dùng model `UNRATED`.
<!-- END: RULES -->

<!-- ANCHOR: TASKS -->
## 3. Theo task
| Chu kỳ · batch | Task | Chỗ | Ưu tiên | Dự phòng |
|---|---|:---:|---|---|
| CYC-03 B1 | TK-0006 hook | W1 | `gpt-5.6-luna` | `gpt-6.1-sol` |
| CYC-03 B1 | TK-0007 pre-flight | W2 | `claude-sonnet-4-6` | `gpt-6.1-sol` |
| CYC-03 B1 | TK-0008 kiểm phía GitHub | W3 | `grok-4.7` | `grok-4.6`, `gpt-5.6-luna` |
| CYC-03 B2 | TK-0018 ca biên, ca lách | W3 | `grok-4.7` | `grok-4.6`, `gpt-5.6-luna` |
| CYC-04 B1 | TK-0009 kiểm schema model | W1 | `gpt-5.6-luna` | `gpt-6.1-sol` |
| CYC-04 B2 | TK-0010 chọn model, fallback | W1 | `gpt-5.6-luna` | `gpt-6.1-sol` |
| CYC-04 B2 | TK-0019 đối chiếu phân công | W3 | `grok-4.7` | `grok-4.6`, `gpt-5.6-luna` |
| CYC-05 B1 | TK-0011 tên nhánh | W1 | `gpt-5.6-luna` | `gpt-6.1-sol` |
| CYC-05 B1 | TK-0012 khối chat | W2 | `claude-sonnet-4-6` | `gpt-6.1-sol` |
| CYC-05 B1 | TK-0020 storage, trace | W3 | `grok-4.7` | `grok-4.6`, `gpt-5.6-luna` |
| CYC-05 B1 | TK-0021 clean liệt kê | W2 | `claude-sonnet-4-6` | `gpt-6.1-sol` |
| CYC-06 B1 | TK-0013 lõi scan | W1 | `gpt-5.6-luna` | `gpt-6.1-sol` |
| CYC-06 B2 | TK-0014 base64, giới hạn | W1 | `gpt-5.6-luna` | `gpt-6.1-sol` |
| CYC-06 B2 | TK-0022 cách ly, thẻ bọc | W2 | `claude-sonnet-4-6` | `gpt-6.1-sol` |
| CYC-06 B3 | TK-0023 phản biện scan | W3 | `grok-4.7` | `grok-4.6`, `gpt-5.6-luna` |
| CYC-07 B1 | TK-0015 kiểm batch | W1 | `gpt-5.6-luna` | `gpt-6.1-sol` |
| CYC-07 B1 | TK-0016 mẫu pytest.ini | W2 | `claude-sonnet-4-6` | `gpt-6.1-sol` |
| CYC-07 B1 | TK-0024 tương thích pytest | W3 | `grok-4.7` | `grok-4.6`, `gpt-5.6-luna` |
| CYC-07 B1 | TK-0025 worktree, nền tạm | W2 | `claude-sonnet-4-6` | `gpt-6.1-sol` |
| CYC-07 B2 | TK-0026 tài liệu | W2 | `claude-sonnet-4-6` | `gpt-6.1-sol` |
| CYC-07 B3 | TK-0017 hồi quy Windows | W3 | `grok-4.7` | `grok-4.6`, `gpt-5.6-luna` |
<!-- END: TASKS -->

<!-- ANCHOR: REVIEW -->
## 4. Kiểm định
- CYC-03, CYC-05, CYC-06, CYC-07 có task của W2: khi W2 chạy bằng `claude-sonnet-4-6`, REVIEWER chỉ có `gemini-3.8-flash-n`; tuyến đó lỗi thì kiểm định `BLOCKED`.
- CYC-04 không có task của W2: REVIEWER dự phòng `claude-opus-4-6-thinking` hợp lệ khi không run nào của chu kỳ dùng model nhóm `claude`.
- W3 rơi về `gpt-5.6-luna` không ảnh hưởng REVIEWER `gemini-3.8-flash-n`.
<!-- END: REVIEW -->
