## GitHub Planner

You have the **github-planner** techpack installed for document-to-issue automation, epic management, backlog triage, and team knowledge management.

### Commands
- `/plan-issues <path>` — Parse a planning document and create GitHub Issues
- `/plan-preview <path>` — Preview issues without creating them (dry run)
- `/plan-epic <path>` — Create a GitHub Project (v2) from a planning document and link issues
- `/plan-epic --link-only #1 #2 #3` — Link existing issues to a new or existing project
- `/issue-triage` — Scan open issues, analyze backlog health, and get PM-level recommendations
- `/plan-discussion [path]` — Create a GitHub Discussion (decision, design, retro, post-mortem, distribution analysis, evaluation/analysis)
- `/plan-insights` — Project delivery metrics (burndown, pipeline, stale work, health dashboard)
- `/dev360-insights` — Developer workload and team health (balance-focused, not surveillance)

### Configuration
- **Repository**: `__GITHUB_REPO__`
- **Label prefix**: `__LABEL_PREFIX__`
- **Default assignee**: `__DEFAULT_ASSIGNEE__`

### When to Use
- After creating refactoring plans, migration plans, or epic documents → `/plan-issues`
- When converting technical debt inventories into trackable issues → `/plan-issues`
- To organize issues into a project board with custom fields → `/plan-epic`
- To link existing issues to an epic after triage → `/plan-epic --link-only`
- For periodic backlog review and priority re-evaluation → `/issue-triage`
- When the PM needs a health check on the project → `/issue-triage`
- To document a decision, proposal, or evaluation → `/plan-discussion`
- When a blocked issue needs team input → `/plan-discussion --type decision`
- To analyze distribution channel feedback → `/plan-discussion --type distribution`
- To evaluate an SDK, tool, vendor, or platform → `/plan-discussion --type analysis`
- For milestone burndown and delivery pipeline status → `/plan-insights`
- To check project health and stale work → `/plan-insights --scope stale`
- To review team workload distribution → `/dev360-insights`
- To check on a specific developer's health signals → `/dev360-insights --dev @username`

### Typical Workflow
1. `/plan-preview plan.md` — review what issues would be created
2. `/plan-issues plan.md` — create the issues
3. `/plan-epic plan.md` — organize them into a project board
4. `/issue-triage` — periodically review and maintain backlog health
5. `/plan-discussion` — document decisions, run retros, evaluate dependencies
6. `/plan-insights` — track delivery progress, burndown, and project health
7. `/dev360-insights` — review team workload balance and sustainability

### Rules
- Always run `/plan-preview` first to review before creating issues
- Never create duplicate issues — check existing issues before creating
- Labels are auto-created if they don't exist (with standard color scheme)
- Milestones are created per document phase/priority group
- Issues are created in execution order so dependency references (#N) resolve correctly
- `/issue-triage` is read-only by default — it only suggests changes until you approve
- `/plan-epic` creates GitHub Projects v2, not classic projects
- `/plan-discussion` maintains a Knowledge Manifest at `docs/github-planner/KNOWLEDGE.md` (20 KB cap, auto-archives)
- GitHub Discussions must be enabled in the repo for `/plan-discussion` to work
- `/plan-insights` and `/dev360-insights` are read-only — they never modify issues or assignments
- `/dev360-insights` is health-focused — no leaderboards, no ranking, no productivity scores
- Stale threshold defaults to 14 days (configurable during `mcs sync`)

### GitHub Auth
- Uses `gh` CLI authentication (keyring-based)
- Required scopes: `repo` (read/write issues, labels, milestones), `project` (read/write projects)
- Verify with: `gh auth status`
