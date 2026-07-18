# Design: Improve SDD Plugins

## Component Boundaries
All changes are contained within the `plugins/sdd` directory:
- `plugins/sdd/skills/run/SKILL.md` (orchestration)
- `plugins/sdd/skills/continue/SKILL.md` (orchestration)
- `plugins/sdd/skills/sync/SKILL.md` (synchronization & drift rules)
- Other worker skills (frontmatter only)

## Data Flow
1. `/sdd:run` -> checks folder -> uses/prompts for slug -> checkout branch `feat/{slug}`.
2. Loops P1-P3 without committing -> Writes specs, design, tasks to `.sdd-docs/development/{slug}/`.
3. End of P3 -> runs `/git:commit` for all docs.
4. P4 (Build) -> implements code -> reviews -> `/git:commit` for implementation.
5. P5 (Validate) -> validation checks.
6. P6 (Deploy) -> push & PR.
7. L2 (P7-P9) -> in auto mode, auto-runs human validation, checks/responds to PR feedback, and runs `/sdd:sync` to copy dev docs to `product/{slug}/`, delete `development/{slug}/`, and commit/push.
