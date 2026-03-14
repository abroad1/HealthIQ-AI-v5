# KB-S30 Thyroid Coverage Check

Thyroid-related signal coverage found:

- `signal_thyroid_tsh_context` — `knowledge_bus/packages/pkg_thyroid_tsh_context`
- `signal_tsh_high` — `knowledge_bus/packages/pkg_s24_tsh_high_hypothyroidism`
- `signal_tsh_low` — `knowledge_bus/packages/pkg_s24_tsh_low_hyperthyroidism`

Related endocrine/hormonal signal also present:

- `signal_calcium_high` — `knowledge_bus/packages/pkg_s24_calcium_high_endocrine`

Coverage assessment: **sufficient coverage**.

Rationale: thyroid/TSH pathway has both context and directional threshold signals available, enabling deterministic thyroid -> lipid -> metabolic edges without introducing invented signal IDs.
