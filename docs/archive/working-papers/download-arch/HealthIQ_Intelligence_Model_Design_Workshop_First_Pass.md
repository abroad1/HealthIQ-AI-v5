# HealthIQ Intelligence Model Design Workshop — First-Pass Completed Report

## Document status

**Purpose of this document:** first-pass completed response to the intelligence-model workshop brief.

**What this is:** a strategic design artefact intended to help the team agree the downstream intelligence target before designing the target schema.

**What this is not:** final schema design, final package design, or a complete clinical ontology.

**Recommended use:** circulate to the team, red-pen aggressively, then use the agreed version as the basis for the target biomarker / signal / phenotype intelligence schema.

---

## Executive summary

HealthIQ should be designed as a deterministic metabolic intelligence platform, not a prettier blood-report application.

In three years, the platform should be able to answer questions for multiple users and internal system layers:

- the consumer who wants to know what is wrong, why it matters, and what to do next
- the advanced user who wants mechanism, trade-offs, and progression signals
- the clinician who wants rapid synthesis, ranked explanations, confirmatory next steps, and a defensible discussion aid
- the internal reasoning system that must connect biomarkers, signals, pathways, phenotypes, context, and longitudinal change into a coherent analytical substrate
- future business-facing layers that support clinical review, phenotype stratification, repeat testing, outcomes analysis, and buyer-grade platform value

The platform will only feel genuinely intelligent if it can do more than say a marker is high or low. It must be able to:

1. explain likely biological meaning
2. distinguish between competing explanations
3. link individual markers into pathway- and system-level states
4. incorporate structured context such as anthropometrics, blood pressure, smoking, alcohol, medications, exercise, sleep, and stress
5. recognise uncertainty, contradiction, and confounding
6. support repeat testing, phenotype tracking, and intervention / outcome analysis
7. remain deterministic, traceable, and clinically defensible

The main design conclusion is simple:

**If a knowledge item changes reasoning, ranking, cross-marker linkage, consistency, or future automation, it must be structured.**

That implies the future target schema must go materially beyond:
- primary marker
- thresholds
- simple signal trigger logic

It will need structured support for:
- supporting and contradiction markers
- mechanism and pathway relationships
- differential explanation logic
- confirmatory tests
- confounders and caveats
- demographic and medication modifiers
- phenotype and cross-signal relationships
- longitudinal interpretation primitives
- structured confidence / uncertainty factors
- structured context-input consumption rules

---

## Strategic framing

The workshop brief asks one core question:

**What questions do we want the platform to be able to answer downstream, and what upstream knowledge must exist to answer them intelligently?**

That is the right question.

HealthIQ's current roadmap already makes clear that the product vision is a deterministic operating system for metabolic interpretation, with broad biomarker coverage, explicit and auditable biological reasoning, connected cross-system interpretation, high-impact context inputs, and eventual longitudinal and outcomes-linked intelligence. It also makes clear that the product is not intended to be a probabilistic black box or a generic LLM wrapper around blood tests. The long-term company vision is explicitly staged as engine moat first, dataset moat second, then outcomes / regulated workflow moat third. That makes this workshop strategically important because the future schema has to support not only current signal reasoning but also future phenotype, trajectory, clinical, and buyer-facing value. 

---

## Part 1 — Future user types

| User / system type | What are they trying to achieve? | Why do they need the platform? |
|---|---|---|
| Consumer user | Understand what their blood results mean in plain English, whether anything important may be wrong, how serious it may be, and what should happen next | Raw commercial blood panels are hard to interpret and most consumer tools are shallow, generic, and non-defensible |
| Advanced user / optimiser / biohacker | Understand mechanisms, hidden suboptimality, interactions, longitudinal movement, and whether interventions are working | They want deeper physiological reasoning, not traffic lights |
| Clinician / GP / specialist | Rapidly synthesise a complex panel, identify likely explanations, assess seriousness, decide what to confirm next, and avoid missing important patterns | Time is short; a useful platform must reduce cognitive load while preserving clinician authority |
| HealthIQ internal intelligence engine | Convert raw markers and context into deterministic signals, hypotheses, pathway interactions, phenotype states, and ranked outputs | This is the core analytical layer; without it the product becomes generic narrative on top of lab values |
| Future phenotype / pathway layer | Understand which patterns cluster together, which metabolic states co-occur, and how systems interact | This is required for system-level metabolic interpretation and future pharma / insurer value |
| Future longitudinal / progress layer | Determine what has changed, whether the change is biologically meaningful, what likely drove it, and what remains unresolved | Repeat testing becomes far more valuable when trajectory and intervention context can be interpreted |
| Future clinical review / audit layer | Assess whether the interpretation was traceable, evidence-grounded, consistent, caveated correctly, and safe | Clinical defensibility and future regulatory alignment require auditable reasoning |
| Future business / pharma / payer layer | Identify phenotypes, likely responders, biologically coherent subgroups, pathway burdens, and outcome-linked patterns | Strategic buyer value depends on structured metabolic intelligence, not raw lab display |

