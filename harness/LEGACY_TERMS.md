# BẢNG ÁNH XẠ THUẬT NGỮ: V5.0 → HARNESS V1.0

> **Tóm tắt 3 dòng**
> 1. File này để model và người dùng quen V5.0 tra nhanh: thuật ngữ, mã, tên file, khóa YAML cũ tương ứng với gì trong Harness V1.0.
> 2. Quy tắc dùng: **đầu vào chấp nhận thuật ngữ V1.0, thuật ngữ V5.0 và các biệt danh ở mục 2; mọi đầu ra (bản ghi, khối chuẩn, code, giao việc) chỉ dùng chuẩn V1.0.** Gặp mã cũ hoặc biệt danh thì đổi sang mã mới theo bảng, rồi làm việc bằng mã mới.
> 3. Dòng ghi **"không có"** nghĩa là V1.0 chưa có khái niệm tương đương; model không được tự suy ra một tên mới.

| Thuộc tính | Giá trị |
|---|---|
| Nguồn đối chiếu | `PHUONG_PHAP_V5.0.0.md` và `harness/HARNESS.md` |
| Ai đọc | LEAD, khi gặp thuật ngữ cũ. WORKER và REVIEWER không đọc |
| Vị trí trong repo | `harness/LEGACY_TERMS.md`; `harness/rules/LEAD.md` trỏ tới file này |

---

## 1. Năm chỗ dễ nhầm nhất

| Ký hiệu | Trong V5.0 | Trong V1.0 | Cách tránh nhầm |
|---|---|---|---|
| `T-xx` | Lý thuyết nền | **Không dùng.** Lý thuyết là `THY-nn`; task là `TK-nnnn` | Thấy `T-07` trong văn bản cũ thì hiểu là lý thuyết, không phải task |
| `TH` | Model Thực hiện | **Không dùng.** Vai thực hiện là `WORKER`; `THY` là lý thuyết | `TH1` → `W1`; `taskee` cũng là `WORKER` |
| `Q-xx` | Quyết định | `DEC-nnnn` | `Q` không phải "question"; câu hỏi mở trong V1.0 là sự kiện `QUESTION` của `DSC` |
| `R-xx` và `Ln` | `R-xx` = rủi ro; `Ln` = lần thực hiện | `RSK-nnnn` = rủi ro; `Rn` = lần nộp (run); `Lnn` = loop trong log | `R2` trong V1.0 là lần nộp thứ 2. `L2` cũ → `R2` mới; `L03` mới là vòng làm–kiểm thứ 3, không phải lần thực hiện |
| Tầng 1 / 2 / 3 | Ba tầng **nén nhật ký** (cờ → nhật ký đợt → tri thức cốt lõi) | `L0` / `L1` / `L2` là ba tầng **đọc bộ nhớ** (trạng thái → sổ đang sống → kho lạnh) | Hai hệ khác trục, **không ánh xạ 1–1**. Xem mục 8 |

**Đổi định dạng số:** mã V5.0 có 2 chữ số, mã V1.0 có 4 chữ số (riêng chu kỳ 2 chữ số). `V07` → `TK-0007`; `Q-04` → `DEC-0004`; `R-11` → `RSK-0011`; `YC-03` → `REQ-0003`; `N-02` → `SRC-0002`; `D02` → `CYC-02`.

## 2. Vai trò

| Đầu vào (V5.0 hoặc biệt danh) | Nghĩa | V1.0 |
|---|---|---|
| `CD` | Chủ dự án | `OWNER` |
| `ĐP` / `DP` | Model Điều phối | `LEAD` |
| `TH`, `TH1`, `TH2`, `taskee` | Model Thực hiện | `WORKER`, `W1`, `W2` |
| `KĐ` / `KD` / `judge` | Kiểm định | `REVIEWER` |
| `SME` | Chuyên gia thẩm định | `REVIEWER` (là người) |

## 3. Mã định danh

