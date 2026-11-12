# LOG GRAMMAR

Định dạng log theo vết, theo `harness/HARNESS.md` mục 7.3. Log nằm ở `<project>.local/logs/TK-nnnn/`, không lên repo; chỉ trường `loops` của run lên repo.

## 1. Dòng log

```text
<timestamp ISO 8601> | <trace id> | <severity> | <source> | <EVENT> | key=value …
```

```regex
^(?P<ts>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})) \| (?P<trace>(?:TK-\d{4}|SES-\d{8}-[a-z0-9]{4})\.L\d{2}(?:\.S\d{2})?) *\| (?P<severity>DEBUG|INFO|WARN|ERROR) *\| (?P<source>[A-Za-z0-9_-]+) *\| (?P<event>LOOP_START|VERIFY_START|VERIFY_END|LOOP_END|LOOP_CLOSED|SPAN|ESCALATE|SCAN_HIT|TOOL_ERROR) *\|(?P<data>(?: [a-z_]+=(?:"[^"]*"|[^\s"]+))*)$
```

- Một dòng một sự kiện; chỉ thêm, không sửa. Được đệm khoảng trắng trước dấu `|` để thẳng cột.
- `source`: vai (`W1`, `LEAD`, `REVIEWER`) hoặc tên script (`trace`, `scan`).
- Giá trị có khoảng trắng đặt trong ngoặc kép. Đầu ra dài để ở file trong `scratch/` và trỏ bằng `ref=`.

## 2. EVENT và khóa đi kèm

| EVENT | Khóa | Mức thường dùng | Ai ghi |
|---|---|---|---|
| `LOOP_START` | — | `INFO` | `trace` |
| `VERIFY_START` | `cmd` | `INFO` | `trace` |
| `VERIFY_END` | `result`, `passed`, `failed`; `ref` khi `FAIL` | `INFO` khi `PASS`, `ERROR` khi `FAIL` | `trace` |
| `LOOP_END` | `result` | `INFO` khi `PASS`, `WARN` khi `FAIL` | `trace` |
| `LOOP_CLOSED` | `loops`, `evidence` | `ERROR` | `trace` |
| `SPAN` | `kind` (`edit`, `cmd`, `tool`); `file` hoặc `cmd` | `DEBUG` | `trace` |
| `ESCALATE` | `run` | `WARN` | `trace` |
| `SCAN_HIT` | `level`, `file` | `WARN` | `scan` |
| `TOOL_ERROR` | `tool`, `ref` | `ERROR` | Script gặp lỗi |

`result` ∈ `PASS`, `FAIL`. `level` ∈ `ALLOW`, `WARN`, `QUARANTINE`, `BLOCK`. Không ghi nội dung nghi vấn của `SCAN_HIT` vào log.

## 3. Đếm loop và giới hạn

1. Mỗi lần `trace` chạy lệnh `verify` của task là một loop; `trace` ghi `LOOP_START`, `VERIFY_START`, `VERIFY_END`, `LOOP_END` với cùng mã `TK-nnnn.Lnn`.
2. Số loop = 1 + số loop lớn nhất đã có của task, đếm liên tục qua mọi run: `R1` gồm `L01`–`L03`, `R2` bắt đầu từ `L04`.
3. Mỗi run tối đa `max_loops` loop: giá trị trong task, nếu không có thì trong `harness.yaml`, mặc định 3. Khi run đã đủ số loop, `trace` từ chối chạy `verify`.
4. Loop `PASS` → run `DONE`. Loop `FAIL` còn lượt → loop kế tiếp.
5. Loop `FAIL` cuối cùng được phép thì loop đóng: `trace` ghi `LOOP_CLOSED` rồi `ESCALATE`, chép đầu ra kiểm của các loop (đã cắt gọn) vào `03_output/CYC-nn/checks/TK-nnnn_Rn_verify.txt`, điền `evidence` và `loops`. WORKER nộp run `BLOCKED` với `escalate: yes` và `escalation`.
6. Mỗi loop thành một dòng trong `loops` của run, đúng biểu thức của `run.schema.json`:

```regex
^L\d{2} \| (?:PASS|FAIL)(?: \| [a-z_]+=\S+(?: [a-z_]+=\S+)*)?$
```

## 4. Thêm span mà không đổi định dạng

- Bật bằng `log_level: SPAN` trong `harness.yaml` (toàn dự án) hoặc trong task (riêng task đó).
- Chỉ thêm dòng `SPAN` có mã vết hậu tố `.Snn`; số span đếm lại từ `S01` trong mỗi loop. Dòng cấp loop giữ nguyên.
- Công cụ đọc ở mức `LOOP` bỏ qua dòng có `.Snn` và vẫn cho cùng kết quả.

## 5. Chỉ mục log `index.md`

Mỗi loop một dòng, sinh lại được từ `trace.log`:

```regex
^- L\d{2} \| (?:PASS|FAIL) \| debug=\d+ info=\d+ warn=\d+ error=\d+ \| first_error: (?:TK-\d{4}\.L\d{2}(?:\.S\d{2})?|none)$
```

## 6. Ví dụ

Đúng:

```text
2026-11-05T09:00:02+07:00 | TK-0001.L01     | INFO  | trace | LOOP_START   |
2026-11-05T09:03:10+07:00 | TK-0001.L01.S01 | DEBUG | trace | SPAN         | kind=edit file=src/dupes.py
2026-11-05T09:05:01+07:00 | TK-0001.L01     | INFO  | trace | VERIFY_START | cmd="python -m pytest -q --tb=short tests/test_dupes.py"
2026-11-05T09:05:03+07:00 | TK-0001.L01     | ERROR | trace | VERIFY_END   | result=FAIL passed=1 failed=2 ref=scratch/TK-0001/L01_verify.txt
```

Sai:

```text
2026-11-05 09:00:02 | TK-0001.L01 | INFO | trace | LOOP_START |
2026-11-05T09:00:02+07:00 | TK-0001.L1 | INFO | trace | LOOP_START |
2026-11-05T09:05:03+07:00 | TK-0001.L01 | ERROR | trace | VERIFY_FAILED | passed=1 failed=2
2026-11-05T09:05:03+07:00 | TK-0001.L01 | ERROR | trace | VERIFY_END | result=FAIL # lỗi ở test 3
```

1. Thời điểm không theo ISO 8601 (thiếu `T` và múi giờ).
2. Số loop không đủ 2 chữ số.
3. `VERIFY_FAILED` không có trong danh sách EVENT.
4. Có lời ghi chú sau cặp khóa–giá trị.
