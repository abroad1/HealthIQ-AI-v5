---
name: repo_preflight_and_merge_prep
description: Inspect branch state, working tree, stashes, and merge readiness for HealthIQ AI under repo governance.
---

Inspect:
- current branch
- git status
- local branches relevant to current work
- stash list
- most recent commits relevant to current branch

If stashes exist:
- summarise each stash briefly
- identify whether it appears related to current work
- do not apply, pop, drop, or delete any stash without explicit user approval

Output:
1. Repo-grounded summary
2. Risks or blockers
3. Merge readiness assessment
4. Exact next step
5. Exact commands if needed

Do not claim merge authority.