| V5.0 | Nghĩa | V1.0 | Ghi chú |
|---|---|---|---|
| `Vxx` | Phiếu việc | `TK-nnnn` | Task |
| `Ln` | Lần thực hiện thứ n | `Rn` | Run. Không nhầm với `Lnn` của V1.0 (loop) |
| `Vxx_Ln_<KET_QUA>` | File cờ | `TK-nnnn_Rn_<OUTCOME>` | Bản ghi lần chạy |
| `Dnn` | Đợt | `CYC-nn` | Cycle |
| `QUY_nn` | Cột mốc quý | không có | V1.0 nhắc "cổng quý" cho hồ sơ `LONG` nhưng chưa định mã và file |
| `Q-xx` | Quyết định | `DEC-nnnn` | |
| `R-xx` | Rủi ro | `RSK-nnnn` | |
| `YC-xx` | Yêu cầu ngoài kế hoạch | `REQ-nnnn` | |
| `CR-Vxx-Ln` | Đề xuất sửa đặc tả của TH | không có mã riêng | Ghi trong bản ghi lần chạy khi `escalate: yes` |
| `N-xx` | Nguồn chuẩn | `SRC-nnnn` | |
| `T-xx` | Lý thuyết nền | `THY-nn` | Số **không giữ nguyên**; tra mục 12 |
| — | — | `DSC-YYYYMMDD-xxxx` | Mới: bản ghi thảo luận |
| — | — | `DC-nn` | Mới: lựa chọn thiết kế của khung |
| — | — | `TK-nnnn.Lnn.Snn` | Mới: mã vết của loop và span |
| — | — | `RVW-CYC-nn` | Mới: bản ghi kiểm định chu kỳ |
| Mã file token `<ngày>_<vai trò>_<tác vụ>_<mã phiên>` | Bản ghi token một phiên | không có | Xem mục 10 |

## 4. Loại yêu cầu, câu lệnh, kết quả

| V5.0 | V1.0 |
|---|---|
| Loại A — hỏi, tra cứu | `ASK` |
| Loại B — giao làm phiếu | `RUN` |
| Loại C — yêu cầu thay đổi | `CHANGE` |
| — | `DISCUSS` (mới: thảo luận, brainstorm) |
| "Làm phiếu V07" | "Run TK-0007" |
| "Làm" (cho TH bắt đầu) | "Go" |
| "OK" (cho ĐP bắt đầu) | "OK" |
| "Đồng ý sửa" (xác nhận lần 2 khi chạm vùng cấm) | chưa định câu cố định; vẫn hỏi xác nhận hai lần |
| Khối 3 Mô Tả | Khối chuẩn `CONFIRM` |
| 1. Hiểu yêu cầu · 2. Phạm vi & cách làm · 3. Kết quả & kiểm chứng | `understanding` · `scope` · `result` |
| "Sẽ KHÔNG làm" | `will_not_do` |
| Đề nghị merge (✅ ĐỀ NGHỊ MERGE) | Khối chuẩn `MERGE` |
| Báo cáo kiểm định của KĐ | Bản ghi `RVW-CYC-nn` + khối chuẩn `REVIEW` |
| Thẻ quyết định | Khối chuẩn `QUESTION` (rút gọn: một ý, hai lựa chọn) |
| — | Khối chuẩn `RESULT` (mới) |

| Kết quả cờ V5.0 | Outcome V1.0 |
|---|---|
| `XONG` | `DONE` |
| `VUONG` | `BLOCKED` |
| `HUY` | `CANCELLED` |

## 5. Phase, hồ sơ quy mô, cổng

