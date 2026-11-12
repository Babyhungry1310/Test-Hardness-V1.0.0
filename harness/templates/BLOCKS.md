# BLOCKS

Năm khối chuẩn theo `harness/HARNESS.md` mục 3.4. Thông điệp cuối của một phiên chỉ gồm đúng một khối, không có lời dẫn trước hay sau. Khóa cố định, thứ tự cố định; `·` ngăn hai khóa trên cùng một dòng. Riêng khối `QUESTION` được đặt nhiều khối (tối đa 5) ngay trước khối cuối.

## CONFIRM

```text
CONFIRM
understanding: <1–2 câu>
scope: <các bước, file sẽ chạm>
will_not_do: <ngoài phạm vi>
result: <nhận được gì, ở đâu, kiểm bằng cách nào>
```

| Khóa | Giá trị |
|---|---|
| `understanding` · `scope` · `will_not_do` · `result` | Văn bản ngắn. WORKER: cả khối ≤ 5 dòng |

## RESULT

```text
RESULT
task: TK-nnnn · run: Rn · outcome: DONE
pr: <url>
done: 0/0
loops: Lnn–Lnn · last: PASS
deviations: 0
escalate: no
```

| Khóa | Giá trị |
|---|---|
| `outcome` | `DONE` · `BLOCKED` · `CANCELLED` |
| `done` | Số điều kiện `done_when` có bằng chứng / tổng số |
| `loops` · `last` | Dải loop của run · `PASS` hoặc `FAIL` |
| `deviations` | Tổng số mục trong `assumptions`, `differences`, `unverified` |
| `escalate` | `yes` · `no` |

## MERGE

```text
MERGE
pr: <url> · type: run
checks: C1–C14 PASS @ main <SHA>
done: 0/0 · tests: PASS
deviations: 0
protected: none
order: none
```

| Khóa | Giá trị |
|---|---|
| `type` | `run` · `lead` · `review` · `upgrade` |
| `checks` | Kiểm tra đạt, kèm `main` SHA lấy bộ kiểm tra; kiểm không áp dụng ghi `N/A` |
| `tests` | `PASS` · `FAIL` · `N/A` |
| `protected` | `none` hoặc danh sách file 🔒, ✍ mà PR chạm |
| `order` | `none` hoặc danh sách PR theo thứ tự merge |

## REVIEW

```text
REVIEW
cycle: CYC-nn · verdict: PASS
tasks: 0 · pass: 0 · fail: 0
record: RVW-CYC-nn
```

| Khóa | Giá trị |
|---|---|
| `verdict` | `PASS` · `FAIL` |
| `record` | Mã bản ghi kiểm định |

## QUESTION

```text
QUESTION
q: <một ý, lời thường, kèm một ví dụ>
a: <lựa chọn> · b: <lựa chọn>
recommend: a
```

| Khóa | Giá trị |
|---|---|
| `recommend` | `a` · `b` |
