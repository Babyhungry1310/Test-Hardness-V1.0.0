---
schema: 1
id: MODEL_MATRIX
updated: 2026-11-18
status: PROPOSED
tier1_candidate_families: ["Claude Opus", "GPT-Series mạnh", "Gemini Pro"]
tier1: []
tier1_approved_by: ""
tier2: ["claude-fable-5-2", "claude-sonnet-5-5", "gemini-3.8-flash-n", "gpt-5.6-luna", "gpt-6.1-sol", "gpt-6.1-terra"]
tier3: []
roles:
  - role: BRAINSTORM
    min_tier: T1
    order: []
    fallback: []
    evidence: []
  - role: PLANNING
    min_tier: T2
    order: ["claude-fable-5-2"]
    fallback: ["claude-sonnet-5-5"]
    evidence: ["DSC-20261112-012x"]
  - role: REVIEWER
    min_tier: T2
    order: ["gemini-3.8-flash-n", "claude-sonnet-5-5"]
    fallback: []
    evidence: ["RVW-CYC-02", "RVW-CYC-01"]
  - role: WORKER
    min_tier: T3
    order: ["gpt-5.6-luna", "gpt-6.1-terra", "gpt-6.1-sol"]
    fallback: []
    evidence: ["02_work/runs/TK-0003_R1_DONE.md", "02_work/runs/TK-0005_R1_DONE.md", "02_work/runs/TK-0002_R1_DONE.md"]
---
<!-- ANCHOR: ASSIGNMENTS -->
## Assignments
- CYC-03 | WORKER | requested: gpt-6.1-sol | actual: gpt-6.1-sol | record: TK-0018 R1 | match: yes | route: cx/gpt-6.1-sol | basis: OWNER selects GPT; confirmed tools; B2 zero-overlap; quota unverified
- CYC-03 | WORKER | requested: gpt-6.1-sol | actual: gpt-6.1-sol | record: TK-0027 R1 | match: yes | route: cx/gpt-6.1-sol | basis: OWNER selects GPT; confirmed tools; B2 zero-overlap; quota unverified
- CYC-03 | WORKER | requested: grok-4.7 | actual: pending | record: TK-0030 R1; DEC-0026 | match: pending | route: xai/grok-4.7 | basis: OWNER requests Grok; prior agent-tools OK; phase-zero pending; quota unverified
- CYC-03 | REVIEWER | requested: gemini-3.8-flash-n | actual: pending | record: TK-0030 delta review; not dispatched | match: pending | route: ag/gemini-3.8-flash | basis: OWNER requests Gemini; new Grok delta only; eligibility recheck before assignment; quota unverified
- CYC-02 | REVIEWER | requested: nhóm Gemini (DEC-0012) | actual: gemini-3.8-flash-n | record: RVW-CYC-02 | match: yes
- CYC-02 | WORKER | requested: nhóm Codex (DEC-0012) | actual: gpt-6.1-terra | record: 02_work/runs/TK-0005_R1_DONE.md | match: yes
- CYC-02 | WORKER | requested: nhóm Codex (DEC-0012) | actual: gpt-5.6-luna | record: 02_work/runs/TK-0003_R1_DONE.md | match: yes
<!-- END: ASSIGNMENTS -->