| V5.0 | V1.0 |
|---|---|
| `PHASE_HIEN_TAI` | `PHASE` |
| `DOT_HIEN_TAI` | `CYCLE` |
| `HO_SO_QUY_MO` | `PROFILE` |
| `PHASE_1_Y_TUONG` | `BRAINSTORM` |
| `PHASE_2_KE_HOACH` | `PLAN` (một lần sau brainstorm, không lặp mỗi đợt) |
| `PHASE_3_THUC_THI` | `EXECUTE` |
| `PHASE_4_KIEM_THU` | `VERIFY` |
| `PHASE_5_TONG_KET` | `CLOSE` |
| `DA_DONG` | `CLOSED` |
| `CHUA_CO` | `NONE` |
| `CHUA_XAC_DINH` | `UNSET` |
| `NGAN` / `TRUNG` / `DAI` | `SHORT` / `MEDIUM` / `LONG` |
| Cổng mở đợt (10 câu), mỗi đợt | Cổng PLAN (`PLAN_GO.md`, 8 câu), một lần |
| Cổng nghiệm thu đợt (8 câu) | PASS gate (8 câu) |
| Cổng quý | nhắc tới, chưa định chi tiết |
| `Đạt` / `Có điều kiện` / `Chưa đạt` / `Không áp dụng` | `PASS` / `CONDITIONAL` / `FAIL` / `N/A` |
| Bài kiểm tra người mới | Câu 8 của PASS gate (newcomer test) |
| Dấu vân tay vật lý | Không có tên riêng; vẫn dùng nguyên tắc "file tồn tại là dấu hiệu tiến độ" |

## 6. Thư mục và file

| V5.0 | V1.0 |
|---|---|
| `RULES.md` | `harness/rules/LEAD.md` |
| `RULES_TH.md` | `harness/rules/WORKER.md` |
| `RULES_KD.md` | `harness/rules/REVIEWER.md` |
| `CLAUDE.md`, `GEMINI.md`, `AGENTS.md` | giữ nguyên |
| `05_MAU/PHUONG_PHAP_V<phiên bản>.md` | `harness/HARNESS.md` + `harness/VERSION` |
| `tools/` | `harness/tools/` |
| `00_DE_BAI/` | `00_brief/` |
| `00_DE_BAI/khoi_tao.md` | `00_brief/BRIEF.md` |
| `00_DE_BAI/bien_ban_phong_van.md` | Bản ghi thảo luận `DSC` trong `05_memory/discussions/YYYY/` (phase `BRAINSTORM`) |
| `01_KE_HOACH/` | `01_plan/` |
| `KE_HOACH_TONG_THE.md` | `PLAN.md` |
| `CAY_VIEC.md` | không có file riêng; danh sách task theo chu kỳ nằm trong `PLAN.md` |
| `TIEU_CHI_NGHIEM_THU.md` | `ACCEPTANCE.md` |
| `DAC_TA/HD_<MODULE>.md` | `01_plan/SPEC_<MODULE>.md` |
| `HOP_DONG_DU_LIEU.md` | không có file riêng; nội dung nằm trong `01_plan/` |
| `02_CONG_VIEC/` | `02_work/` |
| `viec/Dnn/Vxx.md` | `tasks/CYC-nn/TK-nnnn.md` |
| `co/` | `runs/` |
| `dot/Dnn.md` | `cycles/CYC-nn.md` |
| `03_KET_QUA/` | `03_output/` (sản phẩm không phải code); dự án code dùng `product_paths` khai trong `harness.yaml` |
| `03_KET_QUA/Dnn/kiem_thu/` | `03_output/CYC-nn/checks/` |
| `04_QUAN_TRI/` | `04_control/` |
| `TRANG_THAI.md` | `STATE.md` |
| `SO_QUYET_DINH/` · `het_hieu_luc/` | `decisions/` · `superseded/` |
| `SO_RUI_RO/` · `da_dong/` | `risks/` · `closed/` |
| `YEU_CAU/` · `da_xu_ly/` | `requests/` · `resolved/` |
| `CONG/` | `gates/` |
| `CONG/Dnn_GO.md` | `gates/PLAN_GO.md` (một file cho cả plan) |
| `CONG/Dnn_DAT.md` | `gates/CYC-nn_PASS.md` |
| `CONG/NGHIEM_THU_CUOI_DAT.md` | `gates/FINAL_PASS.md` |
| `XAC_NHAN_HOAN_THANH.md` | `gates/CLOSED.md` |
| `CONG/QUY_nn_DAT.md` | không có |
| `SO_TOKEN/` | không có thư mục; xem mục 10 |
| `05_MAU/` (13 mẫu) | `harness/templates/` |
| `06_NHAT_KY/` | `05_memory/` |
| `06_NHAT_KY/DOT_Dnn.md` | `05_memory/digests/CYC-nn.md` |
| `06_NHAT_KY/TRI_THUC_COT_LOI.md` | `05_memory/CORE.md` |
| `06_NHAT_KY/ngoai_phieu/YC-xx.md` | không có; phiên `CHANGE` ghi vào `REQ-nnnn` |
| `07_NGUON_CHUAN/` | `06_sources/` |
| `08_MAU_DU_AN/` | không có |
| `.transcripts/` | `<project>.local/transcripts/` |
| — | `<project>.local/scratch/`, `logs/`, `quarantine/`, `cache/` (mới) |
| — | `harness.yaml` (mới) |
| — | `05_memory/discussions/`, `topics/`, `GLOSSARY.md` (mới) |
| — | `harness/schemas/`, `harness/extensions/` (mới) |

