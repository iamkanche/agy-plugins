# System Design: Audit Improvements for Security, Pre-Execution Inspection, and Skill Resilience

## Approach
Implement surgical security, pre-execution verification, and subagent prompt refinements to reinforce codebase security, guarantee pre-execution inspection of `SKILL.md` files across all orchestrations, and make CLI commands resilient against edge-case flags.

## Architecture Context & Affected Files
1. **Root Configuration:**
   - `.gitignore` (New file: Root secret & artifact exclusion)
2. **Plugins & Skills:**
   - `plugins/kanche/skills/sdd-run/SKILL.md` (Update P1-P4 orchestration instructions to mandate `view_file` pre-execution inspection)
   - `plugins/kanche/skills/gh-cli-pr-create/SKILL.md` (Add fallback logic for `--assignee` when `@me` cannot be resolved)
3. **Subagents:**
   - `plugins/kanche/agents/coder/agent.json` (Refine system prompt to prohibit git mutations and restrict edits to target files)

## Component Modifications
- **.gitignore:** Define exclusion rules for `.env`, `*.log`, `node_modules/`, `.DS_Store`, `.gemini/`, `scratch/`, and temporary build outputs.
- **sdd-run SKILL.md:** Include an explicit pre-execution step: *"Before executing any phase workflow or delegating to a subagent, invoke `view_file` on `plugins/kanche/skills/<skill>/SKILL.md` to verify default flags and execution steps."*
- **gh-cli-pr-create SKILL.md:** Update Step 7 to attempt `gh pr create --assignee "@me"` and fallback to `gh pr create` without `--assignee` if user assignment fails.
