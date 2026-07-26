# Tasks: Audit Improvements for Security, Pre-Execution Inspection, and Skill Resilience

- [x] 1. Create root `.gitignore` with comprehensive exclusions for environment secrets, build logs, and temporary files.
- [x] 2. Update `plugins/kanche/skills/sdd-run/SKILL.md` to add explicit pre-execution `view_file` inspection steps for all subagent phase invocations.
- [x] 3. Update `plugins/kanche/skills/gh-cli-pr-create/SKILL.md` with fallback handling for `--assignee`.
- [x] 4. Update `@coder` subagent definition (`plugins/kanche/agents/coder/agent.json`) to enforce file-only edits and forbid git operations.

## Verification
- Run `git status --ignored` to verify `.gitignore` properly excludes `.env` and `*.log`.
- Inspect `sdd-run/SKILL.md` and `gh-cli-pr-create/SKILL.md` to verify updated skill instructions.
