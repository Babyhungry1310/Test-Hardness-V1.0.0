---
schema: 1
id: "RVW-CYC-01"
cycle: "CYC-01"
date: "2026-11-12"
reviewer_model: "claude-sonnet-5-5"
worker_models: ["gemini-3.8-flash-k", "gpt-6.1-sol"]
verdict: "PASS"
items:
  - "TK-0001 | done 3/3 | PASS"
  - "TK-0002 | done 4/4 | PASS"
  - "TK-0004 | done 3/3 | PASS"
findings:
  - "Vòng kiểm định: 3. Commit main được kiểm định: e306b977f7772eca75fee248e61b9f0db1ab40dd (PR14 squash merge); git rev-parse HEAD khớp origin/main."
  - "Pytest độc lập: clone sạch khác của main, PYTHONDONTWRITEBYTECODE=1, lệnh python -m pytest -q --tb=line (pytest 9.1.1) cho exit code 0, 13 passed, 0 failed, 0 skipped, 0 lỗi thu thập. Chạy riêng tests/test_dupes.py: 8 passed; tests/test_loader.py: 5 passed. Không còn import file mismatch của vòng 2. Cây làm việc sạch sau khi chạy."
  - "TK-0001: done 3/3. src/dupes.py dùng casefold, trả id trùng mỗi id một lần theo thứ tự xuất hiện đầu của nhóm, giữ dạng gốc lần xuất hiện đầu, không sửa danh sách đầu vào; [] khi không trùng; q-001 và Q-001 được báo trùng (trả q-001). Run R2 DONE (gpt-6.1-sol) có L01 8 passed; sha256 src/dupes.py và tests/test_dupes.py trên main khớp execution.json. Run R1 BLOCKED (gemini-3.8-flash-k) đã được thay bằng R2 và khớp CYC-01.md. Không đọc data/bank.json trong test, không có tên học viên thật."
  - "TK-0002: done 4/4. data/bank.json là mảng 5 câu tự soạn, id Q-001 đến Q-005, mỗi câu đúng ba khóa id, text, answer; load_bank trả về 5 câu giữ thứ tự và Unicode; thiếu id, text hoặc answer đều ném ValueError (test parametrize ba trường). Run R1 DONE: L01 FAIL trước khi viết code (test viết trước), L02 PASS 5 passed; sha256 data/bank.json, src/loader.py, tests/test_loader.py trên main khớp execution.json và test không đổi giữa L01 và L02. Không có tên học viên thật trong data/."
  - "TK-0004: done 3/3. pytest.ini ở gốc repo gồm đúng mục [pytest] với testpaths = tests (hai dòng, sha256 c809c969... khớp execution.json); lệnh verify thu thập đủ 13 test của tests/ và cả 13 PASS, không còn import file mismatch, không test bị bỏ qua; sha256 tests/test_dupes.py và tests/test_loader.py trên main khớp giá trị trước và sau của run, không sửa harness/ hay logic sản phẩm."
  - "ACCEPTANCE.md CYC_01: năm điều kiện đều đạt trên main: load_bank trả 5 câu đúng thứ tự và đủ trường; load_bank báo lỗi khi thiếu trường; find_duplicate_ids báo id trùng theo thứ tự xuất hiện và không xóa câu nào; python -m pytest -q --tb=line đạt trên main (exit code 0, 13 passed); data/ không chứa tên học viên thật."
  - "Siêu dữ liệu: 02_work/cycles/CYC-01.md ghi TK-0001 run R2 DONE, TK-0002 run R1 DONE, TK-0004 run R1 DONE, khớp các run hiện có. Không phát hiện lỗi."
---