### Working conclusion

The platform is not serving one user. It is serving a stack:
- end user
- clinician
- internal reasoning layer
- future phenotype / longitudinal / audit / enterprise layers

That means the upstream knowledge model cannot be designed solely around the consumer report.

---

## Part 2 — Downstream questions

### Consumer user

| User / system type | Downstream question | Why this question matters |
|---|---|---|
| Consumer user | Why is this biomarker abnormal? | This is the first natural user question and the minimum bar for perceived intelligence |
| Consumer user | How serious is this result? | Users need significance, not just abnormality |
| Consumer user | What do these abnormal markers mean together? | Real meaning often sits in patterns, not isolated markers |
| Consumer user | Is this likely temporary, lifestyle-related, or something that needs medical follow-up? | Users need triage and direction |
| Consumer user | What should I discuss with my doctor? | This creates practical value and supports clinician handoff |
| Consumer user | What else would make this interpretation stronger or weaker? | This teaches uncertainty and avoids false certainty |
| Consumer user | What changed since my last test? | This is central to repeat-test value |
| Consumer user | Did my recent changes likely help? | This is critical for engagement and future retention |

### Advanced user / optimiser

| User / system type | Downstream question | Why this question matters |
|---|---|---|
| Advanced user | What pathway or system is implicated here? | Advanced users want mechanism, not generic advice |
| Advanced user | What are the leading competing explanations? | Intelligent products distinguish alternatives |
| Advanced user | Which markers support this interpretation and which argue against it? | This separates serious reasoning from shallow commentary |
| Advanced user | What hidden or within-range suboptimality is emerging? | Many users are interested in early pattern detection |
| Advanced user | Which phenotype am I expressing? | This is the bridge from markers to higher-level metabolic states |
| Advanced user | What intervention category is most likely to move this pattern? | Advanced users care about leverage, not only diagnosis |
| Advanced user | What should I retest and when? | This supports longitudinal use and cohort building |

### Clinician

| User / system type | Downstream question | Why this question matters |
|---|---|---|
| Clinician | What is the primary clinical picture here? | Clinicians need fast synthesis |
| Clinician | What are the top ranked explanations for the key abnormality or pattern? | This is core consultation value |
| Clinician | What evidence supports those explanations? | A clinician-grade product must be reviewable, not magical |
| Clinician | What contradictory features are present? | This protects against overstatement |
| Clinician | What confirmatory tests or markers would discriminate between the top explanations? | This directly saves time and increases utility |
| Clinician | Is there a safety / escalation issue here? | Seriousness and risk cannot be buried |
| Clinician | What context inputs materially affect interpretation? | Medication, blood pressure, waist, alcohol, smoking, etc. often change meaning |
| Clinician | How has the phenotype moved over time? | Repeat-testing value becomes much stronger when phenotype movement is visible |

### Internal intelligence engine / future system layers

