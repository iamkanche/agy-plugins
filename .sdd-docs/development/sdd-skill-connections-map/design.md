# System Design: Interactive Skill Connection Map

## 1. SVG Viewport & Grid Layout System

To render a clean, high-performance connection grid, we utilize a single responsive SVG canvas with a static coordinate layout. This prevents rendering delays and layout shifting.

### 1.1 Viewport Parameters
* **Width / Height:** `width="100%"` with a responsive container.
* **ViewBox:** `0 0 1300 700` (provides a 13:7 aspect ratio tailored for widescreen dashboards).
* **Node Dimensions:** Width = `140px`, Height = `36px` (corner radius `rx="8"`).
* **Grid Resolution:** Logical X coordinates space from `120` to `1220`, Y coordinates space from `120` to `640`.

### 1.2 Coordinate Chart mapping (35 Nodes)

| Command ID | Plugin | X (px) | Y (px) | Grid Region / Phase |
| :--- | :--- | :--- | :--- | :--- |
| `/sdd:init` | `sdd` | 120 | 120 | Bootstrap |
| `/sdd:init-update` | `sdd` | 120 | 220 | Bootstrap |
| `/sdd:steering` | `sdd` | 280 | 170 | Bootstrap |
| `/sdd:continue` | `sdd` | 120 | 320 | Bootstrap |
| `/sdd:run` | `sdd` | 440 | 240 | Orchestration |
| `/git:branch-create` | `git` | 600 | 240 | P0 Setup |
| `/sdd:grill` | `sdd` | 600 | 340 | P1 Specs |
| `/sdd:specs` | `sdd` | 600 | 440 | P1 Specs |
| `/sdd:specs-review` | `sdd` | 600 | 540 | P1 Specs |
| `/sdd:design` | `sdd` | 760 | 540 | P2 Design |
| `/sdd:design-review` | `sdd` | 760 | 440 | P2 Design |
| `/sdd:tasks` | `sdd` | 760 | 340 | P3 Tasks |
| `/sdd:tasks-review` | `sdd` | 760 | 240 | P3 Tasks |
| `/sdd:build` | `sdd` | 920 | 240 | P4 Build |
| `/sdd:build-review` | `sdd` | 920 | 340 | P4 Build |
| `/sdd:validate` | `sdd` | 920 | 440 | P5 Validate |
| `/git:commit` | `git` | 1080 | 440 | P6/P8 Commit |
| `/git:push` | `git` | 1080 | 340 | P6 Deploy |
| `/gh-cli:pr-create` | `gh-cli` | 1080 | 240 | P6 Deploy |
| `/gh-cli:pr-list` | `gh-cli` | 1220 | 240 | P7 Review |
| `/gh-cli:pr-review` | `gh-cli` | 1220 | 340 | P7 Review |
| `/gh-cli:pr-respond` | `gh-cli` | 1220 | 440 | P8 Respond |
| `/gh-cli:pr-approve` | `gh-cli` | 1220 | 540 | P8 Align |
| `/gh-cli:pr-merge` | `gh-cli` | 1080 | 540 | P8 Merge |
| `/sdd:sync` | `sdd` | 1080 | 640 | P9 Sync |
| `/git:branch-delete` | `git` | 920 | 640 | P9 Cleanup |
| `/git:status` | `git` | 120 | 460 | Standalone / Utility |
| `/git:fetch` | `git` | 260 | 460 | Standalone / Utility |
| `/git:pull` | `git` | 400 | 460 | Standalone / Utility |
| `/git:switch` | `git` | 120 | 550 | Standalone / Utility |
| `/git:rebase` | `git` | 260 | 550 | Standalone / Utility |
| `/git:stash` | `git` | 400 | 550 | Standalone / Utility |
| `/git:tag-create` | `git` | 120 | 640 | Standalone / Utility |
| `/git:tag-push` | `git` | 260 | 640 | Standalone / Utility |
| `/git:tag-delete` | `git` | 400 | 640 | Standalone / Utility |

### 1.3 Boundary Connector Offsets & Cubic Bezier Calculations

