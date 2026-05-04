You are conducting a repo-grounded reverse-engineering task for HealthIQ AI.

This is not a coding sprint.
Do not change application code.
Do not redesign the product.
Do not write implementation patches.

Your job is to reverse-engineer a saved benchmark narrative report back into the backend and governed asset model, so we can see exactly which parts of the report are already supportable deterministically, which are only partly supportable, and which would require new deterministic assets.

Source report:
C:\Users\abroa\HealthIQ-AI-v5\docs\golden-narrative\AB_GOLD_STANDARD_NARRATIVE_REPORT_CHAT_2_FINAL.md

Your output file:
Place your finished report in the same directory as the source file:
C:\Users\abroa\HealthIQ-AI-v5\docs\golden-narrative\

You may choose the output file type you think is most appropriate for this task, but it must be easy for humans to review and compare side by side. Markdown is likely the best option.

Suggested output filename:
- if you are Cursor: `AB_GOLD_STANDARD_NARRATIVE_REVERSE_ENGINEERING_CURSOR.md`
- if you are Claude Code: `AB_GOLD_STANDARD_NARRATIVE_REVERSE_ENGINEERING_CLAUDE.md`

Core objective

We now have a benchmark narrative report that captures the kind of world-class deterministic blood analysis experience HealthIQ wants to build toward.

Your task is to work backwards from that report and identify, for each major narrative move or claim:
1. what backend/governed assets would be needed to support it
2. whether those assets already exist in the repo
3. whether existing assets are fully sufficient, partly sufficient, or missing
4. what deterministic asset/compiler/content gaps would need to be filled

This is a reverse-engineering and support-mapping task.

Important mindset

Do not evaluate whether the benchmark report is “good writing.”
Treat it as the target-state narrative benchmark.

Do not ask whether the current frontend can display it.
Ask whether the current backend / SSOT / Knowledge Bus / compiled outputs / DTO assets could support it deterministically.

Do not stop at high level.
We need a precise asset-support map grounded in the repo.

What you must do

1. Read the benchmark report carefully.
Break it into narrative moves, not just headings.

Examples of narrative moves include:
- broad body-level reassurance
- hierarchy of concern
- “this is not broad metabolic deterioration”
- lead pathway explanation
- system biology explanation
- marker-to-pathway linkage
- “why this matters beyond itself”
- secondary pattern explanation
- direction-of-travel / longitudinal comparison
- lifestyle-linked interpretation
- uncertainty and limits
- practical next steps

2. For each major narrative move, identify the likely supporting asset classes in the repo.
These may include, for example:
- panel biomarkers and reference ranges
- questionnaire / lifestyle data
- phenotype / interpretation-system definitions
- IDL records
- clinician report assets
- root-cause / chain / signal assets
- Layer C features
- system / cluster assets
- longitudinal comparison assets
- governed educational or explanation-bearing assets
- compiler-mediated text assets
- explicit missing assets

3. Inspect the repo and trace the real asset sources.
Use exact file paths wherever possible.
Look for:
- SSOT files
- Knowledge Bus sources
- backend contracts
- deterministic report builders
- DTO builders
- test fixtures
- golden fixtures
- phenotype maps
- IDL registries
- interaction maps
- questionnaire schema
- any relevant report-generation or compiler layers

4. Produce a support judgement for each narrative move:
- FULLY SUPPORTABLE
- PARTLY SUPPORTABLE
- NOT CURRENTLY SUPPORTABLE

5. For every “partly” or “not” supportable move, explain the gap precisely.
Examples:
- raw data exists but no compiled narrative asset
- questionnaire data exists but no deterministic interpretation join
- system logic exists but no user-safe explanation layer
- longitudinal data exists but no comparative compiler
- phenotype map exists but lacks pathway-grade prose asset
- frontend currently irrelevant; this is a backend asset gap

6. Be careful not to confuse:
- source data
- interpretation logic
- display-layer copy
- test fixtures
- output goldens
- optional examples
- true authoritative sources

Output structure

Please structure your report exactly like this:

# HealthIQ AI — Reverse Engineering of AB Gold Standard Narrative

## 1. Executive summary
A concise top-level judgement:
- how much of the benchmark report looks supportable today
- where the biggest backend strengths are
- where the most important deterministic gaps are

## 2. Source benchmark
State the source file reviewed:
`docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_REPORT_CHAT_2_FINAL.md`

## 3. Reverse-engineering matrix

Use a structured table with these columns:

- Section / narrative move
- Benchmark text summary
- Required support type
- Existing repo asset(s)
- Exact file path(s)
- Support status (FULL / PARTIAL / NONE)
- Gap explanation
- Required deterministic build implication

Be detailed enough that we can use this as a planning artifact.

## 4. Existing backend strengths
Summarise the areas where the current backend/intelligence stack appears already strong enough to support the benchmark.

## 5. Deterministic asset gaps
Summarise the most important missing or weak backend assets that would need to be built or strengthened.

## 6. Recommended next build implications
Translate the findings into practical deterministic build categories.
For example:
- new compiler asset needed
- new longitudinal comparison asset needed
- new lifestyle-to-interpretation asset needed
- new pathway explainer asset needed
- existing governed asset only needs surfacing
- etc.

## 7. Authority and evidence notes
List the key authoritative files you relied on, grouped by category.

Important instructions

- Be repo-grounded.
- Use exact paths.
- Do not hand-wave.
- Do not write generic product advice.
- Do not rewrite the benchmark report.
- Do not propose frontend polish as the answer unless the issue is clearly only surfacing.
- Focus on deterministic supportability.
- Distinguish clearly between:
  - authoritative source
  - fixture/example
  - generated output
  - display copy
- If something is unclear or ambiguous in the repo, say so explicitly.

Final requirement

Save the finished report in the same directory as the benchmark narrative file.

When finished, report back with:
- output filename
- brief summary of top 3 findings
- any areas of ambiguity where human adjudication may be needed