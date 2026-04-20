# HealthIQ AI — AB-Specific Questionnaire Specification v1

## Purpose

This document defines the **short-form, high-value questionnaire** to accompany the AB case for gold-standard narrative analysis.

Its purpose is not to gather every potentially interesting health detail.
Its purpose is to collect the **smallest set of contextual inputs that materially change interpretation** of the blood panel and strengthen the personalised narrative.

This spec is intentionally narrower than the full website questionnaire.
It is designed for:
- sharper interpretation
- stronger lifestyle-to-biology linkage
- better longitudinal comparison between panel 0 and the later panel
- less noise in the narrative layer

---

## Design rule

Every question in this spec must earn its place by doing at least one of the following:

- materially changing biomarker interpretation
- explaining tension between reported lifestyle and observed biology
- helping distinguish adaptation from dysfunction
- sharpening longitudinal comparison between panel 0 and the later panel
- improving consultation-grade personalisation

If a question does not do one of those jobs, it should not be included.

---

## Section 1 — Core identity and interpretation anchors

These fields materially change cardiometabolic, renal, hormonal, and body-composition interpretation.

### Required
- age
- biological sex
- height
- weight
- waist circumference

### Strongly preferred
- blood pressure reading, if known
  - systolic
  - diastolic

### Optional
- body fat %, if known
- lean mass %, if known

### Why this section matters
These fields help interpret:
- cardiometabolic risk context
- renal markers
- hormonal context
- whether muscularity/body composition may be affecting biomarkers
- whether lifestyle claims are plausible against body status

---

## Section 2 — Medications and substances that can alter interpretation

The current website form is too blunt here. For AB-style interpretation, exact medication and supplement context matters.

### Required
- Are you currently taking any prescription medications?
  - yes / no
- If yes, list them

### Must explicitly ask about
- cholesterol-lowering medication (e.g. statin/ezetimibe)
- blood pressure medication
- diabetes / glucose-lowering medication
- thyroid medication
- testosterone / TRT / anabolic agents
- corticosteroids / regular steroid use
- acid-suppressing medication / PPI use

### Supplements — required
Ask which of the following are taken regularly and ideally record dose if known:
- vitamin D
- vitamin B12
- folate / methylfolate
- iron
- omega-3 / fish oil
- magnesium
- zinc
- creatine
- probiotics
- multivitamin
- other

### Why this section matters
These inputs can materially affect interpretation of:
- lipids
- B12 / folate / homocysteine
- vitamin D
- testosterone and related hormones
- thyroid markers
- creatinine / eGFR
- inflammatory or compensatory patterns

---

## Section 3 — Alcohol, smoking, caffeine

### Required
- smoking status
  - never
  - former
  - current occasional
  - current daily
- alcohol intake per week
  - ideally in units or drinks
- drinking pattern
  - spread evenly
  - mostly weekends
  - binge episodes
  - rarely but heavily
- caffeine intake per day

### Why this section matters
These inputs materially change interpretation of:
- lipids
- liver enzymes
- urate
- blood pressure context
- sleep quality and recovery
- macrocytosis / B-vitamin interpretation
- cardiovascular narrative tone

---

## Section 4 — Diet, fasting, hydration

### Required
- dietary pattern
  - omnivore / Mediterranean / low-carb / ketogenic / plant-based / mixed / other
- typical fasting window
- sugary drinks intake
- fruit and vegetable intake
- average fluid intake

### Strongly preferred
- processed food frequency
- protein intake emphasis
  - low / moderate / high
- any intentional calorie restriction or dieting

### Why this section matters
These inputs materially affect interpretation of:
- HbA1c and glucose regulation context
- lipid patterning
- urea and urate context
- homocysteine and B-vitamin story
- hydration-sensitive renal markers
- whether the bloods match the declared lifestyle strategy

---

## Section 5 — Exercise, activity, and body-performance context

### Required
- vigorous exercise days per week
- resistance training days per week
- sitting time / sedentary time

### Strongly preferred
- general activity level outside formal exercise
- would you describe yourself as muscular / strength-trained?
- creatine use (if not already captured above)

### Longitudinal requirement
Ask explicitly:
- compared with panel 0, has your exercise changed in the last 4 months?
  - no real change
  - increased cardio
  - increased resistance training
  - reduced exercise
  - changed training intensity
  - recovering from illness/injury

### Why this section matters
These inputs materially affect interpretation of:
- creatinine / eGFR
- testosterone framing
- recovery / stress biology
- lipids
- glucose handling
- whether a given biomarker pattern may reflect adaptation rather than pathology

