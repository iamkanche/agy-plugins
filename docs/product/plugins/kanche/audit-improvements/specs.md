# Specs: Audit Improvements for Security, Pre-Execution Inspection, and Skill Resilience

## Context
Following a security and architectural audit of `agy-plugins`, several key improvements were identified to harden repository security, prevent secret leaks, guarantee pre-execution inspection of `SKILL.md` contracts across all subagent delegations, and improve command argument resilience.

## Scope
- **In-Scope:**
  - Create root `.gitignore` file with comprehensive exclusions (`.env`, `*.log`, `node_modules/`, `.DS_Store`, etc.).
  - Update `plugins/kanche/skills/sdd-run/SKILL.md` to add explicit `view_file` pre-execution inspection steps for subagents before invoking subagent workflows.
  - Update `plugins/kanche/skills/gh-cli-pr-create/SKILL.md` to fallback cleanly if `--assignee "@me"` fails.
  - Update `@coder` subagent definition (`plugins/kanche/agents/coder/agent.json`) to constrain file edits to non-git operations.
- **Out of Scope:**
  - Rewriting underlying `gh` or `git` CLI binaries.

## User Stories
- **As a Developer/Agent**, I want a root `.gitignore` file, so that environment secrets or build logs are never accidentally staged or committed.
- **As a System Maintainer**, I want subagents to explicitly inspect target `SKILL.md` files before executing skill workflows, so that default flags (like `--merge`) are strictly obeyed.

## Acceptance Criteria
1. Given the repository root, when `git status` runs, ignored files (like `.env` or `*.log`) are untracked and excluded by `.gitignore`.
2. Given `sdd-run/SKILL.md`, when subagent delegation steps are listed, an explicit `view_file` pre-execution requirement is specified.
3. Given `gh-cli-pr-create/SKILL.md`, when `--assignee` is set, a fallback handles unresolvable `@me` parameters gracefully.
4. Given `@coder` subagent manifest (`plugins/kanche/agents/coder/agent.json`), prompt instructions restrict git side-effects to `@git-operator`.

## NFR (Non-Functional Requirements)
- Security: Zero hardcoded secrets staged or committed.
- Reliability: 100% adherence to skill contract defaults.
