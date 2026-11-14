---
schema: 1
id: MODEL_MATRIX
updated: 2026-11-14
status: APPROVED
tier1_candidate_families: ["Claude Opus", "GPT-Series mạnh", "Gemini Pro"]
tier1: []
tier1_approved_by: "DEC-0016"
tier2: ["claude-fable-5-2", "claude-opus-4-6-thinking", "claude-sonnet-4-6", "claude-sonnet-5-5", "gemini-3.8-flash-n", "gpt-5.6-luna", "gpt-6.1-sol", "gpt-6.1-terra", "grok-4.6", "grok-4.7"]
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
    fallback: ["claude-opus-4-6-thinking", "claude-sonnet-5-5"]
    evidence: ["DSC-20261112-012x", "DEC-0017#CONTEXT"]
  - role: REVIEWER
    min_tier: T2
    order: ["gemini-3.8-flash-n", "claude-opus-4-6-thinking", "claude-sonnet-5-5"]
    fallback: []
    evidence: ["RVW-CYC-02", "RVW-CYC-01", "DEC-0017#CONTEXT"]
  - role: WORKER
    min_tier: T3
    order: ["gpt-5.6-luna", "gpt-6.1-sol", "claude-sonnet-4-6", "grok-4.7", "grok-4.6"]
    fallback: []
    evidence: ["02_work/runs/TK-0003_R1_DONE.md", "02_work/runs/TK-0002_R1_DONE.md", "DEC-0017#CONTEXT"]
---
<!-- ANCHOR: ASSIGNMENTS -->
## Assignments
- CYC-02 | REVIEWER | requested: nhóm Gemini (DEC-0012) | actual: gemini-3.8-flash-n | record: RVW-CYC-02 | match: yes
- CYC-02 | WORKER | requested: nhóm Codex (DEC-0012) | actual: gpt-6.1-terra | record: 02_work/runs/TK-0005_R1_DONE.md | match: yes
- CYC-02 | WORKER | requested: nhóm Codex (DEC-0012) | actual: gpt-5.6-luna | record: 02_work/runs/TK-0003_R1_DONE.md | match: yes
<!-- END: ASSIGNMENTS -->
