# HealthIQ AI Wave 1 Health Systems Subsystem Medical Review

## 1. Executive verdict

The current Wave 1 subsystem model is fit for v1 only with substantial changes.

Cardiovascular health and Blood sugar control can support limited visible subsystem structure, but only if weak one-marker constructs are downgraded to contextual evidence rather than shown as full sub-systems. Liver health should not be visibly split into scored sub-systems in v1; the biology is too heterogeneous, and the current marker groups mix injury, cholestatic/excretory context, and chronic synthetic context in a way that will look cleaner in UX than it is medically. The safest v1 is: one strong scored cardiovascular sub-system, one strong scored blood-sugar sub-system, and a flat liver card with grouped evidence rather than scored liver sub-systems.

The biggest trust risk is not that the biology is wrong; it is that the UI may imply more specificity than the biomarker set can support. CRP alone is too non-specific to stand up a “vascular strain” subsystem, homocysteine alone is too thin and not routinely recommended for general cardiovascular risk assessment, triglycerides alone are too weak for a visible insulin-resistance subsystem, and “liver processing context” is not a clean biological subsystem label for albumin + ALP + bilirubin.

## 2. Review principles

I used five medical/product principles.

First, a visible subsystem should correspond to a recognisable biological process or clinical pattern, not just a small pile of available markers. Liver blood tests are a good example: ALT/AST mostly reflect hepatocellular injury, ALP with bilirubin suggests cholestatic/excretory patterning, and albumin is a delayed, non-specific synthetic marker. That is why “liver processing context” is too loose as a named subsystem.

Second, one-marker subsystems are usually unsafe unless the marker is itself highly canonical for the construct being shown. HbA1c can legitimately anchor a glycaemic exposure subgroup; CRP alone cannot legitimately anchor a vascular subsystem; homocysteine alone is biologically relevant but too thin and too non-routine for a visible cardiovascular subsystem in a premium consumer product.

Third, marker roles must be explicit. A marker that helps score direction is not the same as a marker that increases confidence, adds context, or is optional for deeper refinement. Without this distinction, the cards will imply false completeness. HbA1c and fasting glucose are core glycaemic markers; fasting insulin, triglycerides, and HDL are useful context for insulin resistance but are not equivalent to direct glycaemic anchors.

Fourth, risk markers should not be presented as diagnoses. hsCRP is linked to cardiovascular risk and can act as a risk-enhancing or inflammatory context marker, but it is non-specific. Homocysteine is associated with vascular risk in some literature, but current guidance does not support it as a routine general-population cardiovascular risk test.

Fifth, missing markers should only be shown as missing if their absence truly reduces confidence in something the card is claiming today. Optional deeper markers should not appear as if the user has failed to provide required evidence.

## 3. Cardiovascular health review

### Subsystem label assessment

“Lipid transport” should be renamed. With LDL-C, HDL-C, triglycerides, total cholesterol, and TC:HDL ratio, what you have is an atherogenic lipid or lipoprotein-risk pattern, not a true transport subsystem in the mechanistic sense. A safer visible label is:
- Atherogenic lipid pattern
- or Atherogenic lipid burden

“Homocysteine pathway” should be hidden or deferred as a visible subsystem. It is medically legitimate as a contextual vascular-risk signal, but a homocysteine-only visible subsystem is too thin for v1 and too easy to overinterpret. Current clinical guidance does not support homocysteine as a routine general-population cardiovascular risk marker.

“Vascular strain context” should also be hidden or deferred as a visible scored subsystem if it is supported only by CRP. hsCRP has cardiovascular risk value; generic CRP is even less specific. A CRP-only subsystem reads as more vascularly specific than the biology allows. This should be treated as inflammatory vascular-risk context, not a scored subsystem.

### Marker membership

The current lipid set is biologically coherent for a v1 atherogenic lipid pattern. LDL-C, HDL-C, triglycerides, and a ratio derived from them are reasonable score-driving markers. Total cholesterol is usable, but if LDL-C, HDL-C, and TC:HDL ratio are already in play, it should be prevented from double-counting the same biology. ApoB, non-HDL-C, and Lp(a) would strengthen the domain later, but they are not required for a safe v1 lipid subsystem.

