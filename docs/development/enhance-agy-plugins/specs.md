# Functional Specifications: Enhance agy-plugins Development Productivity

## Context
`agy-plugins` is the central developer plugin bundle for Google Antigravity (AGY). To maximize developer productivity, efficiency, and code quality during feature implementation and maintenance, `agy-plugins` needs strategic architecture upgrades including Loop Engineering convergence, AI-driven UI wireframing via StitchMCP, automated E2E & visual testing via Playwright / Chrome DevTools MCP, AI model-task tiering, and self-healing test repair loops.

## Scope

### In-scope
1. **Loop Engineering 2.0 State Tracking & Evaluation**: Enforce closed-loop generator-reviewer pairing in SDD workflows with structured `sdd-review` verdict outputs (`GO`/`NO-GO`) and state tracking (`loop-state.json`).
2. **StitchMCP UI Design Integration**: Integrate StitchMCP tools into design workflows to generate visual UI mockups, screen variants, and design systems during Phase P2 (Design).
3. **Playwright & Chrome DevTools MCP QA Integration**: Extend QA validation skills (`/kanche:qa-validate`, `/kanche:qa-review`) with browser automation, visual screenshots, and accessibility auditing (`a11y-debugging`).
4. **AI Model Tiering Strategy**: Define model assignment guidelines (`pro` for research/architecture/review, `flash` for coding/tasks/git) in subagent manifests and workflow configs.
5. **Self-Healing Test Repair Loop**: Automated feedback loop routing validation/build failures in P5 back to implementation (`/kanche:code-implement`) for up to 3 repair iterations.

### Out of scope / non-goals
- Modifying core Antigravity CLI binary binaries or external non-kanche plugins.
- Replacing existing Git / GitHub hard safety rules.

## User stories
- **As a Developer**, I want SDD review phases to automatically evaluate generator output and perform up to 3 closed-loop retry iterations, so that specification, design, and code quality are enforced without manual back-and-forth.
- **As a UI/UX Architect**, I want to generate visual UI screens and design tokens automatically using StitchMCP during P2 Design, so that UI specifications are clear and visual.
- **As a QA Engineer**, I want QA validation skills to use Playwright and Chrome DevTools MCP tools to execute live browser E2E and visual tests, so that regressions are caught automatically before PR deployment.
- **As a System Maintainer**, I want subagents to be routed to optimal AI model tiers (`pro` vs `flash`), so that complex research/reviews get high reasoning while code edits execute quickly and cost-effectively.

## Acceptance criteria
1. **Given** an SDD workflow execution (P1-P6), **When** a reviewer skill evaluates an artifact, **Then** it must emit a structured `sdd-review` verdict block containing `verdict: GO | NO-GO`, `loop_iteration`, and `findings`.
2. **Given** a `NO-GO` verdict with iterations remaining (<= 3), **When** the generator skill receives the feedback, **Then** it must perform targeted delta fixes addressing the findings automatically.
3. **Given** Phase P2 (Design), **When** UI wireframes or design systems are requested, **Then** the StitchMCP skill/tools (`create_project`, `generate_screen_from_text`, `create_design_system`) are available to produce visual UI specs in `design.md`.
4. **Given** Phase P5 (Validation), **When** `/kanche:qa-validate` is executed, **Then** it uses Playwright MCP / Chrome DevTools MCP tools (`browser_navigate`, `browser_screenshot`, `a11y-debugging`) for live browser & visual checks.
5. **Given** failing tests in P5, **When** validation fails, **Then** the self-healing test repair engine routes stack traces back to `/kanche:code-implement` for up to 3 retry attempts.
6. **Given** subagent definitions in `plugins/kanche/agents/`, **When** subagents are invoked, **Then** high-reasoning tasks (`analyst`, `architect`, `reviewer`, `quality_assurance`) default to model tier `pro`, and fast coding/task/git subagents default to `flash` or `inherit`.

## Data model
- **`loop-state.json`**: Entity storing execution loop state per SDD phase (`phase`, `current_iteration`, `max_loops`, `verdict`, `last_updated`).
- **`sdd-review` block**: Schema containing `verdict`, `loop_iteration`, and `findings` list (`severity`, `msg`, `file`, `line`, `fix_suggestion`).
- **Subagent Manifest (`agent.json`)**: Config schema specifying `name`, `model`, `tools`, and `system_prompt`.

## NFR (non-functional requirements)
- **Performance**: Generator-reviewer loop iterations must complete within 3 cycles maximum.
- **Reliability**: Closed-loop repair must not cause infinite retry loops.
- **Backwards Compatibility**: All changes must remain 100% compatible with existing `kanche` plugin skills and `docs/settings.json`.

## Open questions
- None.
