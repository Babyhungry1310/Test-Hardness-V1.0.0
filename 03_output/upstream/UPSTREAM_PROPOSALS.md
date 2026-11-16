# HỒ SƠ KIỂM KÊ VÀ ĐỀ XUẤT CẬP NHẬT KHUNG (UPSTREAM PROPOSALS)

Tài liệu kiểm kê toàn bộ các đề xuất nâng cấp khung Harness được đúc kết từ quá trình vận hành và thực nghiệm tại repo `Test-Hardness-V1.0.0`.

- Căn cứ quy định: `04_control/decisions/DEC-0020`, `04_control/requests/resolved/REQ-0007`, và `01_plan/SPEC_DRYRUN.md#UPSTREAM`.
- Trạng thái: DỰ THẢO KIỂM KÊ (Chờ hoàn thành đợt dry-run CYC-07 và OWNER phê duyệt trước khi chuyển giao về repo mẹ `Hardness-V1.0.0`).

---

## 1. Danh mục các tài liệu thành phần

* **Phần 1 — Vai trò Brainstorm & Ủy quyền tra cứu Web:**
  - File chi tiết: [`01_brainstorm_va_uy_quyen_web.md`](./01_brainstorm_va_uy_quyen_web.md)
  - Trọng tâm:
    - Định vị Fable là chuyên gia tư vấn kiến trúc (Advisor), không ôm đồm việc gõ plan chi tiết.
    - Cấu trúc **Basic Plan** (8 trường thông tin tối thiểu, không chứa verify/done_when).
    - Cổng tiếp nhận bắt buộc giữa Brainstorm và Planning (tối đa 2 vòng phản biện).
    - **Cơ chế Ủy quyền tra cứu Web:** Fable cấm duyệt web trực tiếp; xuất khối `RESEARCH_REQUEST` để User chuyển sang Orca (qua Clipboard hoặc thư mục dùng chung trên Desktop).

* **Phần 2 — Quyền Worker, Reviewer và Phòng thủ Prompt Injection:**
  - File chi tiết: [`02_quyen_worker_va_phong_thu_injection.md`](./02_quyen_worker_va_phong_thu_injection.md)
  - Trọng tâm:
    - Cấp quyền và chuẩn bị môi trường trước trong task: Worker chạy tự động qua 3 loop, chỉ dừng hỏi khi hết loop hoặc gặp vi phạm ranh giới.
    - Tách biệt: Lỗi quyền/môi trường không tính là một loop (chỉ lỗi logic mới tính loop).
    - Phân loại danh mục điểm dừng khẩn cấp (Sửa file 🔒, đụng `main`, xóa file ngoài scope, đổi bí mật...).
    - Nguyên tắc Zero-Trust: LEAD kết luận dựa trên diff và lệnh verify của máy, không tin vào văn xuôi của Worker; bọc dữ liệu và quét bằng script `scan`.
    - Chạy `verify` cách ly (Mức nhẹ: worktree riêng, không mang secret env, không quyền admin).

---

## 2. Bảng tổng hợp các điểm còn chờ OWNER chốt

1. **Về vai trò Fable:** Fable là LEAD của phiên DISCUSS hay là chuyên gia tư vấn đứng ngoài (để LEAD dự án lập `DSC`)?
2. **Về cổng tiếp nhận Basic Plan:** Bước tiếp nhận phản biện này là bắt buộc cho mọi dự án, hay chỉ áp dụng khi Basic Plan do một phiên khác LEAD soạn?
3. **Về danh mục điểm dừng của Worker:** Thống nhất danh sách điểm dừng khẩn cấp (mục 7.1 + phần chọn thêm ở mục 7.2).
4. **Về cách ly `verify`:** Phê duyệt triển khai ở mức nhẹ cho đợt nâng cấp tới và mở `RSK` theo dõi cho mức cách ly nâng cao (container).

---

## 3. Quy trình chuyển giao về Repo mẹ (`Hardness-V1.0.0`)

1. Tiếp tục hoàn thành các chu kỳ còn lại của dry-run (CYC-04 đến CYC-07).
2. Sau khi có kết quả kiểm định CYC-07: LEAD cập nhật bảng đối chiếu cuối cùng vào file này.
3. OWNER duyệt từng mục đề xuất.
4. Mở PR độc lập chuyển giao các thay đổi đã duyệt từ `Test-Hardness-V1.0.0` sang repo mẹ `Hardness-V1.0.0`.

---

## 4. Phần 3 — phản biện bản tổng hợp sau dry run

- File dự thảo: [03_phan_bien_bo_sung_sau_dry_run.md](./03_phan_bien_bo_sung_sau_dry_run.md).
- Nội dung: phân loại lỗi và thẩm quyền; tiêu chí task/preflight; loop và điểm dừng; quyền/sandbox; model và quota; injection; checkpoint và chi phí token; kiểm định, bằng chứng và thứ tự cập nhật.
- Trạng thái: ý kiến tư vấn và đề xuất do OWNER chuyển tới; chưa tự trở thành DEC, rule hoặc phê duyệt triển khai. Đối chiếu nguyên văn nguồn trong hội thoại trước khi chốt.
- Cập nhật dữ kiện tại 2026-11-16: PR #36 đã merge, PR #31 vẫn mở tại lượt kiểm; các câu nói khác về trạng thái PR/SHA trong nguồn là ảnh chụp lịch sử. Kiểm lại Git trước khi dùng.
- Hai file thành phần 01 và 02 được giữ nguyên từ bản OWNER cung cấp trong checkout ổ D. Bản tổng hợp bổ sung chi tiết từ phiên này nằm tại <project>.local/logs/orca-1.0.1/TONG_HOP_CAP_NHAT_HARDNESS.md; trước khi chuyển về repo mẹ cần kiểm kê, che bí mật và xác minh lại nguồn.
- Việc ghi vào thư mục này chưa chứng minh dry run hoàn tất; sau CYC-07 phải đối chiếu đường dẫn kiểm kê với SPEC_DRYRUN#UPSTREAM và trình OWNER duyệt từng mục.
