# HealthIQ — Research-to-Platform Pipeline: Problem Statement and Options

*Prepared by Claude Code for internal circulation. March 2026.*

---

## The Problem

We have three things that are working independently but are not yet connected:

1. **Research content** — 10 metabolic study topics, well-sequenced, clinically sound (see `10-starter-research-topics.md`)
2. **Validation infrastructure** — the Knowledge Bus (KB-S1 through KB-S7) validates knowledge packages, research briefs, signal libraries, and package manifests against the SSOT
3. **A three-layer analytics pipeline** — Layer A (biomarker ingestion), Layer B (derived signals and ratios), Layer C (insight bundles)

The gap is the translation step between 1 and 3.

Research exists as prose documents and structured study outputs. The platform consumes deterministic Python code. Nothing currently converts one into the other automatically. The Knowledge Bus validates inputs — it does not author them and it does not write code.

Every knowledge package that reaches `ready_for_implementation: true` currently requires a human developer to manually translate its content into Layer B and Layer C code. That step has no tooling, no defined format, and no automation.

This is the bottleneck.

---

## Current State of the Knowledge Bus

The Knowledge Bus validation chain (as of KB-S7) is:

```
run_knowledge_package.py
      ↓
validate_knowledge_package.py
      ↓
validate_package_manifest.py
validate_research_brief.py
validate_signal_library.py
      ↓
knowledge_status.json  →  PASS or FAIL
```

This is working. Gate enforcement is clean. Four consecutive sprints with no failures.

What it validates:
- Package structure and manifest fields
- Biomarkers referenced in research briefs exist in `backend/ssot/biomarkers.yaml`
- Signal library structure conforms to schema

What it does not do:
- Author the YAML package content from research
- Translate signal definitions into Python code
- Populate Layer B or Layer C

---

## A Known Complication: SSOT Coverage Gaps

Several signals in the metabolic research roadmap do not currently exist in `backend/ssot/biomarkers.yaml`:

| Signal | Status |
|--------|--------|
| `fasting_glucose` | Absent — use `glucose` |
| `fasting_insulin` | Likely absent |
| `lactate` | Likely absent |
| `blood_pressure` | Absent (non-lab signal) |
| `waist_circumference` | Absent (non-lab signal) |
| `eGFR` | May be derived, not raw |

Any knowledge package referencing these will fail validation. Before running the 10 metabolic studies through the pipeline, SSOT coverage needs to be assessed and extended where appropriate.

Adding biomarkers to `backend/ssot/biomarkers.yaml` is a HIGH risk change under the Automation Bus SOP and requires full governance treatment.

---

## The Options

### Option 1 — Use Claude Code as the Research-to-Signal Translator

**How it works:**

```
Research document or study output
      ↓
Provide to Claude Code
      ↓
Claude writes: knowledge package YAML + Layer B Python code
      ↓
Knowledge Bus validates the package
      ↓
Gate runs baseline tests
      ↓
If PASS: code is committed
```

**What this requires:**
- A defined output format for research sessions (what must the study output contain?)
- Claude Code to read the research, write the YAML package and the Python signal/bundle code in one governed work package
- No new infrastructure — the existing validation and gate machinery handles the rest

**Advantages:**
- No new tooling
- Existing governance model (Automation Bus SOP) applies unchanged
- Each study becomes a governed sprint: research in → validated code out

**Risks:**
- Claude Code quality depends on research input quality — garbage in, garbage out
- Clinical accuracy of generated signal thresholds must be reviewed by a domain expert before merge
- GPT architectural review (already required for STANDARD risk) becomes the clinical review gate

---

### Option 2 — Single Canonical Signals Registry File

**How it works:**

Replace the multi-file knowledge package system with a single master file:

```
knowledge_bus/signals_registry.yaml
```

Each entry:

```yaml
- signal_id: insulin_resistance_tyg
  layer: B
  required_biomarkers:
    - glucose
    - triglycerides
  formula: "ln((glucose_mg * triglycerides_mg) / 2)"
  thresholds:
    optimal: < 8.31
    suboptimal: 8.31 - 8.52
    at_risk: >= 8.52
  bundles:
    - metabolic_health
    - cardiovascular_risk
    - biological_age
  evidence_source: "Study 1 — Insulin Resistance Signal"
```

Claude populates entries. The test suite validates SSOT coverage and formula references. A secondary validator confirms calculated ratios are correct.

**Advantages:**
- Simpler than the package system
- Single source of truth for all signal definitions
- Easier to diff and review

**Risks:**
- Loses the per-package governance structure (harder to promote individual studies independently)
- Requires rebuilding some of what the Knowledge Bus already does
- Should not be built until Option 1 has been evaluated — no sense replacing working infrastructure prematurely

---

### Option 3 — Structured Research Output Template

**How it works:**

Every AI research session (GPT, Claude, or other) is required to produce a machine-readable block at the end of its output. Claude Code reads this block and translates it into the implementation.

Required output block format:

```
## HealthIQ Platform Signal Mapping

Signal ID: [snake_case_identifier]
Layer: [A | B | C]
Required biomarkers: [comma-separated SSOT keys]
Derived metrics: [formula or calculation]
Thresholds: [optimal / suboptimal / at_risk values with units]
Bundles consuming this signal: [list]
Evidence strength: [exploratory | moderate | strong]
```

Without this block, the research output is not usable in the platform.

**Advantages:**
- Forces research to be structured at the point of generation, not retrospectively
- Creates a reusable prompt template for all 10 studies
- Human-readable and machine-parseable

**Risks:**
- Requires discipline in every research session
- The template needs to be defined and agreed before any studies are run

---

## Recommendation

**Start with Option 1.**

The infrastructure is working. The bottleneck is authoring, not validation. Attempting to resolve this by building new infrastructure (Options 2 or 3) risks adding complexity before validating whether the existing system can carry the load.

Proposed pilot:

1. Run Study 1 (Insulin Resistance) in a research chat with the structured output format from Option 3 applied
2. Bring that output to Claude Code
3. Claude Code writes the knowledge package YAML and the Layer B Python code
4. Run through the Knowledge Bus
5. Gate pass → commit → merge

If that works end-to-end, the pipeline is proven. The 10 studies become 10 governed sprints.

If it breaks, the failure point is identified and can be addressed specifically.

Option 3 (structured research template) is a low-cost addition that makes Option 1 work better. Adopt it alongside Option 1.

Option 2 should be held in reserve. If the package format proves genuinely unworkable after real studies are run through it, revisit then.

---

## Open Questions for Consensus

1. Who reviews clinical accuracy of generated signal thresholds before merge? Is GPT architectural review sufficient, or does a domain expert (clinician) need to be in the loop?

2. How should non-lab signals (blood pressure, waist circumference) be handled? Separate SSOT file? Excluded from the pipeline? This affects studies 5, 7, and 8.

3. Is `fasting_glucose` a meaningful distinction from `glucose` in this platform's context? If yes, it needs adding to SSOT with governance treatment. If no, the research roadmap needs correcting to use `glucose` throughout.

4. What is the target cadence for studies? One per sprint? That determines whether the Automation Bus SOP overhead is acceptable or needs a lighter-weight track for research-to-signal work.

5. Should the Knowledge Bus validation gate include a clinical plausibility check (e.g. threshold ranges within physiologically realistic bounds), or is that out of scope for automated validation?

---

*This document reflects a brainstorming session and does not represent a decision. All architectural changes remain subject to Automation Bus SOP v1.2 governance.*