We use Node centers $(x_c, y_c)$ for positioning, and offset path anchors to the node borders ($W = 140, H = 36$). For a source center $(x_1, y_1)$ and target center $(x_2, y_2)$, edge endpoints are defined dynamically:

1. **Horizontal flow going right:**
   * Start: $(x_1 + 70, y_1)$
   * End: $(x_2 - 70, y_2)$
   * Path: `M (x1+70) y1 C (x1+110) y1, (x2-110) y2, (x2-70) y2`
2. **Horizontal flow going left:**
   * Start: $(x_1 - 70, y_1)$
   * End: $(x_2 + 70, y_2)$
   * Path: `M (x1-70) y1 C (x1-110) y1, (x2+110) y2, (x2+70) y2`
3. **Vertical flow going down:**
   * Start: $(x_1, y_1 + 18)$
   * End: $(x_2, y_2 - 18)$
   * Path: `M x1 (y1+18) C x1 (y1+34), x2 (y2-34), x2 (y2-18)`
4. **Vertical flow going up:**
   * Start: $(x_1, y_1 - 18)$
   * End: $(x_2, y_2 + 18)$
   * Path: `M x1 (y1-18) C x1 (y1-34), x2 (y2+34), x2 (y2+18)`
5. **Special Loopback Path (`/gh-cli:pr-respond` to `/git:commit`):**
   * Curving down beneath the nodes to avoid overlapping straight horizontal edges:
   * Path: `M 1220 (440 + 18) C 1220 510, 1080 510, 1080 (440 + 18)`

---

## 2. Interactive Flow State Machine

We track interaction states using a Vanilla JS state machine.

### 2.1 States and Variables
* `MapState.selectedNodeId` (string | null): The ID of the clicked (locked) node.
* `MapState.hoveredNodeId` (string | null): The ID of the currently hovered node.

### 2.2 Transition Logic

| Current State | Event | Next State | Visual Render Actions |
| :--- | :--- | :--- | :--- |
| **Default** | Hover Node $N$ | **Hovering ($N$)** | Dim non-connected nodes/edges to $0.15$/$0.05$. Highlight node $N$, adjacent nodes, and connected edges. Preview $N$ details. |
| **Hovering ($N$)** | Leave Node $N$ | **Default** | Revert all opacity levels to normal ($1.0$). Revert details panel to default active sidebar item. |
| **Hovering ($N$)** | Click Node $N$ | **Selected Locked ($N$)** | Lock highlight on $N$ & its edges. Update sidebar active command. Set detail panel to lock on $N$. |
| **Selected Locked ($N$)** | Click Node $N$ | **Default** | Clear selected lock state. Revert map colors and details panel to default. |
| **Selected Locked ($N$)** | Click Map BG | **Default** | Clear selected lock state. Revert map colors and details. |
| **Selected Locked ($N$)** | Hover Node $M$ | **Selected + Preview ($M$)** | Dim everything except $M$ and its connected components. Show preview details of $M$. |
| **Selected + Preview ($M$)** | Leave Node $M$ | **Selected Locked ($N$)** | Revert visual highlight/details back to locked node $N$. |

---

## 3. DOM & Styling Specifications

### 3.1 CSS Stylesheet Modifications
We add custom styling classes for hover transitions, highlighting/dimming states, and the animated flow indicator.

