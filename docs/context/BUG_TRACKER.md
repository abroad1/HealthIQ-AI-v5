# 🐞 HealthIQ-AI Bug Tracker

> This file is used to **log, triage, and resolve bugs** encountered across the HealthIQ-AI stack. It is a live operational record and should reflect actual implementation issues — not feature requests or design discussions.

---

## 📌 Usage Rules

- Only **verified regressions or implementation issues** should be logged here
- Use the bug template below for consistency
- Each bug must be assigned a status and triage level
- **DO NOT DELETE** closed bugs — strike them through if resolved

---

## 🧱 Bug Template

```md
### 🐛 Bug Title (short description)

**ID:** BUG-YYYYMMDD-XX
**Date Reported:** YYYY-MM-DD
**Reported By:** @username
**System Area:** `frontend` | `backend` | `api` | `ssot` | `parser` | `pipeline` | `orchestrator` | `cluster-engine` | `insight-engine` | `tests`
**File(s) Involved:** `path/to/file.py` / `path/to/component.tsx`
**Steps to Reproduce:**
1. Step one
2. Step two
3. Step three

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Screenshot/Log:**
[Paste image or error trace if relevant]

**Triage:**
- [ ] Severity: `blocker` | `critical` | `major` | `minor`
- [ ] Status: `open` | `in progress` | `waiting on info` | `fixed` | `wontfix`
- [ ] Assigned to: @team-member-name

---
```

---

## ✅ Example Bug Entry

### 🐛 Insight Engine crashes on null biomarker input

**ID:** BUG-20250920-01  
**Date Reported:** 2025-09-20  
**Reported By:** @anthony  
**System Area:** `insight-engine`  
**File(s) Involved:** `core/insights/base.py`

**Steps to Reproduce:**
1. Upload a parsed panel with one marker missing unit
2. Allow orchestrator to pass it to insight engine
3. Observe engine fails with `NoneType` error

**Expected Behavior:**
Engine should fallback to "insufficient data" status

**Actual Behavior:**
`AttributeError: 'NoneType' object has no attribute 'value'`

**Triage:**
- [x] Severity: `critical`
- [x] Status: `open`
- [x] Assigned to: @vicki

---

## 🧹 TODOs for Bug Ops
- [ ] Link this file to DevOps dashboard
- [ ] Auto-tag engine-specific issues via file path parsing
- [ ] Consider moving closed bugs to archive section

---

> "Every bug is a misunderstood assumption." — HealthIQ Core Team

