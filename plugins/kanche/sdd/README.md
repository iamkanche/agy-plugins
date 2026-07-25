# Antigravity SDD Master Workflow Plugin

A high-level master orchestrator plugin bundle for Google Antigravity that packages the Software Development Document (SDD) lifecycle model: specs → design → tasks → build → validate → deploy → review. 

The `sdd` plugin orchestrates domain-specific capabilities provided by its companion plugins:
- **`design`**: Requirements grilling (`/design:grill`), specs (`/design:specs`), and system design (`/design:design`).
- **`planner`**: Task decomposition (`/planner:tasks`).
- **`dev`**: Incremental building (`/dev:build`).
- **`qa`**: Test planning (`/qa:test-plan`), build code reviews (`/qa:build-review`), and validation (`/qa:validate`).
- **`git`**: Branch management, commits, and pushes.
- **`gh-cli`**: Pull request creation, review responses, and automated merging.

## Workflow Gating Rules (rules/workflow-gating.md)

1. **AI-Driven Decisions**: The AI decides which is the best approach or answer for a task autonomously, and will list all of its decisions for transparency.
2. **Explicit Human Gates**: Repository changes (commits, pushes, tags, PR creation) require explicit confirmation from the human.
3. **Quality Gates**: Inner-loop phases (specs, design, tasks, build) run a generate → review cycle up to 3× until the review returns GO, then commit via `/git:commit`.
4. **Human Review Gate**: Level 2 phases (human review, PR modifications, product alignment) are human-gated throughout.

## Available Slash Commands

Skills are located in [skills/](skills/) and map to the following master orchestrator commands:

- `/sdd:steering` - Analyze the repository and return the four steering guideline bodies (`product.md`, `tech.md`, `structure.md`, `rules.md`).
- `/sdd:run` - Drive a feature work item through the full SDD phase model (P0 to P9) using domain plugins (`design`, `planner`, `dev`, `qa`, `git`, `gh-cli`).
- `/sdd:init` - Bootstrap the steering guidelines (`product.md`, `tech.md`, `structure.md`, `rules.md`) for this repository.
- `/sdd:init-update` - Re-analyze this repository and refresh the guidelines merging new findings into existing docs.
- `/sdd:sync` - Sync development documents to product memory directory.
- `/sdd:continue` - Resume the SDD workflow at the phase inferred from on-disk state.
