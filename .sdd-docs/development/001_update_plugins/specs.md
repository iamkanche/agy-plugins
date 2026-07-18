# Update gh-cli and git Plugins — Specification

<!-- schema: specs | written by /sdd:specs -->

## Context
Google Antigravity utilizes named plugins (`gh-cli` and `git`) to perform operations. These need to be updated with new skills for pull request merging and tag management to support wider automation.

## Scope
- **In scope:**
  - `gh-cli` plugin: Adding a `/pr-merge` skill (with branch deletion as default), and updating the `/pr-create` skill to automatically assign the PR to the author (creator).
  - `git` plugin: Adding a `/tag-delete` skill and a `/tag-push` skill.
  - Updating the inspector `index.html` pages for both plugins and the marketplace dashboard `index.html` to register and explain these new skills.
- **Out of scope:**
  - Modifying other unrelated plugins (e.g., `sdd` rules/skills).
  - Complex merge queue integrations or remote repository branch protection changes.

## User stories
- As an agent developer, I want to merge pull requests and automatically clean up branches using `/gh-cli:pr-merge`.
- As a contributor, I want my PRs to be auto-assigned to me upon creation via `/gh-cli:pr-create`.
- As a release coordinator, I want to delete tags and push tags using namespaced slash commands `/git:tag-delete` and `/git:tag-push`.

## Acceptance criteria
1. `/gh-cli:pr-merge` successfully merges the PR. If `--keep-branch` is not passed, both local and remote feature branches are deleted.
2. `/gh-cli:pr-create` automatically appends `--assignee "@me"` by default to auto-assign the PR creator.
3. `/git:tag-delete` deletes the specified tag locally. If `--remote` is passed, it pushes the deletion to origin.
4. `/git:tag-push` pushes either a specific tag or all local tags to the remote origin.
5. All new commands must be documented and interactive in their respective plugin inspector `index.html` and marketplace `index.html` dashboards.

## Non-functional requirements
- Ensure all side-effects are human-gated behind a STOP confirm prompt.
- Retain existing design system, colors, and layout structure in the dashboards.

## Open questions
- None (fully specified).
