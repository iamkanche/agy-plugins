# SDD Workflows Specification

## 1. Overview
Automates the Spec-Driven Development (SDD) lifecycle for autonomous Google Antigravity agents across phases P0 to P9.

## 2. Included Skills & Commands
- `/kanche:sdd-init`: Bootstraps steering guidelines (`product.md`, `tech.md`, `structure.md`, `rules.md`).
- `/kanche:sdd-init-update`: Re-analyzes repo and merges updates into steering guidelines.
- `/kanche:sdd-run`: Drives feature work items through the full SDD phase model (P0 to P9) with persistent `/goal` support.
- `/kanche:sdd-continue`: Resumes SDD workflow from on-disk state.
- `/kanche:sdd-steering`: Analyzes repository and returns steering guideline bodies.
- `/kanche:sdd-sync`: Promotes feature documentation to domain-level product directories (`.docs/product/{domain}/`) and cleans up dev folders.

## 3. Domain-Based Document Routing
- `/kanche:sdd-sync` maps modified skills and code paths to one of the core domain groups (`sdd`, `git`, `gh-cli`, `design`, `dev`, `planner`, `qa`, `scrum`).
- Document specifications and design decisions are merged into permanent `.docs/product/{domain}/specs.md` and `design.md` files rather than creating transient feature slug subfolders.

## 4. Product Invariants
- Preserves human-tuned guidelines and safety rules during updates.
- Orchestrates the full 16-agent autonomous engineering team and 40 skills across P0 to P9.
- Unconditional human confirmation gating for all destructive commands and checkpoints (`git commit`, `git push`, `rm -rf`, `gh pr merge`, branch/tag deletes) per `destructive-safety.md`. Non-destructive discovery, planning, coding, and validation steps run autonomously.
- Unified model routing: All 16 subagents and 40 skills are standardized on `model: flash` (Gemini Flash High) for ultra-fast, high-capability agentic execution.
- Decoupled standalone skills: Each skill operates independently with its own inputs, flags, and output protocols (`review-verdict`), decoupled from orchestrator internal state.
- `/kanche:sdd-run` supports `/goal` long-running persistent execution mode with automated retry loops and goal completion signaling.
- All commit checkpoints (P3 docs, P4 implementation, P6 PR fix, P7 sync) MUST use `/kanche:git-commit` to enforce Conventional Commits formatting.
- **Pre-Execution Skill Inspection**: Subagent delegation steps and orchestrator execution mandate calling `view_file` on `SKILL.md` before executing any workflow or CLI commands.
