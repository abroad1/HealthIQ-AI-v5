---
name: review_latest_audit_summary
description: Review the latest Claude audit summary under HealthIQ governance and provide a non-binding merge-readiness recommendation.
---

Read:
- automation_bus/latest_audit_summary.md
- automation_bus/latest_cursor_status.json if present
- automation_bus/latest_gate_evidence.json if present

Also consult these governing files when relevant:
- docs/AUTOMATION_BUS_SOP_v1.3.md
- docs/KNOWLEDGE_BUS_SOP_v1.3.md
- docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.4_amended.md

Output:
1. Repo-grounded summary
2. Architectural implications
3. Determinism / drift risk
4. Control-plane / authority-path implications
5. Recommendation

Recommendation must be one of:
- Safe to merge, subject to human approval
- Review required
- Block

Forbidden:
- Merge approved
- Final sign-off granted