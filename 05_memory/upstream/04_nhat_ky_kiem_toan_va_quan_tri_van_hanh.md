Bản tham khảo 2026-11-22. Nguồn hiện hành: SRC-0003 P6d, DEC-0032.

# H4 — Nhật ký kiểm toán và quản trị vận hành

- Trạng thái: DỰ THẢO; chưa mục nào có hiệu lực.
- Nguồn: đúc kết từ phiên thi công CYC03-B2 (TK-0027). Hồ sơ cũ không ghi ngày, model.
- Biên tập lại: 2026-11-19, theo thẩm định Kaizen.
- Cập nhật 2026-11-21: ngữ nghĩa khóa model (E21); hiệu lực DEC có thời hạn (E12); bằng chứng thô và bản đã che (E22); nhãn vai, hạng task và điểm đo cố định (E8); chỉ số tuyến theo hạng (E19); quét secret ở pre-push (E23); fixer loại checks/.
- Hồ sơ được commit ở trạng thái DỰ THẢO (xem H0); chờ OWNER chốt các PROPOSAL.

## 1. Bổ sung schema run
Nhãn: GỘP (vào schema run hiện có) | Đợt: Đ3a | PROPOSAL: E7, E12, E21
- Khóa model hiện có nhận chuỗi hoặc danh sách mã catalog. Không thêm khóa actual_model.
- Ngữ nghĩa (E21, 2026-11-21): mỗi phần tử là mã catalog của một model thực tế đã được preflight hoặc relay xác minh từ metadata response trong run đó. Danh sách có nhiều phần tử khi run dùng nhiều model, ví dụ sau khi leo bậc (H3-16). Tên tuyến không được ghi vào khóa này.
- Phép kiểm SAME_MODEL của validate: REVIEWER hợp lệ khi danh sách model của REVIEWER không giao với danh sách model của mọi WORKER trong chu kỳ.
- Thêm một khóa ghi loại bằng chứng: raw (output gốc của tiến trình), derived (kết quả tính toán, so sánh), report (lời trần thuật của model, tin cậy thấp nhất). Tên khóa: [LEAD chốt]. Không đổi kiểu của khóa evidence hiện có.
- Ghi thêm trong run (tên khóa: [LEAD chốt]): hạng task (E17), tuyến trước và sau khi leo bậc, kết quả phép kiểm CLAIM_MISMATCH.
- Đổi schema mức MINOR, đi qua PR upgrade/, chỉ áp cho run sau mốc kiểm.

## 2. Thời hạn của quyết định
Nhãn: GỘP (vào DEC) | Đợt: [ĐỢT: LEAD chốt] | PROPOSAL: E12
- Quyết định lâu dài của OWNER ghi thành DEC. Thêm khóa tùy chọn về thời hạn hiệu lực vào decision.schema.json; đổi schema mức MINOR, đi qua upgrade/.
- Dòng Status giữ đúng ngữ pháp hiện hành (ACTIVE / SUPERSEDED_BY DEC-nnnn / RETIRED), không thêm khóa.
- Hiệu lực (bổ sung 2026-11-21): DEC có hiệu lực khi Status là ACTIVE và chưa quá thời hạn. validate tính hiệu lực theo quy tắc này; khi DEC quá hạn, LEAD thêm dòng RETIRED (sổ chỉ thêm dòng). Không để hai nguồn sự thật về việc DEC còn hiệu lực.
- Quyết định cấp phiên hoặc cấp PID (ví dụ bypass ExecutionPolicy tạm thời) ghi vào log của trace, kèm nguyên văn, người ban hành, thời điểm UTC, phạm vi. Tới khi có trace (Đ3b), ghi tạm vào [LEAD chốt nơi ghi].
- Không dùng hệ mã riêng cho quyết định của OWNER.

## 3. Nhật ký phê duyệt lệnh
Nhãn: HOÃN (K6) | Đợt: Đợt 3 | PROPOSAL: E13
- Với phiên chạy chế độ hỏi quyền (on-request): ghi lệnh đầy đủ, cờ require_escalated, duyệt hay từ chối, người duyệt, thời điểm.
- Xem trước công cụ tác tử đã tự ghi chưa, rồi mới quyết làm.

