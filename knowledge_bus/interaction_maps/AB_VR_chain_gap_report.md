# AB/VR Interaction Chain Gap Report (KB-S30d Stage 1)

Scope: Stage 1 gap reporting only.  
Constraints honored: no map edits, no backend logic edits, no test edits.

Inputs:
- `backend/tests/fixtures/panels/ab_full_panel_with_ranges.json`
- `backend/tests/fixtures/panels/vr_full_panel_with_ranges.json`
- `knowledge_bus/interaction_maps/interaction_map_v1.yaml` (revision `1.1.0`)

Method (deterministic):
1. Run golden panel for AB and VR fixtures.
2. Read `signal_results`, `interaction_graph`, `interaction_chains`, `interaction_summary`.
3. Keep fired non-optimal signals only (`suboptimal`, `at_risk`).
4. For each fired signal:
   - check node presence in map `nodes`
   - count map adjacency as number of map `edges` where signal appears in `from_signal` or `to_signal`

---

## Panel: AB (`ab_full_panel_with_ranges.json`)

### A) Fired signal set (non-optimal focus)

| signal_id | system | signal_state | confidence |
|---|---|---|---:|
| `signal_homocysteine_elevation_context` | vascular | at_risk | 0.95 |
| `signal_homocysteine_high` | vascular | suboptimal | 0.90 |
| `signal_mcv_high` | other | suboptimal | 0.90 |
| `signal_systemic_inflammation` | inflammatory | suboptimal | 0.30 |

### B) Current interaction_graph coverage

Observed runtime interaction outputs:
- `interaction_graph.nodes`: `signal_homocysteine_elevation_context`, `signal_homocysteine_high`, `signal_mcv_high`
- `interaction_graph.edges`: none
- `interaction_chains`: empty
- `interaction_summary`: empty

Per-fired-signal map coverage:

| signal_id | present in map nodes | map adjacency count |
|---|---|---:|
| `signal_homocysteine_elevation_context` | yes | 1 |
| `signal_homocysteine_high` | yes | 1 |
| `signal_mcv_high` | yes | 2 |
| `signal_systemic_inflammation` | no | 0 |

### C) Why chains are empty or sparse

- All fired mapped nodes are isolated with respect to each other in the current fired set; there is no edge where both endpoints are fired in AB.
- `signal_homocysteine_high` and `signal_homocysteine_elevation_context` each require `signal_crp_high` as the configured upstream connector, but `signal_crp_high` is not firing.
- `signal_mcv_high` has configured connectors (`signal_hemoglobin_low`, `signal_ferritin_low`), but neither is firing.
- `signal_systemic_inflammation` is not a declared interaction-map node, so it cannot participate in map-based chains.

### D) Minimal edge candidates (HYPOTHESES ONLY — not implemented)

Up to five candidates to close observed AB gaps:

1. `from_signal`: `signal_systemic_inflammation`  
   `to_signal`: `signal_homocysteine_high`  
   `proposed_relationship_type`: `driver`  
   `proposed_evidence_strength`: `exploratory`  
   `justification`: Both signals fire in AB and current map connectivity depends on non-firing `signal_crp_high`.

2. `from_signal`: `signal_systemic_inflammation`  
   `to_signal`: `signal_homocysteine_elevation_context`  
   `proposed_relationship_type`: `co_occurrence`  
   `proposed_evidence_strength`: `exploratory`  
   `justification`: AB shows concurrent inflammatory-context and vascular-context signals with no direct map bridge.

3. `from_signal`: `signal_homocysteine_elevation_context`  
   `to_signal`: `signal_homocysteine_high`  
   `proposed_relationship_type`: `co_occurrence`  
   `proposed_evidence_strength`: `exploratory`  
   `justification`: Both vascular signals fire together in AB but have no direct linkage unless `signal_crp_high` fires.

