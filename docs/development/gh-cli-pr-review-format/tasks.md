# Task Manifest: gh-cli-pr-review-format

## Phase 1: Implementation (Skill Prompt Updates)

- [x] Task 1: Update Step 5 in `plugins/kanche/skills/gh-cli-pr-review/SKILL.md` to standardize inline comments structure with explicit `[<SEVERITY>] <Short description>`, `Issue:`, `Suggestion:` block, and `Why:` fields (Traces to `specs.md` AC3, AC4; `design.md` Components)
- [x] Task 2: Update Step 6 in `plugins/kanche/skills/gh-cli-pr-review/SKILL.md` to specify the `# Summary` header layout containing short description, severity score out of 10, total files, and total lines (Traces to `specs.md` AC1; `design.md` Components)
- [x] Task 3: [P] Update Step 6 in `plugins/kanche/skills/gh-cli-pr-review/SKILL.md` to include `## Review Summary` ASCII table specification with `| Severity | Count | Category |` using `🔴 HIGH`, `🟡 MEDIUM`, and `🟢 LOW` indicators (Traces to `specs.md` AC2; `design.md` Components)
- [x] Task 4: [P] Add verbatim template example in `plugins/kanche/skills/gh-cli-pr-review/SKILL.md` demonstrating the full review output structure without modifying underlying review logic or `@gh-operator` delegation (Traces to `specs.md` AC5; `design.md` Risks & Mitigations)

## Phase 2: Verification

- [x] Task 5: Perform static markdown inspection of `plugins/kanche/skills/gh-cli-pr-review/SKILL.md` to verify syntax validity, frontmatter metadata, and rule alignment (Traces to `docs/guidelines/tech.md` Tooling checks)
- [x] Task 6: Verify template completeness against all acceptance criteria (AC1 to AC5) in `specs.md` (Traces to `specs.md` AC1-AC5)

## Verification Commands

| Command / Check | Purpose | Criteria / Target |
|---|---|---|
| Static inspection of `plugins/kanche/skills/gh-cli-pr-review/SKILL.md` | Verify YAML frontmatter and markdown structure | Frontmatter intact, `# Summary`, `## Review Summary`, `### inline comments` sections present |
| Traceability matrix audit | Ensure all specs AC1-AC5 are addressed in tasks and skill template | AC1 (Summary), AC2 (Table), AC3 (Inline), AC4 (Suggestions), AC5 (No Regression) |
