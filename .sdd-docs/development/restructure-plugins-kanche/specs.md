---
feature: restructure-plugins-kanche
module: plugins
created_at: 2026-07-25
---

# Feature Specification: Restructure Plugins to `plugins/kanche/*` Namespace

## Context
Currently, plugin bundles are located directly under `plugins/` (e.g. `plugins/git`, `plugins/sdd`). To support multi-author/publisher namespacing, we want to restructure the plugins folder so all plugins by author `kanche` (or `iamkanche`) are nested inside `plugins/kanche/` (e.g. `plugins/kanche/git`, `plugins/kanche/sdd`, `plugins/kanche/gh-cli`, `plugins/kanche/design`, `plugins/kanche/qa`, `plugins/kanche/planner`, `plugins/kanche/dev`).

## Requirements
1. Move plugin directories:
   - `plugins/git` -> `plugins/kanche/git`
   - `plugins/gh-cli` -> `plugins/kanche/gh-cli`
   - `plugins/sdd` -> `plugins/kanche/sdd`
   - `plugins/design` -> `plugins/kanche/design`
   - `plugins/qa` -> `plugins/kanche/qa`
   - `plugins/planner` -> `plugins/kanche/planner`
   - `plugins/dev` -> `plugins/kanche/dev`

2. Update Registry Configuration:
   - Update `.agents/plugins/marketplace.json` source fields to point to `github:iamkanche/agy-plugins//plugins/kanche/{plugin}`.

3. Update Workspace Documentation & References:
   - Update `README.md` to reflect `plugins/kanche/*` structure and `marketplace.json` example source paths.
   - Update `.sdd-docs/guidelines/structure.md`, `tech.md`, `rules.md` to reference `plugins/kanche/*`.
   - Update `index.html` references to point to `plugins/kanche/*`.

## Acceptance Criteria
1. All 7 plugins exist under `plugins/kanche/`.
2. `.agents/plugins/marketplace.json` lists sources pointing to `github:iamkanche/agy-plugins//plugins/kanche/{plugin}`.
3. All JSON files pass validation and git working tree is clean.
