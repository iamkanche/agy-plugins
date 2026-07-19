# Implementation Tasks - SDD Full Automation Development

## Phase 1: Implementation of Core Automation Skill
- [ ] Task 1.1: Update `plugins/sdd/skills/run/SKILL.md` to include verification receipt generation and confirmation gate (branch, base, target, title, slug) in Phase P0 (Traceability: AC-1)
- [ ] Task 1.2: Add subagent delegation instructions for Phase P1 (sdd-analyst), Phase P2 (sdd-architect), Phase P3 (sdd-planner), Phase P4 (sdd-coder), and Phase P5 (sdd-validator) to `plugins/sdd/skills/run/SKILL.md` (Traceability: AC-2)
- [ ] Task 1.3: Update `plugins/sdd/skills/run/SKILL.md` with instructions for parsing `.sdd-docs/settings.json` and merging with defaults (Traceability: AC-3)
- [ ] Task 1.4: Add 3x loop limits for inner phases (P1-P4) in subagent contexts to `plugins/sdd/skills/run/SKILL.md` (Traceability: AC-3)
- [ ] Task 1.5: Add 3x validation fix loop (P5) in validator subagent context to `plugins/sdd/skills/run/SKILL.md` (Traceability: AC-4)
- [ ] Task 1.6: Add 3x PR feedback polling and automatic response loop (P6-P8) to `plugins/sdd/skills/run/SKILL.md` (Traceability: AC-5)
- [ ] Task 1.7: Add automatic PR merge and post-merge document synchronization to `plugins/sdd/skills/run/SKILL.md` (Traceability: AC-6, AC-7)
- [ ] Task 1.8: Add preservation instructions for `memory.md` and `settings.json` during sync phase to `plugins/sdd/skills/run/SKILL.md` (Traceability: AC-7)
- [ ] Task 1.9: Add final briefing notification template to `plugins/sdd/skills/run/SKILL.md` (Traceability: AC-8)

## Phase 2: Validation & Review
- [ ] Task 2.1: Verify the updated `plugins/sdd/skills/run/SKILL.md` matches formatting guidelines (Traceability: NFR-Security)
- [ ] Task 2.2: Perform a lint/review on the workspace using custom format checks (Traceability: NFR-Resilience)

## Verification
- **Validation Command**: We will perform a dry-run check or read the updated skill file to ensure all instructions are completely documented, consistent, and syntactically valid.
- **Coverage Map**:
  - AC-1 covered by receipt presentation gate check in SKILL.md.
  - AC-2 covered by subagent delegation checks in SKILL.md.
  - AC-3 covered by dry-run and review of loop logic in SKILL.md.
  - AC-4 covered by dry-run and review of validation fix logic in SKILL.md.
  - AC-5 covered by dry-run and review of PR comment checking logic in SKILL.md.
  - AC-6 covered by dry-run and review of PR merge logic in SKILL.md.
  - AC-7 covered by checking file preservation and sync rules in SKILL.md.
  - AC-8 covered by checking the briefing output instructions in SKILL.md.
