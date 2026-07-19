# Tasks Checklist - SDD P9 Alignment Sequence Optimization

This checklist outlines the implementation tasks and verification checks required to reorder the SDD P9 sequence and update the visual workflow graph.

## Phase 1: Modify `/sdd:run` Skill Documentation
- [ ] Edit [SKILL.md](file:///home/kenneth-ancheta/src/github.com/agy-plugins/plugins/sdd/skills/run/SKILL.md#L30-L40) under `## Phase model` to swap `/gh-cli:pr-merge` and `/sdd:sync` in the Level 2 diagram columns. [Trace: specs:AC-7, design:Components]
- [ ] Edit [SKILL.md](file:///home/kenneth-ancheta/src/github.com/agy-plugins/plugins/sdd/skills/run/SKILL.md#L125-L130) under `### P7–P9 — Level 2 Automation` to detail the updated sequence:
  - Run `/sdd:sync` locally and push to the feature branch.
  - Wait/poll for status checks on the new commit (retrieving settings from `.sdd-docs/settings.json`).
  - Run `/gh-cli:pr-merge` (without `--keep-branch`) to squash/merge the PR and delete branches.
  - Set up prompt gates for `/sdd:sync` and `/gh-cli:pr-merge` under manual mode.
  [Trace: specs:AC-1, specs:AC-2, specs:AC-3, specs:AC-4, specs:AC-5, specs:AC-6, design:Components]

## Phase 2: Modify Connections Map Coordinates and Edges
- [ ] Edit [index.html](file:///home/kenneth-ancheta/src/github.com/agy-plugins/plugins/sdd/index.html#L997-L998) to update coordinates in the `nodes` array:
  - Set `/sdd:sync` coordinates to `x: 1080, y: 540, phase: "P9 Sync"`.
  - Set `/gh-cli:pr-merge` coordinates to `x: 1080, y: 640, phase: "P9 Merge"`.
  [Trace: specs:AC-7, design:Nodes (Updates)]
- [ ] Edit [index.html](file:///home/kenneth-ancheta/src/github.com/agy-plugins/plugins/sdd/index.html#L1038-L1040) to update edges in the `edges` array:
  - Remove `{ from: "/gh-cli:pr-approve", to: "/gh-cli:pr-merge", type: "sequence" }`
  - Remove `{ from: "/gh-cli:pr-merge", to: "/sdd:sync", type: "sequence" }`
  - Remove `{ from: "/sdd:sync", to: "/git:branch-delete", type: "sequence" }`
  - Add `{ from: "/gh-cli:pr-approve", to: "/sdd:sync", type: "sequence" }`
  - Add `{ from: "/sdd:sync", to: "/gh-cli:pr-merge", type: "sequence" }`
  [Trace: specs:AC-8, design:Edges (Updates)]

## Phase 3: Modify `/sdd:run` Detail Steps List
- [ ] Edit [index.html](file:///home/kenneth-ancheta/src/github.com/agy-plugins/plugins/sdd/index.html#L751-L759) to append the following step objects to `/sdd:run` steps in `commandData`:
  - `{ title: "Human Review (P7)", desc: "Review the checklist, tests, and code modifications." }`
  - `{ title: "PR Feedback & Approval (P8)", desc: "Poll reviews, address comments, and wait for PR approval." }`
  - `{ title: "Sync & Merge (P9)", desc: "Synchronize documents, push to feature branch, wait for status checks, then merge the PR." }`
  [Trace: specs:AC-9, design:Components]

## Phase 4: Format and Lint Checks
- [ ] Format and check code style of modified files [SKILL.md](file:///home/kenneth-ancheta/src/github.com/agy-plugins/plugins/sdd/skills/run/SKILL.md) and [index.html](file:///home/kenneth-ancheta/src/github.com/agy-plugins/plugins/sdd/index.html) to ensure clean syntax and correct indentation. [Trace: tech:Tech Stack]

---

## Verification Plan

### Manual Verification Checkpoints
Perform these checks using browser rendering or inspection of the modified documents:

1. **Verification of SKILL.md updates**:
   - Check the text formatting and ASCII layout in [SKILL.md](file:///home/kenneth-ancheta/src/github.com/agy-plugins/plugins/sdd/skills/run/SKILL.md) to ensure P9 steps are correctly documented.
   - Covers: **specs:AC-1, specs:AC-2, specs:AC-3, specs:AC-4, specs:AC-5, specs:AC-6**

2. **Verification of Node Positions**:
   - Open [plugins/sdd/index.html](file:///home/kenneth-ancheta/src/github.com/agy-plugins/plugins/sdd/index.html) in a browser or inspect the visual coordinates of `sync` and `pr-merge` on the SVG canvas to ensure `sync` is at `(1080, 540)` and `pr-merge` is at `(1080, 640)`.
   - Covers: **specs:AC-7**

3. **Verification of Edge Routing**:
   - Verify visually in the browser that the sequential path routes from `pr-approve` -> `sync` -> `pr-merge`, and that `branch-delete` has no incoming sequential arrow from `sync`.
   - Covers: **specs:AC-8**

4. **Verification of Execution Plan Steps**:
   - Click on `/sdd:run` in the sidebar and verify that the steps panel under "Execution Plan" correctly lists steps P7, P8, and P9.
   - Covers: **specs:AC-9**

5. **Lint and Formatting Verification**:
   - Verify that there are no HTML syntax or Markdown syntax errors in the updated files.
   - Covers: **tech:Tech Stack**
