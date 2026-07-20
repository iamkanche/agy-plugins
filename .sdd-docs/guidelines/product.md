# Product Guidelines

## Vision
A public registry and marketplace repository for Google Antigravity custom plugin bundles.

## Target Users
- Software developers building autonomous agents on the Google Antigravity platform.
- Autonomous Antigravity agents discovering and installing custom workflow plugins.

## Core Value
Provides pre-packaged workflow plugins (git control, GitHub CLI integrations, SDD lifecycle workflows) that extend agent capabilities with safe side-effect gates.

## In-Scope vs. Out-of-Scope
### In-Scope
- Custom Antigravity plugins for developer workflows (git command execution, GitHub CLI actions, and SDD document lifecycle automation).
- Local and global registry/marketplace configurations via `marketplace.json`.
- Plugin manifests (`plugin.json`), custom rules (`rules/`), and skill files (`skills/*/SKILL.md`) for each plugin.
- A root static website dashboard (`index.html`) to preview available plugins and commands.
- Auto-mode SDD workflow execution that runs P0-P9 end-to-end without interactive confirmation prompts, while preserving all safety invariants.

### Out-of-Scope
- Direct management or storage of user authentication credentials or API keys (delegated to user's local git/gh configurations).
- Supporting IDE platforms or autonomous agent frameworks outside of Google Antigravity.

## Success Signals
- Google Antigravity agents can parse, register, and successfully run slash commands from these plugins in their local environments.
- Active compliance of all command execution with defined gating and output policies.
- (Open Question) Are there telemetry/usage metrics or success rate analytics planned for the registry?
