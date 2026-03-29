# Plan Insights Skill

You are an expert at analyzing project delivery metrics from GitHub data. You produce actionable reports on milestone progress, delivery pipeline health, and stale work — giving PMs the data they need to make sprint decisions.

## Metrics

### 1. Milestone Burndown

Track progress toward each active milestone.

**Data needed**:
- Total issues in milestone (open + closed)
- Closed issues count and close dates
- Milestone due date (if set)

**Calculations**:
- **Progress**: `closed / total * 100`
- **Velocity**: Issues closed per week over the last 4 weeks
- **Projection**: At current velocity, when will the milestone complete?
- **Risk**: If projected completion > due date → flag as AT RISK

**Visualization**:
```
Progress  ████████░░░░░░░░░░░░ 36%   🟢 ON TRACK
Velocity  ▂▄▅▇▅▃  2.5/wk            🟡 DECLINING
```

- Progress bar: filled `█` vs empty `░`, 20 chars wide
- Sparkline: `▁▂▃▄▅▆▇█` mapped to weekly closed counts (last 4-8 weeks)
- Color dots: 🟢 on track / healthy, 🟡 at risk / declining, 🟠 stale, 🔴 behind / critical

**Weekly breakdown**:
| Week | Opened | Closed | Net | Remaining | Velocity |
|------|--------|--------|-----|-----------|----------|
| W12  | 14     | 0      | +14 | 14        | ▁        |
| W13  | 0      | 3      | -3  | 11        | ▃        |
| W14  | 1      | 5      | -4  | 8         | ▆        |
| W15  | 0      | 2      | -2  | 6         | ▃        |

**Sparkline mapping**: Scale the weekly closed count to 8 levels:
- `max_closed = max(weekly_closed_counts)`
- Each week: `level = round(closed / max_closed * 7)` → pick from `▁▂▃▄▅▆▇█`

**Color status rules**:
| Indicator | Condition |
|---|---|
| 🟢 ON TRACK | Progress % ≥ time elapsed % (or no due date and velocity stable) |
| 🟡 AT RISK | Progress % < time elapsed % by ≤ 15 points, or velocity declining 1 week |
| 🔴 BEHIND | Progress % < time elapsed % by > 15 points, or velocity declining 2+ weeks |
| 🟢 IMPROVING | Velocity increasing for 2+ weeks |
| 🟡 DECLINING | Velocity decreasing for 1 week |
| 🔴 STALLED | Zero issues closed for 2+ weeks |

**Decision tips**:
- 🔴 BEHIND → "Milestone is behind schedule — consider scope reduction or deadline extension"
- 🔴 STALLED → "No progress in 2+ weeks — investigate blockers"
- 🟡 DECLINING → "Velocity trending down — check for blockers or context-switching"
- No due date set → "Set a target date to enable burndown tracking"

### 2. Delivery Pipeline

Map every issue to its current stage in the development lifecycle.

**Pipeline stages**:

| Stage | How to detect |
|---|---|
| Backlog | Open issue, no PR linked, no assignee |
| Assigned | Open issue, has assignee, no PR linked |
| In Progress | Open issue, has open PR linked |
| In Review | Open issue, PR has review requested or review submitted |
| Changes Requested | Open issue, PR has changes_requested review |
| Approved | Open issue, PR approved but not merged |
| Merged | Issue has merged PR (may still be open if not auto-closed) |
| Done | Issue is closed |

**PR-to-issue linking**: Detect via:
- PR body contains "Fixes #N", "Closes #N", "Resolves #N"
- PR branch name contains issue number
- GitHub's linked issues API: `gh api repos/OWNER/REPO/issues/N/timeline`

**Report format**:
```
## Delivery Pipeline

| Stage | Count | Issues |
|-------|-------|--------|
| Backlog | 3 | #75, #78, #80 |
| Assigned | 2 | #70, #73 |
| In Progress | 3 | #68, #71, #76 |
| In Review | 2 | #69, #77 |
| Approved | 1 | #74 |
| Done | 3 | #72, #79, #65 |
```

**Bottleneck detection**:
- More than 3 PRs in review for > 48h → "Review bottleneck — N PRs waiting"
- More than 5 issues assigned but no PR after 7+ days → "Work not starting — check blockers"
- Approved PRs not merged for > 24h → "N PRs approved but not merged"

### 3. Stale Work Detection

Flag work items that have gone idle. Uses the configurable `__STALE_THRESHOLD__` (default: 14 days).

**What to check**:

| Item Type | Stale Signal | Threshold |
|---|---|---|
| Issue (assigned) | No PR linked, no comments | `STALE_THRESHOLD` days |
| Issue (unassigned) | No activity at all | `STALE_THRESHOLD` days |
| PR (open) | No commits, no review activity | `STALE_THRESHOLD / 2` days |
| PR (changes requested) | No new commits after review | `STALE_THRESHOLD / 4` days |
| Review request | No review submitted | 48h |

**Severity levels**:
- 🟡 **Warning**: Approaching threshold (> 75% of threshold)
- 🟠 **Stale**: Exceeded threshold
- 🔴 **Critical**: Exceeded 2x threshold

**Report format**:
```
## Stale Work (threshold: 14 days)

|    | Severity | Type | Item | Assignee | Idle Days | Signal |
|----|----------|------|------|----------|-----------|--------|
| 🔴 | CRITICAL | Issue | #70 | @dev1 | 28 | Assigned, no PR |
| 🟠 | Stale | PR | #142 | @dev2 | 8 | Changes requested, no update |
| 🟡 | Warning | Review | PR #138 | @dev1 | 3 | Review requested |
```

