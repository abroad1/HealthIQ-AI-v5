# Activation Compile Gap Report

**Work package:** ARCH-RT-0  
**Generated:** 2026-05-28

## Questions answered

### 1. Governed `investigation_spec → signal_library.yaml` compiler?

| Status | Detail |
|--------|--------|
| **Partial / sprint-specific** | No single governed CLI named in repo |
| Scripts found | `backend/scripts/generate_kb_s45d_batch1_packages.py` (batch packages + signal libraries) |
| | `knowledge_bus/tools/kb_s47_batch2_ingest.py` (kb47 full package + PSI) |
| Validators | `backend/scripts/validate_signal_library.py`, `validate_knowledge_package.py` |

**Gap:** No estate-wide, manifest-emitting **governed activation compiler** with provenance and collision policy.

### 2. Governed `investigation_spec → research_brief.yaml` compiler?

| Status | Detail |
|--------|--------|
| **Partial** | Produced inline by same ingest/generator scripts as signal library |
| Validator | `backend/scripts/validate_research_brief.py` |
| **Gap** | No standalone governed compiler contract or compile manifest |

### 3. Governed `investigation_spec → package_manifest.yaml` compiler?

| Status | Detail |
|--------|--------|
| **Partial** | Manifest written inline during package generation |
| Validator | `backend/scripts/validate_package_manifest.py` |
| **Gap** | No dedicated manifest-only compiler; `source_spec_id` never populated |

### 4. Scripts that generate or ingest package artefacts

| Script | Outputs |
|--------|---------|
| `backend/scripts/generate_kb_s45d_batch1_packages.py` | `signal_library.yaml`, `research_brief.yaml`, `package_manifest.yaml` |
| `knowledge_bus/tools/kb_s47_batch2_ingest.py` | Full package + `promoted_signal_intelligence.yaml` |
| `backend/core/knowledge/investigation_spec_to_promoted_signal.py` | PSI YAML (library API) |
| `backend/scripts/validate_*` | Validation only (no generation) |

### 5. Difference from PSI translator

| Aspect | Activation compile (package) | PSI translator |
|--------|------------------------------|----------------|
| Primary output | `signal_library.yaml` (firing rules) | `promoted_signal_intelligence.yaml` |
| Runtime today | **Consumed** (`SignalRegistry`) | **Not consumed** |
| Hypotheses | Excluded from signal library | **Excluded** per ADR-008 |
| Scope | Full package triple | Signal-layer intelligence only |
| Investigation spec fields used | Activation, overrides, metrics | Semantics, translation metadata |

### 6. Missing before governed estate regeneration

1. **Unified activation compiler** with deterministic `activation_key` / frame identity.  
2. **Compile manifest** per run (see ADR-RT-004).  
3. **Collision policy** at compile time (hard error or explicit multi-frame emit).  
4. **`source_spec_id` on manifests** and reverse index spec → package.  
5. **Hypothesis compile** separate from activation (ADR-RT-003).  
6. **Card evidence compile** (later sprint; not in ARCH-RT-0).  
7. **Promotion gate** linking LC-S18A inventory `runtime_loaded` to compile outputs.

### 7. Owning sprint for activation compile implementation

Per `docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL.md`:

| Sprint | Scope |
|--------|-------|
| **ARCH-RT-1** | Contracts + compile foundation + one low-blast-radius compile pilot |
| **ARCH-RT-2** | Identity runtime pilot (depends on ADR-RT-002) |
| **ARCH-RT-3+** | Estate regeneration, hypothesis compile, card evidence |

**Owner for full activation compile:** **ARCH-RT-1** (foundation) with production scale in **ARCH-RT-3** (estate regeneration).
