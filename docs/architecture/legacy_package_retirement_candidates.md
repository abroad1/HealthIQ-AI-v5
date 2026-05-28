# Legacy Package Retirement Candidates

**Work package:** ARCH-RT-0  
**Generated:** 2026-05-28

## Classification legend

| Class | Meaning |
|-------|---------|
| `active_current` | Loaded by `SignalRegistry`; governed provenance; no duplicate collision loss |
| `legacy_retained_candidate` | Older context package; may overlap newer s24/kb52c; keep until parity |
| `deferred_for_regeneration` | Valid shape; awaiting governed recompile from investigation spec |
| `blocked_pending_spec_extraction` | Batch JSON source; frame/spec linkage not on manifest |
| `retire_candidate` | Superseded duplicate loser or example package |
| `unknown_requires_review` | Insufficient provenance |

## Estate-wide summary

| Class | Approx. count | Notes |
|-------|--------------:|-------|
| `active_current` | ~74 | Pre–LC-S18A inventory packages + s24 + kb45 + kb47 + legacy context (runtime loaded) |
| `deferred_for_regeneration` | 112 | LC-S18A review queue (`runtime_loaded: false`) |
| `legacy_retained_candidate` | 12 | Legacy context `pkg_*` (excl. `pkg_example`) |
| `retire_candidate` | 1 | `pkg_example` |
| `blocked_pending_spec_extraction` | 142 | Batch JSON `source_document` (frame `spec_id` in JSON only) |
| `unknown_requires_review` | 2 | Missing `source_document` |

## By generation

### `pkg_s24_*` (31) — `active_current`

Individual `inv_*.yaml` provenance. Often **lexicographic winner** in `signal_id` collisions. Retain until multi-frame registry replaces overwrite policy.

### `pkg_kb45_*` (10) — `active_current` / `deferred_for_regeneration`

Batch collection source. Classify per-package after spec extraction index exists.

### `pkg_kb47_*` (20) — `active_current`

Only cohort with PSI. Runtime uses `signal_library.yaml`, not PSI.

### `pkg_kb52c_*` (67) — `deferred_for_regeneration`

LC-S18A `post_kb_s49_unreviewed_batch`. Many are **collision losers** for shared `signal_id` (e.g. all ALT kb52c frames). **Do not retire** until multi-frame policy implemented — medical content may be authoritative frame.

### `pkg_kb58_*` (22), `pkg_kb60_*` (7), `pkg_kb56_*` (5), `pkg_kb52d_*` (4), `pkg_kb59_*` (4), `pkg_kb61_*` (3) — `deferred_for_regeneration`

Same LC-S18A queue; batch JSON provenance.

### Legacy context (13)

| Package | Classification | Notes |
|---------|----------------|-------|
| `pkg_hepatic_alt_context` | `legacy_retained_candidate` | Distinct `signal_hepatic_alt_context` |
| `pkg_homocysteine_elevation_context` | `legacy_retained_candidate` | WHY registry + hcy YAML |
| `pkg_lipid_transport` | `unknown_requires_review` | Missing `source_document` |
| `pkg_example` | `retire_candidate` | Excluded from registry load |
| Others (insulin, iron, thyroid, etc.) | `legacy_retained_candidate` | Architecture doc provenance |

### `KBP-0001`

| Classification | Notes |
|----------------|-------|
| `legacy_retained_candidate` | Not `pkg_*`; invisible to some inventory scripts; 7 signals |

## Packages lacking sufficient provenance

| Package | Issue |
|---------|-------|
| `pkg_lipid_transport` | No `source_document` |
| `pkg_example` | No `source_document`; example only |
| All batch JSON packages (142) | No manifest `source_spec_id`; frame identity inside JSON only |

## Retirement policy (decision)

**No package deletions in ARCH-RT-0.** Retirement requires:

1. ARCH-RT-2 multi-frame registry live.  
2. Parity proof per package.  
3. Compile manifest showing supersession.  
4. Human clinical sign-off for kb52c frames currently discarded.
