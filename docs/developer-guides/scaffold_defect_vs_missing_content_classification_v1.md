# Scaffold Defect vs Missing Content Classification v1

Categories from LC-S12B — use when triaging issues:

## Scaffold defect

Runtime or contract bug in deterministic engine, DTO, orchestrator, or validator. Requires code fix + regression test + Sentinel entry.

## Missing knowledge asset

Signal/WHY/lifestyle content not yet authored in Knowledge Bus. Not a code defect — track in content backlog.

## Frontend presentation issue

DTO is correct but UI mis-renders or omits governed fields. Fix in `frontend/` only; do not change analytical output.

## Clinical content backlog

Medically bounded copy improvements within existing asset boundaries — not runtime logic changes.

## Escaped defect

Previously shipped bug now guarded by Sentinel + regression test.

## Governance gap

Process or SOP violation (e.g. unscaffolded core change, missing work package token).

## Standing maintenance

Future KB-WAVE or scaffold sprints must update this document if they introduce or change the relevant architectural pattern.
