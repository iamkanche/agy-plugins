# System Design: SDD Skills & Workflow Map in index.html

## 1. Component Boundaries & UI Architecture
The Skills & Workflow Map is integrated directly into the `index.html` single-page dashboard architecture.

### Data Structures:
- **`sddWorkflowPhases`**: JavaScript data structure representing the 10 SDD phases and their skill/agent dependencies:
```javascript
const sddWorkflowPhases = [
  {
    phase: "P0",
    name: "Setup & Branching",
    desc: "Verify repository, load settings & memory, present receipt, and checkout feature branch.",
    agent: "@git-operator",
    theme: "cyan",
    skills: [
      { name: "/kanche:git-branch-create", label: "Branch Create", path: "plugins/kanche/skills/git/branch-create/SKILL.md" }
    ]
  },
  {
    phase: "P1",
    name: "Specs & Requirements",
    desc: "Adversarial probing, drafting functional specs, and forced specs review.",
    agent: "@analyst",
    theme: "pink",
    skills: [
      { name: "/kanche:design-grill", label: "Design Grill", path: "plugins/kanche/skills/design/grill/SKILL.md" },
      { name: "/kanche:design-specs", label: "Specs Draft", path: "plugins/kanche/skills/design/specs/SKILL.md" },
      { name: "/kanche:design-specs-review", label: "Specs Review", path: "plugins/kanche/skills/design/specs-review/SKILL.md" }
    ]
  },
  {
    phase: "P2",
    name: "Architecture & Design",
    desc: "System design specifications, component boundaries, and forced design review.",
    agent: "@architect",
    theme: "pink",
    skills: [
      { name: "/kanche:design-init", label: "Design Init", path: "plugins/kanche/skills/design/init/SKILL.md" },
      { name: "/kanche:design-review", label: "Design Review", path: "plugins/kanche/skills/design/review/SKILL.md" }
    ]
  },
  {
    phase: "P3",
    name: "Task Planning",
    desc: "Task manifest decomposition, file editing order, and docs commit.",
    agent: "@planner",
    theme: "indigo",
    skills: [
      { name: "/kanche:planner-tasks", label: "Planner Tasks", path: "plugins/kanche/skills/planner/tasks/SKILL.md" },
      { name: "/kanche:planner-review", label: "Planner Review", path: "plugins/kanche/skills/planner/review/SKILL.md" }
    ]
  },
  {
    phase: "P4",
    name: "Implementation",
    desc: "Incremental code implementation and code review audit gate.",
    agent: "@coder",
    theme: "teal",
    skills: [
      { name: "/kanche:dev-implement", label: "Dev Implement", path: "plugins/kanche/skills/dev/implement/SKILL.md" },
      { name: "/kanche:qa-review", label: "QA Review", path: "plugins/kanche/skills/qa/review/SKILL.md" }
    ]
  },
  {
    phase: "P5",
    name: "AI Validation",
    desc: "Automated test suite verification, linter checks, and fix loop.",
    agent: "@validator",
    theme: "emerald",
    skills: [
      { name: "/kanche:qa-validate", label: "QA Validate", path: "plugins/kanche/skills/qa/validate/SKILL.md" }
    ]
  },
  {
    phase: "P6",
    name: "Deploy & PR Review",
    desc: "Push feature branch, open PR, and run AI PR review audit.",
    agent: "@gh-operator",
    theme: "purple",
    skills: [
      { name: "/kanche:git-push", label: "Git Push", path: "plugins/kanche/skills/git/push/SKILL.md" },
      { name: "/kanche:pr-create", label: "PR Create", path: "plugins/kanche/skills/gh-cli/pr-create/SKILL.md" },
      { name: "/kanche:pr-review", label: "PR Review", path: "plugins/kanche/skills/gh-cli/pr-review/SKILL.md" }
    ]
  },
  {
    phase: "P7-P9",
    name: "PR Response & Merge",
    desc: "Human review, PR comment triaging, document sync, and auto-merge.",
    agent: "@gh-operator",
    theme: "amber",
    skills: [
      { name: "/kanche:pr-respond", label: "PR Respond", path: "plugins/kanche/skills/gh-cli/pr-respond/SKILL.md" },
      { name: "/kanche:sdd-sync", label: "SDD Sync", path: "plugins/kanche/skills/sdd/sync/SKILL.md" },
      { name: "/kanche:pr-merge", label: "PR Merge", path: "plugins/kanche/skills/gh-cli/pr-merge/SKILL.md" }
    ]
  }
];
```

## 2. Layout & UI Styling
- **Sidebar Integration**:
  - Add "Workflow & Skills Map" entry in `pluginsData` with key `skills-map`.
  - Clicking `skills-map` renders the interactive flow chart container.
- **Workflow Map Container CSS**:
  - Node grid / timeline track layout with SVG connection arrows (`<svg>` overlay or flex flow with CSS connectors).
  - Phase cards with theme color borders, badge counters, skill pills, and hover animations.
