# 02_work

**Chứa:**
- `tasks/CYC-nn/TK-nnnn.md` — task, gói ngữ cảnh tự thân cho WORKER (≤ 80 dòng).
- `runs/TK-nnnn_Rn_<OUTCOME>.md` — run, bản ghi thuần YAML của một lần nộp (≤ 45 dòng).
- `cycles/CYC-nn.md` — danh sách task, phân công, tiến độ của chu kỳ.

**Ai ghi:**
- `tasks/`, `cycles/`: chỉ LEAD.
- `runs/`: WORKER nộp run của task mình làm. Chỉ thêm file mới, không sửa, không xóa.

**Lưu ý:** thư mục `tasks/CYC-nn/` chỉ xuất hiện khi LEAD tạo task của chu kỳ đó.