| User / system type | Downstream question | Why this question matters |
|---|---|---|
| Internal intelligence engine | Which signals should fire from this marker pattern and context state? | Core engine function |
| Internal intelligence engine | Which candidate explanations should be ranked and why? | Root-cause layer depends on this |
| Internal intelligence engine | Which contradictions or caveats should suppress confidence? | Prevents brittle overcalling |
| Internal intelligence engine | Which pathway and phenotype relationships should be instantiated? | Required for system-level reasoning |
| Internal intelligence engine | Which longitudinal comparisons are meaningful versus noise? | Needed for repeat-test interpretation |
| Future phenotype / pathway layer | Which metabolic states commonly cluster together? | Supports phenotype modelling and enterprise value |
| Future longitudinal layer | Which interventions are associated with improvement or deterioration in this phenotype? | Supports dataset moat and outcomes layer |
| Future clinical audit layer | Can every explanation be traced back to structured rules and evidence? | Required for defensibility |
| Future business / pharma layer | Which patients or users belong to a biologically coherent subgroup? | Strategic commercial value |

### Consolidated downstream question set

The platform should be able to answer at least the following 24 questions well:

1. Why is this biomarker abnormal?
2. What is the most likely explanation?
3. What evidence supports that explanation?
4. What alternative explanations remain plausible?
5. What evidence argues against the leading explanation?
6. How serious is this finding?
7. Is this isolated or part of a wider pattern?
8. What system or pathway is implicated?
9. Which phenotype or metabolic state does this pattern suggest?
10. What would make this interpretation stronger?
11. What would make this interpretation weaker?
12. What context inputs materially change the interpretation?
13. What caveats or confounders apply?
14. What confirmatory markers or tests would help?
15. What should a clinician review next?
16. What does this set of markers mean together?
17. What changed since the last panel?
18. Is the change biologically meaningful?
19. Which phenotype signals improved, worsened, or remained stable?
20. Which reported interventions are directionally consistent with the observed change?
21. Which pathway burdens appear to be driving current risk?
22. Which cross-signal interactions matter here?
23. How auditable and evidence-grounded is this interpretation?
24. Which biologically coherent cohort or subgroup does this user resemble?

---

## Part 3 — What a strong answer looks like

| Downstream question | What would a weak answer look like? | What would a strong answer look like? |
|---|---|---|
| Why is this biomarker abnormal? | “This is high.” | Identifies likely biological mechanisms, ties them to supporting markers and context, and distinguishes possibility from confidence |
| What is the most likely explanation? | “This may indicate inflammation.” | Ranks 2–4 plausible explanations, states why one is leading, and shows what evidence separates them |
| What evidence supports that? | “Based on your results.” | Names the relevant markers, directions, thresholds, ratios, and context inputs supporting the interpretation |
| What alternative explanations remain plausible? | No alternatives mentioned | Explicitly lists meaningful alternatives that remain live, with what is missing to discriminate them |
| What evidence argues against it? | No contradiction handling | Surfaces contradiction markers, normal findings, or missing expected corroboration |
| How serious is this? | “Speak to your doctor.” | Separates urgency, likely burden, progression risk, and whether this appears mild, moderate, or high concern |
| Is this isolated or part of a pattern? | Marker-by-marker comments only | Connects related abnormalities and shows why they may represent a common process |
| What system or pathway is implicated? | “Metabolism may be affected.” | Names the pathway or system, explains mechanism, and links the relevant evidence |
| Which phenotype is suggested? | No phenotype layer | Maps the pattern to a structured metabolic state with supporting and contradiction features |
| What would strengthen this interpretation? | “More testing may help.” | Identifies specific missing corroborating markers, context inputs, or confirmatory tests |
| What would weaken this interpretation? | No uncertainty model | Identifies specific findings that would challenge or suppress the current explanation |
| What context inputs matter? | Generic lifestyle note | Identifies the exact inputs that materially alter meaning: waist, BP, medication, smoking, alcohol, sleep, exercise, stress |
| What caveats or confounders apply? | Caveats omitted | States relevant medication effects, pre-analytic influences, demographic modifiers, acute illness effects, or behavioural confounders |
| What confirmatory tests help? | “Repeat the test.” | Suggests the specific tests or markers that would discriminate between competing hypotheses |
| What should a clinician review next? | Generic GP advice | Provides a succinct clinician discussion pack: top issue, likely explanations, evidence, and confirmatory next steps |
| What do these markers mean together? | Separate comments on each marker | Produces a coherent, integrated biological picture |
| What changed since last time? | “ALT improved.” | Compares markers, signals, and phenotypes, separating noise from meaningful movement |
| Is the change meaningful? | Raw delta only | Interprets the movement relative to baseline, signal state, likely biological significance, and context |
| Did the phenotype improve or worsen? | No phenotype-level comparison | Shows movement in signal pattern and phenotype burden, not just marker movement |
| Did my intervention likely help? | “Walking may have helped.” | States that the reported change is or is not directionally consistent with the observed biological movement, without overclaiming causality |
| Which pathway burdens matter now? | Not addressed | Ranks active pathway burdens and shows the evidence chain behind them |
| Which cross-signal interactions matter? | Signals treated independently | Explains interaction chains such as insulin resistance -> hepatic stress -> inflammation -> vascular burden |
| How defensible is this interpretation? | Opaque reasoning | Shows traceability to structured rules, evidence strength, contradictions, and caveats |
| Which biologically coherent subgroup is this user in? | No subgrouping | Maps to a phenotype cohort defined by structured metabolic-state logic |

