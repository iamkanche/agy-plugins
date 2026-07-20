# Specs: Add Command Arguments/Usage Samples in Connections Dashboard

## Context
The interactive skill connection map in `plugins/sdd/index.html` registers various commands for the `sdd`, `git`, and `gh-cli` plugins. While it displays descriptions, active policies, and steps for each command, there are no argument/usage samples (e.g., `/sdd:run --mode=auto --from=specs --until=build`). The user wants to add usage samples to these commands inside the static HTML dashboard to help users understand their available options at a glance.

## Scope

### In-Scope
- Add a new `usage` string property to command objects in `commandData` and `gitAndGhCliData` in `plugins/sdd/index.html`.
- Update `loadCommandDetails(cmdName)` to dynamically render the `usage` sample inside a styled code block in the header section of the details panel.
- Define accurate usage/argument examples for at least the following major commands:
  - `/sdd:run`
  - `/sdd:continue`
  - `/sdd:validate`
  - `/git:branch-create`
  - `/git:branch-delete`
  - `/git:commit`
  - `/git:push`
  - `/git:pull`
  - `/git:rebase`
  - `/git:stash`
  - `/git:switch`
  - `/gh-cli:pr-create`
  - `/gh-cli:pr-merge`
  - `/gh-cli:pr-respond`
  - `/gh-cli:pr-approve`

### Out of Scope
- Modifying the markdown skill files themselves to add argument lists.
- Modifying the root `index.html` (only the sdd dashboard page `plugins/sdd/index.html` is in scope).
- Adding complex interactive forms to execute commands from the web UI.

## Acceptance Criteria

### UI Acceptance Criteria
- **AC-1**: The details sidebar header section displays a labeled "Arguments / Usage Sample" section when a command that defines a `usage` property is selected/loaded.
- **AC-2**: The usage sample is displayed inside a monospaced block styled matching the `.code-snippet` class (yellow text, dark background, padding, rounded corners).
- **AC-3**: If a command does not define a `usage` property, no usage/arguments block or label is rendered in the header section.

### Data/Command Coverage
- **AC-4**: `/sdd:run` specifies usage: `/sdd:run <slug> --mode=auto|manual --from=<phase> --until=<phase>` (e.g. `/sdd:run my-feature --mode=auto --from=specs --until=build`).
- **AC-5**: `/sdd:continue` specifies usage: `/sdd:continue --mode=auto|manual --from=<phase> --until=<phase> <slug>` (e.g. `/sdd:continue --mode=auto`).
- **AC-6**: `/git:branch-create` specifies: `/git:branch-create <branch-name>`
- **AC-7**: `/git:branch-delete` specifies: `/git:branch-delete <branch-name> [--remote]`
- **AC-8**: `/git:commit` specifies: `/git:commit` (no arguments, message prompt follows)
- **AC-9**: `/git:push` specifies: `/git:push [--set-upstream]`
- **AC-10**: `/git:pull` specifies: `/git:pull`
- **AC-11**: `/git:rebase` specifies: `/git:rebase <target-branch>`
- **AC-12**: `/git:stash` specifies: `/git:stash [push|pop|list|clear]`
- **AC-13**: `/git:switch` specifies: `/git:switch <branch-name>`
- **AC-14**: `/gh-cli:pr-create` specifies: `/gh-cli:pr-create [--title=<title>] [--body=<body>] [--draft] [--base=<branch>]`
- **AC-15**: `/gh-cli:pr-merge` specifies: `/gh-cli:pr-merge [<pr-number>] [--squash|--rebase|--merge] [--keep-branch]`
- **AC-16**: `/gh-cli:pr-respond` specifies: `/gh-cli:pr-respond [<pr-number>]`
- **AC-17**: `/gh-cli:pr-approve` specifies: `/gh-cli:pr-approve [<pr-number>]`
- **AC-18**: Other commands in the registry should have simple usage examples where applicable (e.g., `/sdd:init`, `/sdd:steering`).

## Data Model
Add `usage` key (type: string, optional) to the objects inside `commandData` and `gitAndGhCliData` variables in `plugins/sdd/index.html`.
