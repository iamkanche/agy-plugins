# Antigravity Plugins Workspace — `kanche`

Welcome to the **agy-plugins** repository! This workspace contains the unified **`kanche`** plugin bundle for the **Google Antigravity** AI-first development platform.

The unified `kanche` plugin packages a **complete 17-agent autonomous software engineering team**, developer workflows, slash commands, strict destructive safety rules, and skills into a single namespace: `/kanche:<command>`.

---

## 🛡️ Destructive Action Safety Policy

**Zero Autonomous Destructive Execution:**
All destructive and remote-mutating commands are strictly gated behind mandatory, interactive human confirmation via `default_api:ask_question`. This applies unconditionally across **both manual and auto (`mode=auto`) modes**:

- **Remote Git Mutations**: `git push`, `git push --tags`, `git push origin --delete`
- **History Mutations**: `git commit`, `git merge`, `git rebase`
- **Deletions & Drops**: `rm`, `rm -rf`, `git branch -d/-D`, `git tag -d`, `git stash drop`
- **GitHub PR Merges**: `gh pr merge` (all merge methods)
- **Database Resets**: `migrate:fresh`, dropping tables or databases

Automated modes (`mode=auto` or `/goal`) automate analysis, planning, code drafting, linting, and testing, but **always halt to prompt the human** before executing any of the above operations.

---

## 👥 The Complete Software Development Team (17 Agents)

The `kanche` plugin models a complete, enterprise-grade software engineering organization with 17 specialized subagents:

### 1. Research, System Architecture & Token Economy
- **`@researcher`** (`flash` / Gemini Flash High) — Exploratory codebase surveys, Knowledge Graph discovery, and architectural feasibility research (`/kanche:graph-steering`).
- **`@token-optimizer`** (`flash` / Gemini Flash High) — LLM prompt distillation, instruction compression, context window optimization, and token budgeting (`/kanche:token-optimize`).
- **`@analyst`** (`flash` / Gemini Flash High) — Requirements probing via adversarial grilling (`/kanche:design-grill`) and functional specifications drafting (`/kanche:design-specs`).
- **`@architect`** (`flash` / Gemini Flash High) — System architecture, graph entity topology, component boundaries, API schemas, and data model diffs (`/kanche:design-init`).
- **`@designer`** (`flash` / Gemini Flash High) — UI/UX specialist creating text wireframes, component design specs, user flows, and StitchMCP visual layouts (`/kanche:ui-design-stitch`).

### 2. Implementation Specialists
- **`@coder`** (`flash` / Gemini Flash High) — General incremental implementation and task execution with minimal diffs (`/kanche:code-implement`).
- **`@frontend-expert`** (`flash` / Gemini Flash High) — React 18+, TypeScript 5, TanStack ecosystem, Tailwind CSS, accessible components, and modern web APIs.
- **`@backend-expert`** (`flash` / Gemini Flash High) — MSC architecture, Laravel 10+, Node/Express, Go, Python, database migrations, and REST/GraphQL APIs.

### 3. Quality Assurance & Security
- **`@reviewer`** (`flash` / Gemini Flash High) — Senior code reviewer evaluating multi-file diffs, style conventions, and anti-patterns (`/kanche:code-review`).
- **`@validator`** (`flash` / Gemini Flash High) — Automated check orchestrator running Graph Health integrity diagnostics, static analysis, test suites, and Playwright MCP browser validations (`/kanche:qa-validate`).
- **`@tester`** (`flash` / Gemini Flash High) — Test automation engineer crafting test plan matrices (`/kanche:qa-test-plan`), unit tests, and Playwright E2E suites.
- **`@security-engineer`** (`flash` / Gemini Flash High) — Application security auditor scanning for exposed secrets, dependencies, and OWASP vulnerabilities (`/kanche:security-scan`).

