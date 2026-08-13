---
name: scrum-pbi-create
description: Create structured Product Backlog Items (PBI) with user stories, acceptance criteria, priority, and story points under .docs/backlog/{domain}/.
model: pro
---

# /kanche:scrum-pbi-create

**Summary.** Create a standardized Scrum Product Backlog Item (PBI) with structured User Stories, Acceptance Criteria (Given/When/Then), Priority, Story Points, and Domain links under `.docs/backlog/{domain}/`. State every action before executing it.

## User input

The invocation arguments.

## Inputs

Parse the arguments:

- **title** (positional, required) — concise title for the Product Backlog Item (e.g. `User Authentication with OAuth2`).
- **`--priority=P0|P1|P2`** — priority level (default **P1**).
- **`--points=1|2|3|5|8|13`** — Fibonacci story points estimate (default **3**).
- **`--domain=<domain>`** — target product domain (`scrum`, `auth`, `billing`, `api`, `ui`, etc.; default **scrum**).
- **`--slug=<slug>`** — custom filename slug (derived from title if omitted).

If title is missing, ask the user for it using `default_api:ask_question`.

## Steps

### 1. Prepare Target Directory & Metadata
- Base directory: `.docs/backlog/{domain}/`
- Target domain: default `scrum` if not specified.
- Ensure target directory exists:
  ```bash
  mkdir -p .docs/backlog/{domain}
  ```
- Derive PBI ID timestamp / serial (e.g., `PBI-{YYYYMMDD}-{slug}`).

### 2. Generate PBI Document
Write the PBI document to `.docs/backlog/{domain}/{pbi_id}.md` using the standard PBI template:

```markdown
# {PBI_ID}: {Title}

- **ID:** {PBI_ID}
- **Domain:** {domain}
- **Priority:** {priority}
- **Story Points:** {points}
- **Status:** New

## Summary
{Brief overview of the backlog item}

## User Story
**As a** {role}  
**I want to** {action/feature}  
**So that** {benefit/value}  

## Acceptance Criteria
- [ ] **Given** {precondition}, **When** {action}, **Then** {expected outcome}.
- [ ] **Given** {edge case}, **When** {action}, **Then** {fallback outcome}.

## Technical Notes & Dependencies
- Architecture / API implications
- Relevant skills or subagent roles

## Linked Specs & Design
- Specs: `.docs/product/{domain}/specs.md`
- Design: `.docs/product/{domain}/design.md`
```

### 3. Register in Backlog Index
Append the PBI reference entry to `.docs/backlog/{domain}/backlog.md`:

```markdown
| PBI ID | Title | Priority | Story Points | Status | File |
|---|---|---|---|---|---|
| {PBI_ID} | {Title} | {priority} | {points} | New | [{pbi_id}.md](file://.docs/backlog/{domain}/{pbi_id}.md) |
```

### 4. Commit and Log
Commit the new PBI artifact using **/kanche:git-commit**:
- Message: `docs(scrum): add PBI {PBI_ID} - {Title}`

## Done when

- The structured PBI file is created under `.docs/backlog/{domain}/{PBI_ID}.md`.
- The PBI entry is registered in the backlog index (`.docs/backlog/{domain}/backlog.md`).
- All User Story and Acceptance Criteria fields follow standardized Scrum format.
