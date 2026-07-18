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