**Nhánh Git**

| V5.0 | V1.0 |
|---|---|
| `phieu/Vxx-Ln` | `task/TK-nnnn-Rn` |
| `dieu-phoi/<mo-ta>` | `lead/<slug>` |
| `kiem-dinh/Dnn` | `review/CYC-nn-Rk-xxxx` |
| `nang-cap/<mo-ta>` | `upgrade/<version>` |
| `doi-chung/Vxx-<model>` | không có |

## 7. Khóa YAML và giá trị

### 7.1. Phiếu → Task

| V5.0 | V1.0 |
|---|---|
| `phieu` | `id` |
| `dot` | `cycle` |
| `giao_cho` | `assignee` |
| `muc_tieu` | `goal` |
| `pham_vi_file` | `write_scope` |
| `rang_buoc_cuc_bo` | `constraints` |
| tiền tố `KHÔNG LÀM:` | tiền tố `NEVER:` |
| `dau_ra_phu_thuoc` | `inputs` |
| `doc_them` | `read_also` |
| `ngan_sach_dong` | `line_budget` |
| `cach_kiem_chung` | `verify` |
| `dod` | `done_when` |
| `kich_co` | `size` |
| `phu_thuoc` | `depends_on` |
| `sua_cho` | `fixes` |
| — | `schema`, `origin` (bắt buộc, trỏ `DEC` đang `ACTIVE` hoặc mục chu kỳ của `PLAN.md`), `log_level`, `max_loops` (mới) |

### 7.2. Cờ → Run

| V5.0 | V1.0 |
|---|---|
| `phieu` | `task` |
| `lan` | `run` |
| `ket_qua` | `outcome` |
| `model` | `model` |
| `nhanh` | `branch` |
| `san_pham` | `outputs` |
| `bang_chung` | `evidence` |
| `dod_doi_chieu` | `done_check` |
| giá trị `chay_test` | giá trị `ci` |
| `bao_DP` (`co` / `khong`) | `escalate` (`yes` / `no`) |
| `cham_vung_cam` (`co` / `khong`) | `touched_protected` (`yes` / `no`) |
| `sai_biet` | `deviations` |
| `gia_dinh_ngam` | `assumptions` |
| `khac_biet` | `differences` |
| `chua_kiem` | `unverified` |
| `tu_khoa` | `keywords` |
| `token` | `usage` |
| `ly_do_token` | không có |
| `## Tóm tắt` | không có; run là YAML thuần |
| `## CR-Vxx-Ln` | khóa `escalation` (`spec`, `problem`, `proposal`) |
| — | `loops` (mới: tóm tắt từng vòng làm–kiểm) |

### 7.3. Sổ quyết định, rủi ro, yêu cầu

