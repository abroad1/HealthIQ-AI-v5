# LC-S18A — Package Estate Inventory Delta Report

**Work ID:** LC-S18A  
**Generated:** 2026-05-24

## Summary

| Metric | Before (KB-S49, 2026-03-28) | After (LC-S18A refresh) |
|--------|------------------------------|-------------------------|
| `pkg_*` directories on disk | 186 (incl. `pkg_example`) | 186 |
| Inventory entries | 73 | 185 |
| Disk-not-in-inventory orphans | 112 | 0 |
| Inventory-not-on-disk orphans | 0 | 0 |
| Review queue (`requires_review: true`) | 0 | 112 |
| Lipid-relevant unregistered orphans | 17 | 0 (registered, review pending) |

## Orphan batches added (Option C — partial controlled refresh)

| Batch prefix | Count | Governed tier |
|--------------|-------|---------------|
| `pkg_kb52c_` | 67 | `post_kb_s49_unreviewed_batch` |
| `pkg_kb58_` | 22 | `post_kb_s49_unreviewed_batch` |
| `pkg_kb60_` | 7 | `post_kb_s49_unreviewed_batch` |
| `pkg_kb56_` | 5 | `post_kb_s49_unreviewed_batch` |
| `pkg_kb52d_` | 4 | `post_kb_s49_unreviewed_batch` |
| `pkg_kb59_` | 4 | `post_kb_s49_unreviewed_batch` |
| `pkg_kb61_` | 3 | `post_kb_s49_unreviewed_batch` |

All 112 packages have complete standard three-file shape. None were promoted to runtime-valid.

## KB-WAVE-1 lipid-relevant packages now in inventory (review queue)

17 packages flagged `kb_wave_1_lipid_relevant: true`, including:

- `pkg_kb52c_apob_high_atherogenic_particle_excess`
- `pkg_kb52c_apob_apoa1_ratio_high_atherogenic_particle_imbalance`
- `pkg_kb52c_ldl_high_atherogenic_ldl_burden`
- `pkg_kb52d_non_hdl_cholesterol_high_atherogenic_lipoprotein_burden`
- Existing governed packages: `pkg_lipid_transport`, `pkg_s24_ldl_high_dyslipidaemia`

## Out of scope

- `knowledge_bus/packages/KBP-0001/` — legacy naming; invisible to `list_package_dirs()` (`pkg_` prefix filter). Documented residual; not counted in orphan totals.

## Review queue policy

Registered packages remain `runtime_loaded: false` and `validator_ready_for_implementation: false` until KB-WAVE validation promotes them. No auto-loading was introduced.
