# HealthIQ AI — Interpretation Display Layer  
## Merged design-lock recommendation (Claude + Cursor synthesis)

**Status:** Recommended merged position for team approval  
**Purpose:** To resolve the best parts of the two design-lock drafts into one clear direction for the Interpretation Display Layer (IDL) that must exist before Section 5 can be implemented.

---

## 1. Executive recommendation

The correct merged position is:

1. Build a governed **Interpretation Display Layer (IDL)** as a backend/content contract before any Section 5 frontend implementation.
2. Use **Claude’s architecture and contract discipline** as the structural basis.
3. Use **Cursor’s medical conservatism and naming restraint** as the classification and retail-labelling basis.
4. Keep **phenotype** as a company/category-level strategic term.
5. Do **not** use the word **“phenotype”** on the retail Section 5 cards for the current 9 entities.
6. The next sprint should be a **backend/content registry sprint**, not a frontend sprint.

This is the most defensible position because it gives HealthIQ:
- a strong contract
- medically disciplined naming
- clear frontend rendering rules
- alignment with future commercial screening strategy
- protection against taxonomy drift

---

## 2. What to keep from Claude’s document

Claude’s draft is stronger on architecture, governance, and implementation-readiness.

These decisions should be kept:

### 2.1 The IDL must be a governed backend contract
Section 5 should not read directly from clusters or ad hoc frontend mappings. It should read from a dedicated Interpretation Display Layer that becomes the sole authority for user-facing pattern cards.

### 2.2 Keep the contract-field discipline
The following fields should form the basis of the IDL contract:

**Required**
- `internal_id`
- `scientific_class`
- `clinical_display_label`
- `retail_display_label`
- `subtitle`
- `why_it_matters`
- `severity_state`
- `supporting_biomarkers_summary`
- `frontend_allowed_term`
- `display_order_priority`
- `enabled_for_frontend`

**Optional**
- `supporting_systems_summary`
- `user_safe_description`
- `future_commercial_domain`
- `display_caveat`

### 2.3 Keep the rendering discipline for Section 5
Pattern cards should contain:
- retail display label
- subtitle
- severity/state
- supporting summary
- why-it-matters

They must not contain:
- internal ids
- raw biomarker values
- confidence numbers
- raw scientific class labels
- diagnostic claims

### 2.4 Keep the implementation sequencing
Claude is correct that the next implementation consequence is a backend/content sprint first, with frontend Section 5 blocked until that lands.

Working model:
- **BE-IDL-1** → create the Interpretation Display Layer contract and records
- **FE-R8** → frontend Section 5 surfacing only after BE-IDL-1 exists

---

## 3. What to keep from Cursor’s document

Cursor’s draft is stronger on classification restraint, medical naming discipline, and practical caution.

These decisions should be kept:

### 3.1 Use the conservative classification rule
Where an entity could plausibly fit more than one class, choose the weaker / more conservative claim.

That prevents:
- phenotype overreach
- retail overclaiming
- false scientific precision

### 3.2 Do not allow “phenotype” on the retail frontend for the current 9
This is the most important difference between the two drafts.

Cursor’s position is stronger:
- none of the current 9 should use “phenotype” on the retail Section 5 layer
- several are more honestly framed as:
  - risk constructs
  - organ-patterns
  - syndrome/states

This keeps the frontend medically safer and more commercially credible.

### 3.3 Keep the stronger explanation of why the layer is needed
Cursor’s framing is clearer:
- classification inconsistency
- lack of approved display labels
- lack of language governance

That should be retained in the final paper.

### 3.4 Keep the commercial alignment read of the current 9
Cursor is better at identifying which of the current 9 are strongest against the future screening strategy and which are secondary.

That matters because the IDL should not just be a naming exercise — it should help future product expansion align to:
- dysglycaemia / insulin resistance
- atherogenic cardiometabolic risk
- CKD / kidney risk
- MASLD / liver fibrosis risk
- integrated metabolic clustering
- iron deficiency

---

## 4. Where the two drafts disagree

The main disagreement is whether one of the current 9 should be allowed to use the word “phenotype” on the retail frontend.

### Claude’s position
- exactly one current entity (`ph_metabolic_early_ir_v1`) can use phenotype on day one

### Cursor’s position
- none of the current 9 should use phenotype on the retail frontend yet

### Recommended decision
Adopt **Cursor’s more conservative retail position**.

Reason:
- safer medically
- less likely to overclaim
- more consistent with the earlier terminology research
- easier to defend in B2C and clinical review

This does **not** mean abandoning phenotype strategically.

It means:
- phenotype remains the umbrella category language for HealthIQ
- but the current retail interpretation cards should use medically safer labels

---

## 5. Locked merged decisions

These should now be treated as the merged design lock.

### 5.1 The IDL is mandatory
Section 5 must not be implemented directly from the current cluster/system layer.

### 5.2 Four-class model remains
The IDL should support:

- `phenotype`
- `risk_construct`
- `organ_pattern`
- `syndrome_state`

No extra classes should be introduced without governance review.

### 5.3 Retail phenotype use is currently disallowed
For the current 9 entities:
- `frontend_allowed_term` should not permit phenotype language on the retail Section 5 cards

### 5.4 Company-level phenotype positioning remains valid
HealthIQ can still position itself externally as:
- phenotype-based metabolic interpretation
- phenotype-led blood interpretation

That is a strategic umbrella term, not a requirement that every retail card use the word phenotype.

### 5.5 Frontend naming must be dual-layered
Each record should have:
- `clinical_display_label`
- `retail_display_label`
- `subtitle`
- `why_it_matters`

This prevents:
- overly technical retail labels
- vague generic labels
- naming drift across surfaces

### 5.6 Generic buckets are not card labels
Labels such as:
- Metabolic Health
- Organ Health
- Heart Health

must not be used as Section 5 card labels.

They may only be used as higher-level grouping language if needed elsewhere.

### 5.7 Section 5 remains blocked until BE-IDL-1
Frontend Section 5 should not proceed until the contract and content layer exists.

---

## 6. Recommended merged classification posture for the current 9

At a high level, the merged position is:

- most current entities should be treated as **risk constructs**, **organ-patterns**, or **syndrome/states**
- none of the current 9 should use phenotype on the retail Section 5 cards
- the current 9 should be treated as a **governed interpretation set**, not a “9 phenotypes” set

That gives HealthIQ:
- category ownership at the company level
- medical restraint at the product level

---

## 7. Recommended next sprint

The next sprint should be:

## BE-IDL-1 — Interpretation Display Layer v1

This should be a backend/content sprint that:

1. defines the IDL contract
2. creates the governed records for the current 9
3. locks:
   - classification
   - clinical label
   - retail label
   - subtitle
   - why-it-matters
   - frontend_allowed_term
   - ordering
   - enabled flag
4. exposes the IDL to the results payload
5. adds validation/governance tests

This sprint should not:
- redesign the frontend
- change analytical logic
- invent new interpretation entities
- add Gemini dependence

---

## 8. Final recommendation to the team

The merged recommendation is:

- **Take Claude’s contract architecture**
- **Take Cursor’s classification conservatism**
- **Do not ship retail phenotype language for the current 9**
- **Build the IDL first**
- **Only then implement Section 5**

This is the strongest synthesis because it is:
- implementation-aware
- medically disciplined
- commercially aligned
- governance-safe

It avoids the two main risks:
- a weak, generic middle interpretation layer
- a medically overclaimed phenotype layer

The correct next move is therefore not more frontend work.

It is to build the governed Interpretation Display Layer properly.