### Working conclusion

A strong answer in HealthIQ is not:
- descriptive only
- traffic-light only
- marker-by-marker only
- overconfident
- generic

A strong answer must combine:
- explanation
- ranking
- evidence
- uncertainty
- integration
- practical next steps
- auditability

---

## Part 4 — Upstream knowledge required

### Question-level mapping

| Downstream question | Upstream knowledge needed to answer it properly |
|---|---|
| Why is this biomarker abnormal? | Primary biomarker; trigger direction; threshold notes; plausible mechanisms; supporting markers; context modifiers; confounders |
| What is the most likely explanation? | Ranked explanation candidates; evidence-for markers; evidence-against markers; weighting / ranking logic; context dependencies; contradiction rules |
| What evidence supports that? | Marker-level evidence mapping; directionality; ratios / derived metrics; threshold provenance; rule-level evidence links |
| What alternative explanations remain plausible? | Structured differential explanation set; discriminator markers; missing-data model; phenotype overlap logic |
| What evidence argues against it? | Contradiction markers; suppressor rules; expected-but-missing corroboration; acute confounder flags |
| How serious is this? | Severity markers; escalation markers; burden classification; temporal concern model; system-specific seriousness rules |
| Is this isolated or part of a wider pattern? | Cross-marker relationships; signal relationships; pathway graph; phenotype mapping rules |
| What system or pathway is implicated? | Pathway / system tags; physiological claims; signal-system relationships; interaction graph |
| Which phenotype is suggested? | Phenotype definitions; required and optional features; supporting and contradiction features; minimum expression rules |
| What would strengthen this interpretation? | Corroboration markers; confirmatory tests; context inputs; additional data requirements |
| What would weaken this interpretation? | Contradiction markers; negative discriminators; context caveats; suppression logic |
| What context inputs matter? | Structured context-input model for anthropometrics, BP, medications, smoking, alcohol, exercise, sleep, stress; interpretation-consumption rules |
| What caveats or confounders apply? | Medication effects; demographic modifiers; pre-analytic influences; acute illness / recent exercise / fasting / alcohol effects; menstrual / hormonal context where relevant |
| What confirmatory tests help? | Confirmatory test library; marker-to-test mapping; explanation-to-test mapping; diagnostic discrimination rationale |
| What should a clinician review next? | Clinician-summary contract; top issue synthesis rules; explanation ranking; confirmatory next-step logic; escalation logic |
| What do these markers mean together? | Pattern logic; multi-marker combinations; signal interaction rules; phenotype relationships |
| What changed since last time? | Longitudinal identity continuity; baseline storage; delta logic; natural variation handling; lab compatibility handling |
| Is the change meaningful? | Signal-state comparison rules; phenotype movement rules; marker significance thresholds; noise / confidence model |
| Did the phenotype improve or worsen? | Phenotype scoring / state rules; longitudinal phenotype comparison logic; burden movement logic |
| Did my intervention likely help? | Structured self-reported intervention model; before / after timing; phenotype movement rules; direction-consistency mapping |
| Which pathway burdens matter now? | Pathway burden definitions; burden aggregation logic; pathway-to-signal mapping; severity and dominance logic |
| Which cross-signal interactions matter? | Interaction graph; dependency / cascade / amplification / contradiction relationships |
| How defensible is this interpretation? | Rule-level provenance; evidence strength; caveat model; contradiction model; audit trace output |
| Which subgroup is this user in? | Phenotype ontology; subgroup definitions; cohort-assignment logic; context and longitudinal modifiers |

