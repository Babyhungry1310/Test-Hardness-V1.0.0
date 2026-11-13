# ACCEPTANCE

<!-- ANCHOR: CYC_01 -->
## CYC-01
- `load_bank` đọc `data/bank.json` trả về đủ 5 câu, giữ thứ tự, mỗi câu có `id`, `text`, `answer` theo SRC-0001.
- `load_bank` báo lỗi khi một câu thiếu trường bắt buộc.
- `find_duplicate_ids` báo mọi id trùng theo thứ tự xuất hiện và không xóa câu hỏi nào.
- `python -m pytest -q --tb=line` đạt trên `main`.
- `data/` không chứa tên học viên thật.
<!-- END: CYC_01 -->

<!-- ANCHOR: CYC_02 -->
## CYC-02
- Công cụ xuất một file handout Markdown từ `data/bank.json`, mỗi câu một mục theo thứ tự trong ngân hàng.
- Công cụ dừng và báo id trùng trước khi xuất.
- File handout kết thúc bằng đúng một ký tự LF và không chứa ký tự CR do công cụ thêm vào, trên cả Linux và Windows.
- Không sinh file PDF.
<!-- END: CYC_02 -->