```css
:root {
    --color-sdd: #fbbf24;
    --color-git: #60a5fa;
    --color-gh-cli: #f43f5e;
    --bg-sdd: rgba(245, 158, 11, 0.05);
    --bg-git: rgba(96, 165, 250, 0.05);
    --bg-gh-cli: rgba(244, 63, 94, 0.05);
    --border-sdd: rgba(245, 158, 11, 0.2);
    --border-git: rgba(96, 165, 250, 0.2);
    --border-gh-cli: rgba(244, 63, 94, 0.2);
}

.map-scroll-wrapper {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
}

.map-node {
    cursor: pointer;
    transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.2s ease;
}

.map-node rect {
    fill: #0b0c16;
    stroke-width: 1.5px;
    transition: stroke 0.2s, fill 0.2s, stroke-width 0.2s;
}

.map-node text {
    font-family: var(--font-main);
    font-size: 11px;
    font-weight: 600;
    fill: var(--text-secondary);
    text-anchor: middle;
    dominant-baseline: middle;
    transition: fill 0.2s;
}

/* Colors by plugin */
.map-node.plugin-sdd rect { stroke: var(--border-sdd); }
.map-node.plugin-sdd:hover rect { fill: var(--bg-sdd); stroke: var(--color-sdd); }
.map-node.plugin-git rect { stroke: var(--border-git); }
.map-node.plugin-git:hover rect { fill: var(--bg-git); stroke: var(--color-git); }
.map-node.plugin-gh-cli rect { stroke: var(--border-gh-cli); }
.map-node.plugin-gh-cli:hover rect { fill: var(--bg-gh-cli); stroke: var(--color-gh-cli); }

/* Dimmed / Highlight states */
.map-node.dimmed { opacity: 0.15; }
.map-node.highlighted { opacity: 1.0; }
.map-node.highlighted text { fill: var(--text-primary); }

.map-node.active rect { stroke-width: 2.5px; fill: rgba(255, 255, 255, 0.04); }
.map-node.active.plugin-sdd rect { stroke: var(--color-sdd); filter: drop-shadow(0 0 6px var(--color-sdd)); }
.map-node.active.plugin-git rect { stroke: var(--color-git); filter: drop-shadow(0 0 6px var(--color-git)); }
.map-node.active.plugin-gh-cli rect { stroke: var(--color-gh-cli); filter: drop-shadow(0 0 6px var(--color-gh-cli)); }

.map-edge {
    fill: none;
    stroke-width: 1.5px;
    transition: stroke 0.2s, stroke-width 0.2s, opacity 0.2s;
}

.map-edge.type-sequence { stroke: rgba(255, 255, 255, 0.12); }
.map-edge.type-dependency { stroke: rgba(96, 165, 250, 0.15); stroke-dasharray: 4, 4; }

.map-edge.dimmed { opacity: 0.05; }
.map-edge.highlighted {
    opacity: 1.0;
    stroke-width: 2.5px;
    stroke-dasharray: 6, 6;
    animation: flow-dash 25s linear infinite;
}
.map-edge.highlighted.from-sdd { stroke: var(--color-sdd); }
.map-edge.highlighted.from-git { stroke: var(--color-git); }
.map-edge.highlighted.from-gh-cli { stroke: var(--color-gh-cli); }

@keyframes flow-dash {
    to { stroke-dashoffset: -1000; }
}

/* Accessibility outline */
.map-node:focus-visible { outline: none; }
.map-node:focus-visible rect { stroke-width: 2.5px; stroke: #ffffff; filter: drop-shadow(0 0 8px #ffffff); }
```

### 3.2 HTML Structure Replacements
We replace the existing `.pipeline-group` layout blocks in `plugins/sdd/index.html` with this interactive card container:

```html
<div class="glass-panel" style="margin-bottom: 2rem; overflow-x: auto; padding: 1.5rem;">
    <div class="panel-title" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
        <span style="display: flex; align-items: center; gap: 0.75rem;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: #fbbf24;"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>
            Interactive Skill Connections Map
        </span>
        <span id="map-selection-indicator" style="font-size: 0.8rem; color: var(--text-secondary); font-style: italic;">
            Click a node to lock path selection
        </span>
    </div>
    <div class="map-scroll-wrapper">
        <svg id="connection-map-svg" width="1300" height="700" style="background: rgba(0, 0, 0, 0.25); border-radius: 16px; border: 1px solid var(--card-border);">
            <defs>
                <marker id="arrow-sdd" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                    <path d="M 0 1 L 10 5 L 0 9 z" fill="#fbbf24" />
                </marker>
                <marker id="arrow-git" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                    <path d="M 0 1 L 10 5 L 0 9 z" fill="#60a5fa" />
                </marker>
                <marker id="arrow-gh-cli" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                    <path d="M 0 1 L 10 5 L 0 9 z" fill="#f43f5e" />
                </marker>
            </defs>
            <g id="map-edges"></g>
            <g id="map-nodes"></g>
        </svg>
    </div>
</div>
```