### Consolidated upstream knowledge model

The platform will need upstream knowledge in at least the following categories:

1. Primary biomarker identity
2. Trigger direction
3. Trigger thresholds / threshold notes
4. Supporting biomarkers
5. Supporting biomarker directionality
6. Supporting biomarker role (corroborating, severity, differentiating, etc.)
7. Contradiction biomarkers
8. Negative discriminators / suppressors
9. Derived metrics and ratio dependencies
10. Pathway / system associations
11. Physiological claims
12. Explanation candidates / differential set
13. Explanation ranking logic
14. Confirmatory tests
15. Severity / escalation markers
16. Caveats / confounders
17. Medication effects
18. Demographic modifiers
19. Pre-analytic influences
20. Context-input interpretation rules
21. Signal-to-signal interaction rules
22. Signal-to-phenotype relationships
23. Phenotype definitions
24. Longitudinal comparison primitives
25. Intervention-tracking primitives
26. Rule-level provenance / evidence source links
27. Evidence strength
28. Uncertainty / confidence factors
29. Audit output / traceability fields
30. Cohort / subgroup assignment relationships

### Working conclusion

This is the most important design result of the exercise.

The future intelligence schema cannot simply model:
- a signal
- a primary marker
- some supporting markers
- a description

That is not enough to answer the target downstream questions well.

---

## Part 5 — Structured vs narrative

| Knowledge item | Structured / narrative / hybrid | Why |
|---|---|---|
| Biomarker ID | Structured | Canonical identity is foundational for reasoning and linkage |
| Trigger direction | Structured | Drives deterministic logic |
| Thresholds and boundary notes | Hybrid | Numeric threshold is structured; human nuance around threshold interpretation can be narrative |
| Supporting markers | Structured | Needed for reasoning and ranking |
| Supporting marker role | Structured | Corroboration vs severity vs differential meaning changes interpretation materially |
| Contradiction markers | Structured | Must affect logic and confidence consistently |
| Differential explanation set | Structured | Required for ranking and defensibility |
| Explanation narrative | Narrative / hybrid | The prose can be narrative, but the existence and ranking of explanations must be structured |
| Pathway / system tags | Structured | Needed for cross-biomarker linkage and future automation |
| Physiological claim | Hybrid | Canonical claim label structured; explanatory prose can be narrative |
| Confirmatory tests | Structured | Needed for consistency, clinician value, and future automation |
| Severity classification | Structured | Must be machine-consumable and auditable |
| Caveats / confounders | Hybrid | Confounder categories should be structured; explanatory prose can be narrative |
| Medication effects | Hybrid | Medication classes / impact categories structured; nuance narrative |
| Demographic modifiers | Structured | Affect reasoning directly |
| Pre-analytic influences | Hybrid | Standard categories structured; contextual explanation narrative |
| Context-input fields (waist, BP, smoking, alcohol, exercise, sleep, stress, meds) | Structured | These materially alter reasoning and longitudinal interpretation |
| Context-to-interpretation mapping rules | Structured | Must be deterministic and consistent |
| Signal interaction relationships | Structured | Future pathway / phenotype / burden layers depend on them |
| Phenotype definitions | Structured | Needed for longitudinal, subgrouping, and enterprise use |
| Longitudinal deltas | Structured | Required for repeat-test logic |
| Intervention tracking primitives | Structured | Required for cohort learning and progress interpretation |
| Evidence source links | Structured | Required for provenance and future audit |
| Evidence-strength label | Structured | Needed for prioritisation and defensibility |
| Uncertainty / confidence drivers | Structured | Affects how outputs are ranked and caveated |
| Rich educational explanation | Narrative | Useful for user experience but not core engine reasoning |
| Clinician-facing summary prose | Narrative / hybrid | Rendered output can be prose, but must be driven by structured contract |
| Audit trace output | Structured | Required for defensibility |