## 4. Raw capture: đầu ra của trace
Nhãn: GIỮ | Đợt: Đ3b | PROPOSAL: E7, E22
- Không chỉ báo con số kiểu "18 passed".
- Mỗi lần chạy kiểm ghi: argv đầy đủ; cwd; exit code; stdout, stderr nguyên văn; phiên bản Python, pytest; hash của file log thô.
- Nơi lưu (E22, 2026-11-21): cwd, stdout, stderr có thể chứa đường dẫn máy cá nhân hoặc bí mật, mà repo dry run là public.
  - Bản thô, nguyên byte, kèm hash, lưu ở <project>.local, không commit.
  - Bản commit vào 03_output/CYC-nn/checks/ là bản đã che (đường dẫn cá nhân, giá trị bí mật), kèm hash của bản thô và hash của bản đã che.
  - Kiểm chứng: so hash bản thô ở máy OWNER; người ngoài đối chiếu bản đã che.
- Đây là đặc tả đầu ra của script trace. Lần chạy lại verify do máy (H2 mục 6) là nguồn raw capture duy nhất cho LEAD và REVIEWER.

## 5. Ảnh chụp môi trường
Nhãn: GIỮ (bản rút gọn) | Đợt: Đ1 | PROPOSAL: không
- Chụp đầu mỗi chu kỳ hoặc ngay sau sự cố: phiên bản Git, Python, pytest, 9Router, Codex CLI, bản relay đang chạy; ExecutionPolicy; thư mục đã trust; PID, port, hash của script relay.
- Lưu ở <project>.local, không commit. Repo dry run là public; PATH và cấu hình Git có thể lộ thông tin.

## 6. Hạch toán token theo vai, task và tuyến
Nhãn: GIỮ | Đợt: Đ1 | PROPOSAL: E8
- Ghi prompt_tokens, cached_tokens, completion_tokens cho mỗi lượt gọi.
- Nhãn: session_id, role (LEAD, ADVISOR, WORKER, REVIEWER), task_id (để trống với phiên không gắn task, như phiên LEAD), route_name, hạng task (bổ sung 2026-11-21). Thiếu nhãn role thì không tính được "số đo nền theo vai" mà Đ1 cần.
- Điểm đo cố định: chọn một điểm duy nhất và giữ nguyên từ Đ1 tới Đ5 (bổ sung 2026-11-21).
  - Ưu tiên: 9Router (alias theo vai) hoặc harness đọc usage từ response.
  - Nếu đo ở relay: chỉ khi đã xác định bản relay đang chạy (H0 mục 5) và bản đó không bị thay trước Đ5.
- Mục tiêu: tính Cost per Accepted Task làm căn cứ giữ hay loại một tuyến (H3-13). Chỉ số tính cả các lần thử hỏng và token LEAD dành cho task đó.
- Đây là số đo nền theo vai mà đợt Kaizen đầu cần.

