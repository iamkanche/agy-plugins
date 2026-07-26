# Task Checklist: SDD Phase Model Update

- [ ] Update `plugins/kanche/skills/sdd-run/SKILL.md` Phase Model diagram placing Level 2 below Level 1
- [ ] Add `/kanche:gh-cli-pr-review` to P6 Deploy step in `sdd-run` and `sdd-continue`
- [ ] Enforce mandatory per-phase forced reviews (`/kanche:design-specs-review`, `/kanche:design-review`, `/kanche:planner-review`, `/kanche:qa-review`) with retry loops up to 3x (`≤3x`)
- [ ] Sync changes to installed plugin runtime at `~/.gemini/config/plugins/kanche/skills/`
- [ ] Commit documentation changes via `/kanche:git-commit`
- [ ] Commit implementation changes via `/kanche:git-commit`
- [ ] Push feature branch and create PR via `/kanche:git-push` and `/kanche:pr-create`
- [ ] Run AI PR review (`/kanche:gh-cli-pr-review`) and Level 2 synchronization (`/kanche:sdd-sync`)
