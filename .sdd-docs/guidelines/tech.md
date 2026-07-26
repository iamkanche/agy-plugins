# Technical Guidelines

## Tech Stack
- **Core:** HTML5, Vanilla JavaScript (ES6+).
- **Styling:** CSS3 (Vanilla CSS, custom variables, glassmorphism design layouts).
- **Build/Lint:** Static website repository. No compile or bundle step required.
- **Tooling:** Git, GitHub CLI (gh) for remote repository and PR actions.

## Frameworks & Key Libraries
- Google Antigravity SDK & Built-in Skill templates.
- Google Fonts (`Outfit`, `Plus Jakarta Sans`) loaded dynamically in `index.html`.

## Data Stores & Configs
- Local Registry: `.agents/plugins/marketplace.json` defines registered plugins.
- Plugin manifests: `plugin.json` in each plugin folder (`plugins/kanche/plugin.json`).
- Skill definitions: `SKILL.md` frontmatters (`name: <group>-<action>`) under `plugins/kanche/skills/<group>/<action>/SKILL.md`.
- SDD workflow configurations: `.sdd-docs/settings.json`.
- SDD persistent state: `.sdd-docs/product/memory.md`.

## Build/Test/Lint/Run Commands
- Currently, no automated build, compilation, linting, or test execution suite is configured in the repository (inferred).
- Verification is performed through browser rendering of static HTML files, Antigravity workspace runner checks, and skill frontmatter validation.

## External Services & Integrations
- GitHub Repository Host (git clone/push/pull).
- GitHub API (via `gh` CLI) for pull request reviews, comments, and approvals (`gh-cli-pr-*` workflows).

## Known Technical Constraints
- Side effects are mode-gated: in manual mode, every side effect MUST use the interactive `default_api:ask_question` tool; in SDD auto mode, the gate is suppressed and the action is logged automatically. (Grounded in `.sdd-docs/product/memory.md`.)
- Safety invariants (protected-branch refusal, no force-push, no `--no-verify`, secrets detection, self-approval prohibition) are unconditional and enforced in both modes.
- Skill names in plugin YAML frontmatters MUST include their domain group prefix (`name: <group>-<action>`) so Antigravity registers slash commands as `/kanche:<group>-<action>`.
