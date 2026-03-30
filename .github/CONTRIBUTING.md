# Contributing to GitHub Planner

GitHub Planner is a PM toolkit built as an MCS techpack. If you've managed backlogs, triaged issues, or tracked delivery and found something missing — your contribution is welcome.

## Ways to Contribute

### New Discussion Templates

Add a new type to `/plan-discussion`. The `analysis` type is a good reference — it's intentionally agnostic. A template needs:

- Interview questions (in `src/skills/discussion-builder/SKILL.md`)
- Markdown template (in `src/skills/discussion-builder/references/`)
- Category mapping for GitHub Discussions
- Entry in the Knowledge Manifest schema

### New Insight Scopes

Add a new `--scope` to `/plan-insights`. The `ci` scope is a recent example. A scope needs changes in 4 files:

- **Skill** (`src/skills/plan-insights/SKILL.md`) — metrics, thresholds, decision tips
- **Agent** (`src/agents/plan-insights-analyst.md`) — fetch commands and computation steps
- **Report template** (`src/skills/plan-insights/references/plan-insights-report.md`) — output format
- **Command** (`src/commands/plan-insights.md`) — scope option and report section

### Improved Detection Rules

Better heuristics for:

- Label mapping (document signals → GitHub labels)
- Discussion type detection (content signals → type slug)
- Triage rules (priority re-evaluation, staleness, duplicates)
- Pipeline stage detection (PR-to-issue linking)

### Bug Fixes & Documentation

Fixes, typos, clearer examples, or better `--help`-style descriptions in commands.

## How to Submit

We use a **fork-based workflow**. All contributions come through pull requests from your fork.

### 1. Fork & clone

```bash
gh repo fork anettodev/github-planner --clone
cd github-planner
```

### 2. Create a branch

```bash
git checkout -b <type>/<short-description>
```

Branch naming:

- `feature/` — new capability (template, scope, detection rule)
- `fix/` — bug fix
- `docs/` — documentation only

### 3. Make your changes

See [Techpack Structure](#techpack-structure) below to know where things go.

### 4. Test locally

```bash
# In any project where you want to test:
mcs pack add /path/to/your/github-planner
mcs sync
mcs doctor
```

Verify:

- `mcs doctor` passes with no issues
- Your new command/scope runs without errors
- Existing commands still work (no regressions)

### 5. Submit a PR

```bash
git push origin <your-branch>
gh pr create
```

Include in your PR description:

- **What** — what you added or changed
- **Why** — the use case or problem it solves
- **How to test** — steps to verify it works

## Techpack Structure

```text
src/
  skills/     → Knowledge and rules (what to do)
  agents/     → Execution logic (how to do it)
  commands/   → User entry points (slash commands)
  config/     → Settings and permissions
  hooks/      → Session lifecycle scripts
  templates/  → CLAUDE.local.md content
techpack.yaml → Pack manifest
```

| If you're adding... | You'll touch... |
|---|---|
| A discussion type | `src/skills/discussion-builder/` + `references/` + `src/agents/discussion-manager.md` + `src/commands/plan-discussion.md` |
| An insight scope | `src/skills/plan-insights/` + `references/` + `src/agents/plan-insights-analyst.md` + `src/commands/plan-insights.md` |
| A triage rule | `src/skills/issue-triage/` + `src/agents/issue-analyst.md` |
| A label mapping | `src/skills/plan-to-issues/SKILL.md` |
| A new `gh` command | `src/config/settings.json` (add to permission allowlist) |

Always update `README.md` if your change adds user-facing functionality.

## Style Guide

- **Write for PMs, not developers.** Plain language over jargon.
- **Every report needs color indicators.** Use the severity scale: 🟢 healthy, 🟡 warning, 🟠 stale, 🔴 critical.
- **Include decision tips.** Don't just show data — tell the PM what to do about it.
- **Read-only by default.** Any mutation (create, close, label) requires explicit flags like `--apply`.
- **Sparklines over tables when possible.** `▂▄▅▇▅▃` conveys trends faster than a column of numbers.
- **Keep templates agnostic.** Don't hard-code platform-specific assumptions (e.g., iOS-only, App Store-only).

## Code of Conduct

Be kind. Project management is stressful enough. We're all trying to make backlogs less painful.