### 4. Agile, Planning & Operations
- **`@scrum-master`** (`flash` / Gemini Flash High) — Agile backlog manager creating standardized PBIs with user stories, acceptance criteria, and story points (`/kanche:scrum-pbi-create`).
- **`@planner`** (`flash` / Gemini Flash High) — Implementation planner decomposing system designs into Topological Dependency DAGs (`/kanche:planner-tasks`).
- **`@devops`** (`flash` / Gemini Flash High) — Infrastructure, release tagging (`/kanche:git-tag-*`), and PR merge verification (`/kanche:gh-cli-pr-merge`).
- **`@git-operator`** (`flash` / Gemini Flash High) — Pure Git execution for branching, fetching, stashing, and safe committing.
- **`@gh-operator`** (`flash` / Gemini Flash High) — GitHub CLI and REST/GraphQL integration for PR creation, review posting, and thread resolution.

---

## 🌐 Graph Engineering Workflow (GEW)

The `kanche` suite upgrades traditional Spec-Driven Development into a modern, native **Graph Engineering Workflow (GEW)**. Every lifecycle phase is grounded in AST dependency graphs, topological DAG task planning, and structural graph health integrity checks across 10 structured phases:

```text
LEVEL 1: Autonomous AI Execution (P0 – P7)
┌───────────────────────┬──────────────────────────────────────────┬───────────────────────────────────────────┐
│ Phase                 │ Orchestrator / Subagents                 │ Core Capabilities & Outputs               │
├───────────────────────┼──────────────────────────────────────────┼───────────────────────────────────────────┤
│ P0 Graph Discovery    │ @researcher, @scrum-master, @git-operator│ Knowledge graph survey, PBI, branch setup │
│ P1 Impact Subgraphs   │ @analyst, @scrum-master                  │ Adversarial grilling, functional specs    │
│ P2 Architecture & UI  │ @architect, @designer                    │ Component topology, StitchMCP UI designs  │
│ P3 Topological DAG    │ @planner, @tester                        │ Dependency Tiers 0-3, QA test plan matrix │
│ P4 Graph Build        │ @coder, @frontend, @backend, @token-opt  │ DAG-ordered build, reviews, distillation  │
│ P5 Graph Health & QA  │ @validator, @tester, @security-engineer  │ AST health gates, Playwright E2E checks   │
│ P6 Deploy & PR Blast  │ @devops, @gh-operator, @reviewer         │ Gated PR creation, inline JSON reviews    │
│ P7 Graph Memory Sync  │ @gh-operator, @git-operator              │ Domain memory promotion, dev cleanup      │
└───────────────────────┴──────────────────────────────────────────┴───────────────────────────────────────────┘

LEVEL 2: Gated Human Governance (P8 – P9)
┌───────────────────────┬──────────────────────────────────────────┬───────────────────────────────────────────┐
│ P8 Human Graph Review │ @validator, @tester                      │ Interactive checklist & visual evidence   │
│ P9 PR Merge & Release │ @devops, @gh-operator                    │ Gated PR merge, annotated release tags    │
└───────────────────────┴──────────────────────────────────────────┴───────────────────────────────────────────┘
```

- **Loop Engineering (≤3x)**: Generator skills (`code-implement`, `design-init`, `design-specs`, `planner-tasks`) pair with Reviewer skills (`code-review`, `qa-review`, `design-review`, `planner-review`) consuming structured `review-verdict` machine blocks for automated remediation.
- **Topological Dependency Tiers**: Planning decomposes tasks strictly into **Tier 0** (Models/Contracts) → **Tier 1** (Services) → **Tier 2** (UI/Endpoints) → **Tier 3** (Tests/Docs).
- **Graph Health Gate**: Verifies 0 dangling edges, 0 missing endpoints, and 0 circular dependencies before deployment.

---

## ⚡ Token Optimization & Communication Policy

Enforced across all 17 agents and 47 skills by **`@token-optimizer`** and `rules/token-optimization.md`:

- **Short & Direct**: Deliver actionable answers, conclusions, and code fixes immediately without conversational throat-clearing.
- **Bullets Over Paragraphs**: Use crisp bullet points (`- `) or compact Markdown tables instead of dense narrative prose.
- **Zero Conversational Padding**: Disallow polite pleasantries ("Sure, I can help with that..."), filler words, and meta-commentary.
- **Bottom Line Up Front (BLUF)**: Present verdicts, conclusions, and decisions first; technical details second.
- **Surgical Diffs**: Output only minimal necessary diffs. Never rewrite unchanged files.
- **Prompt Caching Optimization**: Maintain stable prefix ordering for invariant directives to maximize LLM cache hit rates.

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

### 1. Git Workflow Commands (Human-Gated)
- `/kanche:git-commit` - Commit staged work with Conventional Commits message (human-gated).
- `/kanche:git-branch-create` - Create and switch to a new feature branch (gated).
- `/kanche:git-branch-delete` - Delete a git branch locally/remotely (human-gated).
- `/kanche:git-tag-create` - Create an annotated tag at HEAD and push (human-gated).
- `/kanche:git-tag-delete` - Delete a tag locally/remotely (human-gated).
- `/kanche:git-tag-push` - Push local tags to remote origin (human-gated).
- `/kanche:git-fetch` - Fetch branches and tags from origin (gated).
- `/kanche:git-pull` - Integrate changes from upstream (gated).
- `/kanche:git-push` - Push current feature branch to origin (human-gated).
- `/kanche:git-stash` - Save, restore, list, or discard stashes (`drop` is human-gated).
- `/kanche:git-status` - Show working-tree state and branch status (read-only).
- `/kanche:git-rebase` - Rebase current branch onto target branch (gated).
- `/kanche:git-switch` - Switch working tree to a different branch (gated).

### 2. GitHub CLI Commands
- `/kanche:gh-cli-pr-create` - Push branch and open a pull request on GitHub (human-gated).
- `/kanche:gh-cli-pr-list` - List open pull requests and display branch PR context (read-only).
- `/kanche:gh-cli-pr-review` - Review a PR diff and post inline suggestions with `.json` format support (`review.json`).
- `/kanche:gh-cli-pr-approve` - Approve a pull request on GitHub (gated).
- `/kanche:gh-cli-pr-respond` - Triage PR review comments, fix code, and reply in-thread (gated).
- `/kanche:gh-cli-pr-merge` - Merge a pull request on GitHub and delete branch (human-gated).

### 3. Graph Engineering Workflow Commands (`/kanche:graph-*`)
- `/kanche:graph-run` - Drive a work item through the 10-phase Graph Engineering Workflow (P0 to P9).
- `/kanche:graph-continue` - Resume the Graph Engineering Workflow at the phase inferred from on-disk graph state.
- `/kanche:graph-steering` - Analyze repository using Knowledge Graph extraction and return steering guidelines.
- `/kanche:graph-sync` - Promote development docs to product memory, verify module dependency integrity, and clean up dev folder (gated).
- `/kanche:graph-init` - Bootstrap graph-grounded steering guidelines (`product.md`, `tech.md`, `structure.md`, `rules.md`).
- `/kanche:graph-init-update` - Re-analyze repository using Knowledge Graph extraction and refresh guidelines.

#### Legacy SDD Compatibility Forwarders (`/kanche:sdd-*`)
- `/kanche:sdd-run` - [Forwarder] Forwards to `/kanche:graph-run`.
- `/kanche:sdd-continue` - [Forwarder] Forwards to `/kanche:graph-continue`.
- `/kanche:sdd-steering` - [Forwarder] Forwards to `/kanche:graph-steering`.
- `/kanche:sdd-sync` - [Forwarder] Forwards to `/kanche:graph-sync`.
- `/kanche:sdd-init` - [Forwarder] Forwards to `/kanche:graph-init`.
- `/kanche:sdd-init-update` - [Forwarder] Forwards to `/kanche:graph-init-update`.