### 4. Timeline (ASCII Gantt)

Visual timeline of milestones and key issues showing schedule, progress, and dependencies.

**Data needed**:
- Milestones with due dates (or projected dates from burndown)
- Issues with start signals (first assignment or PR) and close dates
- Dependencies between issues (from cross-references)

**Rendering rules**:

1. **Time axis**: Auto-scale to fit all milestones. Use month headers with week divisions.
2. **Row width**: 40 chars for the timeline bar area.
3. **Bar characters**:
   - `█` — completed work (from start to close date)
   - `░` — remaining work (from now to due/projected date)
   - `·` — future/unstarted
   - `▓` — in progress (from start to now)
   - `◆` — milestone marker (due date)
4. **Status indicator**: Color dot + stage at the end of each row.
5. **Dependencies**: Show `→` connector between dependent rows when adjacent.

**Example**:
```
## Timeline

         Mar 2026         Apr 2026         May 2026
         |····|····|····|····|····|····|····|····|
Phase 1 — Foundation
  Auth refactor    ████████                          ✅ Done
  API migration         ▓▓▓▓░░░░                    🟡 In Review
  DB schema                  ··░░░░░                 📋 Blocked
                                    ◆ Phase 1 due
Phase 2 — Features
  Search redesign              ·····▓▓▓░░░           🟢 In Progress
  Notifications                ·····░░░░░░           📋 Assigned
  Dashboard v2                      ·····░░░░░░░░    🔴 Critical path
                                              ◆ v2.0 release
```

**Grouping**: Group by milestone or phase. Within each group, sort by start date.

**Critical path detection**: The longest chain of dependent issues. Mark with 🔴 if any item on the path is stale or behind.

**Fallback**: If no milestones have due dates, show a relative timeline based on creation dates and velocity-projected completion.

### 5. CI/CD Health

Analyze GitHub Actions workflow runs to surface delivery blockers and reliability trends.

**Data needed**:
- Workflow runs (last N days, from `--period`)
- Workflow definitions (name, state)
- PRs with failed checks

**Metrics**:

| Metric | Calculation |
|---|---|
| Success rate | `successful_runs / total_runs * 100` per workflow |
| Avg duration | Mean run time per workflow |
| Failure trend | Weekly failure count → sparkline |
| Flaky tests | Workflows that alternate pass/fail on the same commit |
| Blocked PRs | Open PRs where the latest check run failed |

**Thresholds**:
| Indicator | Condition |
|---|---|
| 🟢 HEALTHY | Success rate ≥ 95%, no blocked PRs |
| 🟡 DEGRADED | Success rate 80-95%, or 1-2 blocked PRs |
| 🟠 UNSTABLE | Success rate 60-80%, or flaky tests detected |
| 🔴 BROKEN | Success rate < 60%, or 3+ blocked PRs |

**Report format**:
```
## CI/CD Health

| Workflow | Runs | Success | Avg Duration | Trend | Status |
|----------|------|---------|--------------|-------|--------|
| CI Tests | 48 | 92% | 4m 12s | ▅▇▅▃▁▃ | 🟡 DEGRADED |
| Deploy | 12 | 100% | 2m 05s | ▇▇▇▇▇▇ | 🟢 HEALTHY |
| Lint | 48 | 98% | 0m 45s | ▇▇▇▇▇▅ | 🟢 HEALTHY |

**Blocked PRs**: 2 — #138 (CI Tests failed), #145 (CI Tests failed)
**Flaky workflows**: CI Tests — 3 pass/fail alternations this week
**Deploy frequency**: 3/week ▃▅▇▅▃▇ (last 6 weeks)
```

**Deploy frequency** (DORA metric):
- Elite: multiple per day
- High: 1-7 per week
- Medium: 1-4 per month
- Low: < 1 per month

**Decision tips**:
- Success rate < 80% → "CI reliability is impacting delivery — investigate top failing workflows"
- Flaky tests detected → "Flaky tests erode trust in CI — quarantine or fix"
- Blocked PRs > 0 → "N PRs blocked by failed CI — unblock to restore pipeline flow"
- Deploy frequency declining → "Deployment cadence slowing — check for release blockers"

### 6. Summary Dashboard

Aggregate project health:

```
## Project Health Summary

| Metric | Value | Status |
|--------|-------|--------|
| Milestone progress | 36% (5/14) | 🟡 AT RISK |
| Velocity | 2.5 issues/week ▂▄▅▇▅▃ | 🟡 DECLINING |
| Pipeline bottleneck | Review (3 PRs) | 🔴 BOTTLENECK |
| Stale items | 4 | 🟡 MEDIUM |
| Avg PR review time | 1.2 days | 🟢 FAST |
| Avg time to merge | 2.1 days | 🟢 FAST |
```

**Thresholds**:
- Velocity: declining 2+ weeks = DECLINING
- Stale: 0-2 = LOW, 3-5 = MEDIUM, 6+ = HIGH
- Review time: < 24h = FAST, 24-72h = NORMAL, > 72h = SLOW
- Merge time: < 48h = FAST, 48h-5d = NORMAL, > 5d = SLOW

## Output Format

The full report follows the template in `references/plan-insights-report.md`.
