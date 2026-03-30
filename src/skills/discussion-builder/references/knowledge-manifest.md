# Knowledge Manifest Template

Initial structure for `docs/github-planner/KNOWLEDGE.md`. Sections are created dynamically — only add a section when the first entry of that type is created.

```markdown
# Knowledge Manifest — {owner/repo}

Last updated: {YYYY-MM-DD} | Entries: {N}

> This file is maintained by github-planner `/plan-discussion`.
> Each row links to a GitHub Discussion with the full content.
```

## Section Templates

Each section is added on first use. Use these formats:

### Decisions
```markdown
## Decisions
| Topic | Discussion | Date | Status | Owner |
|---|---|---|---|---|
| {topic} | [#{N}]({url}) | {YYYY-MM-DD} | {Open/Decided/Superseded} | @{user} |
```

### Architecture
```markdown
## Architecture
| Topic | Discussion | Date | Status | Owner |
|---|---|---|---|---|
| {topic} | [#{N}]({url}) | {YYYY-MM-DD} | {Current/Superseded} | @{user} |
```

### Retrospectives
```markdown
## Retrospectives
| Sprint/Phase | Discussion | Date | Action Items |
|---|---|---|---|
| {name} | [#{N}]({url}) | {YYYY-MM-DD} | {N items} |
```

### Post-mortems
```markdown
## Post-mortems
| Incident | Discussion | Date | Severity |
|---|---|---|---|
| {title} | [#{N}]({url}) | {YYYY-MM-DD} | {Critical/High/Medium/Low} |
```

### Distribution — {Channel Name}
```markdown
## Distribution — {Channel Name}
| Analysis | Discussion | Period | Key Finding |
|---|---|---|---|
| {title} | [#{N}]({url}) | {date range} | {one-line summary} |
```

Note: One section per channel. Channel name is whatever the user provides (e.g., "App Store", "Google Play", "Web", "TestFlight").

### Evaluations
```markdown
## Evaluations
| Subject | Discussion | Version/Scope | Verdict | Last Reviewed |
|---|---|---|---|---|
| {name} | [#{N}]({url}) | {version} | {Adopt/Trial/Hold/Reject} | {YYYY-MM-DD} |
```

## Archival Rules

- **Cap**: 20 KB total file size
- **Trigger**: When adding a new entry would exceed 20 KB
- **Process**:
  1. Move entries with status `Decided`, `Superseded`, `Closed`, or older than 12 months to `docs/github-planner/archive/KNOWLEDGE-{YEAR}.md`
  2. Add a reference at the top of each archived section: `> Previous entries: [2026 archive](archive/KNOWLEDGE-2026.md)`
  3. If archiving resolved entries isn't enough, archive the oldest entries regardless of status
- **Archive file format**: Same section/table structure as the main manifest
