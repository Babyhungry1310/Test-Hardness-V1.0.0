---
schema: 1
id: MODEL_CATALOG
updated: 2026-11-14
models:
  - code: "claude-fable-5-2"
    provider: unverified
    provider_source: none
    group: unverified
    group_source: none
    aliases: []
    recommended_roles: [PLANNING]
    capability_source: none
    price_source: none
    availability: confirmed
    availability_evidence: DSC-20261112-012x
    updated: 2026-11-14
  - code: "claude-opus-4-6-thinking"
    provider: unverified
    provider_source: none
    group: unverified
    group_source: none
    aliases: ["ag/claude-opus-4-6-thinking"]
    recommended_roles: []
    capability_source: none
    price_source: none
    availability: unconfirmed
    availability_evidence: none
    updated: 2026-11-14
  - code: "claude-sonnet-4-6"
    provider: unverified
    provider_source: none
    group: unverified
    group_source: none
    aliases: ["ag/claude-sonnet-4-6"]
    recommended_roles: []
    capability_source: none
    price_source: none
    availability: unconfirmed
    availability_evidence: none
    updated: 2026-11-14
  - code: "claude-sonnet-5-5"
    provider: unverified
    provider_source: none
    group: claude
    group_source: "DEC-0008#RATIONALE"
    aliases: ["ag/claude-sonnet-5-5"]
    recommended_roles: [REVIEWER]
    capability_source: none
    price_source: none
    availability: confirmed
    availability_evidence: RVW-CYC-01
    updated: 2026-11-14
  - code: "gemini-3.8-flash-k"
    provider: unverified
    provider_source: none
    group: gemini
    group_source: "DEC-0005#CONTEXT"
    aliases: []
    recommended_roles: []
    capability_source: none
    price_source: none
    availability: confirmed
    availability_evidence: 02_work/runs/TK-0001_R1_BLOCKED.md
    updated: 2026-11-14
  - code: "gemini-3.8-flash-n"
    provider: unverified
    provider_source: none
    group: gemini
    group_source: "DEC-0012#CONTEXT"
    aliases: ["ag/gemini-3.8-flash", "ag/gemini-3.8-flash-high"]
    recommended_roles: [REVIEWER]
    capability_source: none
    price_source: none
    availability: confirmed
    availability_evidence: RVW-CYC-02
    updated: 2026-11-14
  - code: "gpt-5.6-luna"
    provider: unverified
    provider_source: none
    group: codex
    group_source: "DEC-0012#CONTEXT"
    aliases: ["cx/gpt-5.6-luna", "gpt-5.6-luna[1m]"]
    recommended_roles: [WORKER]
    capability_source: none
    price_source: none
    availability: confirmed
    availability_evidence: 02_work/runs/TK-0003_R1_DONE.md
    updated: 2026-11-14
  - code: "gpt-5.6-sol"
    provider: unverified
    provider_source: none
    group: unverified
    group_source: none
    aliases: ["cx/gpt-5.6-sol"]
    recommended_roles: []
    capability_source: none
    price_source: none
    availability: unconfirmed
    availability_evidence: none
    updated: 2026-11-14
  - code: "gpt-5.6-terra"
    provider: unverified
    provider_source: none
    group: unverified
    group_source: none
    aliases: ["cx/gpt-5.6-terra"]
    recommended_roles: []
    capability_source: none
    price_source: none
    availability: unconfirmed
    availability_evidence: none
    updated: 2026-11-14
  - code: "gpt-6.1-sol"
    provider: unverified
    provider_source: none
    group: codex
    group_source: "DEC-0014#CONTEXT"
    aliases: ["cx/gpt-6.1-sol"]
    recommended_roles: [WORKER]
    capability_source: none
    price_source: none
    availability: confirmed
    availability_evidence: 02_work/runs/TK-0002_R1_DONE.md
    updated: 2026-11-14
  - code: "gpt-6.1-terra"
    provider: unverified
    provider_source: none
    group: unverified
    group_source: none
    aliases: ["cx/gpt-6.1-terra"]
    recommended_roles: [WORKER]
    capability_source: none
    price_source: none
    availability: confirmed
    availability_evidence: 02_work/runs/TK-0005_R1_DONE.md
    updated: 2026-11-14
  - code: "grok-4.3"
    provider: unverified
    provider_source: none
    group: unverified
    group_source: none
    aliases: ["xai/grok-4"]
    recommended_roles: []
    capability_source: none
    price_source: none
    availability: unconfirmed
    availability_evidence: none
    updated: 2026-11-14
  - code: "grok-4.6"
    provider: unverified
    provider_source: none
    group: unverified
    group_source: none
    aliases: ["xai/grok-4.6"]
    recommended_roles: []
    capability_source: none
    price_source: none
    availability: unconfirmed
    availability_evidence: none
    updated: 2026-11-14
  - code: "grok-4.7"
    provider: unverified
    provider_source: none
    group: unverified
    group_source: none
    aliases: ["xai/grok-4.7"]
    recommended_roles: []
    capability_source: none
    price_source: none
    availability: unconfirmed
    availability_evidence: none
    updated: 2026-11-14
  - code: "grok-build-0.1"
    provider: unverified
    provider_source: none
    group: unverified
    group_source: none
    aliases: ["xai/grok-code-fast-1"]
    recommended_roles: []
    capability_source: none
    price_source: none
    availability: unconfirmed
    availability_evidence: none
    updated: 2026-11-14
