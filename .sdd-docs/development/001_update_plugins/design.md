# Update gh-cli and git Plugins — Technical Design

<!-- schema: design | written by /sdd:design -->

## Approach
Extend both `gh-cli` and `git` plugins by writing new skill files (`SKILL.md`), modifying existing ones, updating `plugin.json` to register the commands, and updating dashboard index files to render them correctly.

## Architecture context
All skills reside under the `plugins/{plugin-name}/skills/{skill-name}/SKILL.md` directories.
Configurations are set in `plugins/{plugin-name}/plugin.json`.
Interactive visualization dashboards are in `plugins/{plugin-name}/index.html` and the root `index.html`.

## Components
| Component | Responsibility | New/Modified |
|---|---|---|
| `/gh-cli:pr-merge` | Merge pull request and delete branch by default | New |
| `/gh-cli:pr-create` | Create pull request with auto assignee `@me` | Modified |
| `/git:tag-delete` | Delete local and/or remote tag | New |
| `/git:tag-push` | Push local tags to remote origin | New |
| Plugin Inspector dashboards | Visualize commands and execution steps | Modified |

## Detailed Command Specifications

### 1. `/gh-cli:pr-merge`
- **Invocation**: `agy gh-cli:pr-merge [<pr-number>] [--merge | --squash | --rebase] [--keep-branch]`
- **Behavior**:
  - Resolve default branch.
  - Check `gh auth status`.
  - Fetch PR info.
  - If target branch is current branch:
    - Warn/notify, switch to base branch after successful merge.
  - Prompt user to confirm merge.
  - Execute: `gh pr merge <pr-number> --delete-branch` (or without `--delete-branch` if `--keep-branch` is passed).
  - If current branch was merged, switch to default branch and run `git branch -d <branch>`.

### 2. `/gh-cli:pr-create`
- **Invocation**: `agy gh-cli:pr-create [--draft] [--base=<branch>] [--assignee=<user>]`
- **Behavior**:
  - `--assignee` defaults to `@me` (auto-assign).
  - Execute: `gh pr create --title "<title>" --body "<body>" --assignee "<assignee>" [--draft] [--base "<base>"]`

### 3. `/git:tag-delete`
- **Invocation**: `agy git:tag-delete <tag-name> [--remote]`
- **Behavior**:
  - Verify tag existence.
  - Prompt user to confirm deletion.
  - Execute local: `git tag -d <tag-name>`
  - Execute remote: `git push origin --delete <tag-name>` (if `--remote` is passed).

### 4. `/git:tag-push`
- **Invocation**: `agy git:tag-push [<tag-name>] [--all]`
- **Behavior**:
  - Prompt user to confirm push.
  - If `<tag-name>` is given: `git push origin <tag-name>`
  - Else or if `--all`: `git push origin --tags`

## UI Updates
- **Marketplace Dashboard (`index.html`)**: Register commands in `pluginsData` configuration block.
- **gh-cli Inspector (`plugins/gh-cli/index.html`)**: Register `/gh-cli:pr-merge` command and modify `/gh-cli:pr-create` entry to detail the auto-assign feature.
- **git Inspector (`plugins/git/index.html`)**: Register `/git:tag-delete` and `/git:tag-push` commands.
