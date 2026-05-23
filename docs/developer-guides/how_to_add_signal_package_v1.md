# How to Add a Signal Package v1

## Package lifecycle

Signal packages in `knowledge_bus/packages/` follow states documented in `docs/audit-papers/LC-S17_knowledge_bus_lifecycle_framework.md`:

1. **Draft** — author content locally
2. **Inventory** — register in package estate inventory
3. **Validated** — pass orphan + schema checks
4. **Runtime-linked** — only when explicitly wired (most packages are signal-only today)

## Signal-only vs WHY-enabled

| Type | Requires |
|------|----------|
| Signal-only | Signal definition in signal registry path |
| WHY-enabled | Signal + `RootCauseTargetSpec` in `root_cause_registry_v1.py` + hypothesis asset |

## Required files

- Package manifest and signal definition per KB SOP
- Regression test if package affects consumer-visible output

## Orphan detection

- `backend/core/knowledge/` orphan reporters (LC-S16/S19 patterns)
- Do not auto-load orphan packages into runtime

## Validators

- Signal evaluator unit/regression tests
- Sentinel escaped-defects pack entry when adding new consumer-visible behaviour

## Documentation update obligation

Update `docs/architecture/HealthIQ_AI_runtime_architecture_map_v1.md` when package lifecycle patterns change.

## Standing maintenance

Future KB-WAVE or scaffold sprints must update this document if they introduce or change the relevant architectural pattern.
