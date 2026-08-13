# Implementation Checklist: SDD Workflow Structure & Governance Refactor

- [ ] 1. Move `.docs/` directory to `.docs/` and update product docs structure (`..docs/product/{domain}` -> `.docs/product/{domain}`).
- [ ] 2. Update `plugins/kanche/skills/sdd-sync/SKILL.md` to remove `/plugins/kanche` from sync paths and update `docs` to `.docs`.
- [ ] 3. Update all 39 existing skill `SKILL.md` files in `plugins/kanche/skills/`:
  - [ ] Add `model: flash` or `model: pro` to frontmatter of each skill based on complexity.
  - [ ] Update all references from `.docs/` to `.docs/` and `.docs/product/` to `.docs/product/`.
- [ ] 4. Update `plugins/kanche/skills/sdd-run/SKILL.md` to integrate `/goal` execution mode support and update `.docs/` paths.
- [ ] 5. Create new skill `plugins/kanche/skills/scrum-pbi-create/SKILL.md`:
  - [ ] Set `name: scrum-pbi-create`, `model: pro`.
  - [ ] Belong to group `scrum` (`.docs/product/scrum/`).
  - [ ] Document PBI creation workflow, templates, and acceptance criteria.
- [ ] 6. Register `/kanche:scrum-pbi-create` in `plugins/kanche/plugin.json` and update `index.html`.
- [ ] 7. Update agent definitions in `plugins/kanche/agents/` and rule files in `plugins/kanche/rules/` to reflect `.docs/` and `.docs/product/{domain}/`.
- [ ] 8. Update root documentation files (`README.md`, `index.html`, `.docs/guidelines/*`, `.docs/product/memory.md`).
- [ ] 9. Run `qa-validate` checks to verify all skills, schemas, and links are intact.