| Loại | V5.0 | V1.0 |
|---|---|---|
| Quyết định | `ma` | `id` |
| | `ngay` | `date` |
| | `de_xuat_boi` | `proposed_by` |
| | `quyet_dinh_boi` | `decided_by` |
| | `dot` | `cycle` |
| | `thay_the` | `supersedes` |
| | `huy_phieu` | `cancels` |
| | `mien_tru` | `waives` |
| | `anh_huong` | `affects` |
| | — | `title`, `origin`, `keywords` (mới) |
| | `## Bối cảnh` | `## Context` (neo `CONTEXT`) |
| | `## Các phương án đã cân nhắc` | `## Options considered` (neo `OPTIONS`) |
| | `## Quyết định và lý do` | `## Decision and rationale` (neo `RATIONALE`) |
| | `## Hệ quả` | `## Consequences` (neo `CONSEQUENCES`) |
| Rủi ro | `ma` | `id` |
| | `ngay_mo` | `opened` |
| | `tieu_de` | `title` |
| | `lien_quan` | `related` |
| | `## Mô tả và ảnh hưởng` | `## Impact` (neo `IMPACT`) |
| | `## Cách ứng phó` | `## Response` (neo `RESPONSE`) |
| Yêu cầu | `ma`, `ngay`, `tieu_de` | `id`, `date`, `title` |
| | `nguon` | `proposed_by` |
| | — | `cycle`, `affects`, `keywords` (mới); neo `CONTEXT`, `IMPACT` |
| Chung | `## Trạng thái (mới nhất ở trên)` | `## Status (newest first)` |

### 7.4. Giá trị trạng thái

| V5.0 | V1.0 |
|---|---|
| `Hiệu lực` | `ACTIVE` |
| `Bị thay thế bởi Q-xx` | `SUPERSEDED_BY DEC-nnnn` |
| `Hết hiệu lực` | `RETIRED` |
| `Mở` | `OPEN` |
| `Đang xử lý` | `MITIGATING` |
| `Đã đóng` | `CLOSED` |
| `Mức độ: THAP` / `TRUNG_BINH` / `CAO` | `level: LOW` / `MEDIUM` / `HIGH` |
| `Hạn:` | `due:` |
| `Theo dõi:` | `owner:` |
| Ghi chú tự do ở cuối dòng trạng thái | không có; dòng trạng thái chỉ gồm khóa–giá trị |
| `Khả năng: Hiếm` / `Có thể xảy ra` / `Gần như chắc chắn` | không có |
| `Chờ quyết định` | `PENDING` |
| `Đã xử lý bởi Q-xx` | `RESOLVED_BY DEC-nnnn` |

## 8. Khái niệm

