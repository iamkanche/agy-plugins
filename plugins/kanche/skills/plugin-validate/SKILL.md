---
name: plugin-validate
description: Validate Antigravity plugin structure, plugin.json schema, agents/*.md tools, rules triggers, hooks.json, skills, and index.html parity.
---

# /kanche:plugin-validate

**Summary.** Run deterministic structural and schema checks across an Antigravity plugin repository (`@validator`, `agents/validator.md`).

## Inputs

- `<repo-or-plugin-path>` (optional) — repository root or plugin root. Defaults to `.`.

## Steps

1. **Execute Validator Script:** Run [validate_plugin.py](./scripts/validate_plugin.py):
   ```bash
   python3 plugins/kanche/skills/plugin-validate/scripts/validate_plugin.py .
   ```
   (Fallback to `~/.gemini/config/plugins/kanche/skills/plugin-validate/scripts/validate_plugin.py .` when invoked outside `agy-plugins`.)
2. **Audit Checks Performed:**
   - `plugin.json`: valid JSON, strictly allowed top-level fields only, valid `logo` path, `suggestedPrompts` count `<= 3`.
   - `hooks.json`: valid JSON and referenced hook scripts exist.
   - `agents/*.md`: valid frontmatter (`name`, `description`, `subagent: true`, `mainAgent: false`) and valid Antigravity native `tools` names; flags legacy `agents/*/agent.json`.
   - `rules/*.md`: `AGENTS.md`/`GEMINI.md` has no frontmatter; other rule files declare valid `trigger:` frontmatter and stay under `24,000` bytes.
   - `skills/*/SKILL.md`: `name` matches folder, non-empty `description`, no `model:` frontmatter, no `{NNN}_{slug}`, no `/git:`, no `agent.json` references.
   - `index.html`: command/agent arrays match on-disk skills and agents with zero stale `@laravel-expert` / `agent.json` references.
3. **Report:** Output error/warning counts and exact `file:line` items. Exit code `0` required for pass.
