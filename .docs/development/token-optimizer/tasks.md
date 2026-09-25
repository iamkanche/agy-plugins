# Topological Task DAG: Token Optimizer Agents & Global Token Optimization

- **Feature:** Token Optimizer Agents & Global Token Optimization
- **Slug:** `token-optimizer`
- **PBI:** `PBI-20260926-token-optimizer`
- **Domain:** `optimizer`

## Tier 0: Models, Contracts & Core Rules

- [ ] `T0.1` [P] Create `plugins/kanche/rules/token-optimization.md` defining token economy heuristics, telegraphic styling, anti-bloat directives, and context caching rules.
- [ ] `T0.2` [P] Create `plugins/kanche/agents/token-optimizer/agent.json` declaring `@token-optimizer` subagent with `model: flash`, read-only tools, and compact token-distillation prompt.

## Tier 1: Core Services & Agent Prompt Optimization

- [ ] `T1.1` [P] Create `plugins/kanche/skills/token-optimize/SKILL.md` implementing standalone token audit, compression analysis, and prompt distillation engine.
- [ ] `T1.2` Apply token optimization principles to all 16 existing agents in `plugins/kanche/agents/*/agent.json` (analyst, architect, backend-expert, coder, designer, devops, frontend-expert, gh-operator, git-operator, planner, researcher, reviewer, scrum-master, security-engineer, tester, validator) ensuring lean system prompts while preserving exact boundaries and tools.

## Tier 2: Universal Skill Optimization & Presentation

- [ ] `T2.1` Apply token optimization to all skills in `plugins/kanche/skills/*/SKILL.md` (distilling unnecessary verbiage, consolidating repetitive guidelines, retaining 100% inputs, safety gating, and schemas).
- [ ] `T2.2` [P] Update `plugins/kanche/plugin.json` with updated description, keywords, and 17-agent team count.
- [ ] `T2.3` [P] Update `README.md` to document the `@token-optimizer` agent and `/kanche:token-optimize` command.
- [ ] `T2.4` [P] Update `index.html` to add the `@token-optimizer` agent card in the team grid, update agent counts, and add the `/kanche:token-optimize` skill badge.

## Tier 3: Validation, Synchronization & Docs

- [ ] `T3.1` [P] Execute JSON syntax and schema validation across all `agent.json` and `plugin.json` files.
- [ ] `T3.2` [P] Measure and benchmark token reduction savings across the codebase, confirming zero functional regression or broken safety gates.
- [ ] `T3.3` [P] Synchronize changes from `agy-plugins/plugins/kanche` to local installed plugin `/home/kenneth-ancheta/.gemini/config/plugins/kanche`.

## Verification Checkpoints

```bash
# 1. Validate all agent JSON files
for f in agy-plugins/plugins/kanche/agents/*/agent.json; do jq . "$f" >/dev/null && echo "VALID: $f"; done

# 2. Validate plugin.json
jq . agy-plugins/plugins/kanche/plugin.json >/dev/null && echo "VALID: plugin.json"

# 3. Verify safety invariants preserved across all skills
grep -rn "destructive-safety" agy-plugins/plugins/kanche/skills/ | wc -l
```
