# Kanche Engineering Team Rules

Universal non-negotiable invariants enforced across all `kanche` skills, 19 subagents, and runtime `hooks.json` gates:

- **Destructive & Remote Safety**: Never run `git push`, `git commit`, `git rebase`, `rm -rf`, branch/tag deletions, `git stash drop`, `gh pr merge`, or DB resets autonomously. Gate via `ask_question` (see `rules/destructive-safety.md`). Runtime `PreToolUse` hooks enforce `deny` / `force_ask`.
- **Git & GitHub Hard Rules**: Never force-push, `--no-verify`, amend pushed commits, `reset --hard` shared branches, commit secrets/credentials, work directly on `main`/`master`/`develop`, self-approve PRs, or force-merge (see `rules/git-hard-rules.md`, `rules/gh-hard-rules.md`).
- **Skills Stand Alone**: Individual skills never embed auto-mode bypass logic (see `rules/workflow-gating.md`).
- **Token Optimization**: Keep responses short, direct, BLUF, bulleted, with zero conversational filler and minimal diffs; never weaken safety gates (see `rules/token-optimization.md`).
- **Output Language**: English for prose, logs, reviews, and docs unless configured in `.docs/settings.json`; identifiers and paths verbatim (see `rules/output-language.md`).
- **Loop Engineering & Graph Health**: Use `rules/loop-engineering.md` (loaded on demand) for `<=3x` Generator-Reviewer `review-verdict` cycles and Topological DAG Tiers 0-3.
