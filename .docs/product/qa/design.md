---
feature: qa
module: plugins
integrated_at: 2026-07-25
updated_at: 2026-07-25
---

# QA & Validation Plugin — Architectural Design

## Overview
Modular quality assurance, security scanning, browser automation, and review workflows (`plugins/kanche`).

## Structure
- `plugin.json`: Registers `@validator`, `@tester`, `@reviewer`, and `@security-engineer` subagents and related skills.
- `agents/`:
  - `validator/agent.json` (`model: flash`)
  - `tester/agent.json` (`model: flash`)
  - `reviewer/agent.json` (`model: flash`)
  - `security-engineer/agent.json` (`model: flash`)
- `skills/`:
  - `qa-validate/SKILL.md`
  - `qa-test-plan/SKILL.md`
  - `qa-review/SKILL.md` (emits `review-verdict`)
  - `code-review/SKILL.md` (emits `review-verdict`)
  - `security-scan/SKILL.md`

