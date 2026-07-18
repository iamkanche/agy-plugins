# Antigravity Plugins Workspace

Welcome to the **agy-plugins** repository! This workspace contains custom plugin bundles for the **Google Antigravity** AI-first development platform.

Plugins in this repository extend the capabilities of Antigravity agents by packaging slash commands (workflows), rules, subagents, and skills.

## Marketplace Registration

You can load these plugins from this remote repository either **globally** or **project-based**:

### 1. Global Installation (All Projects)
Create a `marketplace.json` file inside your global plugins directory:
- Registry file: `~/.gemini/config/plugins/marketplace.json`

```json
{
  "name": "global-plugins-registry",
  "plugins": [
    {
      "name": "git",
      "source": "github:iamkanche/agy-plugins//plugins/git"
    },
    {
      "name": "gh-cli",
      "source": "github:iamkanche/agy-plugins//plugins/gh-cli"
    }
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
    {
      "name": "git",
      "source": "github:iamkanche/agy-plugins//plugins/git"
    },
    {
      "name": "gh-cli",
      "source": "github:iamkanche/agy-plugins//plugins/gh-cli"
    }
  ]
}
```

*Note: For local development and contributions, you can clone the repository and point the source to relative directories (e.g. `"source": "../../plugins/git"`).*

---

## Active Plugins

### 1. Git Control Plugin (`git`)
Provides 11 robust slash commands (workflows) to safely manage local Git histories and workspaces from within the Antigravity chat canvas.

- Source directory: [plugins/git/](file:///plugins/git/)
- Main configurations: [plugin.json](file:///plugins/git/plugin.json)
- Rules: [rules/git-hard-rules.md](file:///plugins/git/rules/git-hard-rules.md), [rules/output-language.md](file:///plugins/git/rules/output-language.md)
- Workflows (.agent/workflows/):
  - `/git:commit` - Commit staged changes.
  - `/git:branch-create` - Create and checkout feature branches.
  - `/git:branch-delete` - Delete local/remote branches.
  - `/git:tag-create` - Create and push annotated tags.
  - `/git:fetch` - Fetch remote updates.
  - `/git:pull` - Fast-forward pull or rebase from upstream.
  - `/git:push` - Push current branch.
  - `/git:stash` - Push, pop, list, or drop stashes.
  - `/git:status` - Show workspace status and commits.
  - `/git:rebase` - Rebase onto base branches.
  - `/git:switch` - Safely switch checkout branch.

### 2. GitHub CLI Plugin (`gh-cli`)
Provides 5 slash commands (workflows) to manage the Pull Request lifecycle, reviews, approvals, and threads triaging.

- Source directory: [plugins/gh-cli/](file:///plugins/gh-cli/)
- Main configurations: [plugin.json](file:///plugins/gh-cli/plugin.json)
- Rules: [rules/output-language.md](file:///plugins/gh-cli/rules/output-language.md)
- Workflows (.agent/workflows/):
  - `/gh-cli:pr-create` - Safe branch push and pull request creation.
  - `/gh-cli:pr-list` - Lists repository PRs and identifies current branch connection.
  - `/gh-cli:pr-review` - Audits a PR against `AGENTS.md` rules and submits formatted inline suggestion comments.
  - `/gh-cli:pr-approve` - Submits approval reviews (refusing self-approvals).
  - `/gh-cli:pr-respond` - Coordinates comments triaging, fixes verification, commits, pushes, and thread replies.

---

## Directory Structure

```text
agy-plugins/
├── .agents/
│   └── plugins/
│       └── marketplace.json   # Local registry definition
└── plugins/
    ├── git/                   # Git plugin directory
    │   ├── plugin.json        # Plugin manifest
    │   ├── rules/             # Rule definitions (formatting, hard limits)
    │   └── commands/          # Slash command workflow implementations
    └── gh-cli/                # GitHub CLI plugin directory
        ├── plugin.json        # Plugin manifest
        ├── rules/             # Rule definitions (output format)
        └── commands/          # Slash command workflow implementations
```

