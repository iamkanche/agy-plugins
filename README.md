# Antigravity Plugins Workspace — `kanche`

Welcome to the **agy-plugins** repository! This workspace contains the unified **`kanche`** plugin bundle for the **Google Antigravity** AI-first development platform.

The unified `kanche` plugin packages all developer workflows, slash commands, rules, subagents, and skills into a single namespace: `/kanche:<command>`.

---

## Marketplace Registration

You can load the unified `kanche` plugin from this remote repository either **globally** or **project-based**:

### 1. Global Installation (All Projects)
Create a `marketplace.json` file inside your global plugins directory:
- Registry file: `~/.gemini/config/plugins/marketplace.json`

```json
{
  "name": "global-plugins-registry",
  "plugins": [
    { "name": "kanche", "source": "github:iamkanche/agy-plugins//plugins/kanche" }
  ]
}
```

### 2. Project-Based Installation (Workspace-Level)
Create a `marketplace.json` file inside your project's local customization directory:
- Registry file: `.agents/plugins/marketplace.json`

```json
{
  "name": "project-plugins-registry",
  "plugins": [
    { "name": "kanche", "source": "github:iamkanche/agy-plugins//plugins/kanche" }
  ]
}
```

---

## Available Slash Commands (`/kanche:*`)

### 1. Git Workflow Commands
- `/kanche:git-commit` - Commit staged work with Conventional Commits message (gated).
- `/kanche:git-branch-create` - Create and switch to a new feature branch (gated).
- `/kanche:git-branch-delete` - Delete a git branch locally/remotely (gated).
- `/kanche:git-tag-create` - Create an annotated tag at HEAD and push (gated).
- `/kanche:git-tag-delete` - Delete a tag locally/remotely (gated).
- `/kanche:git-tag-push` - Push local tags to remote origin (gated).
- `/kanche:git-fetch` - Fetch branches and tags from origin (gated).
- `/kanche:git-pull` - Integrate changes from upstream (gated).
- `/kanche:git-push` - Push current feature branch to origin (gated).
- `/kanche:git-stash` - Save, restore, list, or discard stashes (gated).
- `/kanche:git-status` - Show working-tree state and branch status (gated).
- `/kanche:git-rebase` - Rebase current branch onto target branch (gated).
- `/kanche:git-switch` - Switch working tree to a different branch (gated).

### 2. GitHub CLI Commands
- `/kanche:pr-create` - Push branch and open a pull request on GitHub (gated).
- `/kanche:pr-list` - List open pull requests and display branch PR context (gated).
- `/kanche:pr-review` - Review a pull request diff against rules and post inline suggestions (gated).
- `/kanche:pr-approve` - Approve a pull request on GitHub (gated).
- `/kanche:pr-respond` - Triage PR review comments, fix code, and reply in-thread (gated).
- `/kanche:pr-merge` - Merge a pull request on GitHub and delete branch (gated).

### 3. SDD Master Orchestrator Commands
- `/kanche:sdd-run` - Drive a work item through full SDD phase model (P0 to P9).
- `/kanche:sdd-steering` - Analyze repository and return steering guidelines.
- `/kanche:sdd-sync` - Promote development docs to product memory.
- `/kanche:sdd-init` - Bootstrap steering guidelines (`product.md`, `tech.md`, `structure.md`, `rules.md`).
- `/kanche:sdd-init-update` - Re-analyze repository and refresh guidelines.
- `/kanche:sdd-continue` - Resume SDD workflow from on-disk state.

### 4. Design & Specs Commands
- `/kanche:design-grill` - Adversarially probe feature requests for ambiguities.
- `/kanche:design-specs` - Draft functional specifications document.
- `/kanche:design-specs-review` - Perform review on specs draft.
- `/kanche:design-init` - Draft system architecture design specifications.
- `/kanche:design-review` - Perform review on design documents.

### 5. Quality Assurance Commands
- `/kanche:qa-validate` - Run linters, compilers, and test suites.
- `/kanche:qa-test-plan` - Generate comprehensive test plan matrices.
- `/kanche:qa-review` - Audit implementation code modification diffs.

### 6. Task Planner Commands
- `/kanche:planner-tasks` - Formulate task checklist manifests.
- `/kanche:planner-review` - Audit task checklist layout.

### 7. Coding & Development Commands
- `/kanche:dev-implement` - Modify codebase incrementally according to task checklist.

---

## Directory Structure

```text
agy-plugins/
├── .agents/
│   └── plugins/
│       └── marketplace.json   # Local registry definition
└── plugins/
    └── kanche/                # Single Unified Plugin Directory
        ├── plugin.json        # Plugin manifest ("name": "kanche")
        ├── agents/            # Operator subagents (git-operator, gh-operator, etc.)
        ├── rules/             # Hard rules and gating guidelines
        └── skills/            # Skill workflows (/kanche:<skill_name>)
```
