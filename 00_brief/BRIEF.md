# BRIEF

## Mục tiêu
- Công cụ dòng lệnh đọc ngân hàng câu hỏi JSON, báo câu trùng id và xuất handout Markdown cho lớp học.
- Thử khung V1.0.1 trên repo này: triển khai và kiểm định tám nhóm cập nhật của DEC-0015, quy tắc chia batch zero-overlap và mẫu `pytest.ini` (DEC-0016).

## Phạm vi
- Đọc ngân hàng câu hỏi JSON; báo câu trùng id; xuất handout Markdown.
- Hook, script kiểm và bộ test của khung V1.0.1 trong `tools/`; bằng chứng kiểm trong `03_output/`.

## Không làm
- Không xuất PDF.
- Không dùng tên học viên thật trong dữ liệu thử.
- Không sửa `harness/` trong các chu kỳ thử khung; không chọn phương án của RFC-0001.
- Không sửa sản phẩm và bằng chứng của CYC-01, CYC-02.
- Không tuyên bố `scan` chặn được mọi prompt injection.
