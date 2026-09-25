---
name: gh-cli-pr-review
description: Review a pull request diff against repository rules and post structured inline suggestion comments to GitHub with .json format support.
model: flash
---

# /kanche:gh-cli-pr-review

**Summary.** Audit a PR diff against guidelines and post structured review comments with inline code suggestions via `gh api`. Delegated to `@gh-operator` and `@reviewer`. Enforces `rules/destructive-safety.md` and `rules/token-optimization.md`.

## Inputs

- `<pr-number>` (optional positional) — PR number (resolves current branch PR if omitted).
- `--json` / `--format=json` — export and output standardized `review.json` payload.

## Steps

1. **Verify Auth:** Run `gh auth status`.
2. **Fetch Metadata & Diff:**
   ```bash
   PR="<pr-number or current>"
   HEAD_OID=$(gh pr view $PR --json headRefOid -q .headRefOid)
   gh pr diff $PR
   ```
3. **Audit Touched Files:** Check code against `rules/destructive-safety.md`, `rules/token-optimization.md`, security, and style.
4. **Classify Findings:** Categorize as `🔴 HIGH` (bugs/security), `🟡 MEDIUM` (correctness/tests), or `🟢 LOW` (style/nits).
5. **Construct Payload (`review.json`):**
   ```json
   {
     "commit_id": "<HEAD_OID>",
     "body": "#  Summary\n- <summary>\n- Severity: eg: 6/10\n- Total files: <x> files\n- Total lines: <x> lines of codes\n\n## Review Summary\n\n| Severity | Count | Category |\n|---|---|---|\n| 🔴 HIGH | 0 | Critical Bugs / Security / Breaking |\n| 🟡 MEDIUM | 0 | Correctness Risk / Test Coverage |\n| 🟢 LOW | 0 | Documentation / Style Nit |\n\n---\nInline comment directly to the files and lines of codes",
     "event": "COMMENT",
     "comments": [
       {
         "path": "<file_path>",
         "line": 42,
         "side": "RIGHT",
         "body": "[<SEVERITY>] <desc>\nIssue: <details>\nSuggestion:\n```suggestion\n<replacement>\n```\nWhy: <rationale>"
       }
     ]
   }
   ```
6. **Save JSON (if requested):** Write payload to `review.json`.
7. **Gate — Human Confirmation:** Prompt user via `default_api:ask_question` before posting to GitHub. Display severity counts.
8. **Post Review:** Run `gh api --method POST "repos/{owner}/{repo}/pulls/$PR/reviews" --input review.json`.
9. **Report:** Output posted review URL, summary counts, and status.

## Rules

- Enforce `@token-optimizer` standards: keep responses short, direct, and actionable; use bullets; omit conversational filler.
- Default review event is `COMMENT` (no self-approval).
- Read-only to local working tree.

## Done when

- PR diff audited and classified with high signal-to-noise.
- User confirmed posting.
- Review submitted atomically with inline comments via `gh api`.
