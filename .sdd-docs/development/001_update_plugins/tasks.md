# Update gh-cli and git Plugins — Implementation Tasks

<!-- schema: tasks | written by /sdd:tasks, checked off by /sdd:build -->

## Phase A — gh-cli Plugin Changes
- [ ] A1. Create `/gh-cli:pr-merge` skill (`plugins/gh-cli/skills/pr-merge/SKILL.md`)
- [ ] A2. Update `/gh-cli:pr-create` skill (`plugins/gh-cli/skills/pr-create/SKILL.md`)
- [ ] A3. Update `plugins/gh-cli/plugin.json` to register `pr-merge`
- [ ] A4. Update `plugins/gh-cli/index.html` dashboard list

## Phase B — git Plugin Changes
- [ ] B1. Create `/git:tag-delete` skill (`plugins/git/skills/tag-delete/SKILL.md`)
- [ ] B2. Create `/git:tag-push` skill (`plugins/git/skills/tag-push/SKILL.md`)
- [ ] B3. Update `plugins/git/plugin.json` to register tag-delete and tag-push
- [ ] B4. Update `plugins/git/index.html` dashboard list

## Phase C — Marketplace Dashboard Changes
- [ ] C1. Update marketplace dashboard (`index.html`) to include the new commands

## Verification
- [ ] Dashboard pages render and function correctly
- [ ] Skill markdown formats are valid and correct
