B?n tham kh?o 2026-11-22. Ngu?n hi?n h?nh: SRC-0003 P6d, DEC-0032.

# H3 — Hạ tầng, context, cache và điều phối loop

- Trạng thái: DỰ THẢO cho các mục chưa có trạng thái. Mục đã chốt (DEC-0031, DSC-20261121-kzn1) ghi trạng thái ở H0 mục 3.
- Nguồn: bài học vận hành đa model (DeepSeek, Claude, GPT qua DeepInfra, 9Router). Hồ sơ cũ không ghi ngày, phiên, model.
- Biên tập lại: 2026-11-19, theo thẩm định Kaizen.
- Cập nhật 2026-11-21: tuyến free được làm WORKER có điều kiện (E10 sửa); thêm phân hạng task và thang leo tuyến (mục 16, E17); khung thời gian, hạn mức, ngắt mạch cho tuyến free (mục 17); bảng lỗi thống nhất (mục 9, E18); định nghĩa W1–W4 (mục 13, E19); quy tắc LF và raw capture (mục 8, E22); danh sách binary nền (mục 14, E24).
- Cập nhật 2026-11-22 (theo GSD Core, E31–E43): mã 66 NO_INPUT, enum lớp lỗi và quy tắc đối chiếu đĩa trước khi phân loại (mục 9); kiểm lời tự báo cho mọi run từ Bước 3 (mục 16); tách thang leo năng lực và thang nhà cung cấp, thêm bước tách task trước khi leo (mục 16); ngưỡng gói task và luật đọc trước khi sửa cho tuyến free (mục 16); Git Bash không có `jq` (mục 14); E14 đã chốt (mục 15).
- Đã nạp vào repo ở TK-0036 (05_memory/upstream/). File này là bản đề xuất cập nhật 2026-11-22; LEAD đồng bộ vào bản trong repo.

## 1. Ngân sách context và hạn mức theo tuyến
Nhãn: GỘP (vào 04_control/MODEL_CATALOG.md) | Đợt: Đợt 2 (trước khi giao task cho tuyến free) | PROPOSAL: không
- Giới hạn context của từng tuyến ghi vào MODEL_CATALOG.
- Nguyên tắc: input + max_tokens + biên an toàn ≤ giới hạn của provider. Phải tính cả output.
- Bộ đếm token hiệu chỉnh theo usage.prompt_tokens provider trả về; không ước lượng theo số ký tự.
- Chặn lúc giao (bổ sung 2026-11-21): script đếm token của gói task trước khi giao. Vượt ngân sách của tuyến thì không giao; tách task hoặc chọn tuyến khác. Không để tràn context giữa chừng.
- MODEL_CATALOG ghi thêm hạn mức của tuyến: số request mỗi phút, mỗi ngày, số phiên đồng thời. Chưa rõ thì ghi "CHƯA XÁC MINH" và áp mức thấp nhất trong pool.
- Chi tiết cho DeepInfra (trần 32.768, input an toàn 60–70% khi max_tokens = 2048): HOÃN (K5).

## 2. Thứ tự prefix cố định giữa các phiên
Nhãn: GIỮ | Đợt: Đ4 | PROPOSAL: không
- Thứ tự cố định từng byte giữa các phiên: system prompt cố định → schema tool cố định → brief hoặc ngữ cảnh riêng của task.
- Đổi phần đầu prompt giữa các phiên làm mất cache của provider, tăng chi phí và độ trễ.

## 3. Provider có context nhỏ
Nhãn: HOÃN (K5) | Đợt: Đợt 2 | PROPOSAL: không
- Ngắn hạn: chưa rõ provider thì lấy giới hạn thấp nhất trong pool làm trần mặc định.
- Dài hạn: loại provider context nhỏ khỏi routing của task nặng; cần OWNER duyệt cấu hình routing.
- Phần dùng tuyến context nhỏ làm WORKER cho task nhỏ đã chuyển sang mục 1 (chặn lúc giao) và mục 16 (gói ngữ cảnh tối thiểu), Đợt 2.

## 4. Checkpoint do máy xác nhận
Nhãn: GIỮ | Đợt: Đ3b | PROPOSAL: không
- Không lấy checkpoint từ lời tự báo của model (model từng tuyên bố đã tạo file không tồn tại).
- Checkpoint do script hoặc điều phối viên ghi; mỗi mục liên kết với thực thể kiểm được: commit SHA, hash file, file kết quả kiểm thử trên đĩa.
- Phiên mới chỉ kế thừa mục đã được máy xác nhận.
- Mỗi vòng loop dựng lại ngữ cảnh từ checkpoint, không mang lịch sử hội thoại của vòng trước (mục 16).
- Đây là một phần việc của script trace.

