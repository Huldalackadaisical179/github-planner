# Create GitHub Discussion

Create a structured GitHub Discussion from user input or a document. Maintains the Knowledge Manifest at `docs/github-planner/KNOWLEDGE.md`.

Arguments: $ARGUMENTS (optional — path to document, optional flags: `--repo owner/repo`, `--type decision|design|retro|postmortem|distribution|analysis`)

## Steps

### 1. Detect Repository

- If `--repo` flag provided, use that
- Otherwise run `gh repo view --json nameWithOwner -q .nameWithOwner`
- Verify Discussions are enabled: `gh api repos/OWNER/REPO --jq '.has_discussions'`
- If Discussions are disabled, inform the user and stop

### 2. Determine Type

If `--type` flag provided, use that.

If a document path is provided, use the `discussion-builder` skill to infer the type from content signals.

Otherwise, ask the user:

```
What type of discussion?
  1. Decision (RFC)
  2. Design Proposal
  3. Sprint Retro
  4. Post-mortem
  5. Distribution Analysis
  6. Evaluation / Analysis
```

Wait for selection.

### 3. Gather Content

**If document path provided**:
- Read the document
- Use the `discussion-builder` skill to restructure it into the matching template
- Ask the user to confirm or adjust the extracted content

**If no document (interactive mode)**:
- Use the `discussion-builder` skill's interview questions for the selected type
- Ask each question and build the body from answers
- For Distribution Analysis, ask the channel name first (user types freely)

### 4. Build Discussion

Using the gathered content:
- Select the matching template from the `discussion-builder` skill's `references/`
- Fill the template with the content
- Resolve the Discussion category (list available categories, map to the best fit)
- Identify related issues if mentioned

### 5. Present for Approval

Show the full discussion preview:
- Title
- Category
- Body (rendered)
- Related issues
- Manifest entry that will be added

**DO NOT create until user confirms.**

### 6. Create Discussion

Launch the `discussion-manager` agent to:
1. Create the GitHub Discussion
2. Update `docs/github-planner/KNOWLEDGE.md` (create if first time)
3. Archive old entries if manifest exceeds 20 KB
4. Commit manifest changes

### 7. Report

Output the discussion URL and confirm the manifest was updated.

### 8. Evaluate Learnings

If this session produced decisions or patterns worth remembering, save them using whatever knowledge tools are available.
