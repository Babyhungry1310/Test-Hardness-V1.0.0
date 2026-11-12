# STATUS GRAMMAR

Ngữ pháp các dòng có cấu trúc trong bản ghi, theo `harness/HARNESS.md` mục 6.2, 6.3, 6.4, 7.2. Biểu thức chính quy viết theo cú pháp Python `re`, khớp cả dòng.

## 1. Dòng trạng thái

Quy tắc chung cho mọi loại:

- Dòng trạng thái nằm dưới tiêu đề `## Status (newest first)`. Dòng mới chèn ngay dưới tiêu đề; không sửa, không xóa dòng cũ.
- Dạng `- YYYY-MM-DD | <STATE> | key: value | …`: chỉ gồm ngày, trạng thái và cặp khóa–giá trị; không có lời ghi chú.
- Ngày của các dòng giảm dần từ trên xuống (cùng ngày thì giữ thứ tự chèn).
- Lỗi chữ hoa/thường hay khoảng trắng của giá trị liệt kê là `AUTOFIX`; mọi lỗi khác là `REJECT` (mục 8.2).

### DEC

```regex
^- \d{4}-\d{2}-\d{2} \| (?:ACTIVE|SUPERSEDED_BY DEC-\d{4}|RETIRED)$
```

Đúng:

```text
- 2026-11-02 | SUPERSEDED_BY DEC-0002
- 2026-11-01 | ACTIVE
```

Sai:

```text
- 2026-11-01 | ACTIVE | reason: OWNER đồng ý
- 2026-11-02 | SUPERSEDED_BY DEC-2
```

1. Có cặp khóa–giá trị không thuộc loại `DEC`, thực chất là lời ghi chú.
2. Mã `DEC` không đủ 4 chữ số.

### RSK

```regex
^- \d{4}-\d{2}-\d{2} \| (?:OPEN|MITIGATING|CLOSED) \| level: (?:LOW|MEDIUM|HIGH) \| due: \d{4}-\d{2}-\d{2} \| owner: (?:OWNER|LEAD)$
```

Đúng:

```text
- 2026-11-02 | CLOSED | level: LOW | due: 2026-11-05 | owner: LEAD
- 2026-11-01 | OPEN | level: HIGH | due: 2026-11-05 | owner: LEAD
```

Sai:

```text
- 2026-11-01 | OPEN | level: CRITICAL | due: 2026-11-05 | owner: LEAD
- 2026-11-01 | OPEN | level: HIGH | owner: LEAD
```

1. `level` ngoài danh sách `LOW`, `MEDIUM`, `HIGH`.
2. Thiếu khóa bắt buộc `due`.

### REQ

```regex
^- \d{4}-\d{2}-\d{2} \| (?:PENDING|RESOLVED_BY DEC-\d{4})$
```

Đúng:

```text
- 2026-11-03 | RESOLVED_BY DEC-0003
- 2026-11-03 | PENDING
```

Sai:

```text
- 2026-11-03 | RESOLVED
- 03/11/2026 | PENDING
```

1. `RESOLVED` thiếu mã `DEC` đã xử lý yêu cầu.
2. Ngày không theo dạng `YYYY-MM-DD` (`AUTOFIX`).

### DSC

```regex
^- \d{4}-\d{2}-\d{2} \| E[1-9]\d* (?:ACCEPTED → DEC-\d{4}|REJECTED)$
```

Đúng:

```text
- 2026-11-02 | E1 ACCEPTED → DEC-0002
- 2026-11-02 | E3 REJECTED
```

Sai:

```text
- 2026-11-02 | E1 ACCEPTED
- 2026-11-02 | E4 LATER
```

1. `ACCEPTED` thiếu mã `DEC` được sinh ra.
2. `LATER` không phải trạng thái; đề xuất chưa quyết thì không có dòng trạng thái.

### PLAN

```regex
^- \d{4}-\d{2}-\d{2} \| ACTIVE \| version: [1-9]\d*$
```

Đúng:

```text
- 2026-11-10 | ACTIVE | version: 2
- 2026-11-04 | ACTIVE | version: 1
```

Sai:

```text
- 2026-11-04 | ACTIVE
- 2026-11-04 | DRAFT | version: 1
```

1. Thiếu `version`.
2. `DRAFT` không phải trạng thái; plan chưa duyệt chưa vào `main`.

## 2. Các dòng có cấu trúc khác

| Dòng | Nằm ở |
|---|---|
| Sự kiện thảo luận | `## Events` của `DSC` |
| Task trong plan | Neo `CYC_nn` của `PLAN.md` |
| Rủi ro trong plan | Neo `RISKS` của `PLAN.md` |
| Task trong chu kỳ (bản chiếu) | Neo `TASKS` của `02_work/cycles/CYC-nn.md` |
| Quyết định trong tóm tắt | Neo `DECISIONS` của digest chu kỳ và digest chủ đề |
| Kết quả task trong tóm tắt | Neo `RESULTS` của digest chu kỳ |
| Rủi ro chuyển tiếp trong tóm tắt | Neo `RISKS` của digest chu kỳ |
| Câu hỏi cổng | Neo `QUESTIONS` của `PLAN_GO.md`, `CYC-nn_PASS.md` |
| Bảng nghiệm thu | Neo `ACCEPTANCE` của `CYC-nn_PASS.md` |
| Ba dòng đầu `STATE.md` | Đầu `04_control/STATE.md` |

Biểu thức theo đúng thứ tự bảng trên:

```regex
^- E[1-9]\d* \| (?:PROPOSAL|ASSUMPTION|IDEA|QUESTION) \| \S.*$
^- TK-\d{4} \| [^|]*\S \| depends: (?:none|TK-\d{4}(?:, TK-\d{4})*) \| assignee: W[1-9]\d*$
^- RSK-\d{4}$
^- TK-\d{4} \| run: (?:R[1-9]\d*|none) \| outcome: (?:ASSIGNED|DONE|BLOCKED|CANCELLED)$
^- DEC-\d{4} \| \S.*$
^- TK-\d{4} \| (?:DONE|CANCELLED) R[1-9]\d* \| \S.*$
^- RSK-\d{4} \| \S.*$
^\| [1-8] \| [^|]*\S \| (?:PASS|CONDITIONAL|FAIL|N/A) \| [^|]*\S \|$
^\| TK-\d{4} \| (?:DONE|CANCELLED) \| R[1-9]\d* \| \d+/\d+ \| \d+ · last (?:PASS|FAIL) \| (?:PASS|FAIL) \| \d+ \|$
^(?:PHASE: (?:BRAINSTORM|PLAN|EXECUTE|VERIFY|CLOSE|CLOSED)|CYCLE: (?:CYC-\d{2}|NONE)|PROFILE: (?:SHORT|MEDIUM|LONG|UNSET))$
```

- Sự kiện thảo luận: nội dung ≤ 25 từ; `DSC` ≤ 40 dòng.
- Cột bằng chứng của câu hỏi cổng: một hoặc nhiều con trỏ hay đường dẫn, cách nhau bằng `, `. Câu `CONDITIONAL` phải có một mã `RSK` có thật trong cột này (C11).
- `CYCLE: NONE` và `PROFILE: UNSET` chỉ dùng cho `STATE.md` trước khi có plan.