CRP or hsCRP should not be allowed to create a standalone visible vascular subsystem by itself. It is better used as contextual vascular-inflammatory evidence or confidence support around a broader cardiovascular card.

Homocysteine belongs in the cardiovascular card as an optional contextual or advanced marker, not as a first-wave scored visible subsystem.

### Marker roles

Recommended roles:
- Score contributors: LDL-C, HDL-C, triglycerides, TC:HDL ratio
- Confidence/context markers: hsCRP, homocysteine
- Optional deeper markers: ApoB, non-HDL-C, Lp(a)

### Concerns

The current cardiovascular model is the strongest of the three domains, but it will become misleading if it visually implies three equally robust sub-systems. At present, only the lipid subsystem is clearly strong enough to score visibly. The other two are medically better treated as contextual evidence layers.

### Recommended v1 model

Top-level card label: Cardiovascular health

Show visible sub-systems: Yes, but only one scored subsystem in v1:
- Atherogenic lipid pattern

Show as unscored contextual evidence underneath:
- Inflammatory vascular context, if hsCRP is available
- Homocysteine context, if homocysteine is available

Wording caution:
Do not imply direct cardiac-function assessment. Keep the clinical meaning explicitly cardiometabolic / vascular risk oriented.

## 4. Blood sugar control review

### Subsystem label assessment

“Glycaemic control” is medically appropriate, but for consumer-facing UX “Long-term blood sugar” is clearer and safer if HbA1c is the main anchor.

“Insulin and metabolic context” should be renamed and deferred unless the marker set is broadened. With triglycerides present and insulin missing, it is not a robust visible subsystem. The best name for the underlying idea is “Insulin-resistance context,” but it should only become visible when supported by a better constellation such as fasting glucose plus triglycerides/HDL and ideally fasting insulin or another insulin-resistance surrogate.

### Marker membership

HbA1c alone is medically coherent for a glycaemic-exposure subsystem. ADA recognises A1c or plasma glucose for diabetes classification, and a normal or non-diagnostic A1c does not fully exclude glucose-defined dysglycaemia. That means HbA1c can anchor a subsystem, but glucose meaningfully improves completeness.

Triglycerides can support an insulin-resistance context, particularly when paired with HDL or glucose-derived indices such as TG/HDL or TyG, but they should not carry a visible “insulin context” subsystem on their own. TG/HDL-based surrogates are useful but imperfect and population dependent.

### Marker roles

Recommended roles:
- Score contributors: HbA1c, fasting glucose
- Confidence/context markers: fasting insulin, triglycerides, HDL-C
- Optional deeper markers: C-peptide, OGTT-derived data, TyG or TG/HDL derived metrics if governed

### Concerns

The current blood sugar score risks overstating “insulin balance” if HbA1c is present but glucose and insulin are absent. HbA1c can justify a glycaemic subsystem; it cannot, by itself, justify a confident insulin-resistance story. Triglycerides alone are insufficient to rescue that gap.

### Recommended v1 model

Top-level card label: Blood sugar control

Show visible sub-systems: Yes, but only one scored subsystem in v1:
- Long-term blood sugar
  - anchored by HbA1c
  - strengthened by fasting glucose if available

Keep unscored or hidden for now:
- Insulin-resistance context
  - only promote when fasting glucose plus triglycerides/HDL are present, and ideally fasting insulin

Wording caution:
Do not say “sugar and insulin balance” if only HbA1c is present. Use wording that tracks the actual evidence, such as “long-term blood sugar pattern.”

## 5. Liver health review

### Subsystem label assessment

“Liver enzyme pattern” is acceptable as a temporary evidence-group label, but medically it is strongest when it includes AST and ALT together. ALT + GGT is informative but not the full canonical hepatocellular pattern. A safer v1 label is:
- Liver enzyme pattern
not
- Hepatocellular injury pattern
unless AST is also present.

