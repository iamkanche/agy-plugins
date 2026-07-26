# Structure Guidelines

## Repository Layout
- `plugins/`: Plugin bundle directories.
  - `kanche/`: Unified plugin directory (`plugin.json` with `"name": "kanche"`).
    - `skills/`: Workflow skills exposed as `/kanche:<skill_name>` (e.g. `git-commit`, `pr-create`, `sdd-run`).
    - `agents/`: Operator subagents (`git-operator`, `gh-operator`, `analyst`, `architect`, `planner`, `coder`, `validator`).
    - `rules/`: Hard rules and gating guidelines.
- `index.html`: Root registry dashboard for browser preview.
- `README.md`: Registry global/local installation guidelines.
- `.agents/`: Project-based agent configurations and plugins workspace.
  - `plugins/marketplace.json`: Local registration mapping single plugin `kanche` to source.
- `.sdd-docs/`: SDD documentation guidelines and metadata.
  - `guidelines/`: Steering guidelines (`product.md`, `tech.md`, `structure.md`, `rules.md`).
  - `product/`: Long-term project memory (`memory.md`) and feature specifications (`plugins/kanche/`).

## Module/Layer Boundaries
- The single unified plugin `kanche` packages all Git, GitHub CLI, SDD, Design, QA, Planner, and Dev skills into one cohesive bundle.
- Skills reference subagents in `plugins/kanche/agents/` and rules in `plugins/kanche/rules/`.

## Naming Conventions
- **Plugin Name:** `"kanche"` (`plugins/kanche/plugin.json`).
- **Slash Commands / Skills:** Skill directories under `plugins/kanche/skills/` formatted as `/<group>-<action>` (e.g., `git-commit`, `sdd-run`) or `<action>` (e.g. `pr-create`). Triggers are invoked as `/kanche:<skill_name>`.
- **Subagents:** Operator subagents are defined inside `plugins/kanche/agents/` folders containing `agent.json`.
- **Rules:** Rules are stored in `plugins/kanche/rules/` as `.md` files.

## Tests and Fixtures
- No automated test files are present (inferred).
- Development workflow templates and examples are housed in `plugins/kanche/sdd/.sdd-docs-example/`.
