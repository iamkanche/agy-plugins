---
feature: qa
module: plugins
integrated_at: 2026-07-25
updated_at: 2026-07-25
---

# QA & Validation Plugin — Architectural Design

## Overview
Modular plugin providing testing, validation, and code review workflows (`plugins/qa`).

## Structure
- `plugin.json`: Defines metadata, output-language rules, skills directory, and agent (`validator`).
- `agents/`:
  - `validator/agent.json`
- `skills/`:
  - `validate/SKILL.md`
  - `test-plan/SKILL.md`
  - `review/SKILL.md`