“Liver processing context” should be merged or hidden. Albumin, ALP, and bilirubin do not form one neat subsystem. Albumin is a delayed and non-specific synthetic marker; ALP points toward cholestatic patterning but is not liver-specific without GGT support; bilirubin is an excretory/cholestatic marker and, if elevated, can also reflect hemolysis rather than liver disease.

### Should Liver health be split in v1?

My answer is: no, not into visible scored sub-systems.

Liver is the clearest case where marker groups are reasonable but scored sub-systems are premature. The safest v1 liver card is:
- one flat Liver health score
- with grouped evidence beneath it, not scored sub-systems

If you must group the evidence, use:
- Enzyme pattern: ALT, AST, GGT
- Supportive liver context: ALP, bilirubin, albumin

But do not score those separately in v1. The biology is too mixed, and the UI would overstate certainty.

### Marker membership

For a safe blood-led liver card:
- Core top-level markers: ALT, AST, ALP, bilirubin
- Helpful confidence markers: GGT, albumin
- Advanced/nice-to-have: INR/PT, platelets, AST/ALT-derived ratios, fibrosis-related derived scores when governed

AST should be treated as a genuine missing-for-confidence marker if ALT is present and you are showing an enzyme-pattern interpretation. GGT is helpful when ALP is abnormal because it helps confirm hepatic/biliary origin. Albumin is useful contextual information, but it should not drive a v1 liver subsystem score.

### Bilirubin / Total bilirubin issue

In this context, bilirubin and total bilirubin should be treated as one concept unless the panel truly distinguishes total, direct, and indirect bilirubin. Do not show both as if they are separate missing markers.

### Recommended v1 model

Top-level card label: Liver health

Show visible sub-systems: No

If grouped evidence is shown, use unscored evidence groups only:
- Liver enzyme pattern
- Supportive liver context

Wording caution:
The card must remain explicitly blood-based and strain-oriented. Do not imply that routine liver bloods provide a full assessment of liver function or a diagnosis of liver disease. Liver tests are a mix of injury, cholestatic, and synthetic-context signals, not a single unified subsystem.

## 6. Thin subsystem assessment

| Domain | Subsystem | Current markers | Medical adequacy | Recommendation |
|---|---|---|---|---|
| Cardiovascular | Lipid transport | HDL-C, LDL-C, TC:HDL, total cholesterol, triglycerides | Adequate for a visible v1 lipid-risk subsystem | Keep, but rename to “Atherogenic lipid pattern” |
| Cardiovascular | Homocysteine pathway | Homocysteine | Too thin for a visible scored subsystem | Hide/defer; keep as contextual or advanced marker |
| Cardiovascular | Vascular strain context | CRP | Inadequate as a visible subsystem; too non-specific on its own | Hide/defer; use as inflammatory vascular-risk context only |
| Blood sugar | Glycaemic control | HbA1c; glucose missing | Adequate for a limited glycaemic subsystem, but confidence incomplete | Keep as one scored subsystem; show glucose as helpful missing-for-confidence marker |
| Blood sugar | Insulin and metabolic context | Triglycerides; insulin missing | Too thin for visible subsystem | Rename conceptually to “Insulin-resistance context” and hide/defer unless marker support improves |
| Liver | Liver enzyme pattern | ALT, GGT; AST missing | Partial only | Do not score separately in v1; show as grouped evidence if needed |
| Liver | Liver processing context | Albumin, ALP, bilirubin; total bilirubin missing | Not a coherent single subsystem | Merge/hide; use as supportive liver context, not a scored subsystem |

## 7. Proposed marker role taxonomy

Yes — this is needed before the UX becomes trustworthy.

Recommended taxonomy:

1. Score contributor  
A marker that directly drives the direction or magnitude of the score.
- Examples: LDL-C in a lipid subsystem, HbA1c in a glycaemic subsystem, ALT in a liver-strain card

2. Confidence support  
A marker that strengthens certainty or sharpens the pattern, but should not dominate score direction by itself.
- Examples: fasting glucose alongside HbA1c; AST alongside ALT; GGT when ALP is abnormal