---

## 4. Keyboard Accessibility & Spatial Navigation

To meet accessibility NFR requirements:
1. Every `<g class="map-node">` is rendered with `tabindex="0"`.
2. Keyboard triggers: Listening to `Enter` and `Spacebar` keydowns to toggle locked selection state.
3. **Spatial Keyboard Navigation Algorithm:** Focuses the closest node matching the directional arrow pressed, calculated using Euclidean coordinate distance:

```javascript
nodeElement.addEventListener('keydown', (e) => {
    let dirX = 0, dirY = 0;
    if (e.key === 'ArrowRight') dirX = 1;
    else if (e.key === 'ArrowLeft') dirX = -1;
    else if (e.key === 'ArrowDown') dirY = 1;
    else if (e.key === 'ArrowUp') dirY = -1;
    else if (e.key === ' ' || e.key === 'Enter') {
        e.preventDefault();
        MapState.select(node.id);
        return;
    } else {
        return;
    }
    e.preventDefault();

    let bestNode = null;
    let minDistance = Infinity;

    nodes.forEach(n => {
        if (n.id === node.id) return;
        const dx = n.x - node.x;
        const dy = n.y - node.y;

        // Verify direction constraint
        if (dirX > 0 && dx <= 10) return;
        if (dirX < 0 && dx >= -10) return;
        if (dirY > 0 && dy <= 10) return;
        if (dirY < 0 && dy >= -10) return;

        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < minDistance) {
            minDistance = dist;
            bestNode = n;
        }
    });

    if (bestNode) {
        const targetEl = document.querySelector(`[data-node-id="${bestNode.id}"]`);
        if (targetEl) targetEl.focus();
    }
});
```

---

## 5. Cross-Plugin Command Metadata Mirror

To implement the inline mirror configurations for all 19 `git` and `gh-cli` commands, we extend the static JS `commandData` object:

