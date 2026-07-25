# Antigravity Plugins Workspace

Welcome to the **agy-plugins** repository! This workspace contains modular plugin bundles for the **Google Antigravity** AI-first development platform.

Plugins in this repository extend the capabilities of Antigravity agents by packaging slash commands (workflows), rules, subagents, and skills.

## Marketplace Registration

You can load these plugins from this remote repository either **globally** or **project-based**:

### 1. Global Installation (All Projects)
Create a `marketplace.json` file inside your global plugins directory:
- Registry file: `~/.gemini/config/plugins/marketplace.json`

```json
{
  "name": "global-plugins-registry",
  "plugins": [
    { "name": "git", "source": "github:iamkanche/agy-plugins//plugins/git" },
    { "name": "gh-cli", "source": "github:iamkanche/agy-plugins//plugins/gh-cli" },
    { "name": "sdd", "source": "github:iamkanche/agy-plugins//plugins/sdd" },
    { "name": "design", "source": "github:iamkanche/agy-plugins//plugins/design" },
    { "name": "qa", "source": "github:iamkanche/agy-plugins//plugins/qa" },
    { "name": "planner", "source": "github:iamkanche/agy-plugins//plugins/planner" },
    { "name": "dev", "source": "github:iamkanche/agy-plugins//plugins/dev" }
  ]
}
```

### 2. Project-Based Installation (Workspace-Level)
Create a `marketplace.json` file inside your project's local customization directory:
- Registry file: `.agents/plugins/marketplace.json`

```json
{
  "name": "project-plugins-registry",
  "plugins": [
    { "name": "git", "source": "github:iamkanche/agy-plugins//plugins/git" },
    { "name": "gh-cli", "source": "github:iamkanche/agy-plugins//plugins/gh-cli" },
    { "name": "sdd", "source": "github:iamkanche/agy-plugins//plugins/sdd" },
    { "name": "design", "source": "github:iamkanche/agy-plugins//plugins/design" },
    { "name": "qa", "source": "github:iamkanche/agy-plugins//plugins/qa" },
    { "name": "planner", "source": "github:iamkanche/agy-plugins//plugins/planner" },
    { "name": "dev", "source": "github:iamkanche/agy-plugins//plugins/dev" }
  ]
}
```

---

## Active Plugins

### 1. Git Control Plugin (`git`)
Provides 11 robust slash commands to manage local Git histories and workspaces safely.

### 2. GitHub CLI Plugin (`gh-cli`)
Provides 5 slash commands to manage the Pull Request lifecycle, reviews, approvals, and thread triaging.

### 3. Design & Specs Plugin (`design`)
Provides skills and specialized agents (`design-analyst`, `design-architect`) for requirements grilling, functional specs, and system design architecture:
- `/design:grill` - Adversarially probe feature requests and compile questions.
- `/design:specs` - Generate functional specifications draft.
- `/design:specs-review` - Validate specifications draft against rules.
- `/design:design` - Generate architectural and database specifications.
- `/design:design-review` - Verify architecture design against guidelines.

### 4. Quality Assurance Plugin (`qa`)
Provides skills and subagents (`qa-validator`) for testing, test plan creation, build code review, and automated validation:
- `/qa:validate` - Run linters, compilers, and test suites.
- `/qa:test-plan` - Generate test plan matrix and test cases.
- `/qa:build-review` - Audit code diffs and test coverage.

### 5. Task Planner Plugin (`planner`)
Provides skills and subagents (`planner-agent`) for task breakdown and task manifests:
- `/planner:tasks` - Generate implementation checklist task manifest.
- `/planner:tasks-review` - Audit task list completeness and ordering.

### 6. Development & Coding Plugin (`dev`)
Provides skills and subagents (`dev-coder`) for code implementation:
- `/dev:build` - Modify codebase incrementally and run verifications.

### 7. SDD Master Orchestrator Plugin (`sdd`)
Provides master workflow orchestrator slash commands for lifecycle steering and document synchronization:
- `/sdd:run` - Drive a feature work item through the full SDD phase model (P0 to P9).
- `/sdd:steering` - Analyze the repository and return steering guideline bodies.
- `/sdd:sync` - Promote development docs to product memory.
- `/sdd:init` - Bootstrap steering guidelines product.md/tech.md/structure.md/rules.md.
- `/sdd:init-update` - Re-analyze repository and refresh guidelines by merging.
- `/sdd:continue` - Resume SDD workflow from the current on-disk state.

---

## Directory Structure

```text
agy-plugins/
├── .agents/
│   └── plugins/
│       └── marketplace.json   # Local registry definition
└── plugins/
    ├── git/                   # Git plugin directory
    ├── gh-cli/                # GitHub CLI plugin directory
    ├── design/                # Design & Specs plugin directory
    ├── qa/                    # Quality Assurance & Testing plugin directory
    ├── planner/               # Task Planner plugin directory
    ├── dev/                   # Coding & Development plugin directory
    └── sdd/                   # Master SDD Orchestrator plugin directory
```
