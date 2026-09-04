# Structure Guidelines

## Repository Layout
- `plugins/`: Plugin bundle directories.
  - `kanche/`: Unified plugin directory (`plugin.json` with `"name": "kanche"`).
    - `skills/`: Flattened workflow skill directories across 40 skills (`sdd-init/`, `sdd-run/`, `git-commit/`, `gh-cli-pr-create/`, `design-init/`, `code-implement/`, `planner-tasks/`, `qa-test-plan/`, `security-scan/`, `scrum-pbi-create/`, etc.), exposed as `/kanche:<skill-name>`.
    - `agents/`: 16 specialized autonomous subagents (`researcher`, `scrum-master`, `analyst`, `architect`, `designer`, `planner`, `coder`, `frontend-expert`, `backend-expert`, `reviewer`, `validator`, `tester`, `security-engineer`, `devops`, `git-operator`, `gh-operator`).
    - `rules/`: Hard rules, destructive safety (`rules/destructive-safety.md`), and loop engineering guidelines.
- `index.html`: Root registry dashboard for browser preview and interactive phase orchestration.
- `README.md`: Registry global/local installation guidelines and team documentation.
- `.agents/`: Project-based agent configurations and plugins workspace.
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
- **Subagents:** Operator subagents are defined inside `plugins/kanche/agents/` folders containing `agent.json`.
- **Rules:** Rules are stored in `plugins/kanche/rules/` as `.md` files.

## Tests and Fixtures
- No automated test files are present (inferred).
- Verification is performed by inspecting plugin structure and checking installed skill definitions.
