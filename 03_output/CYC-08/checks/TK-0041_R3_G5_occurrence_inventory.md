# TK-0041 R3 G5 occurrence inventory

- Base: `72159cf645bc75ccd84cf377e46a3990d528a41f`; head: `c65d0b6ead5dff11f072faa49ecc760b08ed73dd`.
- Scanner and rules: base `tools/scan.py` and `tools/scan_rules.json`; ruleset `scan-core-1`.
- Each base and head has 16 occurrences: HARNESS 2, LEAD 3, README 11. Details, positions, contexts, levels and SHA-256 values: `TK-0041_R3_G5_occurrence_inventory.json`.
- LEAD hits are outside section 9: line 42 `dangerous_automerge` and `impersonation_owner_approved`; line 76 `impersonation_owner_approved`.
- OWNER selected frozen C4. No remediation, verification loop, exact-head gate or regression was run.