| V5.0 | V1.0 | Ghi chú |
|---|---|---|
| Tấm bảng giao ca | Handover board (trong `STATE.md`) | Năm mục giữ nguyên thứ tự: Progress · Open risks · Recent decisions · Next action · Never do |
| Vùng cấm (Nhóm A) 🔒 | Protected area 🔒 | |
| File ký duyệt (Nhóm B) ✍️ | Sign-off file ✍ | |
| Vùng 1 / Vùng 2 / Vùng 3 | Zone 1 / Zone 2 / Zone 3 | |
| Kho lạnh | Cold storage | |
| Neo `<!-- NEO: X -->` … `<!-- HET: X -->` | `<!-- ANCHOR: X -->` … `<!-- END: X -->` | Cú pháp trỏ `file#X` giữ nguyên |
| Sai biệt | Deviations | |
| Gói ngữ cảnh tự thân | Self-contained task | |
| DoR (Definition of Ready) | Chuẩn sẵn sàng của task | |
| DoD | `done_when` | |
| Học hai vòng | Loop đóng sau `max_loops` loop `FAIL` (mặc định 3): run `BLOCKED`, `escalate: yes`. Run thứ hai vẫn `BLOCKED` thì LEAD đưa về OWNER | |
| Đề nghị merge | Khối chuẩn `MERGE` | Mẫu nằm trong `harness/templates/` |
| Xác nhận 2 bước | Hỏi xác nhận hai lần trước khi sửa vùng 🔒 | Không có tên mã |
| Bản chiếu | Projection | |
| Sự kiện gốc | Bản gốc: sổ, run, file cổng | |
| Bốn lớp bảo vệ | Bốn lớp bảo vệ (mục 10.1) | Nội dung tương đương |
| Lớp phát hiện | Lớp 4: Detective | |
| Nhật ký Tầng 1 (khối `sai_biet` trong cờ) | `deviations` trong run | |
| Nhật ký Tầng 2 (`DOT_Dnn.md`) | Cycle digest (`digests/CYC-nn.md`) | |
| Nhật ký Tầng 3 (`TRI_THUC_COT_LOI.md`) | `CORE.md` | |
| — | `L0` / `L1` / `L2` | Mới. Tầng **đọc**: `STATE.md` / sổ đang sống / kho lạnh và lịch sử |
| Retro cuối đợt | Mục bài học trong cycle digest | |
| Thẻ quyết định | Khối chuẩn `QUESTION` | Rút gọn |
| Phỏng vấn Phase 1 | Phase `BRAINSTORM`: các phiên `DISCUSS` với OWNER | |
| Lập kế hoạch đợt (mỗi đợt) | Phase `PLAN`: LEAD lập `PLAN.md` một lần từ các `DEC`; OWNER duyệt | |
| Pre-mortem | Câu 7 cổng PLAN | |
| 2 cờ `VUONG` liên tiếp → học hai vòng | `max_loops` loop `FAIL` (mặc định 3) → loop đóng, run `BLOCKED`, `escalate: yes` | Giới hạn ba lần |
| — | Loop trigger: "Start CYC-nn" hoặc script `loop` | Mới |
| — | No-annotation rule | Mới: không ghi chú trong bản ghi, dữ liệu, code |
| — | Loop, Span, Trace ID, Log level | Mới |
| — | Acceptance sheet | Mới: bảng nghiệm thu đầu cổng PASS |
| — | Squash merge; `product_paths`; Project kind | Mới |
| Sáu quy tắc viết cho con người duyệt | Rút gọn thành: một ý mỗi câu, lời thường, kết luận trước | |
| Mức review Nhẹ / Trung bình / Sâu | không có | |
| Kiểm tra ngẫu nhiên 1/10 | không có | |
| Lô đề nghị merge có thứ tự | Rút gọn: merge từng PR theo thứ tự LEAD đề nghị | |
| Mutation testing, RTM, Bảng Key Points, phiếu thẩm định SME | không có | Phần mở rộng theo loại dự án |
| Đối chứng chéo model | không có | |
| — | Discussion record, Event, `PROPOSAL` / `ASSUMPTION` / `IDEA` / `QUESTION` | Mới |
| — | Extension, manifest, hook | Mới |
| — | Scan level `ALLOW` / `WARN` / `QUARANTINE` / `BLOCK` | Mới |
| — | Validation result `PASS` / `REJECT` / `AUTOFIX` | Mới |
| — | Call mode `SETUP` / `AGENT` / `MANUAL` | Mới |

## 9. Công cụ

| V5.0 | V1.0 | Ghi chú |
|---|---|---|
| `tools/thu_vien.py` | Thư viện đọc/ghi chung | Chưa đặt tên file |
| `tools/kiem_tra_co.py` | `validate` | |
| `tools/doc_doan.py` | `get` | Mở rộng: nhận cả mã, không chỉ `file#NEO` |
| `tools/cap_nhat_bang.py` | `state` (sinh `STATE.md`, bảng nghiệm thu) + `ledger` (chuyển kho lạnh) | Tách làm hai |
| `tools/ghi_token.py` | `budget` | Phạm vi hẹp hơn; xem mục 10 |
| `tools/tong_hop_token.py` | `budget` (một phần) | Báo cáo theo đợt, theo model: không có |
| `tools/lap_phieu.py` | không có | LEAD lập task bằng tay; kiểm con trỏ bằng `validate` (C9) |
| `tools/bao_cao_review.py` | không có | |
| — | `doctor`, `discuss`, `loop`, `trace`, `context`, `scan`, `index` | Mới |

Toàn bộ script V1.0 mới ở mức ý tưởng, chưa có code.