## 5. Chuyển phiên: phép kiểm một writer
Nhãn: GỘP (vào phép kiểm đầu phiên, harness/tools/PREFLIGHT.md) | Đợt: Đ3b | PROPOSAL: không
- Bài học TK-0027: hai tiến trình tác tử có thể cùng ghi vào một workdir.
- Phép kiểm đầu phiên: không còn tiến trình nào trỏ vào workdir.

## 6. Chuyển phiên qua relay và relay thống nhất
Nhãn: HOÃN (K6) | Đợt: Đợt 3 | PROPOSAL: E13
- Dừng phiên cũ; đưa session_id cũ vào denylist của relay; mở phiên mới sau phép kiểm ở mục 5.
- Relay thống nhất: gộp các bản relay về một relay độc lập, có phiên bản và hash, đặt ngoài cây repo.
- Kiểm thử tự động: đổi cấu hình một tuyến không làm đổi byte nào của tuyến khác.
- Ràng buộc với Đ1 (2026-11-21): đo token (H4-6) không được phụ thuộc vào bản relay sẽ đổi sau Đ1, nếu không Đ5 không so được với Đ1. Xem H0 mục 5.

## 7. Nén output công cụ không mất bằng chứng
Nhãn: GIỮ | Đợt: Đ4 | PROPOSAL: không
- Output thô ghi nguyên văn vào file, kèm hash.
- Context của tác tử chỉ giữ tóm tắt ngắn, đường dẫn file và hash.
- Output FAIL luôn lưu đủ trên đĩa, không cắt. Phần đưa vào ngữ cảnh WORKER là đầu và đuôi của output FAIL, kèm đường dẫn bản đủ.

## 8. EOL và hash bằng chứng
Nhãn: GIỮ (phần phòng ngừa) | Đợt: Đ1 | PROPOSAL: E9, E22
- Vấn đề: .gitattributes ép eol=lf; hash bằng chứng tính trên byte CRLF trên Windows sẽ lệch sau khi Git chuẩn hóa.
- Phòng ngừa:
  - File văn bản do khung tự viết (run log, sổ, file kết quả do script soạn) ghi bằng LF ngay từ đầu (newline='\n').
  - Raw capture (stdout, stderr của công cụ) lưu nguyên byte, kể cả CRLF do công cụ Windows xuất ra; hash tính trên byte gốc. Quy tắc LF không áp cho raw capture (sửa 2026-11-21).
  - .gitattributes đặt -text cho 03_output/**/checks/.
  - end-of-file-fixer, mixed-line-ending không chạy trên 03_output/**/checks/ (H4-11).
- Không sửa hash trong hồ sơ kiểm định đã niêm phong.
- Chứng minh khả nghịch LF → CRLF chỉ áp cho dữ liệu cũ của TK-0027 (đã ghi nhận 7/7 hash khớp), không thành luật thường trực.

## 9. Bảng lỗi thống nhất và ngắt mạch tuyến
Nhãn: GIỮ (bảng lỗi), HOÃN (K6, ngắt mạch chung) | Đợt: Đ3a, TK-0042 (bảng lỗi, enum lớp lỗi, mã 66), Đợt 2 (script phân loại, ngắt mạch tuyến free, mục 17), Đợt 3 (ngắt mạch chung) | PROPOSAL: E18, E13, E35, E36
- Bảng lỗi đặt ở 01_plan/SPEC_TOOLS.md#CONVENTIONS khi được chốt. E5 là mặc định; trần của lỗi hạ tầng là ngoại lệ có tên.

