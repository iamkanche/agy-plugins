# Functional Specifications: SDD Skills & Workflow Map in index.html

## 1. Overview
This specification defines the addition of an interactive "Skills & Phase Map" to the SDD Orchestrator dashboard (`index.html`). The map visually displays the end-to-end SDD phase flow (P0 to P9), showing how `/kanche:sdd-run` orchestrates specialized subagents and sub-skills (e.g. `sdd-run` -> `design-grill` -> `design-specs` -> `design-init` -> `planner-tasks` -> `dev-implement` -> `qa-validate` -> `pr-create` -> `pr-merge`).

## 2. Target Requirements & User Experience
- **Interactive Navigation Entry**:
  - Add a "Skills Map" option in the left sidebar panel or view selector in `index.html`.
  - Provide a toggle / view button to switch between the Grid View of commands and the Visual Workflow Map View.
- **Visual Phase Model Pipeline (P0-P9)**:
  - Render connected node cards for each phase:
    - **P0 Setup**: Receipt & Branch Creation (`/kanche:git-branch-create`, `@git-operator`)
    - **P1 Specs**: Interrogation & Specs (`/kanche:design-grill` -> `/kanche:design-specs` -> `/kanche:design-specs-review`, `@analyst`)
    - **P2 Design**: Architecture Specs (`/kanche:design-init` -> `/kanche:design-review`, `@architect`)
    - **P3 Tasks**: Task Checklist (`/kanche:planner-tasks` -> `/kanche:planner-review`, `@planner`)
    - **P4 Build**: Implementation (`/kanche:dev-implement` -> `/kanche:qa-review`, `@coder`)
    - **P5 Valid**: QA Validation (`/kanche:qa-validate`, `@validator`)
    - **P6 Deploy**: Push & PR Review (`/kanche:git-push` -> `/kanche:pr-create` -> `/kanche:gh-cli-pr-review`, `@gh-operator`)
    - **P7 Human Review**: Verification Checklist
    - **P8 PR Mods**: Triage & Respond (`/kanche:pr-respond`, `@gh-operator`)
    - **P9 Alignment**: Sync & Merge (`/kanche:sdd-sync` -> `/kanche:pr-merge`)
- **Node Connections & Visual Interactivity**:
  - SVG flow vectors / directional connectors linking nodes (`sdd-run` -> `design` -> `planner` -> `dev` -> `qa` -> `gh-cli`).
  - Hovering over a skill node highlights its parent phase, associated subagent tag, and next sequence skill.
  - Clicking a skill card opens or links to the skill documentation.
- **Aesthetic Excellence**:
  - Dark mode glassmorphism matching `index.html` CSS design tokens (`var(--glass-bg)`, `var(--glass-border)`, color accents per phase).

## 3. Acceptance Criteria
- [x] "Skills Map" view item added to sidebar navigation and header switch.
- [x] Interactive workflow diagram dynamically renders P0-P9 phase nodes with SVG directional arrows.
- [x] Subagent handles (@analyst, @architect, @planner, @coder, @validator, @gh-operator, @git-operator) displayed on respective phase cards.
- [x] Filtering/searching updates or highlights relevant nodes in the skills map.
- [x] Fully responsive layout for desktop and laptop screens without breaking existing dashboard functionality.
