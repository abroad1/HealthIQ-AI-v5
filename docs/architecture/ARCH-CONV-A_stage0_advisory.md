# ARCH-CONV-A — Stage 0 Advisory

Work ID: ARCH-CONV-A-STAGE0. Date: 2026-07-27. Runtime change: NONE.

Three packages (A, B, C) remain the minimum safe structure for the ratified GO decision. Package A is scoped, its target count verified against repository reality (not the carried-forward estimate), and its internal wave plan, STOP gates, and legacy-retirement policy are designed. Nothing is implemented, compiled, deleted, or promoted by this work.

Verified facts that change the prior estimate: the registry holds exactly 41 targets, not "approximately 36." Five are already compiled and ratified (the proven pilot). Package A's actual remaining scope is 36 targets across seven internal medical-review waves, not a flat file count.

Two structural findings matter most for how Package A must be sequenced. First, the registry that decides which signals attempt root-cause compilation has no way to see that a signal produces more than one runtime frame — three pilot signals already do, invisibly, and any newly migrated signal that grows a second frame will hit the same situation. This is handled safely today by an existing fail-closed guard, but every wave's identity-closure step must declare expected frame count up front rather than discovering it during compilation. Second, exactly one legacy file is already serving two competing identities at once — a fully-legacy signal and a mostly-compiled one share the same source file. That case is sequenced as its own first wave because it is the one place today where legacy and compiled authority already coexist for overlapping medical content, and because a shared file cannot be safely retired while one of its two dependents is still unconverted.

A third finding is a data-quality flag, not an architecture defect: a second, older governance register still contradicts the current pilot state for one signal and cites a stale filename for another. It should not be consulted as authority for any wave-scoping decision, and refreshing it is folded into the very first internal phase rather than made a separate package.

One identity question needs resolving before any medical review begins on the hepatic wave: two separately registered signals may represent the same clinical concept (bilirubin elevation) under two different names, each with its own legacy file and no research spec yet for either. Compiling both without resolving that first risks manufacturing a new internal duplicate authority.

Medical-review capacity is the real pacing constraint, not architecture. Sixteen of the 36 remaining targets already have a matching research document and just need review and compilation — these are sequenced early to bank progress. Eleven have no research document at all yet; that is a research-intake dependency the programme must schedule, not a Package A scope gap. Eight sit in between, with a candidate document that needs confirming or rejecting before it can be trusted.

The package is classified HIGH risk, MIXED change type, two-phase execution, consistent with prior expectation. It requires the strategic Stage B mode already anticipated, because wave sequencing and medical-review capacity allocation are programme-level decisions, not code-discovery questions Stage D hardening could resolve on its own.

Recommendation: proceed to GPT architectural review and Anthony ratification of the full Package A design pack before any formal Automation Bus prompt is authored. No blocker in this pack requires new research or new engineering before ratification can occur — the open research gaps (11 missing specs, 8 unconfirmed matches, 1 identity duplication) are scheduled inside the wave plan, not blockers to accepting the plan itself.
