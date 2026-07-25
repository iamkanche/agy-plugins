# Feature Specification: Human-Gated PR Merge Workflow

## Overview
Modify the SDD execution workflow and GitHub CLI integration in `agy-plugins` so that PR merging (`/gh-cli:pr-merge` / Phase P9) is human-gated by default (`auto_merge: false` in `.sdd-docs/settings.json`), requiring explicit user confirmation before merging to `main`.

## Requirements
1. **Settings Configuration**:
   - `.sdd-docs/settings.json` must specify `"auto_merge": false` by default or allow setting `"auto_merge": false`.
2. **Product Memory Persistence**:
   - `.sdd-docs/product/memory.md` must document that PR merges to `main` require explicit human confirmation via `default_api:ask_question`.
3. **Skill Gating Updates**:
   - `plugins/sdd/skills/run/SKILL.md` P9 alignment step must check `auto_merge`. If `false`, it must pause and ask for human confirmation before running `/gh-cli:pr-merge`.
   - `plugins/gh-cli/skills/pr-merge/SKILL.md` must enforce mode-conditional gating: if `auto_merge: false`, require explicit prompt.
   - `plugins/sdd/rules/workflow-gating.md` must specify that PR merges in auto mode gate on human confirmation when `auto_merge: false`.

## Acceptance Criteria
- `auto_merge: false` is configured in `settings.json`.
- All SDD workflow documentations and gating rules require interactive confirmation prior to merging to `main`.
