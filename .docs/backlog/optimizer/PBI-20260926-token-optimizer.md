# PBI-20260926-token-optimizer: Add Token Optimizer Agent and Apply to Skills & Agents

- **ID:** PBI-20260926-token-optimizer
- **Domain:** optimizer
- **Priority:** P1
- **Story Points:** 5
- **Status:** In Progress

## Summary
Introduce the `@token-optimizer` subagent and associated optimization capabilities (`/kanche:token-optimize`, token economics guidelines, context minimization patterns) to the `kanche` developer suite. Apply token optimization across all skills, agent definitions, and rule systems to maximize context efficiency, reduce token usage and costs, eliminate bloat, and maintain 100% functionality and strict safety invariants.

## User Story
**As an** AI agent, developer, or team using the `kanche` plugin bundle in Google Antigravity  
**I want to** leverage a specialized `@token-optimizer` agent and systematically optimized skills, agent definitions, and workflows  
**So that** LLM context windows are preserved, token costs and response latencies are minimized, and all skills execute concisely with zero loss in capabilities or safety gating.

## Acceptance Criteria
- [ ] **Given** the agent ecosystem, **When** `@token-optimizer` is registered in `plugins/kanche/agents/token-optimizer/agent.json`, **Then** it operates with `model: flash`, specialized prompt distillation instructions, token budgeting, and zero write permissions by default.
- [ ] **Given** the skill catalog, **When** `/kanche:token-optimize` is executed or called, **Then** it analyzes target prompt files, SKILL.md documents, or agent configurations, identifying token bloat, redundant instructions, and emitting high-efficiency compressed alternatives.
- [ ] **Given** all existing skills in `plugins/kanche/skills/` and agents in `plugins/kanche/agents/`, **When** the token optimization is applied, **Then** verbosity, repetitive text, and excessive framing are distilled into concise actionable instructions, while strictly maintaining all input schemas, safety invariants, destructive action gating, and review interfaces.
- [ ] **Given** the plugin registry and docs, **When** `plugin.json`, `README.md`, and `index.html` are rendered, **Then** the new `@token-optimizer` agent (17 agents total) and `/kanche:token-optimize` skill are displayed in the showcase catalog and flow.
- [ ] **Given** the automated validation suite, **When** `/kanche:qa-validate` runs, **Then** all JSON structures, schemas, and links validate cleanly with zero regressions.

## Technical Notes & Dependencies
- New agent: `plugins/kanche/agents/token-optimizer/agent.json`
- New skill: `plugins/kanche/skills/token-optimize/SKILL.md`
- Token optimization guidelines & rule: `plugins/kanche/rules/token-optimization.md`
- Affected components: all `plugins/kanche/skills/*/SKILL.md`, `plugins/kanche/agents/*/agent.json`, `plugins/kanche/plugin.json`, `README.md`, `index.html`.

## Linked Specs & Design
- Specs: `.docs/product/optimizer/specs.md`
- Design: `.docs/product/optimizer/design.md`
