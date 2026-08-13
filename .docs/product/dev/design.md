# System Design: Rename dev-implement to code-implement & Update index.html

## Architecture & Design

### Component Modifications
1. **Skill Renaming:**
   - `plugins/kanche/skills/dev-implement/SKILL.md` moved to `plugins/kanche/skills/code-implement/SKILL.md`.
   - Update frontmatter to `name: code-implement`.

2. **Subagent & SDD Integration:**
   - `plugins/kanche/agents/coder/agent.json`: update `system_prompt` from `dev-implement` to `code-implement`.
   - `plugins/kanche/skills/sdd-run/SKILL.md`: replace `/kanche:dev-implement` with `/kanche:code-implement` in P4 table & steps.
   - `plugins/kanche/skills/sdd-continue/SKILL.md`: replace `/kanche:dev-implement` with `/kanche:code-implement`.

3. **Dashboard Registry (`index.html`):**
   - In `qaCommands`: Add `code-review` and `security-scan`.
   - Rename `devCommands` to `codeCommands` or keep key while updating name/path to `/kanche:code-implement` and `plugins/kanche/skills/code-implement/SKILL.md`.
   - In `agentsData`: Update `@coder` skill list to `["/kanche:code-implement"]`.
   - In `sddWorkflowPhases`: Update P4 skills array to reference `/kanche:code-implement`.
