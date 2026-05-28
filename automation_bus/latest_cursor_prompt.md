---
work_id: WAVE1-EQUIV1_total_bilirubin_false_missing_fix
branch: work/WAVE1-EQUIV1-total-bilirubin-false-missing-fix
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# WAVE1-EQUIV1 — total_bilirubin false-missing fix

## Purpose

Fix the confirmed Wave 1 liver-card subsystem false-missing defect where `total_bilirubin` is treated as an expected missing marker even though canonical SSOT identifies `total_bilirubin` as a display/rail label and canonical lab identity is `bilirubin`.

This is a narrow defect-remediation sprint. It must not become part of the wider day-one architecture rework.

## Risk classification

This work is classified as:

```yaml
risk_level: HIGH
change_type: BEHAVIOUR
````

Reason:

```text
backend/core/analytics/wave1_subsystem_evidence.py
```

is under `backend/core/analytics/`, which is an unconditional HIGH-risk path under Automation Bus SOP v1.3.1.

HIGH-risk process applies:

* Claude hardening required before kernel start
* Cursor implementation only after kernel start
* Claude audit after implementation
* GPT architectural review before merge
* dual approval before merge

## Pre-branch preservation requirement

Before creating or switching to the sprint branch, verify the current `main` working tree.

There are known untracked planning and architecture documents across:

```text
docs/planning-papers/
docs/architecture/
docs/audit-papers/
docs/sprints/
```

Run and report:

```powershell
git branch --show-current
git status --short
git diff --name-only
git diff --cached --name-only
```

If any newly created or modified planning/audit/sprint documents are present, STOP before creating the sprint branch.

Those files must be preserved separately before this sprint begins.

Expected action:

```text
Create a separate docs-only preservation commit before creating the WAVE1-EQUIV1 sprint branch.
```

Do not allow sprint implementation changes to mix with uncommitted planning documents.

## Confirmed defect

Hardening confirmed:

```text
backend/core/analytics/wave1_subsystem_evidence.py
```

contains liver processing expected markers equivalent to:

```python
expected_marker_ids=("alp", "albumin", "bilirubin", "total_bilirubin")
```

Hardening also confirmed:

```text
backend/ssot/biomarkers.yaml
```

marks `total_bilirubin` as:

```yaml
display_label_rail_only: true
```

with description indicating canonical lab identity is `bilirubin`.

Therefore, the correct fix is to remove `total_bilirubin` from the liver subsystem expected-marker tuple and preserve `bilirubin` as the canonical expected marker.

## Existing assembler workaround

Do not modify the domain-level workaround in:

```text
backend/core/analytics/domain_score_assembler.py
```

Hardening identified that this file already compensates at the domain-level missing list.

That workaround is out of scope.

The live defect is at the subsystem evidence partition visible through `SubsystemEvidenceV1` / frontend card evidence.

## Authority preflight

Before editing, verify and report:

1. The current liver subsystem expected-marker tuple in `wave1_subsystem_evidence.py`.
2. The SSOT entry for `total_bilirubin`.
3. The SSOT / canonical identity for `bilirubin`.
4. The existing domain-level workaround in `domain_score_assembler.py`, confirming it will not be changed.
5. The existing test currently asserting `total_bilirubin` appears in governed display-label output.

If any of these cannot be verified, STOP and report the missing authority.

## Scope

Allowed scope:

* Remove `total_bilirubin` from the liver subsystem expected-marker tuple.
* Preserve `bilirubin` as the canonical expected marker.
* Update the conflicting regression test that currently asserts `total_bilirubin` appears in the label map.
* Add or amend regression coverage proving:

  * `bilirubin` is the expected canonical marker
  * `total_bilirubin` is not reported as missing in subsystem evidence when `bilirubin` is present
  * domain-level behaviour remains unchanged
  * no broader SSOT/canonicalisation policy is changed

Likely files:

```text
backend/core/analytics/wave1_subsystem_evidence.py
backend/tests/**/test_domain_ux1c_governed_subsystem_evidence.py
```

Final touched files must be justified by the preflight findings.

## Out of scope

Do not:

* Modify `backend/core/analytics/domain_score_assembler.py`.
* Change biomarker canonicalisation policy.
* Change `backend/ssot/biomarkers.yaml`.
* Change unit conversion policy.
* Change biomarker reference ranges.
* Change scoring rails.
* Change domain scoring.
* Change Health Systems Card design.
* Change frontend components.
* Start the day-one architecture rework.
* Create card evidence schemas.
* Create compiled card evidence artefacts.
* Modify root-cause YAML.
* Modify PSI.
* Modify SignalRegistry or SignalEvaluator.
* Modify package files.
* Modify investigation specs.
* Modify control-plane scripts.
* Introduce fallback parsers.

## Required implementation

If the defect exists as confirmed:

1. Remove `total_bilirubin` from the liver subsystem expected-marker set.
2. Preserve `bilirubin`.
3. Replace the existing conflicting test:

```text
test_total_bilirubin_emits_governed_display_label
```

or equivalent test currently asserting `total_bilirubin` appears in `label_map`.

4. The replacement test must assert the corrected behaviour:

```text
bilirubin is the expected canonical marker
total_bilirubin is absent from missing subsystem markers when bilirubin is present
```

5. Ensure existing domain-level tests still pass.
6. Do not modify the assembler workaround.

## Required tests

Run the narrowest relevant tests first.

At minimum, run the test file containing:

```text
test_total_bilirubin_emits_governed_display_label
```

Expected likely path:

```text
backend/tests/**/test_domain_ux1c_governed_subsystem_evidence.py
```

Also run any existing tests covering:

```text
Wave 1 subsystem evidence
liver subsystem included/missing marker partitioning
domain-level missing marker behaviour
```

If no suitable regression exists after updating the conflicting test, create a targeted regression test.

## STOP conditions

STOP and report without implementing if:

1. `total_bilirubin` is not present in the liver subsystem expected-marker logic.
2. The defect has already been fixed.
3. The issue is not local to Wave 1 subsystem evidence and instead exposes a broader canonical resolver defect.
4. Fixing the issue would require changing canonical biomarker policy.
5. Fixing the issue would require changing scoring/domain logic.
6. Fixing the issue would require modifying `domain_score_assembler.py`.
7. Regression coverage cannot be added or updated.
8. Any uncommitted planning documents are still present on `main` and have not been safely preserved before branch creation.
9. The current branch does not match the declared sprint branch after branch setup.
10. `automation_bus/state/work_package_active.json` is missing or does not match this work_id after kernel start.

## Evidence required from Cursor

Cursor must report:

1. Pre-branch preservation check output.
2. Confirmation that docs-only preservation was completed before sprint branch creation, if required.
3. Authority preflight findings.
4. Exact file(s) changed.
5. Exact defect found.
6. Exact fix applied.
7. Regression test added or updated.
8. Test commands run.
9. Test results.
10. Confirmation that `domain_score_assembler.py` was not modified.
11. Confirmation that `backend/ssot/biomarkers.yaml` was not modified.
12. Confirmation that no broader architecture files were modified.
13. Confirmation that the Sprint 0 fix does not introduce new card-evidence authority.

## Closure requirements

Before `run_work_package.py finish`, Cursor must complete the Automation Bus post-implementation closure protocol.

Run and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 5
git diff --name-only
git diff --cached --name-only
git stash list
```

Cursor must explicitly classify:

* tracked modified files
* staged files
* untracked files
* tooling files
* out-of-scope files
* any stash entries

Do not run finish unless:

* current branch matches `work/WAVE1-EQUIV1-total-bilirubin-false-missing-fix`
* working tree is clean except intended staged sprint changes
* no unrelated planning documents are included
* no tooling files are included
* no ambiguous stash exists
* latest commit contains only in-scope work

## Success criteria

This sprint is complete only if:

1. The false-missing `total_bilirubin` defect is fixed.
2. `bilirubin` remains the canonical expected marker for the relevant liver subsystem evidence.
3. `total_bilirubin` is not falsely reported missing when `bilirubin` is present.
4. Existing domain-level workaround behaviour is preserved.
5. Existing liver-card behaviour is otherwise preserved.
6. Regression coverage proves the fix.
7. `domain_score_assembler.py` is unchanged.
8. `backend/ssot/biomarkers.yaml` is unchanged.
9. No architecture rework is included.
10. No unmerged planning documents are mixed into the sprint branch.
11. Automation Bus gate passes.

```
```
