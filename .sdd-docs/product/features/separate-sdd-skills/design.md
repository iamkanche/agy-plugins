# System Design: Modular SDD Plugins Architecture

## 1. Overview & Architectural Goals
This design reorganizes the monolithic `plugins/sdd` directory into 5 modular, focused plugins under `plugins/`:
- `plugins/design`: Requirements, specifications, UI/UX, and architecture design.
- `plugins/qa`: Verification, validation, test plans, and quality audits.
- `plugins/planner`: Task manifests, breakdown, and project tracking.
- `plugins/dev`: Code implementation and incremental building.
- `plugins/sdd`: Steering guidelines, documentation sync, and master workflow orchestrator.

## 2. Directory Tree & Plugin Structure

```text
plugins/
├── design/
│   ├── plugin.json
│   ├── rules/
│   │   └── output-language.md
│   ├── agents/
│   │   ├── design-analyst/agent.json
│   │   └── design-architect/agent.json
│   └── skills/
│       ├── grill/SKILL.md
│       ├── specs/SKILL.md
│       ├── specs-review/SKILL.md
│       ├── design/SKILL.md
│       └── design-review/SKILL.md
├── qa/
│   ├── plugin.json
│   ├── rules/
│   │   └── output-language.md
│   ├── agents/
│   │   └── qa-validator/agent.json
│   └── skills/
│       ├── validate/SKILL.md
│       ├── test-plan/SKILL.md
│       └── build-review/SKILL.md
├── planner/
│   ├── plugin.json
│   ├── rules/
│   │   └── output-language.md
│   ├── agents/
│   │   └── planner-agent/agent.json
│   └── skills/
│       ├── tasks/SKILL.md
│       └── tasks-review/SKILL.md
├── dev/
│   ├── plugin.json
│   ├── rules/
│   │   └── output-language.md
│   ├── agents/
│   │   └── dev-coder/agent.json
│   └── skills/
│       └── build/SKILL.md
└── sdd/
    ├── plugin.json
    ├── rules/
    │   ├── output-language.md
    │   └── workflow-gating.md
    └── skills/
        ├── init/SKILL.md
        ├── init-update/SKILL.md
        ├── steering/SKILL.md
        ├── sync/SKILL.md
        ├── run/SKILL.md
        └── continue/SKILL.md
```

## 3. Plugin Manifests (`plugin.json`)

### 3.1 `plugins/design/plugin.json`
```json
{
  "name": "design",
  "version": "0.1.0",
  "description": "Design & Specifications plugin: grill, specs, specs-review, design, design-review.",
  "author": { "name": "iamkanche" },
  "rules": ["rules/output-language.md"],
  "agents": [
    "agents/design-analyst/agent.json",
    "agents/design-architect/agent.json"
  ],
  "skills": "skills"
}
```

### 3.2 `plugins/qa/plugin.json`
```json
{
  "name": "qa",
  "version": "0.1.0",
  "description": "Quality Assurance & Testing plugin: validate, test-plan, build-review.",
  "author": { "name": "iamkanche" },
  "rules": ["rules/output-language.md"],
  "agents": ["agents/qa-validator/agent.json"],
  "skills": "skills"
}
```

### 3.3 `plugins/planner/plugin.json`
```json
{
  "name": "planner",
  "version": "0.1.0",
  "description": "Planning & Task Manifests plugin: tasks, tasks-review.",
  "author": { "name": "iamkanche" },
  "rules": ["rules/output-language.md"],
  "agents": ["agents/planner-agent/agent.json"],
  "skills": "skills"
}
```

### 3.4 `plugins/dev/plugin.json`
```json
{
  "name": "dev",
  "version": "0.1.0",
  "description": "Software Development & Code Implementation plugin: build.",
  "author": { "name": "iamkanche" },
  "rules": ["rules/output-language.md"],
  "agents": ["agents/dev-coder/agent.json"],
  "skills": "skills"
}
```

### 3.5 `plugins/sdd/plugin.json`
```json
{
  "name": "sdd",
  "version": "0.1.0",
  "description": "SDD Master Workflow Orchestrator & Steering Guidelines: init, init-update, steering, sync, run, continue.",
  "author": { "name": "iamkanche" },
  "rules": [
    "rules/output-language.md",
    "rules/workflow-gating.md"
  ],
  "agents": [],
  "skills": "skills"
}
```

## 4. Marketplace Registration Updates

Both `.agents/plugins/marketplace.json` and global/local instructions will list all 5 active workflow plugins (`git`, `gh-cli`, `sdd`, `design`, `qa`, `planner`, `dev`).

## 5. UI Dashboard (`index.html`) Updates
The root `index.html` visual marketplace will be updated with interactive cards, command lists, and badges for `design`, `qa`, `planner`, `dev`, and updated `sdd`.