4. `from_signal`: `signal_systemic_inflammation`  
   `to_signal`: `signal_mcv_high`  
   `proposed_relationship_type`: `co_occurrence`  
   `proposed_evidence_strength`: `exploratory`  
   `justification`: AB has simultaneous inflammation-context and hematologic morphology-context signals without a chain path.

5. `from_signal`: `signal_mcv_high`  
   `to_signal`: `signal_homocysteine_high`  
   `proposed_relationship_type`: `co_occurrence`  
   `proposed_evidence_strength`: `exploratory`  
   `justification`: This would create a minimal AB path between currently disconnected fired nodes for synthesis continuity.

---

## Panel: VR (`vr_full_panel_with_ranges.json`)

### A) Fired signal set (non-optimal focus)

| signal_id | system | signal_state | confidence |
|---|---|---|---:|
| `signal_homocysteine_elevation_context` | vascular | suboptimal | 0.90 |
| `signal_homocysteine_high` | vascular | suboptimal | 0.90 |
| `signal_systemic_inflammation` | inflammatory | suboptimal | 0.30 |
| `signal_vitamin_d_low` | other | suboptimal | 0.90 |

### B) Current interaction_graph coverage

Observed runtime interaction outputs:
- `interaction_graph.nodes`: `signal_homocysteine_elevation_context`, `signal_homocysteine_high`
- `interaction_graph.edges`: none
- `interaction_chains`: empty
- `interaction_summary`: empty

Per-fired-signal map coverage:

| signal_id | present in map nodes | map adjacency count |
|---|---|---:|
| `signal_homocysteine_elevation_context` | yes | 1 |
| `signal_homocysteine_high` | yes | 1 |
| `signal_systemic_inflammation` | no | 0 |
| `signal_vitamin_d_low` | no | 0 |

### C) Why chains are empty or sparse

- VR fired mapped nodes are limited to the two vascular homocysteine signals; there is no direct edge between them in the map.
- Both homocysteine signals currently depend on `signal_crp_high` as connector, and `signal_crp_high` is not firing.
- `signal_systemic_inflammation` and `signal_vitamin_d_low` are not map nodes, so they cannot be included in runtime chain enumeration.
- Result: zero map-valid fired-edge connections, therefore empty chains and summary.

### D) Minimal edge candidates (HYPOTHESES ONLY — not implemented)

Up to five candidates to close observed VR gaps:

1. `from_signal`: `signal_systemic_inflammation`  
   `to_signal`: `signal_homocysteine_high`  
   `proposed_relationship_type`: `driver`  
   `proposed_evidence_strength`: `exploratory`  
   `justification`: VR shows concurrent inflammation-context and vascular elevation with missing `signal_crp_high` connector.

2. `from_signal`: `signal_systemic_inflammation`  
   `to_signal`: `signal_homocysteine_elevation_context`  
   `proposed_relationship_type`: `co_occurrence`  
   `proposed_evidence_strength`: `exploratory`  
   `justification`: This would bridge observed fired inflammation-context signal to the homocysteine context signal.

3. `from_signal`: `signal_homocysteine_elevation_context`  
   `to_signal`: `signal_homocysteine_high`  
   `proposed_relationship_type`: `co_occurrence`  
   `proposed_evidence_strength`: `exploratory`  
   `justification`: Both homocysteine signals fire in VR yet remain disconnected under current map adjacency.

4. `from_signal`: `signal_vitamin_d_low`  
   `to_signal`: `signal_systemic_inflammation`  
   `proposed_relationship_type`: `co_occurrence`  
   `proposed_evidence_strength`: `exploratory`  
   `justification`: Both are fired in VR and currently excluded from chain logic due to absent map nodes/edges.

5. `from_signal`: `signal_vitamin_d_low`  
   `to_signal`: `signal_homocysteine_elevation_context`  
   `proposed_relationship_type`: `co_occurrence`  
   `proposed_evidence_strength`: `exploratory`  
   `justification`: This offers a minimal bridge from VR nutritional-context signal to existing vascular-context chain nodes.
