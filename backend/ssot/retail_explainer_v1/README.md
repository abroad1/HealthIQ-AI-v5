# `retail_explainer_v1` SSOT

Governed location for **retail / educational** copy keyed by biomarker id and cluster-schema system key.

- **Registry:** `registry.yaml` — human-edited; validated at load time and by `tests/enforcement/test_retail_explainer_registry_b1b.py`.
- **Schema:** see `core/contracts/retail_explainer_v1.py` and `docs/architecture/RETAIL_EXPLAINER_CONTENT_BOUNDARIES_v1.md`.

## Authoring rules (B1B+)

- **Biomarker keys** must match **canonical ids** in `backend/ssot/biomarkers.yaml` (not aliases).
- **System keys** must match a `system:` value used there (cluster ids map to `{system}_{n}_biomarkers`).
- Each entry needs non-empty `title` and `body`; keep tone **educational**, **non-diagnostic**, and **non-personalised**.
- Close with a short disclaimer that this is general education, not a diagnosis, and not a substitute for clinical advice.
- **Contribution context** is **not** stored here; `ContributionContextV1` is built at runtime from cluster membership.

B1A delivered schema + pilot sample; B1B populates the first production-ready educational set and guardrails.
