Yes. Use these instead.

## 1. Start-of-sprint preflight

```text
Run repo preflight:
- check current branch
- verify required branch from latest_cursor_prompt.md
- create it if missing
- confirm working tree is clean
- inspect stashes and relevance
- summarise any blockers
- give exact next step

Do not execute anything destructive.
```

## 2. Working tree + stash triage

```text
Run full repo preflight and resolution plan:
- inspect working tree
- classify all changes (keep / discard / stash / review)
- inspect stashes and relevance

Output:
- what I should do with each change
- whether repo is safe to proceed
- exact next step
- exact commands if needed

Do not execute anything.
```

## 3. “What stage am I at?”

```text
Based on current repo state, tell me:
- what stage I am at (pre-start / in-progress / ready for finish / ready for merge)
- any governance violations
- exact next step
```

## 4. Audit review

```text
Review the latest audit summary and gate outputs.

Tell me:
- repo-grounded summary
- architectural implications
- determinism / drift risk
- control-plane implications
- whether this is safe to merge, subject to human approval
- exact next step

Do not claim final authority.
```

## 5. Merge preflight

```text
Run full merge preflight:
- confirm branch alignment
- inspect working tree
- classify all changes (keep / discard / stash / review)
- inspect stashes and relevance
- check recent commits
- assess merge readiness

Output:
- blockers
- risks
- recommendation
- exact next step
- exact commands if needed

Do not execute anything destructive.
```

## 6. “Give me the exact commands”

```text
Prepare the exact local commands to:
- commit current work if needed
- merge this branch into main safely
- preserve deterministic workflow discipline

Do not execute.
```

## 7. Diff / PR sanity check

```text
Analyse current branch vs main:
- summarise what changed
- classify as CONTENT / BEHAVIOUR / MIXED
- flag any behavioural drift
- flag any HIGH-risk areas
- tell me if this looks mis-scoped for the intended sprint
```

## 8. No-op check

```text
Check repo reality against intended change:
- does the underlying problem still exist?
- is this sprint now a no-op?
- should it be cancelled, narrowed, or re-scoped?
```

## 9. Authority-path inspection

```text
Inspect authority paths for this change:
- identify source-of-truth files
- identify runtime loaders, validators, or consumers
- check for duplicate authority creation
- flag any architectural or control-plane violations
```

## 10. One-shot operational prompt

```text
Run full repo workflow:
- check branch alignment
- inspect working tree
- classify all changes (keep / discard / stash / review)
- inspect stashes and relevance
- review audit summary if present
- assess merge readiness

Output:
- current repo state
- risks
- recommendation
- exact next step
- exact commands if needed

Do not execute destructive actions.
```

## 11. Branch creation from latest cursor prompt

```text
Read latest_cursor_prompt.md and:
- identify the required branch
- check whether it exists locally
- create it if missing
- confirm I am on the correct branch
- report any blockers

Do not modify anything else.
```

## 12. Stash investigation only

```text
Inspect all stashes:
- summarise each stash
- identify likely branch or workstream relevance
- tell me which are probably related to current work
- recommend keep / apply later / drop candidate

Do not apply, pop, or drop anything.
```

## 13. Commit readiness

```text
Inspect current changes and tell me:
- what belongs in this commit
- what should not be included
- whether the change set is cleanly scoped
- exact next step
- exact commit commands if appropriate

Do not execute.
```

## 14. Post-finish review

```text
Review the repo after kernel finish:
- inspect latest audit summary
- inspect gate evidence if present
- inspect working tree
- assess whether anything still blocks merge
- give exact next step
```

## 15. “Just sort out what I need to look at”

```text
Inspect current repo state and reduce decision overhead for me:
- classify all current changes
- identify what actually needs my attention
- separate important issues from noise
- give me the shortest safe path forward

Do not execute anything.
```

Best three to use most often are:

* “Run full repo preflight and resolution plan…”
* “Review the latest audit summary and gate outputs…”
* “Run full merge preflight…”
