# Functional Specifications: Token Optimizer Agents & Global Token Optimization

- **Feature:** Token Optimizer Agents & Global Skill/Agent Optimization
- **Slug:** `token-optimizer`
- **PBI:** `PBI-20260926-token-optimizer`
- **Domain:** `optimizer`
- **Status:** Draft

## Context
Large Language Models (LLMs) operate under finite context windows and per-token pricing/latency models. In multi-agent autonomous engineering suites like `kanche`, repetitive preambles, verbose markdown phrasing, unoptimized system prompts, and duplicated instructions inflate context window usage across multi-turn agent conversations. Introducing a dedicated `@token-optimizer` agent along with systematic token pruning, compact instructional grammars, and `/kanche:token-optimize` ensures substantial token savings across all 46+ skills and 16+ agents without degrading functional execution or compromising destructive action safety.

## Scope

### In-Scope
- **Agent Definition:** New `@token-optimizer` agent in `plugins/kanche/agents/token-optimizer/agent.json` configured with `model: flash`, read-only tools, and token minimization heuristics.
- **Skill Addition:** New `/kanche:token-optimize` skill in `plugins/kanche/skills/token-optimize/SKILL.md` capable of analyzing and compressing prompts, rule files, and skill markdown documents.
- **Rule Addition:** New token economy rule `plugins/kanche/rules/token-optimization.md` establishing universal token minimization standards (anti-bloat, information density, telegraphic instruction patterns, context cache friendliness).
- **Systematic Optimization:** Apply token optimization across all existing agents in `plugins/kanche/agents/` and skills in `plugins/kanche/skills/`, stripping redundant text and padding while maintaining 100% semantic fidelity and all required flags/interfaces.
- **Documentation & UI Alignment:** Update `plugins/kanche/plugin.json`, `README.md`, and `index.html` to reflect the 17-agent team and token optimization capabilities.
- **Local Plugin Mirroring:** Sync changes to `/home/kenneth-ancheta/.gemini/config/plugins/kanche`.

### Out of Scope / Non-Goals
- Modifying underlying LLM model weights or external API protocols.
- Bypassing or loosening any safety invariants or human confirmation checks.
- Eliminating required CLI arguments, parameters, or step sequence requirements.

## User Stories
- **US-1 (Agent Invocation):** As an engineering workflow or developer, I want to invoke `@token-optimizer` to audit and compress prompts, workflows, and rule sets, so that token usage is minimized across my project.
- **US-2 (Skill Execution):** As a developer or agent, I want to run `/kanche:token-optimize` on any file or directory, so that redundant tokens, bloated prose, and duplicated constraints are distilled into high-density instructions.
- **US-3 (Universal Efficiency):** As a developer running `kanche` workflows, I want all skills and agent system prompts to consume minimum context tokens, so that overall execution is faster, cheaper, and avoids hitting context window limits.

## Acceptance Criteria
1. **AC-1 (Agent Registration):** Given the agent registry `plugins/kanche/agents/token-optimizer/agent.json`, when inspected, then it must declare `name: "token-optimizer"`, `model: "flash"`, `enable_write_tools: false`, and specialized token optimization system prompts.
2. **AC-2 (Skill Contract):** Given the `/kanche:token-optimize` skill, when invoked with a target file or `--path`, then it analyzes token usage, identifies compression opportunities (deduplication, telegraphic syntax, table compaction), and outputs optimized content with estimated token reduction metrics.
3. **AC-3 (Safety Invariance):** Given any optimized skill or agent in `plugins/kanche/`, when executed, then all destructive action gating (`destructive-safety.md`, `default_api:ask_question`), review verdict interfaces (`review-verdict`), and argument schemas remain completely intact.
4. **AC-4 (Global Token Reduction):** Given the audited skills and agent prompts, when compared against pre-optimization state, then total token/character count across prompt files is measurably reduced (target ≥ 15-25% reduction in non-essential token overhead) with zero semantic regression.
5. **AC-5 (Team Catalog & UI):** Given `plugin.json`, `README.md`, and `index.html`, when rendered, then the total subagent count reflects 17 agents, including the Research & Architecture / Performance category with `@token-optimizer`.

## Data Model & Impact Subgraph
- **New Nodes:**
  - `agent:token-optimizer` (depends on `rules/token-optimization.md`)
  - `skill:token-optimize` (depends on `agent:token-optimizer`)
  - `rule:token-optimization.md` (consumed by all skills and agents)
- **Modified Nodes:**
  - `agents/*` (all 16 existing agents distilled for token efficiency)
  - `skills/*` (all 46 existing skills pruned for high information density)
  - `plugin.json`, `README.md`, `index.html`

## Non-Functional Requirements (NFR)
- **Token Efficiency:** Measurable reduction in character and token count across agent prompts and skill files.
- **Determinism:** Zero ambiguity introduced into execution steps or schemas.
- **Security & Safety:** Complete adherence to zero autonomous destructive actions policy.

## Open Questions & Assumptions
- *Assumption:* Subagent model for `@token-optimizer` should default to `flash` to maintain consistency with all other kanche agents.
