# Design: Add Command Arguments/Usage Samples in Connections Dashboard

## Approach
Add a `usage` property containing a string representing a valid CLI command syntax sample to each command in `commandData` and `gitAndGhCliData` objects in `plugins/sdd/index.html`. Modify `loadCommandDetails(cmdName)` to check for `data.usage` and render it using a `.code-snippet` wrapper if present.

## UI Modification

### Render Block in `loadCommandDetails`
```javascript
            headerSection.innerHTML = `
                <div class="details-title-row">
                    <h3 class="details-title">${cmdName}</h3>
                    <span class="details-badge ${data.gated ? '' : 'direct'}">${data.gated ? 'Gated Confirmation' : 'Direct Action'}</span>
                </div>
                <p class="details-desc">${data.desc}</p>
                ${data.usage ? `
                    <div style="margin-top: 1rem;">
                        <span style="font-family: var(--font-title); font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-secondary); display: block; margin-bottom: 0.5rem;">Arguments / Usage Sample</span>
                        <div class="code-snippet" style="font-size: 0.8rem; padding: 0.5rem 0.75rem;">${data.usage}</div>
                    </div>
                ` : ''}
            `;
```

## Data Changes

### 1. `commandData` Updates:
- `/sdd:steering`: `usage: "/sdd:steering"`
- `/sdd:grill`: `usage: "/sdd:grill \"<feature-request-description>\""`
- `/sdd:specs`: `usage: "/sdd:specs <slug>"`
- `/sdd:design`: `usage: "/sdd:design <slug>"`
- `/sdd:tasks`: `usage: "/sdd:tasks <slug>"`
- `/sdd:build`: `usage: "/sdd:build <slug>"`
- `/sdd:specs-review`: `usage: "/sdd:specs-review <slug>"`
- `/sdd:design-review`: `usage: "/sdd:design-review <slug>"`
- `/sdd:tasks-review`: `usage: "/sdd:tasks-review <slug>"`
- `/sdd:build-review`: `usage: "/sdd:build-review <slug>"`
- `/sdd:validate`: `usage: "/sdd:validate <slug>"`
- `/sdd:sync`: `usage: "/sdd:sync <slug>"`
- `/sdd:run`: `usage: "/sdd:run <slug> [--mode=auto|manual] [--from=<phase>] [--until=<phase>]"`
- `/sdd:init`: `usage: "/sdd:init"`
- `/sdd:init-update`: `usage: "/sdd:init-update"`
- `/sdd:continue`: `usage: "/sdd:continue [--mode=auto|manual] [--from=<phase>] [--until=<phase>] [<slug>]"`

### 2. `gitAndGhCliData` Updates:
- `/git:branch-create`: `usage: "/git:branch-create <branch-name>"`
- `/git:branch-delete`: `usage: "/git:branch-delete <branch-name> [--remote]"`
- `/git:commit`: `usage: "/git:commit"`
- `/git:fetch`: `usage: "/git:fetch"`
- `/git:pull`: `usage: "/git:pull"`
- `/git:push`: `usage: "/git:push [--set-upstream]"`
- `/git:rebase`: `usage: "/git:rebase <target-branch>"`
- `/git:stash`: `usage: "/git:stash [push|pop|list|clear]"`
- `/git:status`: `usage: "/git:status"`
- `/git:switch`: `usage: "/git:switch <branch-name>"`
- `/git:tag-create`: `usage: "/git:tag-create <tag-name> -m \"<message>\""`
- `/git:tag-delete`: `usage: "/git:tag-delete <tag-name>"`
- `/git:tag-push`: `usage: "/git:tag-push"`
- `/gh-cli:pr-create`: `usage: "/gh-cli:pr-create [--title=<title>] [--body=<body>] [--draft] [--base=<branch>]"`
- `/gh-cli:pr-list`: `usage: "/gh-cli:pr-list"`
- `/gh-cli:pr-review`: `usage: "/gh-cli:pr-review [<pr-number>] [--approve|--request-changes|--comment] [-body=<body>]"`
- `/gh-cli:pr-respond`: `usage: "/gh-cli:pr-respond [<pr-number>]"`
- `/gh-cli:pr-approve`: `usage: "/gh-cli:pr-approve [<pr-number>]"`
- `/gh-cli:pr-merge`: `usage: "/gh-cli:pr-merge [<pr-number>] [--squash|--rebase|--merge] [--keep-branch]"`
