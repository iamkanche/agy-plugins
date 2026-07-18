# Antigravity SDD Workflow Plugin

A namespaced plugin bundle for Google Antigravity that packages the Software Development Document (SDD) workflow model: specs → design → tasks → build → validate → deploy → review, with quality-gate loops and human-gated steps. Pairs with the git plugin.

This plugin ensures all agent-driven development conforms to structured architecture guidelines and quality standards before making repository changes.

## Workflow Gating Rules (rules/workflow-gating.md)

The following gating rules are active across all SDD operations:

1. **AI-Driven Decisions**: The AI decides which is the best approach or answer for a task autonomously, and will list all of its decisions for transparency (e.g. in specs, designs, or notes).
2. **Explicit Human Gates**: Repository changes (commits, pushes, tags, PR creation) still require explicit confirmation from the human.
3. **Quality Gates**: Inner-loop phases (specs, design, tasks, build) run a generate → review cycle up to 3× until the review returns GO, then commit via the `git` plugin's `commit` workflow.
4. **Human Review Gate**: Level 2 phases (human review, PR modifications, product alignment) are human-gated throughout.

## Available Slash Commands

Skills are located in [skills/](skills/) and map to the following commands:

- `/sdd:steering` - Analyze the repository and return the four steering guideline bodies (`product.md`, `tech.md`, `structure.md`, `rules.md`).
- `/sdd:grill` - Interrogate the feature request adversarially and return a ranked list of clarifying questions.
- `/sdd:specs` - Generate the functional specifications file based on feature description and guidelines.
- `/sdd:design` - Generate system design specifications including component boundaries, data model, and user flow.
- `/sdd:tasks` - Generate implementation checklist task manifest.
- `/sdd:build` - Implement target changes incrementally and run tests.
- `/sdd:specs-review` - Review specifications against rules and guidelines.
- `/sdd:design-review` - Review design documents.
- `/sdd:tasks-review` - Review tasks layout.
- `/sdd:build-review` - Review build modifications.
- `/sdd:validate` - Verify task checklist and run validations.
- `/sdd:sync` - Sync development documents to product directory.
- `/sdd:run` - Drive a feature work item through the full SDD phase model (P0 to P9) using specifications, system designs, task check-lists, and testing loops.
- `/sdd:init` - Bootstrap the steering guidelines (product.md, tech.md, structure.md, rules.md) for this repository.
- `/sdd:init-update` - Re-analyze this repository and refresh the guidelines merging new findings into existing docs.
- `/sdd:continue` - Resume the SDD workflow at the phase inferred from on-disk state instead of starting fresh.
