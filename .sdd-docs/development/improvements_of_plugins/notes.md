# Development Notes - improvements_of_plugins

## Grill Phase Questions & Assumptions

### 1. Options Format for Gates
- **Question**: When asking the user for confirmation (e.g. git push, commit), what options should the model provide in the `ask_question` modal?
- **Assumption if unanswered**: The options should be:
  1. `"(Recommended) Yes, proceed"` (mapped to continuing the workflow)
  2. `"No, abort"` (mapped to stopping/aborting)

### 2. Details/Context inside the Modal
- **Question**: How much details (e.g. diff, status, commit message) should be put inside the question text of the modal?
- **Assumption if unanswered**: The full context (such as the commit message or the command to run) should be passed in the `question` argument so the user sees exactly what they are approving in the modal.

### 3. Read Only Gates
- **Question**: Are read-only actions (like git status or git diff) gated by the `ask_question` tool?
- **Assumption if unanswered**: No, only repository-modifying actions/side effects (git commit, git push, tag creation, PR creation, PR approval) are human-gated.

## Readiness
The feature is ready for specifications.
