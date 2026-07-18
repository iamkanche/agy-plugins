# Specifications - Interactive Gating via AskQuestion

## Context
Antigravity custom plugins (git, gh-cli, sdd) currently use text-based inputs (like `[Yes|No]`) to confirm gated actions. Text-based confirmations can be error-prone and disrupt the agent's flow. Utilizing the `default_api:ask_question` tool provides a structured, modal-driven popup interface for human confirmation, improving the usability and robustness of gated operations.

## Scope
- **In Scope:**
  - Updating the steering rules and individual command/skill definitions in `git`, `gh-cli`, and `sdd` to mandate and use the `default_api:ask_question` tool for all human gates.
  - Ensuring the question context shown in the modal contains all necessary information (e.g. proposed commits, diffs, branch details) so the user can make an informed decision.
  - Specifying the exact options layout (e.g. `(Recommended) Yes, proceed`, `No, abort`).
- **Out of Scope / Non-Goals:**
  - Developing new MCP tools or browser-based popups (we must use the existing `default_api:ask_question` tool).
  - Modifying non-gated read-only operations.

## User Stories
- **As a Developer/User**, I want the agent to present interactive modals for confirmations so that I do not need to manually type `yes` or `no` in a text prompt.
- **As a Developer/User**, I want to see the full details of what is being confirmed within the modal so that I can confidently approve or decline the action.

## Acceptance Criteria
1. **Interactive Gating for Commit:**
   - Given staged changes, when `/git:commit` is run, the agent must invoke `default_api:ask_question` to ask if the user wants to commit with the generated message.
   - The options presented must include a clear option to proceed and a clear option to abort.
2. **Interactive Gating for Push:**
   - Given a branch to push, when `/git:push` is run, the agent must invoke `default_api:ask_question` showing the target branch, remote, and command, asking for confirmation.
3. **Interactive Gating for SDD Transitions:**
   - Given a manual SDD run, when transitioning to a new phase or handling validation/verdict loops, the agent must call `default_api:ask_question` to determine how to proceed.
4. **General Side Effects Gating:**
   - All other side effects (tag creation, branch deletion, PR creation, PR approval) must use `default_api:ask_question` for gating.

## Data Model
There are no changes to database entities or schemas as this is a configuration/rules update.

## NFR (Non-functional requirements)
- **Usability:** The gating prompt must be clear and readable in the UI modal form.
- **Reliability:** If the user declines (selects "abort" or skips), the execution must stop cleanly without running any side-effect commands.

## Open Questions
- None.