## 10. Đo token

| V5.0 | V1.0 |
|---|---|
| Sổ `SO_TOKEN/phien/*.json`, mỗi phiên một file | không có thư mục; `budget` ghi "bản ghi số liệu", chưa định nơi lưu |
| Trường `token` của cờ | Trường `usage` của run |
| Bảy mã nguyên nhân (`TRONG_DINH_MUC`, `DAC_TA_PHIEU_MO_HO`, `DOC_VUOT_PHAM_VI`, `TAI_LIEU_NGUON_LON`, `LAP_SUA_LOI_TEST`, `LOI_MOI_TRUONG_CONG_CU`, `SUY_LUAN_SAU`) | không có |
| `in_moi`, `cache_ghi`, `cache_doc`, `out`, `suy_luan`, `tong_xu_ly` | không có |
| Hệ số quy đổi chéo model, FPY, tỷ lệ hao phí | không có |
| `ngan_sach_dong` so với `dong_da_doc` | `line_budget`; phần đối chiếu do `budget` đảm nhận |

## 11. Kiểm tra trên PR

| V5.0 (15 kiểm tra) | V1.0 (C1–C14) |
|---|---|
| 1 — `co/` chỉ thêm file | C1 |
| 2 — Cờ hợp lệ, `lan` = 1 + max, DoD phủ đủ | C1, C2 |
| 3 — Phạm vi theo loại PR | C3 |
| 4 — Chạm Nhóm A, Nhóm B | C3, C4 |
| 5 — Sổ chỉ-thêm, kho lạnh | C5 |
| 6 — Header khớp dấu vân tay | C6 |
| 7 — Độ dài file | C7 |
| 8 — Quét bí mật, chặn dữ liệu thật | C8 |
| 9 — Bằng chứng tồn tại | C2 |
| 10 — Cờ `HUY` có `Q-xx` hợp lệ | không có kiểm tra riêng |
| 11 — File cổng GO đủ câu | C11 (cổng `PLAN_GO.md`) |
| 12 — Đúng một bản phương pháp, khớp phiên bản | C12 |
| 13 — Tấm bảng khớp bản gốc | C6 |
| 14 — File token hợp lệ | không có |
| 15 — Mã và neo trong phiếu tra được | C9 |
| — | C10 (mới): `DEC` có `origin` là `DSC…#Ex` thì `DSC` có dòng `ACCEPTED` tương ứng |
| — | C13 (mới): không ghi chú |
| — | C14 (mới): đánh dấu PR xóa hoặc nới test |

## 12. Lý thuyết nền: `T-xx` → `THY-nn`

