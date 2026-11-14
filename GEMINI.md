# Routing
- Phiên `RUN` ("Run TK-nnnn") → chỉ đọc `harness/rules/WORKER.md` và task được giao.
- Được giao kiểm định một chu kỳ → chỉ đọc `harness/rules/REVIEWER.md` và gói kiểm định.
- Phiên `ASK`, `CHANGE`, `DISCUSS` và mọi trường hợp còn lại → đọc `harness/rules/LEAD.md`.
- Mọi vai: được đọc `main`; không commit trên `main`, không đẩy thẳng, không merge, không bật auto-merge, không đụng thẻ git (`harness/MAIN_PROTECTION.md`).
- LEAD chia task chạy song song: `write_scope` của các task cùng batch không giao nhau (zero-overlap) và không phụ thuộc nhau; chia batch theo neo `CYC_nn_BATCHES` của `harness/templates/plan.md`.
