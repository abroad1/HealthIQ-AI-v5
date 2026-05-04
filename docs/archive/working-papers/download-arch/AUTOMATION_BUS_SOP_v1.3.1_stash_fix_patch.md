# AUTOMATION BUS SOP v1.3.1 (ALIGNED + STASH FIX)

This version includes explicit stash lifecycle enforcement.

--- SNIPPED HEADER (UNCHANGED FROM PRIOR FILE) ---

### Stage 4A.5 — Stash Rule (UPDATED)

Stash is emergency-only during sprint closure.

Cursor must not use stash during normal closure unless it first states:

- exactly why stash is required
- exactly which files will enter the stash
- whether untracked files are involved
- whether ignored files are involved
- the exact recovery command needed to restore the stash contents

If ignored files are involved, Cursor must explicitly state that standard stash behaviour does not include ignored files unless handled with the correct mode.

No stash creation, pop, apply, or drop is permitted without explicit user approval once closure has entered stash-remediation territory.

#### Stash Resolution Requirement

Any stash created during a work package lifecycle is considered a tracked closure artifact.

Cursor must explicitly track and resolve every stash created during the active sprint.

A stash is only considered resolved if it is:

- restored and fully consumed into the working tree
- explicitly retained with human approval and a stated reason
- explicitly dropped with human approval

Cursor must not leave any stash in an unresolved state at the end of closure.

Creation of a stash introduces a mandatory resolution obligation before closure can be declared complete.

---

### Stage 4A.6 — Finish Readiness Gate (UPDATED ADDITION)

Add requirement:

- no unresolved stash entries exist that were created during this sprint

---

### Stage 4A.8 — Post-Finish Confirmation (UPDATED)

Replace stash line with:

- whether any stash entries remain from the sprint, and explicit classification of each as:
  - resolved (restored)
  - retained with approval
  - dropped

Any unresolved stash entry blocks closure completeness.

---

### Stage 4A.9 — Local Merge Execution Rule (UPDATED)

Replace stash line with:

- confirmation that no unresolved stash entries from the sprint remain

Merge must not proceed if any stash created during the sprint remains unresolved.

---

### Section 14 — Non-Negotiable Rules (ADDITION)

* No sprint may reach closure-complete or merge-ready state while a stash created during that sprint remains unresolved

---

END OF AMENDMENT
