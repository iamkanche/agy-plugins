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
- Skill definitions: `SKILL.md` frontmatters (`name: <skill-name>`) under flattened directories `plugins/kanche/skills/<skill-name>/SKILL.md`.
- SDD workflow configurations: `.docs/settings.json`.
- SDD persistent state: `.docs/product/memory.md`.

## Build/Test/Lint/Run Commands
- Currently, no automated build, compilation, linting, or test execution suite is configured in the repository (inferred).
- Verification is performed through browser rendering of static HTML files, Antigravity workspace runner checks, and skill frontmatter validation.

## External Services & Integrations
- GitHub Repository Host (git clone/push/pull).
- GitHub API (via `gh` CLI) for pull request reviews, comments, and approvals (`gh-cli-pr-*` workflows).
- Playwright MCP / Chrome DevTools MCP for automated browser E2E, visual regression verification, and UI console log capture (`/kanche:qa-validate`, `/kanche:qa-review`).

## Known Technical Constraints
- Destructive operations policy: all destructive and remote-mutating actions (`git push`, `git commit`, `rm`, `rm -rf`, branch/tag deletion, PR merge) MUST gate on interactive human confirmation via `default_api:ask_question` unconditionally. (Grounded in `plugins/kanche/rules/destructive-safety.md` and `.docs/product/memory.md`.)
- Skills stand alone: individual skills are decoupled and never embed auto-mode bypass branches or caller-mode checks.
- AI Model routing: all 16 subagents in `plugins/kanche/agents/` and all 40 skills in `plugins/kanche/skills/` are unified on `model: flash` (Gemini Flash High).
- Safety invariants (protected-branch refusal, no force-push, no `--no-verify`, secrets detection, self-approval prohibition) are unconditional.
- Skill directories inside `plugins/kanche/skills/` use a flattened single-level directory structure (`plugins/kanche/skills/<skill-name>/SKILL.md`) for CLI plugin installation compatibility, and frontmatters specify `name: <skill-name>` so Antigravity registers slash commands as `/kanche:<skill-name>`.
