# HealthIQ Phase 1 Launch Readiness / UAT Checklist

## Purpose

This checklist is intended to support the final pre-launch validation of the HealthIQ Phase 1 product.

It is designed to confirm that the current product is not just built, but usable as a real end-to-end experience in a live-like environment.

It covers:
- environment readiness
- end-to-end user journey testing
- wedge-metrics verification
- trust/launch-posture checks
- go/no-go decision support

---

## A. Environment readiness

### Deployment
- latest approved code is deployed
- frontend and backend are on the intended environment
- environment variables are set correctly
- no local-only configuration is still required for the core flow

### Auth
- register works
- login works
- logout works
- protected routes redirect correctly when signed out
- signed-in users land back in the right place after auth

### Persistence
- database is connected
- analyses persist correctly
- historical results can be retrieved after re-login
- no environment mismatch exists between write path and read path

### Analysis runtime
- upload/parse path works
- analysis start works
- analysis completes successfully
- results payload returns correctly
- clinician report is present when expected
- narrative summaries are present or truthfully absent
- wedge event endpoint is reachable

### Operational dependencies
- support inbox is real and monitored
- Privacy page is live
- Terms page is live
- Contact page is live
- links to all three work from landing and app shell

---

## B. End-to-end user acceptance test

## Journey 1 — New user to results

### Registration and login
- user can register successfully
- user can log in successfully
- user lands in the correct post-auth flow

### Upload and analysis
- user can reach upload page
- user can upload or paste results successfully
- parse step completes
- questionnaire step completes
- analysis starts
- analysis completes
- results page loads

### Results review
- hero interpretation displays
- trust/data-quality strip displays
- biomarker/system sections display
- narrative summaries display correctly, or a truthful empty/degraded state appears
- clinician report tab displays correctly

### Results actions
- JSON export works
- share action works if supported in that environment
- no misleading “clinician report download” behaviour is implied unless it actually exists

---

## Journey 2 — Return user / history continuity

### Re-login
- user can log out
- user can log back in
- dashboard loads
- reports/history loads

### Historical access
- saved analyses are visible
- user can reopen a historical analysis
- canonical route works correctly
- historical results render correctly
- clinician report remains accessible on reopened result
- narrative state remains truthful on reopened result

---

## Journey 3 — Error and degraded states

### Upload / parse failures
- invalid upload shows calm, understandable feedback
- parse failure does not break the session
- user can retry

### Analysis failure
- failed analysis shows understandable feedback
- no broken or infinite loading state remains
- user can recover or retry appropriately

### Narrative degraded states
- narrative disabled / unavailable / no accepted summaries states are truthfully differentiated where supported
- lack of narrative does not imply lack of analysis result

### Auth/session issues
- signed-out access to protected pages redirects correctly
- expired session behaviour is understandable
- historical result reopening does not silently fail without explanation

---

## C. Wedge metrics verification

Confirm that the measurable-now events are actually being emitted for:

- registration completed
- registration failed
- login success
- login failed
- upload started
- upload parse completed
- upload parse failed
- questionnaire submitted
- analysis started
- analysis completed
- analysis failed
- results viewed
- clinician report viewed
- results export JSON clicked
- results share link clicked
- historical result reopened

Also confirm:
- deferred events are not being faked
- payloads contain no raw biomarker values
- payloads contain no questionnaire answers
- payloads contain no clinician-report narrative text

---

## D. Trust and launch posture check

Confirm the launch-facing product still matches the agreed posture:

- UK-first B2C posture is reflected honestly
- no HIPAA / bank-level / medical-grade overclaim has reappeared
- product remains non-diagnostic in public-facing language
- clinician report is positioned as something to support clinical discussion, not replace it

---

## E. Go / no-go decision check

You are ready for Phase 1 launch only if:

- end-to-end user journey works
- historical continuity works
- clinician report is viewable in the real journey
- trust/legal/contact surfaces are live
- ops artifacts exist and open items are known
- wedge metrics are being captured
- no critical blocker remains in auth, persistence, or analysis runtime

---

## F. Open-items log for signoff

Before go-live, record:
- known non-blocking issues
- operational dependencies still owned by humans
- what is explicitly deferred beyond Phase 1
- who signs off product
- who signs off ops/trust
- who owns launch-day monitoring
