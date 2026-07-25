# Tasks Checklist: Restructure Plugins to `product/plugins/kanche/*`

- [ ] 1. Create `product/plugins/kanche/` directory and move plugin folders (`git`, `gh-cli`, `sdd`, `design`, `qa`, `planner`, `dev`) into it.
- [ ] 2. Update `.agents/plugins/marketplace.json` plugin sources to `github:iamkanche/agy-plugins//product/plugins/kanche/<plugin>`.
- [ ] 3. Update `README.md` to reflect the new `product/plugins/kanche/` directory structure and registry examples.
- [ ] 4. Update `.sdd-docs/guidelines/` files (`structure.md`, `tech.md`, `rules.md`) to reference `product/plugins/kanche/*`.
- [ ] 5. Update `index.html` to reflect new `product/plugins/kanche/` paths.
- [ ] 6. Run verification checks to ensure git tree is clean and all files exist.
