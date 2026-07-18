# Implementation Checklist - Interactive Gating via AskQuestion

## Phase 1: Rules Updates
- [ ] Update `plugins/sdd/rules/workflow-gating.md` to specify using `default_api:ask_question` for gating.
- [ ] Update `plugins/git/rules/git-hard-rules.md` to mandate `default_api:ask_question` for all human gates.
- [ ] Update `plugins/gh-cli/rules/gh-hard-rules.md` to mandate `default_api:ask_question` for all GitHub actions gating.

## Phase 2: SDD Plugin Skill Updates
- [ ] Update `plugins/sdd/skills/run/SKILL.md` to specify `default_api:ask_question` for all interactive prompts/loops.

## Phase 3: Git Plugin Skill Updates
- [ ] Update `plugins/git/skills/commit/SKILL.md` to use the interactive question form.
- [ ] Update `plugins/git/skills/push/SKILL.md` to use the interactive question form.
- [ ] Update `plugins/git/skills/branch-delete/SKILL.md` to use the interactive question form.
- [ ] Update `plugins/git/skills/tag-create/SKILL.md` to use the interactive question form.
- [ ] Update `plugins/git/skills/tag-delete/SKILL.md` to use the interactive question form.
- [ ] Update `plugins/git/skills/tag-push/SKILL.md` to use the interactive question form.
- [ ] Update `plugins/git/skills/rebase/SKILL.md` to use the interactive question form.

## Phase 4: GitHub CLI Plugin Skill Updates
- [ ] Update `plugins/gh-cli/skills/pr-approve/SKILL.md` to use the interactive question form.
- [ ] Update `plugins/gh-cli/skills/pr-create/SKILL.md` to use the interactive question form.
- [ ] Update `plugins/gh-cli/skills/pr-merge/SKILL.md` to use the interactive question form.
- [ ] Update `plugins/gh-cli/skills/pr-respond/SKILL.md` to use the interactive question form.
- [ ] Update `plugins/gh-cli/skills/pr-review/SKILL.md` to use the interactive question form.

## Verification
- [ ] Verify that all files match the proposed changes.
- [ ] Verify that git status remains clean after documentation commit.
