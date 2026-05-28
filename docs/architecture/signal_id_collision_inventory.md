# Signal ID Collision Inventory

**Work package:** ARCH-RT-0  
**Generated:** 2026-05-28

## Detection method

Read-only scan of every `knowledge_bus/packages/pkg_*/signal_library.yaml` (excluding `pkg_example`). Command summary:

```text
dup_families: 45
dup_package_rows: 96
total distinct signal_ids loaded: (registry hash over unique ids after overwrite)
```

## Current retained / discarded behaviour

**Authority:** `backend/core/analytics/signal_evaluator.py` (`SignalRegistry._load`, lines 54–60).

**Policy:** When the same `signal_id` appears in multiple package libraries, the definition from the **lexicographically later** `signal_library.yaml` path **overwrites** earlier definitions. No error, no merge, no multi-frame retention.

**Live runtime effect:** **YES** — only one definition per `signal_id` reaches `SignalEvaluator`.

## Collision taxonomy

| Category | Description | Count (families) |
|----------|-------------|-----------------:|
| Single-frame duplicate | Same medical frame, redundant packages (legacy vs s24 vs kb52c) | ~30 |
| Multi-frame medical case | Distinct `spec_id` / package suffix, **same** `signal_id` (Pass 3 pattern) | ~15 (incl. ALT, homocysteine) |
| Distinct signal_id, shared YAML | Not a `signal_id` collision | N/A (e.g. homocysteine context id) |

## ALT high — explicit row

| Field | Value |
|-------|-------|
| `signal_id` | `signal_alt_high` |
| Collision type | **Multi-frame medical case** (4 packages, 1 retained) |
| Packages (all paths under `knowledge_bus/packages/`) | |
| | `pkg_kb52c_alt_high_hepatocellular_injury_pattern` |
| | `pkg_kb52c_alt_high_metabolic_steatotic_liver_pattern` |
| | `pkg_kb52c_alt_high_muscle_source_or_exertional_pattern` |
| | `pkg_s24_alt_high_hepatocellular_injury` |
| **Retained at runtime (lexicographic winner)** | `pkg_s24_alt_high_hepatocellular_injury` |
| **Discarded at runtime** | All three `pkg_kb52c_alt_high_*` definitions |
| Affects live runtime | **YES** |
| Recommended handling | **Multi-frame support** + retire duplicate single-frame policy (see ADR-RT-002) |

**Related (not same `signal_id`):** `signal_hepatic_alt_context` in `pkg_hepatic_alt_context` — legacy context package; separate registry entry.

## Homocysteine — explicit rows

### `signal_homocysteine_high` (3 packages)

| Packages | Retained (lex winner) |
|----------|----------------------|
| `pkg_kb52c_homocysteine_high_b_vitamin_related_methylation_impairment` | |
| `pkg_kb52c_homocysteine_high_renal_clearance_reduction` | |
| `pkg_s24_homocysteine_high_metabolic` | **`pkg_s24_homocysteine_high_metabolic`** |

Collision type: **Multi-frame medical case** (2 kb52c frames + 1 s24). Recommended: **multi-frame support**.

### `signal_homocysteine_elevation_context` (1 package)

| Package | Notes |
|---------|-------|
| `pkg_homocysteine_elevation_context` | Distinct `signal_id`; shares `hcy_hypotheses_v1.yaml` with `signal_homocysteine_high` in root-cause registry |

## All duplicate `signal_id` families (45)

| `signal_id` | # pkgs | Recommended handling |
|-------------|-------:|------------------------|
| `signal_albumin_low` | 3 | Multi-frame support |
| `signal_alt_high` | 4 | Multi-frame support |
| `signal_alp_high` | 2 | Governed arbitration or multi-frame |
| `signal_alp_low` | 2 | Multi-frame support |
| `signal_apoa1_low` | 2 | Multi-frame support |
| `signal_apob_apoa1_ratio_high` | 2 | Multi-frame support |
| `signal_apob_high` | 2 | Multi-frame support |
| `signal_basophil_pct_high` | 2 | Multi-frame support |
| `signal_basophils_abs_high` | 2 | Multi-frame support |
| `signal_creatine_kinase_high` | 2 | Multi-frame support |
| `signal_creatinine_high` | 2 | Governed arbitration |
| `signal_egfr_low` | 2 | Multi-frame support |
| `signal_eosinophil_pct_high` | 2 | Multi-frame support |
| `signal_eosinophils_abs_high` | 2 | Multi-frame support |
| `signal_ferritin_low` | 2 | Governed arbitration |
| `signal_folate_low` | 2 | Governed arbitration |
| `signal_ggt_high` | 3 | Multi-frame support |
| `signal_globulin_high` | 2 | Multi-frame support |
| `signal_hba1c_high` | 2 | Governed arbitration |
| `signal_hba1c_pct_high` | 2 | Multi-frame support |
| `signal_hdl_low` | 2 | Multi-frame support |
| `signal_homocysteine_high` | 3 | Multi-frame support |
| `signal_ldl_high` | 2 | Multi-frame support |
| `signal_lipoprotein_a_high` | 2 | Multi-frame support |
| `signal_magnesium_high` | 2 | Multi-frame support |
| `signal_mch_low` | 2 | Multi-frame support |
| `signal_mcv_high` | 3 | Multi-frame support |
| `signal_monocytes_abs_high` | 2 | Multi-frame support |
| `signal_plt_high` | 2 | Multi-frame support |
| `signal_rbc_high` | 2 | Multi-frame support |
| `signal_rbc_low` | 2 | Multi-frame support |
| `signal_rdw_cv_high` | 2 | Multi-frame support |
| `signal_rdw_sd_high` | 2 | Multi-frame support |
| `signal_tgab_high` | 2 | Multi-frame support |
| `signal_total_cholesterol_high` | 2 | Multi-frame support |
| `signal_tpo_ab_high` | 2 | Multi-frame support |
| `signal_transferrin_low` | 2 | Multi-frame support |
| `signal_triglycerides_high` | 2 | Governed arbitration |
| `signal_tsh_high` | 2 | Governed arbitration |
| `signal_tsh_low` | 2 | Governed arbitration |
| `signal_urea_high` | 2 | Governed arbitration |
| `signal_urate_high` | 2 | Governed arbitration |
| `signal_vitamin_b12_low` | 2 | Governed arbitration |
| `signal_wbc_high` | 2 | Governed arbitration |

**Post–ARCH-RT-2 target:** Collisions must become **hard errors at compile time** or **explicit multi-frame registry entries** — not silent lexicographic overwrite.

## Uncertainty

- Per-package `spec_id` inside batch JSON was not denormalised into this table; frame identity is inferred from package directory suffix and PSI `investigation_spec_id` (kb47 only).