### 4. Design & Specs Commands
- `/kanche:design-grill` - Adversarially probe feature requests for ambiguities.
- `/kanche:design-specs` - Draft functional specifications document.
- `/kanche:design-specs-review` - Perform review on specs draft.
- `/kanche:design-init` - Draft system architecture design specifications.
- `/kanche:design-review` - Perform review on design documents.
- `/kanche:ui-design-stitch` - Generate visual UI wireframes and themes using StitchMCP.

### 5. Quality Assurance & Security Commands
- `/kanche:qa-validate` - Run linters, test suites, and Playwright MCP browser checks.
- `/kanche:qa-test-plan` - Generate comprehensive test plan matrices and test stubs.
- `/kanche:qa-review` - Audit implementation diffs and perform visual verification via Playwright MCP.
- `/kanche:code-review` - Perform standalone deep code review with `--auto-apply` option.
- `/kanche:security-scan` - Audit codebase for hardcoded secrets, dependencies, and security vulnerabilities.

### 6. Task Planner & Scrum Commands
- `/kanche:planner-tasks` - Formulate task checklist manifests.
- `/kanche:planner-review` - Audit task checklist layout.
- `/kanche:scrum-pbi-create` - Create standardized Product Backlog Items with user stories and story points.

### 7. Coding & Implementation Commands
- `/kanche:code-implement` - Incremental codebase implementation and task checklist execution.

### 8. Token & Context Optimization Commands
- `/kanche:token-optimize` - Audit and compress prompts, skills, and agent instructions for maximum context efficiency and token savings.

---

## 🔍 `/kanche:gh-cli-pr-review` Format & JSON Support

PR reviews support the `--json` / `--format=json` flag to produce a standardized `review.json` payload, which can be posted to GitHub in a single request:

```bash
gh api --method POST "repos/{owner}/{repo}/pulls/{pr}/reviews" --input review.json
```

### GitHub Review Comment Body Format
```markdown
#  Summary
- Short PR review summary
- Severity: eg: 6/10
- Total files: x files
- Total lines: x lines of codes

## Review Summary
  
 Severity       │ Count         │ Category
────────────────┼───────────────┼─────────────────────────────────────
 🔴 HIGH        │ 0             │ Critical Bugs / Security / Breaking
 🟡 MEDIUM      │ 0             │ Correctness Risk / Test Coverage
 🟢 LOW         │ 1             │ Documentation / Style Nit

---
Inline comment directly to the files and lines of codes
```

*Individual code suggestions are anchored directly to file paths and line numbers on the pull request diff.*

---

## Directory Structure

```text
agy-plugins/
├── .agents/
│   └── plugins/
│       └── marketplace.json   # Local registry definition
├── index.html                 # Interactive showcase and skill catalog
└── plugins/
    └── kanche/                # Single Unified Plugin Directory
        ├── plugin.json        # Manifest (v0.5.0)
        ├── agents/            # Complete Software Engineering Team (17 agents)
        │   ├── analyst/
        │   ├── architect/
        │   ├── backend-expert/
        │   ├── coder/
        │   ├── designer/
        │   ├── devops/
        │   ├── frontend-expert/
        │   ├── gh-operator/
        │   ├── git-operator/
        │   ├── planner/
        │   ├── researcher/
        │   ├── reviewer/
        │   ├── scrum-master/
        │   ├── security-engineer/
        │   ├── tester/
        │   ├── token-optimizer/
        │   └── validator/
        ├── rules/             # Hard rules & gating guidelines
        │   ├── destructive-safety.md
        │   ├── gh-hard-rules.md
        │   ├── git-hard-rules.md
        │   ├── loop-engineering.md
        │   ├── output-language.md
        │   ├── token-optimization.md
        │   └── workflow-gating.md
        └── skills/            # 47 specialized workflow skills (/kanche:*)
```
