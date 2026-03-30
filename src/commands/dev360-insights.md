# Developer Workload & Health Insights

Analyze developer activity, workload balance, and team health. Focused on sustainability and balance — not productivity surveillance.

Arguments: $ARGUMENTS (optional flags: `--repo owner/repo`, `--dev @username`, `--period 30d`)

## Steps

### 1. Detect Repository

- If `--repo` flag provided, use that
- Otherwise run `gh repo view --json nameWithOwner -q .nameWithOwner`

### 2. Configure Report Type

Parse flags:
- No `--dev` flag (default): **Team overview** — workload distribution and team health signals
- `--dev @username`: **Individual report** — detailed activity, consistency, workload, and health signals for one developer
- `--period 30d` (default): Time window for activity metrics

### 3. Run Analysis

Launch the `dev360-analyst` agent to:

**For team overview**:
1. Fetch all issues, PRs, commits, and reviews within the period
2. Build a profile for each developer (open issues, PRs merged, reviews given)
3. Classify workload per developer (Light / Balanced / High / Overloaded)
4. Compute team health signals (balance, review culture, sustainability, knowledge sharing, bus factor)
5. Generate recommendations

**For individual report** (`--dev @username`):
1. Fetch all activity for the specified developer
2. Compute activity summary (commits, PRs, reviews, issues closed)
3. Analyze consistency pattern (weekly breakdown, active days, trend)
4. Assess health signals (consistency, weekend work, declining trends)
5. Compute contribution patterns (PR size, merge time, review turnaround, self-merge rate)
6. List workload (open issues, pending reviews, stale assignments)
7. Identify blocked/stale items
8. Generate recommendations

### 4. Present Report

**Team overview**: Workload table + team health signals + recommendations.

**Individual report**: Activity summary + work pattern + contribution patterns + workload + blocked items + recommendations.

Use the templates from `dev360-insights` skill's `references/dev360-report.md`.

### 5. Evaluate Learnings

If this session produced decisions or patterns worth remembering, save them using whatever knowledge tools are available.