| Loại lỗi | Ví dụ | Mã thoát | Tính loop logic | Trần thử | Khi chạm trần |
| --- | --- | --- | --- | --- | --- |
| Đạt | verify PASS, có ít nhất một đơn vị được kiểm | 0 | — | — | — |
| Không có gì để kiểm (thêm 2026-11-22, E36) | diff rỗng, không file nào trong phạm vi, danh sách file bị `gh` cắt | 66 | Không | 0 | Cổng gác: chặn; cổng quan sát: ghi log |
| Logic | test FAIL | 1 | Có | max_loops 3; tuyến free 2 lần liên tiếp | BLOCKED; tuyến free thì leo bậc |
| Bịa | CLAIM_MISMATCH (mục 16) | 1 | Có | 1 | Leo bậc ngay; ghi ROUTE_CHECKS |
| Môi trường, quyền | thiếu gói, quyền đọc ghi | 2 | Không | 2 (E5) | BLOCKED, báo LEAD |
| Hạ tầng tạm thời | 429, 503 quá tải, mất kết nối, timeout lượt gọi | 2 | Không | Theo ma trận dưới | Chuyển tuyến |
| Hạ tầng không phục hồi | 402, 503 tương thích | 2 | Không | 0 | 402 báo OWNER; 503 chuyển tuyến |
| Tràn context | vượt ngân sách | 2 | Không | 0 | Chặn lúc giao; nếu xảy ra thì tách task hoặc chuyển tuyến |
| Quá khung thời gian task | mục 17 | 2 | Không | 0 | Leo bậc |
| Không xác định | mã lạ, thiếu bằng chứng | 3 | Không | 0 | Chặn, BLOCKED kèm chẩn đoán (E16) |

- Ma trận lỗi hạ tầng tạm thời:
  - 429: thử lại với độ trễ tăng dần, tối đa [LEAD chốt] lần trong ngân sách riêng của tuyến.
  - 503 quá tải: chờ 30s → 60s → 120s, tối đa 3 lần, rồi chuyển tuyến.
  - Mất kết nối hoặc timeout lượt gọi: bỏ phần đầu ra dở dang, thử lại 1 lần từ checkpoint, rồi chuyển tuyến.
- Ngắt mạch chung (K6): tuyến gặp 503 từ 3 lần trong 30 phút thì tạm ngưng 60 phút; ghi thời điểm ngắt và mở lại. Riêng tuyến free áp sớm từ Đợt 2 (mục 17).
- Bổ sung 2026-11-22 (E35, theo GSD Core):
  - Lớp lỗi là một enum duy nhất, dùng chung cho bộ phân loại và mọi nơi kiểm lớp lỗi; quy ước ghi ở TK-0042.
  - Run kết thúc bất thường thì đối chiếu sản phẩm trên đĩa (commit, file, kết quả run) **trước** khi phân loại lỗi, để không chạy lại phần đã commit. Có commit mà thiếu kết quả run thì tiếp tục từ đĩa, không chạy lại từ đầu.
  - Thân trả về rỗng là lỗi không xác định (mã 3), không phải thành công.
  - Script phân loại ưu tiên mã HTTP từ relay hoặc 9Router; chỉ dùng chuỗi nhận diện ("rate limit", "quota", "too many requests"…) khi không có mã. Làm ở Đợt 2.

## 10. Tách chỉ số độ sẵn sàng và chất lượng
Nhãn: GIỮ | Đợt: Đ1 | PROPOSAL: E8, E19
- Báo cáo sau mỗi batch tách độ sẵn sàng (tần suất lỗi 503, 429, 402, mất kết nối, timeout) và chất lượng (FAIL do logic, CLAIM_MISMATCH, vi phạm brief).
- Tách theo tuyến và theo hạng task (T0, T1, T2), để thấy tuyến free hỏng vì hạ tầng hay vì năng lực.

## 11. Tuyến miễn phí
Nhãn: GIỮ (viết lại 2026-11-21) | Đợt: Đợt 2 | PROPOSAL: E10, E17
- Tuyến miễn phí: tuyến có hậu tố :free hoặc đơn giá bằng 0.
- Được làm WORKER khi đủ các điều kiện:
  - Task hạng T0 hoặc T1 (mục 16); không làm task T2.
  - Tuyến đạt W1–W4 cho đúng hạng task đó (mục 13) và đang không ở trạng thái UNQUALIFIED.
  - Có tuyến trả phí dự phòng được chỉ định sẵn cho task.
  - Gói task nằm trong ngân sách context của tuyến (mục 1).
  - Tuân thủ khung thời gian và hạn mức (mục 17).
- Không làm REVIEWER chính, không đứng ở bước chặn xuất bản.
- Vẫn làm việc phụ: tra cứu, tóm tắt, hỗ trợ phân tích, có tuyến trả phí dự phòng.
- Đây là điều kiện mới, thu hẹp DEC-0018. Ghi vào harness/MODEL_POLICY.md#ELIGIBILITY.
- Lý do nới so với bản 2026-11-19: nhiều loại việc cần đến tuyến free (OWNER, 2026-11-21); rủi ro bịa, context nhỏ, chậm được chặn bằng hạng task, phép kiểm máy và thang leo tuyến thay vì cấm hẳn.