### Working conclusion

The rule of thumb in the brief holds.

If the item affects:
- reasoning
- ranking
- cross-marker linkage
- auditability
- future automation
- consistency

it should be structured.

Narrative belongs downstream, as a rendering layer on top of the structured model.

---

## Part 6 — Core now vs later

| Knowledge item | Core now / later | Why |
|---|---|---|
| Primary biomarker identity | Core now | Foundational |
| Trigger direction and thresholds | Core now | Foundational |
| Supporting biomarkers and roles | Core now | Required for serious reasoning |
| Contradiction markers | Core now | Needed to avoid brittle overcalling |
| Differential explanation set | Core now | Required for “WHY” to be credible |
| Confirmatory tests | Core now | Required for clinician and advanced-user value |
| Pathway / system associations | Core now | Needed for pattern and system-level interpretation |
| Caveats / confounders | Core now | Required for defensibility |
| Medication-context caveat model | Core now | Already strategically important and explicitly bounded in roadmap |
| Demographic modifiers | Core now | Needed for correct interpretation |
| Structured high-impact context inputs | Core now | Explicitly part of product roadmap and materially interpretation-changing |
| Rule-level provenance / evidence strength | Core now | Needed for trust and future audit |
| Longitudinal identity and delta model | Core now | Repeat testing is central to roadmap value |
| Basic intervention tracking primitives | Core now | Needed to support future progress / outcome value even if causal use remains conservative |
| Signal interaction model | Core now | Needed to avoid isolated-marker architecture |
| Phenotype definitions | Later but begin early | Important for dataset moat and enterprise value; minimal scaffolding should begin now |
| Pathway burden aggregation | Later but begin early | High-value future layer; likely follows stronger signal-interaction substrate |
| Full subgroup / cohort assignment logic | Later | More valuable once phenotype layer matures |
| Quantitative confidence model | Later / open question | Important but easy to misuse if rushed |
| Detailed confounder classes | Later / partial now | Start with key classes now; expand later |
| Full medication-aware reasoning | Later | Current roadmap correctly limits medication handling to interpretation caveats |
| Outcomes prediction layer | Later | Requires longitudinal and phenotype density first |
| Enterprise trial / companion-diagnostic layer | Later | Requires phenotype, subgroup, and outcomes scaffolding first |

### Working conclusion

The “core now” layer is already bigger than current simple signal architecture.

That is acceptable and strategically correct.

A schema that cannot support contradiction, differential logic, context inputs, caveats, provenance, and longitudinal comparison will force a later redesign.

---

## Part 7 — Open design questions

| Open question | Why it matters | Needed before target schema? |
|---|---|---|
| Do we need explicit contradiction markers as a first-class schema primitive? | Without them, the system risks overstating confidence and missing suppression logic | Yes |
| Do we need supporting-marker roles beyond a simple list? | Corroboration, severity, differential, and contradiction are not interchangeable | Yes |
| Do we need a structured differential-explanation model per biomarker / signal? | “WHY” quality will remain shallow without explicit alternatives | Yes |
| How should seriousness be modelled separately from abnormality? | A mild but interesting abnormality is different from a clinically urgent pattern | Yes |
| How should confidence / uncertainty be represented without introducing pseudo-precision? | Confidence is useful but easy to misuse if turned into fake numerical certainty | Yes |
| Do we need explicit rule-level provenance everywhere? | Important for future audit and clinical defensibility, but it increases authoring burden | Yes, at least in a minimal structured form |
| How should phenotype definitions relate to signals? | This determines future dataset, enterprise, and longitudinal value | Yes, conceptually; exact implementation can follow later |
| Do we need explicit pathway burden objects now or can they emerge later from signal interactions? | Affects schema complexity and future analytics | Desirable before final schema freeze |
| How should repeat-test meaning be modelled: marker-level only, signal-level, phenotype-level, or all three? | Longitudinal value depends on this | Yes |
| How should self-reported intervention data be structured and consumed? | Needed for progress interpretation and future outcomes layer | Yes |
| How should medication effects be represented without allowing unsafe medication-specific reasoning? | Must respect current strategic boundary | Yes |
| Do we need explicit confounder classes (acute illness, fasting status, recent exercise, alcohol, lab variance, menstrual cycle, etc.)? | Confounding is central to defensible reasoning | Yes, at least for major classes |
| How should missing data be represented? | Many good interpretations depend on knowing what is absent, not only what is present | Yes |
| How should the clinician-summary contract constrain output so the renderer never improvises clinically? | Critical for safe clinician-facing artefacts | Yes |
| Should phenotype and subgroup definitions be shared across consumer, clinician, and enterprise layers or separated? | Affects product coherence and downstream commercial value | Later but important |

