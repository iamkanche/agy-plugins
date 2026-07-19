# SDD Plugin — Decisions (ADR log)

<!-- schema: decisions | written by /sdd:sync-product -->

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

