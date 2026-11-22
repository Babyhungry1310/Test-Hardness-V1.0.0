---
schema: 1
id: SRC-0005
date: 2026-11-22
title: "Phương án chọn model linh hoạt cho Kaizen"
decided_by: OWNER
related: [SRC-0002]
keywords: [kaizen, model-routing]
---
<!-- ANCHOR: CONTEXT -->
## Context
Nguồn: OWNER cung cấp/duyệt trong phiên lập kế hoạch Kaizen, 2026-11-21–22; thư mục làm việc ngoài repo ghi là `<SHARED>`. scan: ALLOW (`tools/scan.py`, scan-core-1).

# PHƯƠNG ÁN CHỌN MODEL LINH HOẠT — Đợt Kaizen 1

- Lập: Claude (Lead Brainstorm) theo yêu cầu OWNER, 2026-11-21.
- Mục tiêu: (1) OWNER đổi model bất kỳ lúc nào mà không phải sửa kế hoạch; (2) loop WORKER không dừng bất ngờ vì một tuyến lỗi/hết hạn mức; (3) vẫn giữ luật repo (MODEL_POLICY: chỉ dùng model đủ điều kiện; SAME_MODEL; ghi model thực tế).

## 1. Ba lớp quyết định (lớp trên thắng lớp dưới)
1. **Lệnh OWNER** cho lượt giao cụ thể (trong chat hoặc một dòng `OWNER-OVERRIDE` trong `SO_GIAO_VIEC.md`). Không cần sửa kế hoạch.
2. **Chuỗi dự phòng theo vai** (mục 2) — LEAD tự áp khi giao.
3. **Model đề xuất** ghi trong bảng task — chỉ là gợi ý mặc định.

## 2. Nhóm model đủ điều kiện (POOL) và chuỗi dự phòng
Chỉ model trong POOL mới được giao. Một model vào POOL khi: có mục trong `04_control/MODEL_CATALOG.md` + dòng ROUTE_CHECKS `agent-tools` OK gần nhất cho đúng tuyến.

| Vai / loại việc | Chuỗi ưu tiên (đi tiếp khi mục trước lỗi/hết hạn mức/OWNER loại) |
|---|---|
| WORKER code (T2) | xai/grok-4.5 → cx/gpt-6.1-terra → xai/grok-4.7 → cx/gpt-6.1-sol → ag/gemini-3.8-flash |
| WORKER không code (T0–T1: sổ, văn bản, schema mô tả) | ag/gemini-3.8-flash → cx/gpt-6.1-terra → xai/grok-4.5 → cx/gpt-6-luna |
| REVIEWER | ag/gemini-3.8-flash → cx/gpt-6.1-terra → xai/grok-4.5 → cx/gpt-6.1-sol — **bỏ qua mọi mục cùng họ với model thực tế của WORKER** |
| LEAD | xai/grok-4.5 (2) : cx/gpt-6.1-terra hoặc cx/gpt-6-luna (1) — theo sổ, không gắn cứng |

- Họ model: grok-* (xAI) · gpt-* (OpenAI) · gemini-* (Google). REVIEWER phải khác họ với WORKER.
- Tỉ lệ (LEAD 2:1, WORKER Gemini ~50%) là **mục tiêu mềm** tính trên sổ; không bao giờ là lý do dừng loop.

## 3. Đủ điều kiện TRƯỚC, để đổi model không phải dừng
- L0.1 (LEAD, trước lần giao WORKER đầu): probe `agent-tools` cho **toàn bộ chuỗi** ở mục 2, không chỉ model đề xuất. Mục nào đạt → vào POOL (ghi catalog/ROUTE_CHECKS trong TK-0040).
- Probe lại một tuyến khi: lỗi 2 lần liên tiếp, hoặc > 7 ngày chưa kiểm, hoặc provider đổi phiên bản.

## 4. Khi tuyến lỗi giữa loop (không dừng bất ngờ)
1. Lỗi do tuyến/model (403, 429, 5xx, timeout, "model unavailable"): chờ theo `reset after` nếu ≤ 5 phút; nếu không, **chuyển ngay sang mục kế trong chuỗi** đã ở POOL.
2. Đổi model **không cộng thêm loop** và không reset loop (giữ luật hiện hành); ghi dòng sổ: `match: no`, lý do, model thực tế mới.
3. Nếu model mới làm REVIEWER trùng họ với WORKER → bỏ qua, lấy mục kế.
4. **Chỉ dừng (BLOCKED)** khi cả chuỗi của vai đó không còn mục nào trong POOL → báo OWNER kèm danh sách đã thử.
5. Lỗi do nội dung task (test FAIL, sai scope) **không** phải lý do đổi model.

## 5. Ghi nhận
Mỗi lượt giao/đổi: một dòng `SO_GIAO_VIEC.md` — thời điểm | TK | vai | đề xuất | thực nhận (model thực tế từ nhật ký phiên) | lý do đổi (OWNER / fallback / quota) | người giao.