| V5.0 | Lý thuyết | V1.0 |
|---|---|---|
| T-01 | Orchestrator–Workers; Evaluator–Optimizer | THY-01 |
| T-02 | Lost in the Middle | THY-02 |
| T-03 | Progressive Disclosure | THY-03 |
| T-04 | Convention over Configuration | THY-04 |
| T-05 | Single Source of Truth / DRY | THY-05 |
| T-06 | Information Hiding | THY-06 |
| T-07 | Bộ nhớ phân tầng (MemGPT, HSM) | THY-07 |
| T-08 | Event Sourcing & CQRS | THY-08 |
| T-09 | Least Privilege | THY-09 |
| T-10 | Fail-safe Defaults | THY-10 |
| T-11 | Defense in Depth | THY-11 |
| T-12 | Separation of Duties | THY-12 |
| T-13 | Human-in-the-Loop | THY-13 |
| T-14 | Closed-loop Communication | THY-14 |
| T-15 | Routing | không có mã riêng (phân loại phiên dẫn THY-04) |
| T-16 | Poka-yoke | THY-15 |
| T-17 | Bounded Context | không có |
| T-18 | Integrated Change Control | không có |
| T-19 | CRDT G-Set & 2P-Set | THY-16 |
| T-20 | Lamport Clock | THY-17 |
| T-21 | Architecture Decision Records | THY-18 |
| T-22 | Single-Writer Principle | THY-19 |
| T-23 | Feature Branch Workflow | THY-20 |
| T-24 | Kanban & giới hạn WIP | THY-50 |
| T-25 | Little's Law | không có |
| T-26 | INVEST | THY-21 |
| T-27 | Goodhart's Law & Specification Gaming | THY-22 |
| T-28 | Thiên lệch LLM-as-a-Judge | THY-23 |
| T-29 | Design by Contract | THY-24 |
| T-30 | Mutation Testing | không có |
| T-31 | Shift-left Testing | không có |
| T-32 | Definition of Done / Ready | THY-25 |
| T-33 | Retrieval-Augmented Generation | THY-47 |
| T-34 | Requirements Traceability Matrix | không có |
| T-35 | Analytic Rubric | không có |
| T-36 | Thang Bloom | không có |
| T-37 | Semantic Versioning | THY-26 |
| T-38 | Rolling Wave Planning | THY-27 |
| T-39 | WBS & quy tắc 100% | không có |
| T-40 | Stage-Gate | THY-28 |
| T-41 | Timeboxing | không có |
| T-42 | Single-loop & Double-loop Learning | THY-29 |
| T-43 | Jidoka / Andon | không có mã riêng (dừng khi lỗi lặp lại dẫn THY-54) |
| T-44 | After Action Review / Retrospective | không có |
| T-45 | 5 Whys | không có |
| T-46 | Pre-mortem | THY-27 (gộp) |
| T-47 | Cognitive Load Theory | không có |
| T-48 | Atomic Notes / Zettelkasten | THY-30 |
| T-49 | Tóm tắt phân cấp đệ quy | THY-31 |
| T-50 | Plain Language | THY-32 |
| T-51 | BLUF | THY-32 (gộp) |
| T-52 | Ma trận RACI | THY-33 |
| T-53 | Dự báo burn-down | không có |
| T-54 | Detective Controls | THY-34 |
| T-55 | Complete Mediation | THY-35 |
| T-56 | Reference Monitor | THY-49 |
| T-57 | Kiểm thử chấp nhận | không có (bài kiểm tra người mới vẫn giữ ở PASS gate câu 8) |
| T-58 | Management by Exception | THY-36 |
| T-59 | Audit Sampling | không có |
| T-60 | Goal–Question–Metric | THY-37 |

**Lý thuyết chỉ có ở V1.0:** THY-38 Power of Plain Text · THY-39 Cool URIs don't change · THY-40 Inverted Index · THY-41 Schema Evolution · THY-42 Parse, don't validate · THY-43 Repository pattern · THY-44 Open–Closed Principle · THY-45 Microkernel architecture · THY-46 Indirect Prompt Injection / OWASP LLM01 · THY-48 Unix philosophy · THY-51 Clean Code · THY-52 Distributed Tracing · THY-53 Trunk-Based Development · THY-54 Circuit Breaker.

## 13. Ví dụ đổi một câu

| Viết theo V5.0 | Viết theo V1.0 |
|---|---|
| "TH1 làm phiếu V07 đợt D02, lần L2, nộp cờ VUONG có bao_DP: co" | "W1 runs TK-0007 in CYC-02, run R2, files a BLOCKED run with escalate: yes" |
| "ĐP lập kế hoạch đợt D03" | "LEAD creates the CYC-03 tasks from PLAN.md; OWNER merges, then says: Start CYC-03" |
| "ĐP ghi Q-09 thay Q-03, chuyển Q-03 vào het_hieu_luc/" | "LEAD writes DEC-0009 superseding DEC-0003, moves DEC-0003 to superseded/" |
| "CD merge CONG/D02_DAT.md" | "OWNER merges gates/CYC-02_PASS.md" |
| "Phiếu trỏ N-02#COT_VA_FONT trong doc_them" | "Task points to SRC-0002#COT_VA_FONT in read_also" |
| "R-04 mức CAO, hạn 2026-11-05, đang mở" | "RSK-0004 \| OPEN \| level: HIGH \| due: 2026-11-05" |
