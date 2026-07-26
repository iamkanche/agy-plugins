# GitHub Hard Rules

- **No Self Approvals**: Never approve your own pull request via GitHub API or CLI.
- **Default Event Policy**: Use `event=COMMENT` by default when posting reviews; do not approve or request changes automatically unless instructed.
- **No Force Merge**: Do not force-merge pull requests or bypass required status checks / branch protection rules.
- **Head SHA Anchoring**: Anchor inline review comments to the exact `headRefOid` commit SHA to prevent comment drift.
- **Secret Safety**: Do not post confidential tokens or credentials in PR comments or review bodies.
