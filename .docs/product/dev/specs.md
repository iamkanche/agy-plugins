# Functional Specification: Rename dev-implement to code-implement & Update index.html

## Overview
Align skill naming by renaming `dev-implement` to `code-implement` across skills, subagents, steering docs, and SDD orchestrators. In addition, update `index.html` to register all missing skills (`code-review`, `code-implement`, `security-scan`) and ensure the dashboard is fully aligned.

## Requirements
1. **Rename Skill Folder & Frontmatter:**
   - Move `plugins/kanche/skills/dev-implement/` → `plugins/kanche/skills/code-implement/`.
   - Update frontmatter `name: code-implement` and title `# /kanche:code-implement`.
   - Update return data references inside `SKILL.md`.

2. **Update Subagent & SDD References:**
   - Update `@coder` subagent definition (`plugins/kanche/agents/coder/agent.json`) to reference `code-implement` skill.
   - Update SDD orchestrators (`sdd-run/SKILL.md`, `sdd-continue/SKILL.md`) to invoke `/kanche:code-implement` in Phase P4 (Build).
   - Update documentation (`README.md`, `.docs/guidelines/structure.md`, product specs/changelogs).

3. **Update Dashboard (`index.html`):**
   - Update command definition `devCommands` / `codeCommands` from `/kanche:dev-implement` to `/kanche:code-implement` with path `plugins/kanche/skills/code-implement/SKILL.md`.
   - Add `/kanche:code-review` and `/kanche:security-scan` to `qaCommands`.
   - Update `agentsData` `@coder` skills to `["/kanche:code-implement"]`.
   - Update `sddWorkflowPhases` P4 (Build) skills list to show `/kanche:code-implement`.