## 12. Verify do máy chạy lại và cưỡng chế phía khung
Nhãn: GIỮ | Đợt: Đ3b | PROPOSAL: E6
- PASS hoặc FAIL cuối cùng do điều phối viên hoặc script chạy lại verify một lần trên môi trường sạch, cách ly mức nhẹ (H2 mục 6); không lấy từ văn bản của WORKER. LEAD và REVIEWER đọc kết quả lần chạy đó.
- Cưỡng chế phía khung:
  - Cấu hình cố định theo tuyến.
  - File tạo mới: UTF-8 không BOM; line ending theo .gitattributes.
  - Cờ no_tool_execution từ relay là điều kiện dừng an toàn.
  - Giới hạn số lệnh thực thi do khung kiểm soát, không dựa vào câu nhắc trong prompt.
- Zero-trust với lời khuyên của AI: mọi đoạn mã, lệnh shell do AI đề xuất là dữ liệu chưa kiểm chứng. Kiểm cú pháp chỉ là bước đầu; an toàn khi chạy dựa vào cách ly và phạm vi quyền, không dựa vào việc đọc mã.

## 13. Tuyến đã chứng minh theo vai
Nhãn: GỘP (vào MODEL_POLICY#ELIGIBILITY và MODEL_CATALOG#ROUTE_CHECKS) | Đợt: Đợt 2 (catalog bổ sung model đang dùng ở Đ2) | PROPOSAL: E10, E19
- Tuyến được kiểm theo đúng vai, đúng hạng task và đúng cấu hình sẽ chạy thật.
  - Phân tích: đạt P4.
  - Thi công: đạt P4 và W1–W4 cho hạng task sẽ nhận.
  - Kiểm định: đạt P4 và có quyền truy cập Git hoặc gói dữ kiện kiểm định.
- P4: [CẦN ĐỊNH NGHĨA: LEAD].
- W1–W4 (đề xuất 2026-11-21, E19); mỗi phép kiểm chạy trên bộ task mẫu cố định của từng hạng:
  - W1 — Làm đúng: hoàn thành task mẫu có test cho sẵn; verify PASS do máy chạy lại.
  - W2 — Trong giới hạn: hoàn thành task mẫu nhiều bước mà mỗi lượt gọi vẫn nằm trong ngân sách context của tuyến.
  - W3 — Báo thật: với task mẫu không làm được (thiếu đầu vào, mâu thuẫn), báo BLOCKED đúng lý do thay vì tự báo đã xong; không có CLAIM_MISMATCH.
  - W4 — Tự sửa: sau khi nhận đầu ra test lỗi, đạt PASS trong tối đa 2 vòng.
  - Ngưỡng đạt và cỡ bộ mẫu: [LEAD chốt].
- Đánh giá tuyến bằng Cost per Accepted Task, tính cả các lần thử hỏng, token LEAD và token điều phối, không bằng giá token. Tuyến free không phải không tốn: mỗi lần hỏng vẫn tốn token LEAD và thời gian.
- Lỗi tương thích (tên tool, context) sửa được một lần; lỗi năng lực (bịa kết quả, xin cài phần mềm) thì không.
- Hạ hạng tự động: tuyến vượt ngưỡng tỷ lệ FAIL hoặc CLAIM_MISMATCH trong ROUTE_CHECKS thì về UNQUALIFIED cho hạng đó (H4-7).
- Quan sát tại ngày ghi của hồ sơ cũ (không rõ ngày):
  - DeepSeek: chỉ đọc và phân tích; W1 FAIL, W2–W4 chưa chạy, gặp 402. Chưa có trong catalog.
  - Nvidia Nano Free: dễ xin escalation (FAIL 1/2). Chưa có trong catalog.
  - Grok: ổn định nhất trong vai REVIEWER.
- DeepSeek, Nvidia Nano phải vào catalog ở trạng thái UNQUALIFIED hoặc bị loại khỏi routing trước Đ3b (H0 mục 5).

## 14. Bẫy Windows, PowerShell 5.1 và binary nền
Nhãn: GIỮ | Đợt: Đ1 | PROPOSAL: E9, E24
- Không dùng toán tử > hoặc Out-File mặc định của PowerShell 5.1; chúng ghi UTF-16.
- Đọc, ghi file cần chính xác byte: dùng Python hoặc PowerShell 7.
- Tránh alias lệnh dễ nhầm (where và where.exe).
- Không duyệt yêu cầu có cờ require_escalated hoặc lệnh cài phần mềm hệ thống (winget, choco).
- Có sẵn danh sách thư mục an toàn được cấp quyền.
- Danh sách binary nền đã duyệt (E24, 2026-11-21): Git, Python, pwsh 7.4, 9Router, Codex CLI, [LEAD bổ sung]. Binary mới (ví dụ gitleaks, Docker, Windows Sandbox) cần DEC. Công cụ Python mới cài qua pip. Thay cho cách hiểu "không binary ngoài", vốn mâu thuẫn với việc mục này khuyên dùng PowerShell 7.
- Lưu ý 2026-11-22: Git Bash đi kèm Git nên có `bash`, `perl`, `timeout`; không có `jq`. Script của GSD Core dùng `jq` (ví dụ `sync-rulesets.sh`) phải viết lại bằng Python, hoặc thêm `jq` qua DEC theo E24.

## 15. Quyền riêng của OWNER
Nhãn: GIỮ (viết lại) | Đợt: [ĐỢT: LEAD chốt] | PROPOSAL: E11
- Chỉ OWNER: merge PR; đẩy hoặc sửa main; tạo, sửa, xóa thẻ git; đổi cấu hình nhạy cảm, bí mật, quyền; cấp miễn trừ.
- Tác tử vẫn đẩy nhánh của mình và mở PR (WORKER.md luật 12, REVIEWER.md luật 8).
- Thi hành (bổ sung 2026-11-21): luật này không có rào kỹ thuật khi tác tử dùng chung tài khoản với OWNER (DEC-0019). Cần tài khoản tác tử riêng (E14) và ruleset cấm tạo thẻ, cập nhật main, chỉ OWNER bypass. validate ở PR không thấy các hành động này (H2 mục 2).
- Cập nhật 2026-11-22: E14 đã chốt tách tài khoản (DEC-0031). Ruleset bật ở O1.1–O1.4 (Bước 1); chuyển thành file JSON và script áp ở TK-0054 (E43). Luật thẻ cần chặn cả tạo, sửa, xóa; chỉ OWNER bypass.

## 16. Phân hạng task và thang leo tuyến
Nhãn: GIỮ | Đợt: Đợt 2 (riêng kiểm lời tự báo: Bước 3, E40) | PROPOSAL: E17, E31, E34, E35, E38, E40, E42
- Hạng task ghi trong task spec, do LEAD Planning gán; script đọc và chặn giao sai hạng.
  - T0 — cơ học: định dạng, đổi tên, sửa lint, cập nhật tài liệu theo mẫu.
  - T1 — logic nhỏ: một file sản phẩm, test do Planning viết sẵn; WORKER không viết test cho chính nó.
  - T2 — thiết kế hoặc nhiều file, cần tự viết test, chạm hợp đồng dùng chung.
- Thang leo tuyến: tuyến free → tuyến trả phí rẻ → tuyến mạnh. Task spec ghi sẵn tuyến kế tiếp.
- Cập nhật 2026-11-22 (E34, E35, E42, theo GSD Core):
  - Hai thang tách nhau. Lỗi năng lực (FAIL logic, CLAIM_MISMATCH) thì leo tuyến. Lỗi hạn mức (429, hết quota) thì đổi nhà cung cấp, vì tuyến mạnh hơn trên cùng tài khoản bị giới hạn vẫn bị giới hạn.
  - Trần leo mặc định 1 bậc mỗi task (`max_escalations`); lỗi crash không leo, báo ngay.
  - Trước khi leo, thử tách task thành tối đa 3 bước con. Thứ tự: thử lại có điều chỉnh → tách → leo → báo BLOCK. Ngân sách sửa 2 lần mỗi task.
  - Không bỏ task (PRUNE) mà không có BLOCK lên LEAD.
  - Thang nhà cung cấp cạn thì báo lỗi kèm danh sách mọi tuyến đã thử; không âm thầm thử lại tuyến cuối.
- Leo bậc khi gặp một trong các điều kiện:
  - 2 lần FAIL logic liên tiếp trên tuyến free.
  - 1 lần CLAIM_MISMATCH.
  - Quá khung thời gian task (mục 17).
  - Hết trần lỗi hạ tầng của tuyến (mục 9). Từ 2026-11-22 trường hợp này đi theo thang nhà cung cấp (đổi nhà cung cấp), không phải thang năng lực.
- Phép kiểm bịa (CLAIM_MISMATCH), do script chạy sau mỗi lượt WORKER. Cập nhật 2026-11-22 (E40): áp cho mọi run, mọi tuyến, từ Bước 3 (schema ở TK-0042, phép kiểm ở TK-0043), không chờ Đợt 2. SHA khai báo phải nằm trên đúng nhánh của task:
  - File WORKER nói đã tạo hoặc sửa có tồn tại và có trong diff.
  - Diff không rỗng khi WORKER báo đã xong.
  - Lệnh, test WORKER nói đã chạy có trong raw capture.
  - Bất kỳ phép nào lệch thì ghi CLAIM_MISMATCH; đây là lỗi năng lực, không thử lại cùng tuyến.
- Đầu ra của WORKER trên tuyến free: chỉ patch. Harness tự áp; patch không áp được thì loại, không cần LEAD đọc.
- Luật đọc trước khi sửa cho tuyến free (thêm 2026-11-22, E38, theo `gsd-read-guard` của GSD): model không phải Claude hay sửa file mà không đọc trước, bị từ chối rồi thử lại mãi, đốt hạn mức. Gói ngữ cảnh đã chứa file trong write_scope; luật nhắc WORKER dùng bản đó thay vì ghi đè mù.
- Gói ngữ cảnh tối thiểu cho tuyến context nhỏ:
  - Cỡ gói (thêm 2026-11-22, E31): không quá khoảng 50% ngân sách context của tuyến; task kiểu TDD khoảng 40%. Đây là ngưỡng khởi đầu lấy từ GSD Core, hiệu chỉnh bằng số liệu Đợt 1.
  - File trong write_scope, test liên quan, chữ ký hàm của module xung quanh do script trích, không đưa nguyên repo.
  - Không mang lịch sử hội thoại sang vòng sau. Mỗi vòng dựng lại từ checkpoint đã xác nhận, ghi chú phản tư ≤ 3 câu của vòng trước, đầu và đuôi output FAIL (mục 7).
  - Cấp 3 tuần tự hợp với tuyến context nhỏ: mỗi bước là một lượt gọi riêng, trạng thái truyền qua file và checkpoint.

## 17. Khung thời gian, hạn mức và ngắt mạch cho tuyến free
Nhãn: GIỮ | Đợt: Đợt 2 | PROPOSAL: E17, E13 (phần tuyến free)
- Khung thời gian, do harness đặt, không dựa vào câu nhắc:
  - Timeout cho mỗi lượt gọi; streaming cho lượt dài; timeout khi luồng im lặng quá [LEAD chốt] giây.
  - Tổng thời gian cho cả task: [LEAD chốt] theo hạng task. Quá khung thì leo bậc, không chờ thêm.
- Hạn mức: script điều phối đọc hạn mức của tuyến trong MODEL_CATALOG (mục 1); không giao hai task song song lên cùng một tuyến free; không vượt số request mỗi phút, mỗi ngày.
- Ngắt mạch áp sớm cho riêng tuyến free: tuyến gặp lỗi hạ tầng tạm thời từ 3 lần trong 30 phút thì tạm ngưng 60 phút; task đang chờ chuyển sang tuyến kế tiếp.
- Mất kết nối giữa chừng: harness bỏ phần đầu ra dở dang và chạy lại từ checkpoint; không áp patch dở.

## Đã loại
- "git push lên remote" và "mở PR" chỉ OWNER → trái WORKER.md luật 12, REVIEWER.md luật 8.
- "Thêm, xóa tuyến" chỉ OWNER → LEAD đang ghi ROUTE_CHECKS; cấu hình router thuộc "cấu hình nhạy cảm".
- "Restart, cấu hình lại relay" chỉ OWNER → thuộc hạ tầng, xét cùng mục 6.
- "Xóa file ngoài write_scope" chỉ OWNER → đã là điểm dừng và phép kiểm validate (H2).
- Con số cache hit ~96,6% → không có nguồn đo.
- Chứng minh khả nghịch làm luật thường trực → chỉ cần cho dữ liệu cũ TK-0027.
- Cấm hẳn tuyến free làm WORKER (bản 2026-11-19) → OWNER cần tuyến free cho nhiều loại việc; thay bằng điều kiện ở mục 11, 16, 17 (2026-11-21).
- Để WORKER free dùng hết max_loops = 3 → tốn token LEAD và thời gian cho lỗi năng lực; thay bằng ngưỡng leo bậc (2026-11-21).