---
<!-- ANCHOR: ROUTE_CHECKS -->
## Route checks (newest first)
- 2026-11-14T06:32Z | route: Hardeness | actual: gpt-5.6-luna[1m] | kind: chat | result: OK | source: POST /v1/chat/completions tại http://localhost:20128, gọi từ trình duyệt của ứng dụng trên máy OWNER | note: combo; không dùng để giao việc
- 2026-11-14T06:32Z | route: xai/grok-4 | actual: grok-4.3 | kind: chat | result: OK | source: POST /v1/chat/completions tại http://localhost:20128, gọi từ trình duyệt của ứng dụng trên máy OWNER | note: tên tuyến khác model trả về
- 2026-11-14T06:32Z | route: xai/grok-4.6 | actual: grok-4.6 | kind: chat | result: OK | source: POST /v1/chat/completions tại http://localhost:20128, gọi từ trình duyệt của ứng dụng trên máy OWNER | note: none
- 2026-11-14T06:32Z | route: ag/gemini-3.8-flash-high | actual: gemini-3.8-flash-n | kind: chat | result: OK | source: POST /v1/chat/completions tại http://localhost:20128, gọi từ trình duyệt của ứng dụng trên máy OWNER | note: tên tuyến khác model trả về
- 2026-11-14T06:32Z | route: cx/gpt-5.6-sol | actual: gpt-5.6-sol | kind: chat | result: OK | source: POST /v1/chat/completions tại http://localhost:20128, gọi từ trình duyệt của ứng dụng trên máy OWNER | note: none
- 2026-11-14T06:32Z | route: cx/gpt-5.6-terra | actual: gpt-5.6-terra | kind: chat | result: OK | source: POST /v1/chat/completions tại http://localhost:20128, gọi từ trình duyệt của ứng dụng trên máy OWNER | note: none
- 2026-11-14T06:32Z | route: ag/claude-opus-4-6-thinking | actual: claude-opus-4-6-thinking | kind: chat | result: OK | source: POST /v1/chat/completions tại http://localhost:20128, gọi từ trình duyệt của ứng dụng trên máy OWNER | note: none
- 2026-11-14T06:32Z | route: ag/claude-sonnet-4-6 | actual: claude-sonnet-4-6 | kind: chat | result: OK | source: POST /v1/chat/completions tại http://localhost:20128, gọi từ trình duyệt của ứng dụng trên máy OWNER | note: none
- 2026-11-14T06:32Z | route: ag/gemini-3.1-pro-high | actual: none | kind: chat | result: FAIL | source: POST /v1/chat/completions tại http://localhost:20128, gọi từ trình duyệt của ứng dụng trên máy OWNER | note: HTTP 503; phía trên trả 404
- 2026-11-14T06:32Z | route: cu/claude-4.6-opus-max | actual: none | kind: chat | result: FAIL | source: POST /v1/chat/completions tại http://localhost:20128, gọi từ trình duyệt của ứng dụng trên máy OWNER | note: HTTP 400; lượt trả lời rỗng
- 2026-11-14T06:32Z | route: cu/claude-4.5-sonnet | actual: none | kind: chat | result: FAIL | source: POST /v1/chat/completions tại http://localhost:20128, gọi từ trình duyệt của ứng dụng trên máy OWNER | note: HTTP 400; lượt trả lời rỗng
- 2026-11-14T06:32Z | route: cu/claude-4.5-opus | actual: none | kind: chat | result: FAIL | source: POST /v1/chat/completions tại http://localhost:20128, gọi từ trình duyệt của ứng dụng trên máy OWNER | note: HTTP 400; lượt trả lời rỗng
- 2026-11-14T06:32Z | route: ag/claude-sonnet-5-5-high | actual: none | kind: chat | result: FAIL | source: POST /v1/chat/completions tại http://localhost:20128, gọi từ trình duyệt của ứng dụng trên máy OWNER | note: HTTP 503; phía trên trả 404
- 2026-11-14T06:32Z | route: ag/claude-opus-5-5-high | actual: none | kind: chat | result: FAIL | source: POST /v1/chat/completions tại http://localhost:20128, gọi từ trình duyệt của ứng dụng trên máy OWNER | note: HTTP 503; phía trên trả 404
- 2026-11-14T06:30Z | route: ag/gemini-4-carbon | actual: none | kind: chat | result: FAIL | source: POST /v1/chat/completions tại http://localhost:20128, gọi từ trình duyệt của ứng dụng trên máy OWNER | note: HTTP 503; phía trên trả 404
- 2026-11-14T06:30Z | route: ag/gemini-3.8-flash | actual: gemini-3.8-flash-n | kind: chat | result: OK | source: POST /v1/chat/completions tại http://localhost:20128, gọi từ trình duyệt của ứng dụng trên máy OWNER | note: tên tuyến khác model trả về
- 2026-11-14T06:30Z | route: cx/gpt-6.1-terra | actual: gpt-6.1-terra | kind: chat | result: OK | source: POST /v1/chat/completions tại http://localhost:20128, gọi từ trình duyệt của ứng dụng trên máy OWNER | note: none
- 2026-11-14T06:30Z | route: cx/gpt-6.1-sol | actual: gpt-6.1-sol | kind: chat | result: OK | source: POST /v1/chat/completions tại http://localhost:20128, gọi từ trình duyệt của ứng dụng trên máy OWNER | note: none
- 2026-11-14T06:30Z | route: cx/gpt-5.6-luna | actual: gpt-5.6-luna | kind: chat | result: OK | source: POST /v1/chat/completions tại http://localhost:20128, gọi từ trình duyệt của ứng dụng trên máy OWNER | note: none
- 2026-11-14T06:30Z | route: xai/grok-code-fast-1 | actual: grok-build-0.1 | kind: chat | result: OK | source: POST /v1/chat/completions tại http://localhost:20128, gọi từ trình duyệt của ứng dụng trên máy OWNER | note: tên tuyến khác model trả về
- 2026-11-14T06:30Z | route: xai/grok-4.7 | actual: grok-4.7 | kind: chat | result: OK | source: POST /v1/chat/completions tại http://localhost:20128, gọi từ trình duyệt của ứng dụng trên máy OWNER | note: none
- 2026-11-14T06:30Z | route: ag/claude-sonnet-5-5 | actual: none | kind: chat | result: FAIL | source: POST /v1/chat/completions tại http://localhost:20128, gọi từ trình duyệt của ứng dụng trên máy OWNER | note: HTTP 503; phía trên trả 404
- 2026-11-14T06:30Z | route: ag/claude-opus-5-5 | actual: none | kind: chat | result: FAIL | source: POST /v1/chat/completions tại http://localhost:20128, gọi từ trình duyệt của ứng dụng trên máy OWNER | note: HTTP 503; phía trên trả 404
<!-- END: ROUTE_CHECKS -->
