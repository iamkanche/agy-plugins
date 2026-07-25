# Tasks Checklist: Restructure Plugins to `plugins/kanche/*` Namespace

- [ ] 1. Create `plugins/kanche/` directory and move plugin folders (`git`, `gh-cli`, `sdd`, `design`, `qa`, `planner`, `dev`) into it.
- [ ] 2. Update `.agents/plugins/marketplace.json` plugin sources to `github:iamkanche/agy-plugins//plugins/kanche/<plugin>`.
- [ ] 3. Update `README.md` to reflect the new directory structure and registry examples.
- [ ] 4. Update `.sdd-docs/guidelines/` files (`structure.md`, `tech.md`, `rules.md`) to reference `plugins/kanche/*`.
- [ ] 5. Update index HTML files (`index.html`, `plugins/kanche/sdd/index.html`) to reflect new paths.
- [ ] 6. Run verification checks to ensure git tree is clean and all files exist.
