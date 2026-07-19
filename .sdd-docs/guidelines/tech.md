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
- Plugin manifests: `plugin.json` in each plugin folder.
- SDD workflow configurations: `.sdd-docs/settings.json`.
- SDD persistent state: `.sdd-docs/product/memory.md`.

## Build/Test/Lint/Run Commands
- Currently, no automated build, compilation, linting, or test execution suite is configured in the repository (inferred).
- Verification is primarily performed manually through browser rendering of the static HTML files and execution of the Antigravity workspace runner.

## External Services & Integrations
- GitHub Repository Host (git clone/push/pull).
- GitHub API (via `gh` CLI) for pull request reviews, comments, and approvals.

## Known Technical Constraints
- Every side effect must be human-gated.
- Gated operations (commits, pushes, tag creations/deletions, branch deletions, PR creations, PR approvals, and PR merges) MUST use the interactive `default_api:ask_question` tool (grounded in `.sdd-docs/product/memory.md`).
