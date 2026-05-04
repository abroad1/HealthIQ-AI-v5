# HealthIQ AI — Platform IA Boundary Note

Version: v1
Scope: Brief boundary-setting note only
Status: Companion note to results-page UX package

---

## 1. Purpose

This note defines the high-level platform journey boundaries around the results experience.

It is intentionally brief.
It is not a full redesign of the whole application.
Its purpose is to stop the results-page work from drifting into a disconnected UX island.

---

## 2. High-Level Platform Journey

The platform journey is best understood as five connected areas:

1. Public site
2. Auth
3. Upload
4. Results
5. Account / history

---

## 3. Public Site

Purpose:
- explain the product
- build trust
- convert interest into sign-up or trial

Primary user questions here:
- what is this product?
- why is it better than a standard blood report?
- can I trust it?
- what do I do next?

Boundary note:
The public site is a sales and trust surface.
It is not part of the results experience itself.

---

## 4. Auth

Purpose:
- establish identity
- secure access
- support consent and account ownership

Boundary note:
Auth is the gateway into the private application.
It should feel secure and low-friction, but it is not part of the results-page design package.

Key architectural question to resolve later:
- whether upload starts only after login or whether a limited pre-auth upload flow is allowed

---

## 5. Upload

Purpose:
- submit a new blood panel
- collect any required supporting context
- confirm processing state

Boundary note:
Upload is the transition from account activity to analysis activity.
Its job is operational: get clean data into the system and move the user toward results.

It should connect clearly to:
- prior uploads / history
- processing state
- next-step routing into the results page

---

## 6. Results

Purpose:
- present the interpreted output of a completed analysis
- communicate the main biological story
- support evidence inspection
- provide optional deeper analysis

Boundary note:
This is the current main design focus.

The results area is not the user’s full account home.
It is the specific interpreted-view experience for one analysis.

---

## 7. Account / History

Purpose:
- act as the user’s secure home area
- hold profile data
- show prior tests / analyses
- provide access back into previous results

Expected contents later:
- age / sex / profile details
- weight / other stored context fields where appropriate
- test history
- saved analyses
- account settings / preferences as needed

Boundary note:
This area should own continuity over time.
The results page should own interpretation for one analysis.

---

## 8. Relationship Between Results and Account / History

Recommended boundary:

- Account / history answers: what analyses do I have?
- Results answers: what does this specific analysis mean?

That boundary should stay clean.
The results page should not become a bloated account dashboard.
The account area should not try to inline the full interpretive experience for every past test.

---

## 9. Current Design Focus

The active design focus remains:
- the results-page UX / design package only

The wider platform journey is acknowledged here only so that:
- the results experience has proper context
- adjacent future work can be sequenced cleanly
- we do not accidentally redesign public site, auth, upload, and account flows inside the results deliverable

---

## 10. Practical Sequencing Recommendation

Recommended order of design work:

1. results-page UX/design package
2. light platform IA note
3. later, separate focused workstreams for:
   - public site / hero experience
   - auth and secure-area entry
   - upload flow
   - account / history area

---

## 11. Summary

Yes, the overall user journey is broadly:

public site -> auth -> upload -> results -> account/history

But the current deliverable should stay tightly focused on the results experience.
This note exists only to set boundaries around that work, not to create a second major design project at this stage.