3. Context marker  
A marker that changes interpretation or narrative but should not create the visible subsystem alone.
- Examples: hsCRP in cardiovascular context, homocysteine in cardiovascular context, albumin in liver context

4. Missing-for-confidence  
A marker whose absence should reduce confidence in a claim the card is making today.
- Examples: fasting glucose when showing a glycaemic subsystem; AST when showing a liver enzyme-pattern explanation

5. Optional deeper marker  
A marker that meaningfully refines the domain when available but should not be shown as “missing” on standard panels.
- Examples: ApoB, Lp(a), fasting insulin, C-peptide, INR/PT

Without this taxonomy, users will not know whether a marker helped score the card, merely increased confidence, or was optional advanced evidence. That is a direct trust problem.

## 8. Recommended v1 subsystem model

| Domain | Show subsystems? | Recommended subsystem/group label | Core markers | Confidence/context markers | Missing markers to show | Markers to defer |
|---|---|---|---|---|---|---|
| Cardiovascular health | Yes | Atherogenic lipid pattern | LDL-C, HDL-C, triglycerides, TC:HDL ratio | hsCRP, homocysteine | None required if core lipid set is present | ApoB, Lp(a), visible homocysteine subsystem, visible CRP-only vascular subsystem |
| Cardiovascular health | No scored subsystem | Inflammatory vascular context (unscored evidence only) | None as a standalone v1 core | hsCRP | Do not show as required missing | Standalone CRP-only score |
| Cardiovascular health | No scored subsystem | Homocysteine context (unscored evidence only) | None as a standalone v1 core | Homocysteine | Do not show as required missing | Standalone homocysteine score |
| Blood sugar control | Yes | Long-term blood sugar | HbA1c | Fasting glucose | Fasting glucose | Insulin as visible missing requirement |
| Blood sugar control | No scored subsystem in v1 | Insulin-resistance context | Fasting glucose + triglycerides + HDL-C if available | Fasting insulin, ALT/GGT as broader metabolic context | None in basic v1 | Standalone TG-only or TG+missing-insulin subsystem |
| Liver health | No | Flat card only | ALT, AST, ALP, bilirubin | GGT, albumin | AST if missing from an enzyme-pattern explanation; GGT if ALP is abnormal | Separate scored “processing” subsystem |
| Liver health | Evidence groups only, not scored | Liver enzyme pattern / Supportive liver context | ALT + AST for enzyme pattern; ALP + bilirubin for supportive context | GGT, albumin | Only markers that genuinely improve confidence in a shown group | Total bilirubin as a second “missing” marker if bilirubin already represents total bilirubin |

## 9. Risks if unchanged

- Users will over-trust thin subsystems that look medically precise but are actually one-marker constructs.
- CRP-only “vascular strain” will read as vascular-specific when CRP is fundamentally non-specific.
- Homocysteine-only visible scoring will suggest routine cardiovascular significance stronger than current practice supports.
- HbA1c-only blood sugar scoring may imply insight into insulin balance that the evidence set does not actually provide.
- Liver sub-scores will look cleaner than the biology, because injury, cholestatic/excretory context, and synthetic context are being mixed.
- If context markers appear to have “scored” the subsystem, users will not understand what actually drove the result.
- If optional advanced markers are shown as missing, the product will imply false incompleteness and undermine trust.
- If bilirubin and total bilirubin are both shown, users will think two separate liver concepts are missing when the issue may just be naming duplication.

## 10. Recommended next step

Hand this back to the architecture lead as a medical target model for v1.

Specifically:
1. collapse visible scored subsystems to only those that are biologically coherent and sufficiently supported
2. adopt an explicit marker-role taxonomy before subsystem UX is finalised
3. keep cardiovascular visible splitting limited to the lipid subsystem in v1
4. keep blood sugar visible splitting limited to a glycaemic subsystem in v1
5. keep liver flat in v1, with grouped evidence only if needed
6. resolve bilirubin/total bilirubin as an SSOT normalisation issue
7. only after that, run the repo-grounded implementation audit against this target model to determine what is already deliverable and what still needs governed/backend work

That sequence gives you a medically coherent subsystem architecture first, then an honest implementation plan second.
