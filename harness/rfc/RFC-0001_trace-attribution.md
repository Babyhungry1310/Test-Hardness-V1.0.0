# RFC-0001 — GHI MODEL VÀ PHIÊN VÀO DÒNG LOG THEO VẾT

| Thuộc tính | Giá trị |
|---|---|
| Trạng thái | `OPEN` — chưa chọn phương án; chưa triển khai |
| Ngày | 2026-11-14 |
| Người quyết | OWNER |
| Liên quan | `harness/HARNESS.md` mục 7.3 · `harness/schemas/LOG_GRAMMAR.md` · `harness/schemas/POINTER_GRAMMAR.md` · `harness/MODEL_POLICY.md` mục 5 |

Khi RFC này còn `OPEN`, định dạng dòng log giữ nguyên như `LOG_GRAMMAR.md`. Không script, luật hay bản ghi nào được dựa vào một trong ba phương án dưới đây.

## 1. Vấn đề

Dòng log hiện có sáu trường: thời điểm, mã vết, mức, `source`, `EVENT`, cặp `key=value`. Không trường nào cho biết **model thực tế** và **mã phiên** đã sinh ra dòng đó. Cổng model có thể đổi model giữa phiên, nên muốn truy một loop do model nào làm thì hiện phải đối chiếu tay với trường `model` của run, vốn chỉ ghi một giá trị cho cả run.

Phạm vi của RFC: chọn **chỗ đặt** hai dữ kiện này trong dòng log. RFC không bàn cách lấy model thực tế (`harness/tools/INTEGRATION.md#SESSION_MODEL`).

## 2. Ba phương án

<!-- ANCHOR: OPTIONS -->
**A. Metadata `key=value`.** Thêm khóa vào trường cuối, ví dụ `model=<code> session=<mã phiên>`.

```text
2026-11-11T10:42:07+07:00 | TK-0007.L03 | INFO | trace | LOOP_START | model=gpt-5.6-luna session=a1b2
```

**B. Nhúng vào Trace ID.** Mã vết mang thêm một đoạn định danh model hoặc phiên.

```text
2026-11-11T10:42:07+07:00 | TK-0007.L03@a1b2 | INFO | trace | LOOP_START |
```

**C. Đặt trong trường `source`.** `source` ghi cả vai lẫn model.

```text
2026-11-11T10:42:07+07:00 | TK-0007.L03 | INFO | W1:gpt-5.6-luna | LOOP_START |
```

Ba ví dụ chỉ minh họa vị trí; cú pháp chính xác của từng phương án chưa được chốt.
<!-- END: OPTIONS -->

## 3. So sánh

<!-- ANCHOR: COMPARISON -->
### 3.1. Khả năng truy vết

| Tiêu chí | A. `key=value` | B. Trace ID | C. `source` |
|---|---|---|---|
| Ghi được mã model đầy đủ, kể cả dấu chấm và hậu tố biến thể | Có; giá trị không khoảng trắng đã hợp lệ | Khó: mã vết dài, mã model chứa `.` trùng dấu phân cách `.Lnn.Snn`; thực tế chỉ nhúng được mã phiên rồi tra model qua mã phiên | Có, nếu nới ký tự cho phép của `source` |
| Model đổi giữa một loop | Mỗi dòng mang giá trị riêng; mã vết của loop không đổi | Một loop có hai mã vết, hoặc mã vết không còn phản ánh đúng model | Mỗi dòng mang giá trị riêng |
| Nguy cơ thiếu dữ kiện | Có: khóa là tùy chọn, script quên ghi thì dòng vẫn hợp lệ | Thấp: thiếu thì mã vết sai ngữ pháp | Trung bình: `source` luôn có, nhưng phần model có thể bị bỏ |
| Dòng do script ghi (`trace`, `scan`) | `source` vẫn là tên script; model nằm ở khóa riêng | Không ảnh hưởng `source` | Mâu thuẫn: `source` hiện là tên script, không phải vai; phải định nghĩa lại `source` |
| Giữ nguyên tắc mã bất biến [THY-39] | Giữ | Không giữ: định danh gắn với thuộc tính có thể đổi | Giữ |

### 3.2. Tương thích ngược

| Tiêu chí | A. `key=value` | B. Trace ID | C. `source` |
|---|---|---|---|
| Biểu thức dòng log trong `LOG_GRAMMAR.md` | Không đổi; khóa mới đã khớp `[a-z_]+=…` | Phải đổi nhóm `trace` | Phải đổi nhóm `source` (hiện chỉ `[A-Za-z0-9_-]+`) |
| Log cũ đọc bằng công cụ mới | Hợp lệ | Hợp lệ nếu đoạn nhúng là tùy chọn | Hợp lệ nếu biểu thức mới là tập cha |
| Log mới đọc bằng công cụ cũ | Hợp lệ | Bị từ chối | Bị từ chối |
| Con trỏ mã vết (`POINTER_GRAMMAR.md`, `$defs.pointer` trong các schema) | Không đổi | Phải đổi, hoặc phải quy định cách bỏ đoạn nhúng khi làm con trỏ | Không đổi |
| Chỉ mục `index.md` (`first_error`) và trường `loops` của run | Không đổi | `first_error` phải đổi biểu thức | Không đổi |
| Bản ghi đã có trên repo | Không ảnh hưởng | Không ảnh hưởng trực tiếp; `origin` dạng `TK-nnnn.Lnn` trong `DEC` cũ vẫn phải tra được | Không ảnh hưởng |
| Mức thay đổi theo `harness/schemas/EVOLUTION.md` | MINOR (thêm khóa tùy chọn) | MAJOR (đổi định dạng mã) | MINOR nếu chỉ nới ký tự; MAJOR nếu đổi nghĩa `source` |

### 3.3. Truy vấn

| Tiêu chí | A. `key=value` | B. Trace ID | C. `source` |
|---|---|---|---|
| Lọc mọi dòng của một model | Tìm chuỗi `model=<code>` | Tìm theo đoạn nhúng; qua mã phiên thì cần thêm một bước tra | Lọc cột 4 |
| Lọc mọi dòng của một loop | Tìm đúng mã vết, như hiện nay | Phải tìm theo tiền tố; so khớp chính xác không còn dùng được | Như hiện nay |
| Lọc theo vai | Như hiện nay | Như hiện nay | Phải so khớp tiền tố của cột 4 |
| Nếu chỉ ghi ở `LOOP_START` để đỡ lặp | Phải nối dòng theo mã vết mới biết model của một dòng `SPAN` | Không cần nối | Không áp dụng; `source` có ở mọi dòng |
| Công cụ dòng lệnh thông thường (`Select-String`, `grep`) | Đủ | Đủ, nhưng dễ khớp nhầm khi tìm theo tiền tố (`L03` và `L03@…`) | Đủ |
<!-- END: COMPARISON -->

## 4. Điều OWNER cần quyết

1. Chọn A, B, C, hoặc giữ nguyên hiện trạng.
2. Dữ kiện nào bắt buộc: model, mã phiên, hay cả hai.
3. Ghi ở mọi dòng, hay chỉ ở dòng mở loop.

Sau khi OWNER quyết: LEAD ghi một `DEC`, sửa `LOG_GRAMMAR.md` và các file liên quan trong một PR `upgrade/<version>`, và đổi trạng thái RFC này thành `ACCEPTED → DEC-nnnn` hoặc `REJECTED`. RFC không được sửa nội dung so sánh sau khi đóng.
