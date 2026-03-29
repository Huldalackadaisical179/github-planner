# Project Delivery Insights

Analyze project delivery metrics — milestone burndown, delivery pipeline, stale work, and overall project health.

Arguments: $ARGUMENTS (optional flags: `--repo owner/repo`, `--scope burndown|pipeline|stale|health|all`, `--milestone "name"`, `--period 30d`)

## Steps

### 1. Detect Repository

- If `--repo` flag provided, use that
- Otherwise run `gh repo view --json nameWithOwner -q .nameWithOwner`

### 2. Configure Scope

Parse flags:
- `--scope all` (default): Generate full report
- `--scope burndown`: Milestone burndown only
- `--scope pipeline`: Delivery pipeline only
- `--scope stale`: Stale work detection only
- `--scope timeline`: ASCII Gantt timeline only
- `--scope ci`: CI/CD health only
- `--scope health`: Summary dashboard only
- `--milestone "name"`: Filter to a specific milestone
- `--period 30d` (default): Time window for velocity and activity metrics

### 3. Run Analysis

Launch the `plan-insights-analyst` agent to:
1. Fetch all issues, PRs, and milestones
2. Link PRs to issues (body references, branch names)
3. Compute milestone burndown with velocity projections
4. Build the delivery pipeline (backlog → assigned → in progress → review → merged → done)
5. Detect stale work using the configured threshold (`__STALE_THRESHOLD__` days, default 14)
6. Compute PR metrics (review turnaround, time to merge, PR size)
7. Build the health summary dashboard
8. Generate prioritized recommendations

### 4. Present Report

Display the full report using the template from `plan-insights` skill's `references/plan-insights-report.md`:

1. **Milestone Burndown** — progress, velocity, projection, weekly breakdown
2. **Delivery Pipeline** — issues by stage, bottleneck detection
3. **Stale Work** — idle issues, PRs, and reviews by severity
4. **Timeline** — ASCII Gantt with milestones, progress bars, and critical path
5. **CI/CD Health** — workflow success rates, blocked PRs, flaky tests, deploy frequency
6. **Project Health Summary** — aggregate metrics with status indicators
7. **Recommended Actions** — prioritized list of what to do next

### 5. Evaluate Learnings

If this session produced decisions or patterns worth remembering, save them using whatever knowledge tools are available.