```javascript
// Append the following items to the existing commandData object in plugins/sdd/index.html
const gitAndGhCliData = {
    "/git:branch-create": {
        gated: false,
        desc: "Create and switch to a new feature branch checked out from the remote master/main.",
        policies: [
            { enforced: true, name: "Up-to-date baseline", desc: "Performs remote fetch on default branch before branching." }
        ],
        steps: [
            { title: "Fetch Remote States", desc: "Retrieve active repository listings from origin.", code: "git fetch origin" },
            { title: "Switch and Create", desc: "Checkout new feature branch.", code: "git checkout -b feature-branch origin/main" }
        ]
    },
    "/git:branch-delete": {
        gated: true,
        desc: "Securely delete a branch locally and on origin remote, refusing protected branches.",
        policies: [
            { enforced: true, name: "Protected Branch Guard", desc: "Refuses to delete main or master branches." }
        ],
        steps: [
            { title: "Local Branch Cleanup", desc: "Delete local pointer reference.", code: "git branch -d branch-name" },
            { title: "Remote Cleanup", desc: "Push delete action to upstream.", code: "git push origin --delete branch-name" }
        ]
    },
    "/git:commit": {
        gated: true,
        desc: "Commit staged workspace modifications using structured Conventional Commits templates.",
        policies: [
            { enforced: true, name: "Strict Messages", desc: "Requires Overview, Changes, and Impact sections." }
        ],
        steps: [
            { title: "Stage Modifications", desc: "Stages active modifications.", code: "git add ." },
            { title: "Create Commit", desc: "Records snapshot with human-gated confirmation description.", code: "git commit -m \"feat: description\"" }
        ]
    },
    "/git:fetch": {
        gated: false,
        desc: "Fetch branches and tags from origin remote updating remote-tracking branches.",
        policies: [],
        steps: [
            { title: "Fetch Changes", desc: "Fetch references from the remote server.", code: "git fetch" }
        ]
    },
    "/git:pull": {
        gated: false,
        desc: "Integrate modifications from the remote tracking branch into local active branch.",
        policies: [],
        steps: [
            { title: "Pull Branch", desc: "Integrate upstream changes securely.", code: "git pull origin branch" }
        ]
    },
    "/git:push": {
        gated: true,
        desc: "Push current feature commits to remote origin setting tracking reference.",
        policies: [],
        steps: [
            { title: "Push Reference", desc: "Pushes local commits upstream.", code: "git push -u origin branch" }
        ]
    },
    "/git:rebase": {
        gated: true,
        desc: "Rebase active branch commits onto a clean target branch.",
        policies: [],
        steps: [
            { title: "Rebase Execution", desc: "Rebase onto target branch.", code: "git rebase target-branch" }
        ]
    },
    "/git:stash": {
        gated: false,
        desc: "Temporarily save, list, restore or discard uncommitted working directory changes.",
        policies: [],
        steps: [
            { title: "Stash Modifications", desc: "Saves changes to stack.", code: "git stash" },
            { title: "Restore Modifications", desc: "Pops changes from stack.", code: "git stash pop" }
        ]
    },
    "/git:status": {
        gated: false,
        desc: "Inspect working tree modifications and tracking comparison.",
        policies: [],
        steps: [
            { title: "Check Status", desc: "Check current modifications state.", code: "git status" }
        ]
    },
    "/git:switch": {
        gated: false,
        desc: "Switch the workspace working tree to a target branch.",
        policies: [],
        steps: [
            { title: "Switch Branch", desc: "Changes directory state to targeted branch.", code: "git checkout branch" }
        ]
    },
    "/git:tag-create": {
        gated: true,
        desc: "Create an annotated release tag at current HEAD.",
        policies: [],
        steps: [
            { title: "Tag Local HEAD", desc: "Creates annotated tag.", code: "git tag -a v1.0.0 -m \"msg\"" }
        ]
    },
    "/git:tag-delete": {
        gated: true,
        desc: "Delete a local and remote tag reference.",
        policies: [],
        steps: [
            { title: "Delete Local Tag", desc: "Removes tag reference locally.", code: "git tag -d tag-name" }
        ]
    },
    "/git:tag-push": {
        gated: true,
        desc: "Push local tags upstream to remote origin.",
        policies: [],
        steps: [
            { title: "Push Tags", desc: "Pushes tags to remote repository.", code: "git push origin --tags" }
        ]
    },
    "/gh-cli:pr-create": {
        gated: true,
        desc: "Open a pull request on GitHub tracking current commits.",
        policies: [
            { enforced: true, name: "Gated Validation", desc: "Verifies builds pass before creating PR." }
        ],
        steps: [
            { title: "Create Pull Request", desc: "Initializes PR utilizing gh client.", code: "gh pr create --title \"title\" --body \"body\"" }
        ]
    },
    "/gh-cli:pr-list": {
        gated: false,
        desc: "List the repository's open pull requests.",
        policies: [],
        steps: [
            { title: "List Pull Requests", desc: "List current repository pull requests.", code: "gh pr list" }
        ]
    },
    "/gh-cli:pr-review": {
        gated: false,
        desc: "Review pull request diffs and submit structured feedback comments.",
        policies: [
            { enforced: true, name: "Review Restrictions", desc: "Enforces COMMENT reviews by default." }
        ],
        steps: [
            { title: "Submit review", desc: "Posts structured feedback comments to GitHub thread." }
        ]
    },
    "/gh-cli:pr-respond": {
        gated: false,
        desc: "Triage review comments and apply local codebase fixes.",
        policies: [],
        steps: [
            { title: "Fetch reviews", desc: "Retrieves pull request comments and suggestions." }
        ]
    },
    "/gh-cli:pr-approve": {
        gated: true,
        desc: "Approve the current branch's PR on GitHub.",
        policies: [
            { enforced: true, name: "No Self-Approve", desc: "Prevents developers from approving their own PRs." }
        ],
        steps: [
            { title: "Approve Pull Request", desc: "Submits approval review.", code: "gh pr review --approve" }
        ]
    },
    "/gh-cli:pr-merge": {
        gated: true,
        desc: "Merge the active pull request securely with squash merging default.",
        policies: [],
        steps: [
            { title: "Merge PR", desc: "Merges the branch on GitHub.", code: "gh pr merge --squash" }
        ]
    }
};
```