---

## Additional strategic observations

### 1. The schema must support both present value and future buyer value

If HealthIQ’s long-term company vision is:
- engine moat
- then dataset moat
- then outcomes / regulated workflow moat

then the intelligence schema cannot be optimised only for current consumer UX.

It must support:
- deterministic reasoning now
- repeat-test longitudinal interpretation next
- phenotype and subgrouping after that
- enterprise / pharma / payer use cases later

### 2. Context is not a nice-to-have decoration

The roadmap is explicit that high-impact inputs such as anthropometrics, blood pressure, smoking, alcohol, medications, sleep, exercise, and stress are strategically important enough to be treated as governed platform inputs, not loose questionnaire decoration.

That means the workshop answer is clear:

**Any future intelligence schema that ignores context as first-class knowledge will be strategically wrong.**

### 3. HealthIQ will eventually need two linked but distinct knowledge layers

A likely future architecture is:

- **Reasoning layer**  
  biomarker / signal / explanation / caveat / pathway / context / longitudinal primitives

- **Rendering layer**  
  patient education, clinician summary prose, advanced-user mechanism view, future enterprise view

This matters because many things the team may be tempted to encode as prose actually belong in structured reasoning form.

### 4. “Why” requires explicit modelling of contradiction, not just support

A shallow system can say:
- marker X is high
- this supports explanation Y

A strong system must also say:
- marker A supports Y
- marker B weakens Y
- marker C is missing and would have discriminated between Y and Z

That requires explicit upstream representation.

### 5. Repeat-test value will depend on phenotype movement, not only marker deltas

Longitudinal value is not just:
- ALT down 6 points

It is:
- hepatic stress phenotype weakened
- inflammatory burden stable
- insulin resistance phenotype partially improved
- reported walking increase is directionally consistent with the shift, but alcohol intake remains a potential confounder

The schema should therefore be designed so future longitudinal logic can operate above raw marker deltas.

---

## Draft design implications for the future target schema

This document is not designing YAML yet, but it does imply the future schema will almost certainly need explicit places for:

1. biomarker-level trigger metadata
2. supporting markers with typed roles
3. contradiction / suppressor markers
4. ranked explanation candidates
5. confirmatory markers / tests
6. severity / escalation metadata
7. pathway / system relationships
8. context-input interpretation rules
9. confounders / caveats / medication caveats
10. evidence source and evidence-strength metadata
11. signal interaction relationships
12. phenotype relationships
13. longitudinal comparison primitives
14. intervention-tracking primitives
15. audit / provenance outputs

If these concepts do not exist in the target schema, the downstream questions identified in this workshop will not be answerable well.

---

## Recommended next step after team review

After review and iteration, run a second pass that does only three things:

1. **Agree the minimum canonical downstream questions**  
   Reduce the long list to the non-negotiable intelligence questions the platform must answer in Phase 1 and Phase 2.

2. **Freeze the upstream knowledge primitives**  
   Agree the smallest set of upstream knowledge types that must be structured for those answers to be possible.

3. **Only then design the target schema**  
   Start from the agreed intelligence primitives, not from existing source-file convenience.

---

## Final recommendation

The most important strategic decision from this exercise is this:

**Design the target schema around the questions the platform must answer well in 3 years, not around what is easiest to encode today.**

If the team does that, the resulting model can support:
- stronger consumer value
- stronger clinician usefulness
- repeat-test retention
- phenotype and dataset moat construction
- future auditability
- future buyer relevance

If the team does not do that, the platform will likely accumulate a brittle set of partial structures that eventually need to be redesigned.

---