---

## Section 6 — Sleep and recovery

### Required
- sleep hours per night
- sleep quality
- snoring / suspected sleep apnoea / diagnosed sleep apnoea

### Strongly preferred
- sleep schedule consistency
- waking refreshed vs unrefreshed
- recovery after exertion

### Why this section matters
These inputs materially affect interpretation of:
- cortisol and stress framing
- glucose and cardiometabolic strain
- fatigue and recovery narratives
- inflammatory burden interpretation
- mismatch between “good habits” and persistent biological strain

---

## Section 7 — Stress and current life load

### Required
- average stress level
- any major life stressors in the past 6 months

### Strongly preferred
- primary stress management method
- whether stress has improved, worsened, or stayed similar since panel 0

### Why this section matters
These inputs materially affect interpretation of:
- cortisol-related framing
- sleep disruption context
- recovery and fatigue
- why an apparently healthy routine may not yet be translating into improved biology

---

## Section 8 — Key symptoms that help the bloods “land”

This should stay tight. Only include symptoms that help connect biology to lived experience.

### Required
- current energy pattern
- fatigue
- brain fog
- digestive issues
- sleep problems
- mood changes

### Male-specific strongly preferred
- libido / sexual function
- perceived change in strength or muscle mass

### Longitudinal requirement
- any new symptoms since panel 0?
- any symptoms that improved since panel 0?

### Why this section matters
Symptoms stop the report feeling like sterile analytics and help prioritise what matters most in the narrative.

---

## Section 9 — Personal and family history that materially changes the story

### Required
- diagnosed high blood pressure
- diagnosed high cholesterol
- diagnosed diabetes / prediabetes
- thyroid disorder
- kidney disease
- liver disease
- cardiovascular disease

### Family history — required
- premature cardiovascular disease in immediate family
- type 2 diabetes / metabolic syndrome in immediate family

### Why this section matters
These inputs sharpen:
- cardiometabolic interpretation
- vascular risk framing
- how aggressively a lipid or glucose story should be interpreted
- whether a pattern is more likely incidental or part of a family tendency

---

## Section 10 — The most important longitudinal section

This section is critical for creating a joined-up returning-customer narrative.

### Required
Ask explicitly:
**Since panel 0, what did you intentionally change?**

Include:
- diet
- fasting pattern
- alcohol intake
- smoking
- exercise
- weight
- supplements
- medications
- sleep
- stress
- hydration

### Required follow-up
For each intentional change, ask:
- started / stopped / increased / reduced
- roughly how long you maintained it
- whether you felt better, worse, or unchanged

### Why this section matters
This is what allows the second report to say not just:
- what changed in the bloods

but:
- whether the biology appears to be responding to the user’s effort
- whether the user’s intended intervention is visible yet
- whether one part of the body responded while another still lagged behind

This is one of the most commercially valuable parts of the HealthIQ experience.

---

## Questions to exclude from the AB-specific short form

These questions may have value in a broader platform, but they are not core for this gold-standard AB narrative task unless a specific signal demands them.

### Exclude / de-prioritise
- full name
- email address
- phone number
- country / state
- balance ability
- stair climbing ability
- push-up count
- grip strength squeeze test
- memory changes
- family lifespan
- family cancer history
- antibiotic courses in past 2 years
- migraines
- recent infections unless current immune/inflammatory findings need it

### Reason
These questions add breadth, but not enough interpretation value for this AB-specific narrative exercise.

---

## Minimum viable AB questionnaire

If you want the shortest possible useful version, ask only:

1. age, sex, height, weight, waist, BP
2. exact medications
3. exact supplements
4. smoking, alcohol, caffeine
5. dietary pattern, fasting, sugary drinks, hydration
6. exercise, resistance training, sedentary time
7. sleep, snoring/apnoea, stress
8. key symptoms
9. personal/family cardio-metabolic history
10. what changed intentionally since panel 0

That is the minimum set most likely to produce a genuinely personalised, consultation-grade AB narrative.

---

## Final design principle

The AB-specific questionnaire must help the report answer questions like:

- does the blood panel fit the user’s declared lifestyle?
- where does the biology support the user’s effort?
- where does it contradict it?
- what appears improved since panel 0?
- what remains unchanged despite effort?
- what hidden tension or trade-off is still present?

If the questionnaire cannot help answer those questions, it is too long, too noisy, or pointed at the wrong things.
