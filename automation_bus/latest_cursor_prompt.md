---
work_id: N-1
branch: feature/n-1-narrative-target-lock-and-authority-map
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# N-1 — Narrative target lock and authority map

## Objective

Create the formal authority package that locks the benchmark AB gold-standard narrative as the target-state reference and converts the reverse-engineering work into one approved deterministic support matrix.

This is not a coding sprint.
Do not modify backend or frontend application code.
Do not redesign the product.
Do not write implementation patches.

This sprint exists to turn the strategic narrative work into execution authority so that later deterministic build sprints are grounded, precise, and governed.

---

## Strategic context already settled

The following are already decided and are not open for reinterpretation in this sprint:

- The saved benchmark narrative is the preferred target-state narrative reference for this workstream.
- The key problem is not missing raw data alone and not frontend polish alone.
- The main gap is the missing deterministic narrative support stack:
  - data/contract support where needed
  - governed narrative assets
  - compiler/assembly layer
  - output/display layer
- The final sprint strategy document is now the planning authority for this workstream.
- The purpose of N-1 is to lock authority, not to debate the product vision again.

Your job is to produce the formal authority artifacts that the rest of the sprint series will build from.

---

## Inputs you must use

Treat the following as required inputs:

1. Final benchmark narrative
`docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_REPORT_CHAT_2_FINAL.md`

2. Reverse-engineering reports
- `docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_REVERSE_ENGINEERING_CURSOR.md`
- `docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_REVERSE_ENGINEERING_CLAUDE.md`

3. Final sprint strategy
`docs/golden-narrative/HealthIQ_Deterministic_Narrative_Sprint_Strategy_FINAL.md`

4. Relevant repo-grounded authority files referenced by those documents

---

## Required outcome

Deliver a clean authority package that does all of the following:

1. locks the benchmark narrative as the approved target-state narrative reference for this workstream
2. produces one merged reverse-engineering matrix from the Cursor and Claude reports
3. resolves any remaining ambiguity in support classification where possible
4. identifies the approved deterministic asset-gap categories
5. states clearly which future sprint in the strategy is expected to address each major gap
6. leaves behind a planning-ready artifact that later sprint authors can use without redoing the narrative-analysis work

---

## In scope

### 1. Narrative target lock
Produce a short authority note that states:
- which benchmark narrative file is the approved reference
- what role it plays
- what it is not
- how it should be used in later sprints

This should make clear that the benchmark is:
- a target-state narrative standard
- not current product truth
- not current deterministic runtime output
- not freeform copy to paste into the frontend

### 2. Merged reverse-engineering matrix
Produce one merged matrix that combines the strongest findings from the Cursor and Claude reports into a single planning artifact.

The matrix must include, at minimum:

- section / narrative move
- benchmark text summary
- required support type
- existing repo asset(s)
- exact file path(s)
- support status:
  - FULL
  - PARTIAL
  - NONE
- gap explanation
- required deterministic build implication
- likely owning sprint from the final strategy

### 3. Support-status adjudication
Where Cursor and Claude differ in emphasis or segmentation, adjudicate and produce one settled position.

Do not preserve duplicate rows unless they are meaningfully different.
Do not average differences vaguely.
Produce one clear planning-ready matrix.

### 4. Deterministic asset-gap categories
Create a compact section that groups the major gaps into approved build categories, such as:

- narrative compiler layer
- body-overview / reassurance compiler
- longitudinal raw-value and delta support
- lifestyle-to-pathway joins
- pathway-grade explainer assets
- functional reading / confidence / monitoring assets
- new governed interpretation entities
- retail patient summary compiler
- clinician synthesis compiler

### 5. Sprint linkage
For each major gap category, state which sprint in the final strategy is intended to address it.

This should create a clear bridge from:
benchmark narrative → merged support matrix → sprint series

---

## Out of scope

The following are explicitly out of scope:

- implementation changes to backend or frontend
- new contracts or code
- changes to the benchmark narrative itself
- new medical research
- frontend redesign
- Gemini / LLM integration work
- changing the approved sprint strategy beyond minor authority clarifications if needed in the output notes

---

## Required output files

Create the following files in the same directory as the benchmark narrative and sprint strategy:

### 1. Narrative target lock
Suggested filename:
`AB_GOLD_STANDARD_NARRATIVE_TARGET_LOCK.md`

### 2. Merged reverse-engineering matrix
Suggested filename:
`AB_GOLD_STANDARD_NARRATIVE_REVERSE_ENGINEERING_MERGED.md`

You may keep these filenames unless repo reality strongly suggests a better naming pattern.

---

## Output structure requirements

### File 1 — Narrative target lock
Must include:

- purpose
- approved benchmark file path
- what the benchmark is
- what the benchmark is not
- how later sprints must use it
- relation to the final sprint strategy

### File 2 — Merged reverse-engineering matrix
Must include:

#### 1. Executive summary
- top-level supportability judgement
- strongest existing backend strengths
- most important deterministic gaps

#### 2. Source authorities used
List the benchmark narrative, both reverse-engineering reports, and the final strategy file.

#### 3. Merged reverse-engineering matrix
Use a structured table with the required columns listed above.

#### 4. Approved deterministic gap categories
Grouped build categories.

#### 5. Sprint linkage map
Gap category → intended sprint(s).

#### 6. Authority notes / ambiguities
Only include unresolved ambiguities if they genuinely remain after adjudication.

---

## Adjudication rules

### Rule 1 — prefer precision over breadth
If one report is more precise and repo-grounded on a specific issue, prefer that wording.

### Rule 2 — preserve complementary insight
If Cursor and Claude each contributed distinct value, merge them rather than choosing one voice wholesale.

### Rule 3 — distinguish confirmed gaps from probable gaps
Do not use weak language where the repo evidence is already decisive.

### Rule 4 — maintain authority clarity
Be explicit about what is:
- authoritative source
- fixture/example
- compiled output
- display-layer artifact
- benchmark target

### Rule 5 — no hand-waving
This document will become planning authority.
Use exact paths and grounded statements.

---

## Expected implementation shape

This sprint should amount to:

1. read benchmark
2. read both reverse-engineering reports
3. read final sprint strategy
4. reconcile and adjudicate
5. write target lock
6. write merged matrix
7. save both files in `docs/golden-narrative/`

No code changes should result.

---

## STOP conditions

STOP immediately and report if any of the following are true:

1. the benchmark file path is not the same file the strategy assumes
2. the reverse-engineering reports materially conflict in ways that cannot be adjudicated without new repo investigation
3. the final sprint strategy materially contradicts the benchmark or merged support findings
4. required authority files are missing or stale enough to make the output unreliable

If blocked, report the exact blocker and the smallest safe remediation path.

---

## Success criteria

This sprint is successful only if:

1. the benchmark narrative is formally locked as the approved target-state reference
2. one merged reverse-engineering matrix exists
3. the matrix is repo-grounded and adjudicated
4. the major deterministic gap categories are clearly defined
5. those categories are linked to the approved sprint series
6. later sprint authors could use these files without rerunning the whole narrative exercise

---

## Deliverables

At finish, the sprint should leave behind:

- `docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_TARGET_LOCK.md`
- `docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_REVERSE_ENGINEERING_MERGED.md`

plus a short completion note stating:
- output filenames
- top 3 findings
- any remaining ambiguities needing human judgement

---

## Evidence requirements

You must show, with exact file paths and grounded references:

- which benchmark file was locked
- which reverse-engineering files were merged
- which strategy file the sprint linked to
- where the strongest backend supports are
- where the main deterministic gaps remain

Do not produce a vague summary.
Produce planning authority.