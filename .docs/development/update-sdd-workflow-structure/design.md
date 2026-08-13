# Design: SDD Workflow Structure & Governance Refactor

## System Architecture

```
.docs/
├── development/
│   └── {slug}/                # Temporary active feature dev docs
├── guidelines/
│   ├── product.md
│   ├── rules.md
│   ├── structure.md
│   └── tech.md
├── product/
│   ├── memory.md              # Long-term system memory
│   ├── design/                # Domain product docs
│   ├── dev/
│   ├── gh-cli/
│   ├── git/
│   ├── planner/
│   ├── qa/
│   ├── scrum/                 # Scrum PBI domain product docs
│   └── sdd/
└── settings.json

plugins/kanche/
├── agents/                    # Subagent definitions
├── plugin.json                # Plugin manifest
├── rules/                     # Workflow & loop rules
└── skills/                    # Flat skill directories
    ├── code-implement/
    ├── ...
    └── scrum-pbi-create/
```

## Component Changes

### 1. `plugins/kanche/skills/sdd-sync/SKILL.md`
- Updates source and target path logic.
- Target path: `.docs/product/{domain}/`
- Clean up dev folder: `.docs/development/{slug}/`

### 2. Frontmatter AI Model Schema
Every `SKILL.md` frontmatter will conform to:
```yaml
---
name: <skill-name>
description: <skill-description>
model: <flash|pro>
---
```

### 3. `/kanche:sdd-run` `/goal` Protocol
- `/kanche:sdd-run` includes `--goal` / `/goal` parameter and execution rules.
- When `/goal` is active, the orchestrator executes with goal-driven persistence, re-running failed phases up to limits, self-auditing all artifacts, and outputting `<!-- GOAL_COMPLETE -->` upon full completion.

### 4. `/kanche:scrum-pbi-create` Design
- **Path:** `plugins/kanche/skills/scrum-pbi-create/SKILL.md`
- **Domain:** `scrum`
- **Inputs:** `<title>` `--priority=<P0|P1|P2>` `--points=<1|2|3|5|8|13>` `--domain=<domain>`
- **Output:** Creates or appends to `.docs/product/{domain}/backlog/PBI-{id}.md` or `.docs/product/scrum/backlog.md` with structured PBI fields (Title, Description, User Story, Acceptance Criteria, Story Points, Priority, Linked Specs).
