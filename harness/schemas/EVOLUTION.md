# SCHEMA EVOLUTION

Theo `harness/HARNESS.md` mục 8.1 và 11. Mỗi bản ghi có trường `schema`; mỗi file `*.schema.json` mô tả đúng một phiên bản.

## 1. Được đổi gì

| Mức khung | Schema được đổi | Bản ghi cũ |
|---|---|---|
| PATCH | Không đổi schema; chỉ sửa câu chữ tài liệu | Đọc như cũ |
| MINOR | Thêm trường **tùy chọn**; thêm giá trị liệt kê mới | Vẫn hợp lệ; `schema` tăng 1 |
| MAJOR | Đổi tên, xóa, đổi kiểu trường; thêm trường bắt buộc; bỏ giá trị liệt kê | Cần nâng đời; kèm công cụ chuyển đổi và `DEC` |

## 2. Đọc bản ghi

- Đọc YAML theo YAML 1.2 core schema: chỉ `true`/`false` là boolean; `yes`/`no` là chuỗi; ngày giữ dạng chuỗi `YYYY-MM-DD`; số nguyên là số.
- Lấy `schema` của bản ghi, áp các bước nâng đời từ phiên bản đó lên phiên bản hiện tại **trong bộ nhớ**, rồi kiểm theo schema hiện tại.
- File gốc không bị viết lại; dòng trạng thái không bị sửa.
- Bản ghi có `schema` lớn hơn phiên bản công cụ biết: dừng, báo cần nâng cấp khung.

## 3. Ví dụ: decision 1 → 2

Thay đổi: thêm trường tùy chọn `related` (danh sách con trỏ, như ở `RSK`). Mức MINOR.

| | Phiên bản 1 | Phiên bản 2 |
|---|---|---|
| `schema` | `const: 1` | `const: 2` |
| `related` | Không có; có là `REJECT` | Tùy chọn, mặc định `[]` |
| Bản ghi `schema: 1` khi đọc | — | Nâng đời: đặt `schema: 2`, thêm `related: []` |

1. Thêm `decision.v2.schema.json`; giữ `decision.schema.json` cho phiên bản 1.
2. Thêm bước nâng đời `1 → 2` vào thư viện chung của script.
3. Mẫu `decision.md` ghi `schema: 2`; bản ghi mới dùng mẫu này.
4. `DEC-0002` cũ vẫn ghi `schema: 1` trong file và vẫn đạt khi kiểm.
