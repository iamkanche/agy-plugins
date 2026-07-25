---
feature: product-plugins-kanche
module: plugins
created_at: 2026-07-25
---

# Feature Specification: Restructure Plugins to `product/plugins/kanche/*`

## Context
To establish a structured product hierarchy for Antigravity plugin packages, plugin bundles should be relocated under `product/plugins/kanche/` (e.g. `product/plugins/kanche/sdd`, `product/plugins/kanche/git`, `product/plugins/kanche/gh-cli`, `product/plugins/kanche/design`, `product/plugins/kanche/qa`, `product/plugins/kanche/planner`, `product/plugins/kanche/dev`).

## Requirements
1. Move plugin directories:
   - `plugins/git` -> `product/plugins/kanche/git`
   - `plugins/gh-cli` -> `product/plugins/kanche/gh-cli`
   - `plugins/sdd` -> `product/plugins/kanche/sdd`
   - `plugins/design` -> `product/plugins/kanche/design`
   - `plugins/qa` -> `product/plugins/kanche/qa`
   - `plugins/planner` -> `product/plugins/kanche/planner`
   - `plugins/dev` -> `product/plugins/kanche/dev`

2. Update Marketplace Registry (`.agents/plugins/marketplace.json`):
   - Update plugin sources to `github:iamkanche/agy-plugins//product/plugins/kanche/{plugin}`.

3. Update Workspace Documentation & References:
   - Update `README.md` to reflect `product/plugins/kanche/*` structure and `marketplace.json` example source paths.
   - Update `.sdd-docs/guidelines/` files (`structure.md`, `tech.md`, `rules.md`).
   - Update `index.html` and `product/plugins/kanche/sdd/index.html` references.

## Acceptance Criteria
1. All 7 plugins are located under `product/plugins/kanche/`.
2. `.agents/plugins/marketplace.json` source URLs point to `github:iamkanche/agy-plugins//product/plugins/kanche/{plugin}`.
3. All JSON files pass validation and git working tree is clean.
