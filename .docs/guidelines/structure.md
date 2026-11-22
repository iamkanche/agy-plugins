# Structure Guidelines

## Repository Layout
- `plugins/`: Plugin bundle directories.
  - `kanche/`: Unified plugin directory (`plugin.json` with `"name": "kanche"`, `"version": "0.6.0"`).
    - `skills/`: Flattened workflow skill directories across 56 skills (`graph-*`, `sdd-*`, `git-*`, `gh-cli-*`, `design-*`, `code-*`, `debug-rca/`, `db-migrate/`, `planner-*`, `qa-*`, `test-data/`, `plugin-validate/`, `security-scan/`, `scrum-pbi-create/`, `token-optimize/`, `team-swarm/`), exposed as `/kanche:<skill-name>`, plus executable scripts under `qa-validate/scripts/` and `plugin-validate/scripts/`.
    - `agents/`: 19 native Markdown subagents (`researcher`, `scrum-master`, `analyst`, `architect`, `data-architect`, `designer`, `planner`, `coder`, `frontend-expert`, `backend-expert`, `debugger`, `reviewer`, `validator`, `tester`, `security-engineer`, `token-optimizer`, `devops`, `git-operator`, `gh-operator`) in `plugins/kanche/agents/<name>.md`.
    - `hooks.json` & `hooks/`: Runtime `PreToolUse` hooks (`destructive_gate.py`, `secret_guard.py`).
    - `rules/`: `AGENTS.md` plus frontmatter-triggered rule files (`destructive-safety.md`, `git-hard-rules.md`, `gh-hard-rules.md`, `workflow-gating.md`, `token-optimization.md`, `output-language.md`, `loop-engineering.md`).
- `index.html`: Root registry dashboard for browser preview and interactive phase orchestration.
- `README.md`: Registry global/local installation guidelines and team documentation.
- `.agents/`: Project-based agent configurations and plugins workspace.
  - `plugins.json`: Workspace plugin discovery config pointing to `plugins`.
  - `plugins/marketplace.json`: Local registration mapping single plugin `kanche` to source.
- `.docs/`: SDD documentation guidelines and metadata.
  - `guidelines/`: Steering guidelines (`product.md`, `tech.md`, `structure.md`, `rules.md`).
  - `product/`: Long-term project memory (`memory.md`) and domain product specifications (`git`, `gh-cli`, `sdd`, `design`, `dev`, `planner`, `qa`, `scrum`).

## Module/Layer Boundaries
- The single unified plugin `kanche` packages all Git, GitHub CLI, SDD, Design, QA, Planner, Dev, and Scrum skills into one cohesive bundle.
- Skills reference subagents in `plugins/kanche/agents/` and rules in `plugins/kanche/rules/`.

## Naming Conventions
- **Plugin Name:** `"kanche"` (`plugins/kanche/plugin.json`).
- **Slash Commands / Skills:** Skill directories under `plugins/kanche/skills/` structured as flat directories (`plugins/kanche/skills/<skill-name>/SKILL.md`). Frontmatter specifies `name: <skill-name>` (e.g. `name: sdd-run`, `name: git-commit`, `name: gh-cli-pr-create`). Commands are invoked as `/kanche:<skill-name>`.
- **Subagents:** Operator subagents are defined as native Antigravity Markdown files under `plugins/kanche/agents/<name>.md`.
- **Rules:** Consolidated `plugins/kanche/rules/AGENTS.md` and frontmatter-triggered `.md` files in `plugins/kanche/rules/`.
- **Hooks:** Runtime `PreToolUse` enforcement via `plugins/kanche/hooks.json` and `plugins/kanche/hooks/*.py`.

## Tests and Fixtures
- Automated structural checks: `plugins/kanche/skills/plugin-validate/scripts/validate_plugin.py` and `plugins/kanche/skills/qa-validate/scripts/graph_health.py`.
