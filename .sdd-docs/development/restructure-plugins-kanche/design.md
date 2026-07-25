---
feature: restructure-plugins-kanche
module: plugins
created_at: 2026-07-25
---

# System Design: Restructure Plugins to `plugins/kanche/*` Namespace

## Directory Layout Changes

Before:
```text
plugins/
├── git/
├── gh-cli/
├── sdd/
├── design/
├── qa/
├── planner/
└── dev/
```

After:
```text
plugins/
└── kanche/
    ├── git/
    ├── gh-cli/
    ├── sdd/
    ├── design/
    ├── qa/
    ├── planner/
    └── dev/
```

## Marketplace Registry Contract

Updated `.agents/plugins/marketplace.json`:
```json
{
  "name": "agy-plugins",
  "owner": { "name": "iamkanche" },
  "plugins": [
    { "name": "git", "source": "github:iamkanche/agy-plugins//plugins/kanche/git" },
    { "name": "gh-cli", "source": "github:iamkanche/agy-plugins//plugins/kanche/gh-cli" },
    { "name": "sdd", "source": "github:iamkanche/agy-plugins//plugins/kanche/sdd" },
    { "name": "design", "source": "github:iamkanche/agy-plugins//plugins/kanche/design" },
    { "name": "qa", "source": "github:iamkanche/agy-plugins//plugins/kanche/qa" },
    { "name": "planner", "source": "github:iamkanche/agy-plugins//plugins/kanche/planner" },
    { "name": "dev", "source": "github:iamkanche/agy-plugins//plugins/kanche/dev" }
  ]
}
```

## Migration Plan & Dependency Graph
1. Create directory `plugins/kanche/`.
2. Move directories `git`, `gh-cli`, `sdd`, `design`, `qa`, `planner`, `dev` into `plugins/kanche/`.
3. Update `.agents/plugins/marketplace.json`.
4. Search & replace path references across `.sdd-docs/`, `README.md`, `index.html`.
5. Verify integrity of all plugin files (`plugin.json`, `SKILL.md`, rules).
