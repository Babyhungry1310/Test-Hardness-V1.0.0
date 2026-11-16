# TK-0030: chẩn đoán main trước sửa

- Thời điểm: 2026-11-16T02:43:43Z; LEAD chẩn đoán, không phải loop R1.
- Main mới nhất sau fetch --no-tags: 8dcf58b1e680cfade770acd7678165714f7b3d09.
- Worktree riêng sạch trước/sau: verify-CYC03-B1, HEAD đúng origin/main; không tích hợp PR31.
- OS: Windows-11-10.0.26300-SP0; Python 3.14.5 (MSC v.1944, AMD64).
- Môi trường mặc định: PYTHONUTF8 và PYTHONIOENCODING đều không đặt; utf8_mode=0; stdout/stderr/preferred=cp1252.
- Lệnh: python -m pytest -q --tb=line tools/tests/test_preflight_main.py::test_cli_usage_and_errors.
- Kết quả: exit 1; 1 failed in 1.00s; assertion returncode 1 == 2 không đạt tại dòng 194.
- Lý do: CLI ngoài Git repo in Lỗi; cp1252 không mã hóa được U+1ED7; UnicodeEncodeError làm mã thoát thành 1. Stderr tiến trình pytest rỗng; traceback của CLI được subprocess test thu lại.
- Đối chứng chỉ đổi môi trường tiến trình: PYTHONUTF8=1, PYTHONIOENCODING=utf-8.
- Lệnh đối chứng: python -m pytest -q --tb=line tools/tests.
- Kết quả đối chứng: exit 0; 54 passed in 33.18s; stderr rỗng.
- Không thay môi trường toàn cục, file sản phẩm, ref, Git config hoặc bằng chứng lịch sử.
- Log đầy đủ: <project>.local/scratch/preflight-encoding/reproduction.json; script diagnose.py cùng thư mục.
- Cấp mã: kiểm 43 commit từ refs/35 PR và file sổ/task chưa commit ở các worktree, gồm kho lạnh; max REQ-0008, DEC-0025, TK-0029. Inventory ở <project>.local/scratch/preflight-encoding/id-inventory.json.
