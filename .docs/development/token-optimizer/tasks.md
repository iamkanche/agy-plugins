# Topological Task DAG: Token Optimizer Agents & Global Token Optimization

- **Feature:** Token Optimizer Agents & Global Token Optimization
- **Slug:** `token-optimizer`
- **PBI:** `PBI-20260926-token-optimizer`
- **Domain:** `optimizer`

## Tier 0: Models, Contracts & Core Rules

- [x] `T0.1` [P] Create `plugins/kanche/rules/token-optimization.md` defining token economy heuristics, telegraphic styling, anti-bloat directives, response formatting (short & direct, bullets), and context caching rules.
- [x] `T0.2` [P] Create `plugins/kanche/agents/token-optimizer/agent.json` declaring `@token-optimizer` subagent with `model: flash`, read-only tools, and compact token-distillation prompt.

## Tier 1: Core Services & Agent Prompt Optimization

- [x] `T1.1` [P] Create `plugins/kanche/skills/token-optimize/SKILL.md` implementing standalone token audit, compression analysis, and prompt distillation engine.
- [x] `T1.2` Apply token optimization principles to all 16 existing agents in `plugins/kanche/agents/*/agent.json` (analyst, architect, backend-expert, coder, designer, devops, frontend-expert, gh-operator, git-operator, planner, researcher, reviewer, scrum-master, security-engineer, tester, validator) ensuring lean system prompts, explicit `@token-optimizer` standards, short/direct bullet rules, while preserving exact boundaries and tools.

## Tier 2: Universal Skill Optimization & Presentation

- [x] `T2.1` Apply token optimization to all skills in `plugins/kanche/skills/*/SKILL.md` (distilling unnecessary verbiage, consolidating repetitive guidelines, retaining 100% inputs, safety gating, and schemas).
- [x] `T2.2` [P] Update `plugins/kanche/plugin.json` with updated description, keywords, and 17-agent team count.
- [x] `T2.3` [P] Update `README.md` to document the `@token-optimizer` agent and `/kanche:token-optimize` command.
- [x] `T2.4` [P] Update `index.html` to add the `@token-optimizer` agent card in the team grid, update agent counts, and add the `/kanche:token-optimize` skill badge.

## Tier 3: Validation, Synchronization & Docs

- [x] `T3.1` [P] Execute JSON syntax and schema validation across all `agent.json` and `plugin.json` files.
- [x] `T3.2` [P] Measure and benchmark token reduction savings across the codebase, confirming zero functional regression or broken safety gates.
- [x] `T3.3` [P] Verify repository plugin integrity in `agy-plugins/plugins/kanche`.

## Verification Checkpoints

```bash
# 1. Validate all agent JSON files
for f in agy-plugins/plugins/kanche/agents/*/agent.json; do jq . "$f" >/dev/null && echo "VALID: $f"; done

# 2. Validate plugin.json
jq . agy-plugins/plugins/kanche/plugin.json >/dev/null && echo "VALID: plugin.json"

# 3. Verify safety invariants preserved across all skills
grep -rn "destructive-safety" agy-plugins/plugins/kanche/skills/ | wc -l
```
