# Post-mortem Template

```markdown
## Incident: {title}
**Date**: {YYYY-MM-DD}
**Severity**: {Critical | High | Medium | Low}
**Duration**: {how long the impact lasted}
**Impact**: {users affected, scope}

## Timeline
| Time | Event |
|---|---|
| {HH:MM} | {what happened} |
| {HH:MM} | {what happened} |
| {HH:MM} | {resolved} |

## Root Cause
{What actually caused the issue — be specific}

## What Failed in Our Process
- {gap 1 — e.g., "no test coverage for this path"}
- {gap 2 — e.g., "no rollback plan documented"}

## What Went Right
- {thing 1 — e.g., "detected within 5 minutes"}
- {thing 2}

## Preventive Actions
| Action | Owner | Priority | Status |
|---|---|---|---|
| {what we'll do to prevent recurrence} | @{user} | {HIGH/MED/LOW} | TODO |

## Related Issues
- {#N — created as a result of this incident}

---
*Created by github-planner `/plan-discussion`*
```
