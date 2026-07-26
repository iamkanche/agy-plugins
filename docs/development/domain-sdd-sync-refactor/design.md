# Technical Design: Domain-Based SDD Sync Architecture

## 1. Domain Group Mapping
The `sdd-sync` skill maps modified files to domain directories:
- `plugins/kanche/skills/sdd-*` -> `docs/product/plugins/kanche/sdd/`
- `plugins/kanche/skills/git-*` -> `docs/product/plugins/kanche/git/`
- `plugins/kanche/skills/gh-cli-pr-*` -> `docs/product/plugins/kanche/gh-cli/`
- `plugins/kanche/skills/design-*` -> `docs/product/plugins/kanche/design/`
- `plugins/kanche/skills/dev-*` -> `docs/product/plugins/kanche/dev/`
- `plugins/kanche/skills/planner-*` -> `docs/product/plugins/kanche/planner/`
- `plugins/kanche/skills/qa-*` -> `docs/product/plugins/kanche/qa/`

## 2. Sync Execution Flow
1. Parse modified skills/files to determine domain group.
2. Read and merge `specs.md` and `design.md` into target `docs/product/plugins/kanche/{domain}/`.
3. Remove `docs/development/{slug}/`.
4. Run `/kanche:git-commit` and `/kanche:git-push`.
