# SDD P9 Alignment Sequence Optimization - Specification

## Context
Currently, the Software Development Document (SDD) Level 2 alignment sequence (P9) merges the PR via `/gh-cli:pr-merge` first, and then runs `/sdd:sync` to promote files to the product folder and clean up the dev folder. This introduces two issues:
1. Pushing synchronized documentation directly to the main branch after merge is often blocked by branch protection rules on the default branch (e.g. `main`).
2. It fragments the work into two separate operations: the feature PR and a secondary documentation commit on the default branch.

By running `/sdd:sync` immediately *after PR approval*, committing/pushing the sync files directly to the feature branch, and then executing `/gh-cli:pr-merge`, all implementation and final documentation changes are consolidated into a single PR and branch. The PR merge automatically includes the finalized product documentation and deletes the branch.

This specification details the logic changes to `/sdd:run` and `/sdd:sync`, along with the visual and structural updates to the interactive connections map in `plugins/sdd/index.html`.

## Scope
### In-Scope
- Refactoring the sequence in `/sdd:run` (specifically Level 2, P9) to execute `/sdd:sync` (and its nested commit/push) on the feature branch after PR approval, and subsequently call `/gh-cli:pr-merge`.
- Updating the interactive graph in `plugins/sdd/index.html` (nodes, coordinates, steps, and edges) to represent this new sequence.
- Ensuring `/sdd:run` waits for status checks of the new doc-sync commit to pass (if status checks are configured) before triggering the merge.
- Updating root `index.html` details if necessary to align with the new sequence.

### Out-of-Scope
- Bypassing branch protection rules or force-pushing.
- Modifying how `/sdd:sync` works internally (its core promotion logic remains unchanged, but its execution context is updated to run on the feature branch).

## User Stories
- **As an Antigravity agent or developer running `/sdd:run`**, I want the final documentation promotion to happen on the feature branch before merging, so that all changes are merged together cleanly and default branch protection rules are not violated.
- **As a developer inspecting the registry dashboard (`plugins/sdd/index.html`)**, I want the connection graph and steps to accurately reflect the real sequence of command execution.

## Acceptance Criteria
### Automated / Orchestrated Flow (`auto` mode)
1. **Given** a pull request that has been approved in P8,
   **When** `/sdd:run` transitions to P9,
   **Then** the orchestrator must execute `/sdd:sync` locally.
2. **Given** `/sdd:sync` has completed locally,
   **When** it stages and commits the sync changes,
   **Then** it must push the commit to the remote feature branch (associated with the open PR).
3. **Given** the new doc-sync commit has been pushed,
   **When** there are pending status/CI checks on the pull request,
   **Then** `/sdd:run` must poll and wait for all status checks to pass before merging.
4. **Given** status checks have passed,
   **When** `/sdd:run` executes the merge,
   **Then** it must invoke `/gh-cli:pr-merge` (without the `--keep-branch` flag) to squash/merge the PR and delete both the remote and local feature branches.

### Manual Flow (`manual` mode)
5. **Given** `/sdd:run` is in manual mode and has transitioned to P9,
   **When** documentation sync is ready to execute,
   **Then** the system must prompt: "Proceed with running /sdd:sync to promote docs and push to the feature branch? [Yes|No]".
6. **Given** the sync has pushed successfully,
   **When** the pull request is ready to merge,
   **Then** the system must prompt: "Proceed with running /gh-cli:pr-merge to merge the PR and clean up feature branch? [Yes|No]".

### UI Dashboard (`plugins/sdd/index.html`)
7. **Given** the interactive connections map renders,
   **When** checking node coordinates,
   **Then** `/sdd:sync` must be positioned at `x: 1080, y: 540` and `/gh-cli:pr-merge` must be positioned at `x: 1080, y: 640`.
8. **Given** the connection paths render,
   **When** tracing the sequence edges,
   **Then** there must be:
   - A sequential edge from `/gh-cli:pr-approve` (`x: 1220, y: 540`) to `/sdd:sync` (`x: 1080, y: 540`).
   - A sequential edge from `/sdd:sync` (`x: 1080, y: 540`) to `/gh-cli:pr-merge` (`x: 1080, y: 640`).
   - No direct sequential edge from `/gh-cli:pr-merge` to `/sdd:sync`.
   - No direct sequential edge from `/sdd:sync` to `/git:branch-delete`.
9. **Given** the `/sdd:run` command details panel is selected,
   **When** viewing the steps list,
   **Then** the steps must include:
   - `P7: Human review`
   - `P8: PR mods & approval`
   - `P9: Sync documentation & Merge` (describing the sync-before-merge order).

## Data Model & Graph Transitions
The graph layout modifications in `plugins/sdd/index.html` are:

### Nodes (Updates)
- `/sdd:sync`:
  - `x`: 1080
  - `y`: 540 (swapped with `pr-merge` to keep visual flow tidy)
  - `phase`: `"P9 Sync"`
- `/gh-cli:pr-merge`:
  - `x`: 1080
  - `y`: 640 (swapped with `sync`)
  - `phase`: `"P9 Merge"` (updated from `"P8 Merge"`)

### Edges (Updates)
- **Remove**: `{ from: "/gh-cli:pr-approve", to: "/gh-cli:pr-merge", type: "sequence" }`
- **Remove**: `{ from: "/gh-cli:pr-merge", to: "/sdd:sync", type: "sequence" }`
- **Remove**: `{ from: "/sdd:sync", to: "/git:branch-delete", type: "sequence" }`
- **Add**: `{ from: "/gh-cli:pr-approve", to: "/sdd:sync", type: "sequence" }`
- **Add**: `{ from: "/sdd:sync", to: "/gh-cli:pr-merge", type: "sequence" }`

## Non-Functional Requirements (NFR)
- **Performance**: The polling frequency of status/CI checks on the newly pushed commit should be configurable via `.sdd-docs/settings.json` (default 30 seconds, maximum 3 retries/checks or until timeout).
- **Security**: No tokens or credentials may be leaked or stored during the push/merge operation.
- **Traceability**: All transitions and command logs must be printed to the execution stdout/logs for auditing.

## Open Questions
- **CI Triggering on Doc Pushes**: What happens if the docs-only push triggers a CI check that takes a long time?
  - *Assumption*: We will poll with a configurable timeout. If CI fails, the orchestrator aborts or prompts the user (in manual mode).
