# example-skill — đối chiếu thuật ngữ trước khi ghép ngữ cảnh

Phần mở rộng mẫu loại `skill`. Nó chứng minh một chức năng mới được thêm chỉ bằng một thư mục trong `harness/extensions/`: không file nào của lõi bị sửa. Khai báo ở [`manifest.yaml`](manifest.yaml); đặc tả ở [`../README.md`](../README.md).

## Làm gì

Trong phiên `DISCUSS` hoặc `CHANGE`, hoặc khi prompt có từ `glossary`, LEAD đối chiếu thuật ngữ OWNER dùng trong prompt với thuật ngữ đã có của dự án và của khung. Thuật ngữ chưa có ở đâu thì LEAD hỏi lại OWNER thay vì tự hiểu, đúng quy tắc không tự đặt thuật ngữ mới.

## Khi nào

Điểm cắm `pre_context`: sau khi LEAD xếp loại phiên, trước khi ghép ngữ cảnh.

## Các bước (LEAD làm tay khi chưa có script `context`)

1. Lấy các thuật ngữ trong prompt của OWNER: cụm trong dấu backtick, từ viết hoa toàn bộ, thuật ngữ tiếng Anh chuyên môn.
2. Tra cột 1 và 2 của bảng trong `05_memory/GLOSSARY.md`, rồi của `harness/HARNESS.md#CONCEPTS`. Thuật ngữ cũ hoặc biệt danh vẫn xử lý theo `harness/rules/LEAD.md` luật 2 trước bước này.
3. Ghi kết quả vào `<project>.local\scratch\example-skill\terms.txt`, ghi đè mỗi phiên, mỗi thuật ngữ một dòng: `- <thuật ngữ> | found: GLOSSARY`, `- <thuật ngữ> | found: CONCEPTS` hoặc `- <thuật ngữ> | found: none`.
4. Mỗi dòng `found: none`: trong phiên `DISCUSS`, LEAD ghi một sự kiện `QUESTION` vào `DSC` và hỏi OWNER nghĩa của thuật ngữ; trong phiên `CHANGE`, LEAD hỏi bằng khối `QUESTION`. Thuật ngữ chỉ vào `GLOSSARY.md` khi OWNER đã chốt bằng một `DEC`.

## Ngân sách đọc

`GLOSSARY.md` và neo `CONCEPTS` cộng lại khoảng 70 dòng, nằm trong phần đoạn trích ≤ 120 dòng của LEAD (`harness/tools/README.md` mục 2.9.2). `GLOSSARY.md` lớn lên làm tổng vượt ngân sách thì chỉ đọc các dòng chứa thuật ngữ cần tra.

## Kiểm rằng phần mở rộng này không sửa lõi

```powershell
git diff --name-status origin/main...HEAD -- harness/extensions/example-skill
git diff --name-status origin/main...HEAD -- . ":(exclude)harness/extensions"
```

Lệnh thứ nhất chỉ có hai dòng `A` (`manifest.yaml`, `README.md`) trong PR thêm phần mở rộng. Lệnh thứ hai không in gì nếu PR chỉ thêm phần mở rộng.
