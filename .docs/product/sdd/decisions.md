# SDD Plugin — Decisions (ADR log)

<!-- schema: decisions | written by /kanche:sdd-sync -->

## ADR-001: Double-Commit Checkpoint Policy
- **Context:** Committing at every single sub-phase (P1, P2, P3, P4) causes excessive git history clutter with tiny WIP commits.
- **Decision:** Consolidate documentation drafts (specs, design, tasks) into a single docs commit after P3, and implementation files into a single commit after P4.
- **Consequences:** Cleaner git logs and more coherent commit diffs.

## ADR-002: Slugs for Feature Folders and Branches
- **Context:** Numeric ID counters (e.g. `001_`) require tracking global state and prefix increments, creating unnecessary friction.
- **Decision:** Eliminate numeric ID prefixes and rely entirely on short-description feature slugs for both branch names and dev folders.
- **Consequences:** Simplified branch management and folder layout.

## ADR-003: Interactive Gating via AskQuestion
- **Context:** Command confirmations via text prompt (yes/no) interrupt execution flow and require manual typing in the terminal.
- **Decision:** Mandate using the `default_api:ask_question` tool for all human gates across all sdd manual phase transitions, validation checkpoints, and Level 2 gates.
- **Consequences:** Modal-driven, structured confirmations that prevent CLI disruption and reduce keystroke errors.

## ADR-004: Role-Based Specialized Subagents Partitioning
- **Context:** Running all SDD tasks through a single agent context leads to prompt bloating, context pollution, and safety risks if write tools are granted unconditionally.
- **Decision:** Partition the SDD workflow into 5 specialized subagents (analyst, architect, planner, coder, validator) mapped to phase-based skills, restricting write tools only to the coder and planner agents.
- **Consequences:** More modular prompt contexts, safer execution bounds, and improved execution quality.

## ADR-005: SDD Full Automation Development
- **Context:** Manual phase transitions, review loops, validation checks, and PR feedback tracking require frequent human interactions, slowing down autonomous development and causing context fragmentation.
- **Decision:** Automate all SDD workflow loops (specs/design/tasks/build reviews, validation fixing, and PR comments polling) up to a hard limit of 3x iterations. Introduce a verification receipt in P0 for upfront alignment, delegate phases to token-optimized subagents, and automate post-merge document sync and file preservation.
- **Consequences:** End-to-end headless capability that runs safely, minimizes token overhead, and maintains memory integrity without manual intervention.

## ADR-006: Layout Blowout and Clipping Fixes
- **Context:** Hardcoded card heights and grid column tracking created horizontal body scroll blowouts and bottom content clipping on smaller viewports.
- **Decision:** Apply flexible `minmax(0, 1fr)` tracks for main dashboard columns, use `min-width: 0` on content wrappers, and swap fixed heights for `min-height: 180px` on command cards.
- **Consequences:** Bulletproof viewport constraints that restrict horizontal scrolling solely to local SVG map and pipeline step scroll containers.

## ADR-007: LEVEL 1 AI (P0-P7) and LEVEL 2 Human (P8-P9) Workflow Partitioning
- **Context:** Coupling AI deployment loops with human review gates caused boundary confusion in automated SDD runs.
- **Decision:** Explicitly partition the 10 SDD phases into LEVEL 1 AI Automation (P0-P7: P1 specs loop, P2 design loop, P3 tasks loop & commit, P4 build loop & commit, P5 validation, P6 deploy & 3x PR review-respond loop with commit/push, P7 sdd-sync document promotion) and LEVEL 2 Human Review & Deployment (P8 gated human review checklist, P9 PR merge).
- **Consequences:** Clean separation of AI autonomous work (P0-P7) and human release authorization (P8-P9).
