# Task Checklist: SDD Phase Model Update

- [x] Update `plugins/kanche/skills/sdd-run/SKILL.md` Phase Model diagram placing Level 2 below Level 1
- [x] Add `/kanche:gh-cli-pr-review` to P6 Deploy step in `sdd-run` and `sdd-continue`
- [x] Enforce mandatory per-phase forced reviews (`/kanche:design-specs-review`, `/kanche:design-review`, `/kanche:planner-review`, `/kanche:qa-review`) with retry loops up to 3x (`≤3x`)
- [x] Sync changes to installed plugin runtime at `~/.gemini/config/plugins/kanche/skills/`
- [x] Commit documentation changes via `/kanche:git-commit`
- [x] Commit implementation changes via `/kanche:git-commit`
- [x] Push feature branch and create PR via `/kanche:git-push` and `/kanche:pr-create`
- [x] Run AI PR review (`/kanche:gh-cli-pr-review`) and Level 2 synchronization (`/kanche:sdd-sync`)
