# Structure Guidelines

## Repository Layout
- `.sdd-docs/product/plugins/kanche/`: Subdirectories for individual plugin bundles under kanche author namespace.
  - `git/`: Git command workflows, rules, and operator subagent definition.
  - `gh-cli/`: GitHub CLI PR workflow commands, rules, and operator subagent definition.
  - `sdd/`: SDD Lifecycle workflow commands, gating rules, and template examples.
- `index.html`: Root registry dashboard for browser preview.
- `README.md`: Registry global/local installation guidelines.
- `.agents/`: Project-based agent configurations and plugins workspace.
  - `plugins/marketplace.json`: Local registration mapping plugin names to sources.
- `.sdd-docs/`: SDD documentation guidelines, metadata, and plugin packages.
  - `guidelines/`: Steering guidelines (`product.md`, `tech.md`, `structure.md`, `rules.md`).
  - `product/`: Long-term project memory (`memory.md`), plugin packages (`product/plugins/kanche/`), and feature specifications.

## Module/Layer Boundaries
- Each folder under `.sdd-docs/product/plugins/kanche/` (e.g. `git`, `gh-cli`, `sdd`) must remain fully self-contained and modular.
- Individual plugins declare their metadata, dependencies, skills, and agents within their respective directories.
- (Inferred) The `sdd` plugin references and integrates with the `git` plugin commands (e.g. `commit`, `branch-create`) to perform repository actions.

## Naming Conventions
- **Plugins:** Lowercase, kebab-case directory names under `.sdd-docs/product/plugins/kanche/` (e.g. `gh-cli`).
- **Slash Commands / Skills:** Folder names under `<plugin>/skills/` matching the command name. Each must contain a `SKILL.md` file. Commands are namespaces in format `/<plugin_name>:<command_name>` (e.g., `/git:commit`).
- **Subagents:** Operator subagents are defined inside `<plugin>/agents/` folders containing `agent.json`.
- **Rules:** Rules are stored in `<plugin>/rules/` as `.md` files.

## Tests and Fixtures
- No automated test files are present (inferred).
- Development workflow templates and examples are housed in `.sdd-docs/product/plugins/kanche/sdd/.sdd-docs-example/`.