## 7. Sổ kiểm định tuyến
Nhãn: GỘP (vào MODEL_CATALOG#ROUTE_CHECKS) | Đợt: Đợt 2 | PROPOSAL: E10, E19
- ROUTE_CHECKS ghi thêm: cấu hình chạy thật của tuyến, kết quả P4, W1–W4 theo từng hạng task, khả năng làm REVIEWER, ngân sách context, hạn mức (request mỗi phút, mỗi ngày, đồng thời), thời điểm kiểm, phiên bản model hoặc provider.
- Chỉ số vận hành theo tuyến và hạng task (E19, 2026-11-21), cập nhật sau mỗi batch:
  - Tỷ lệ đạt ngay lần đầu.
  - Tỷ lệ CLAIM_MISMATCH.
  - Độ trễ trung vị.
  - Tỷ lệ lỗi hạ tầng.
  - Cost per Accepted Task.
- Tuyến vượt ngưỡng tỷ lệ FAIL hoặc CLAIM_MISMATCH thì về UNQUALIFIED cho hạng đó. Ngưỡng: [LEAD chốt].
- Provider đổi phiên bản thì tuyến về UNQUALIFIED và phải kiểm lại.

## 8. Báo cáo sự cố
Nhãn: GỘP (vào REQ) | Đợt: [ĐỢT: LEAD chốt] | PROPOSAL: không
- Sự cố ghi thành REQ theo mẫu 4 mục:
  - Diễn biến và tác động.
  - Phát hiện và khoanh vùng.
  - Nguyên nhân: tách "đã xác minh bằng chứng" và "mới là giả thuyết".
  - Khắc phục: việc cần làm, người phụ trách, hạn.

## 9. Khối trạng thái gửi OWNER
Nhãn: GỘP (vào harness/CHAT_UX.md) | Đợt: Đợt 4 (có thể làm sớm hơn nếu LEAD chốt) | PROPOSAL: không
- Dòng 1: đối tượng chính (task, PR hay phiên).
- Dòng 2: thay đổi kể từ lần trước.
- Dòng 3: điểm nghẽn (chờ ai, cần quyết gì).
- Dòng 4: rủi ro còn lại.
- Lý do đề xuất đưa lên sớm (2026-11-21): thời gian OWNER là nguồn khan nhất (H0 mục 2); khối trạng thái ngắn giúp OWNER chốt nhanh hơn.

## 10. Quét secret và nơi lưu bằng chứng
Nhãn: GIỮ | Đợt: Đ1 (push protection phía GitHub), Đ3b (hook pre-push) | PROPOSAL: E9, E23
- Kho cố định của bằng chứng là 03_output/CYC-nn/checks/ (bản đã che, mục 4). scratch/ chỉ là vùng tạm.
- Thời điểm quét (E23, sửa 2026-11-21): repo dry run là public, nên đẩy nhánh đã là công khai.
  - Quét secret tự động ở pre-push (tools/hooks/), có che giá trị trong báo cáo.
  - Quét lại trước khi nộp gói kiểm định.
  - Hook có thể bị bỏ qua, nên preflight đầu phiên hoặc github_audit kiểm lại các nhánh đã đẩy.
- Che giá trị chỉ áp cho báo cáo quét và bản commit; bản thô kèm hash giữ ở <project>.local (mục 4).

## 11. Linter có sẵn thay một phần script tự viết
Nhãn: GIỮ | Đợt: Đ3b | PROPOSAL: E9, E24
- Chỉ dùng công cụ cài qua pip:
  - check-jsonschema: kiểm phần YAML đầu file của task, run, DEC theo schema.
  - pre-commit-hooks: mixed-line-ending, end-of-file-fixer. Hai công cụ này sửa file, nên loại trừ 03_output/**/checks/ để không phá hash bằng chứng (E22).
  - detect-secrets: quét secret.
- Gọi các công cụ từ tools/hooks/ hiện có. Không dùng khung pre-commit để cài hook: xung đột với core.hooksPath = tools/hooks và tải hook từ mạng lúc chạy.
- Thêm thư viện là sửa file khai báo gói (🔒), cần DEC. Ghi rõ đây là công cụ của khung, tách khỏi phụ thuộc của sản phẩm nếu file khai báo cho phép: [LEAD chốt].
- Script vẫn phải tự viết:
  - validate cho các kiểm ngữ nghĩa: write_scope, SAME_MODEL (theo mục 1), kiểm trôi, hiệu lực DEC (mục 2), test được phép đổi (E20), hạng task (E17).
  - state (sinh STATE.md từ sổ gốc).
  - ledger, discuss (cấp mã tuần tự, chuyển kho lạnh).
  - trace, loop (điều phối vòng lặp, phép kiểm CLAIM_MISMATCH, leo bậc tuyến).

## Đã loại
- Chuỗi băm prev_record_sha256 → Git đã bảo đảm lịch sử bất biến.
- Sổ mục lục INDEX.jsonl → trùng run, loop, trace; lại đặt trong scratch/ là vùng tạm.
- Sổ quyết định OWNER riêng và hệ mã OWNER-DEC → trùng DEC, trái LEAD.md luật 9.
- markdownlint-cli2, gitleaks → cần Node hoặc binary ngoài danh sách nền (H3 mục 14, E24); muốn dùng thì cần DEC.
- Khung pre-commit để cài hook → xung đột core.hooksPath, tải hook từ mạng.
- "Thay 80% code của validate" → không có số đo; validate chủ yếu là kiểm ngữ nghĩa.
- Commit raw capture nguyên văn vào checks/ → lộ đường dẫn cá nhân trong repo public; che giá trị trên chính bản đó thì phá hash (2026-11-21).
- Quét secret chỉ trước khi mở PR → quá muộn với repo public (2026-11-21).
