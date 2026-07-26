# Structure Guidelines

## Repository Layout
- `plugins/`: Plugin bundle directories.
  - `kanche/`: Unified plugin directory (`plugin.json` with `"name": "kanche"`).
    - `skills/`: Nested workflow skills across 7 domain groups (`sdd/`, `git/`, `gh-cli/`, `design/`, `dev/`, `planner/`, `qa/`), exposed as `/kanche:<group>-<action>` (e.g. `/kanche:sdd-run`, `/kanche:git-commit`, `/kanche:gh-cli-pr-create`).
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
- **Slash Commands / Skills:** Skill directories under `plugins/kanche/skills/` structured as `plugins/kanche/skills/<group>/<action>/SKILL.md`. Frontmatter specifies `name: <group>-<action>` (e.g. `name: sdd-run`, `name: git-commit`, `name: gh-cli-pr-create`). Commands are invoked as `/kanche:<group>-<action>`.
- **Subagents:** Operator subagents are defined inside `plugins/kanche/agents/` folders containing `agent.json`.
- **Rules:** Rules are stored in `plugins/kanche/rules/` as `.md` files.

## Tests and Fixtures
- No automated test files are present (inferred).
- Verification is performed by inspecting plugin structure and checking installed skill definitions.
