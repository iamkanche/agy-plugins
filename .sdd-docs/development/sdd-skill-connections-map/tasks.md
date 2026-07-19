# Tasks: Interactive Skill Connection Map

This document outlines the implementation task checklist for the Interactive Skill Connections Map feature in the SDD Inspector Dashboard.

---

## Phase 1: CSS Additions
*Target File:* [index.html](file:///home/kenneth-ancheta/src/github.com/agy-plugins/plugins/sdd/index.html)

- [ ] **CSS-1**: Add custom CSS properties for plugin themes (`--color-sdd`, `--color-git`, `--color-gh-cli`, and respective translucent background/border variables) to the `:root` rule. `[P]` *[Design Section 3.1] [Specs AC-1]*
- [ ] **CSS-2**: Define the `.map-scroll-wrapper` rule with `overflow-x: auto` to enable clean horizontal scrolling on narrow screens. `[P]` *[Design Section 3.1] [Specs AC-6]*
- [ ] **CSS-3**: Add styling rules for SVG nodes (`.map-node`, `.map-node rect`, `.map-node text`) detailing fonts, sizes, pointer cursors, transitions, and hover-triggered fills/strokes. `[P]` *[Design Section 3.1] [Specs AC-1]*
- [ ] **CSS-4**: Implement highlight and dim states classes (`.dimmed`, `.highlighted`, `.active`) for interactive map elements. `[P]` *[Design Section 3.1] [Specs AC-2, AC-3]*
- [ ] **CSS-5**: Define styling rules for connection edges (`.map-edge`, `.map-edge.type-sequence`, `.map-edge.type-dependency`) including baseline opacities, strokes, and dasharrays. `[P]` *[Design Section 3.1] [Specs AC-1]*
- [ ] **CSS-6**: Implement the flow dash animation keyframe (`@keyframes flow-dash`) and class assignments for path animation. `[P]` *[Design Section 3.1] [Specs AC-4]*
- [ ] **CSS-7**: Add keyboard accessibility outlines (`.map-node:focus-visible rect`) to indicate active tab-focus. `[P]` *[Design Section 3.1] [Specs NFR / AC-6]*

---

## Phase 2: HTML Template Modifications
*Target File:* [index.html](file:///home/kenneth-ancheta/src/github.com/agy-plugins/plugins/sdd/index.html)

- [ ] **HTML-1**: Locate and replace the entire `.pipeline-group` layout blocks (currently lines 467-553) with the new `glass-panel` container for the Interactive Skill Connections Map. *[Design Section 3.2] [Specs AC-1, AC-6]*
- [ ] **HTML-2**: Inject the responsive `<svg>` canvas with attributes `id="connection-map-svg"`, `width="1300"`, `height="700"`, and custom styling. *[Design Section 1.1] [Specs AC-1]*
- [ ] **HTML-3**: Embed the SVG `<defs>` block with color-coded `<marker>` arrowheads (`arrow-sdd`, `arrow-git`, `arrow-gh-cli`) matching the target plugins. *[Design Section 3.2] [Specs AC-1]*
- [ ] **HTML-4**: Add structural SVG container groups `<g id="map-edges"></g>` and `<g id="map-nodes"></g>` to control layering (edges rendered behind nodes). *[Design Section 3.2] [Specs AC-1]*

---

## Phase 3: JavaScript Data Registry Setup
*Target File:* [index.html](file:///home/kenneth-ancheta/src/github.com/agy-plugins/plugins/sdd/index.html)

- [ ] **JS-DATA-1**: Declare a static `nodes` array containing metadata for all 35 dashboard commands (`id`, `name`, `plugin`, `x`, `y`, `phase`). *[Design Section 1.2] [Specs Data Model]*
- [ ] **JS-DATA-2**: Declare a static `edges` array mapping the 31 lifecycle connections, defining `from`, `to`, and `type` (`sequence` | `dependency`). *[Specs Data Model]*
- [ ] **JS-DATA-3**: Append the `gitAndGhCliData` object containing metadata configurations (descriptions, policies, steps) for the 19 non-sdd commands. *[Design Section 5] [Specs AC-5]*
- [ ] **JS-DATA-4**: Add a startup script hook to dynamically merge `gitAndGhCliData` into the core `commandData` object on page load. *[Design Section 5] [Specs AC-5]*

---

## Phase 4: JavaScript Math & Drawing Engine
*Target File:* [index.html](file:///home/kenneth-ancheta/src/github.com/agy-plugins/plugins/sdd/index.html)

- [ ] **JS-RENDER-1**: Write the connection maths function calculating Cubic Bezier anchors based on source/target node coordinate bounds (horizontal left/right, vertical up/down, and custom loopback curvature). *[Design Section 1.3] [Specs AC-1]*
- [ ] **JS-RENDER-2**: Implement the edge rendering engine to construct and inject path elements into `<g id="map-edges">` with markers and interaction tags. *[Design Section 3.1] [Specs AC-1]*
- [ ] **JS-RENDER-3**: Implement the node rendering engine to construct and inject `<g class="map-node">` elements with background `<rect>`, `<text>`, and correct class configurations. *[Design Section 3.1] [Specs AC-1]*
- [ ] **JS-RENDER-4**: Bind standard event handlers (`mouseover`, `mouseout`, `click`, `focus`, `blur`) dynamically to each node element during creation. *[Design Section 2.2] [Specs AC-2, AC-3]*

---

## Phase 5: Interactive State Machine & Side-Effects
*Target File:* [index.html](file:///home/kenneth-ancheta/src/github.com/agy-plugins/plugins/sdd/index.html)

- [ ] **JS-STATE-1**: Declare the `MapState` controller containing `selectedNodeId` and `hoveredNodeId` trackers. *[Design Section 2.1]*
- [ ] **JS-STATE-2**: Implement the `hover` transition handler: highlight hovered node, update details panel dynamically, and apply `.dimmed` classes to all unrelated nodes/edges. *[Design Section 2.2] [Specs AC-2]*
- [ ] **JS-STATE-3**: Implement the `select` toggle lock handler: lock selection on clicked node, synchronize active state with the sidebar list, and update details card selection. *[Design Section 2.2] [Specs AC-3]*
- [ ] **JS-STATE-4**: Implement selection clearance: revert visual states and panel data when clicking the active node, the map background, or on a reset trigger. *[Design Section 2.2] [Specs AC-3]*
- [ ] **JS-STATE-5**: Add support for preview overlays: hovering over a node while selection-locked overlays the preview path highlight and metadata temporarily. *[Design Section 2.2] [Specs AC-3]*

---

## Phase 6: Keyboard Accessibility & Spatial Navigation
*Target File:* [index.html](file:///home/kenneth-ancheta/src/github.com/agy-plugins/plugins/sdd/index.html)

- [ ] **JS-A11Y-1**: Ensure all rendered node elements are output with `tabindex="0"`. *[Design Section 4] [Specs NFR]*
- [ ] **JS-A11Y-2**: Bind keydown event listeners on node elements to support `Enter` and `Spacebar` for toggling locks. *[Design Section 4] [Specs AC-3 / NFR]*
- [ ] **JS-A11Y-3**: Implement the Euclidean distance spatial navigation algorithm for direction arrow keys (`ArrowUp`, `ArrowDown`, `ArrowLeft`, `ArrowRight`) to cycle focus to the nearest logical node in that direction. *[Design Section 4] [Specs NFR]*

---

## Verification & Checkpoints

Since there is no automated test runner, validation is done manually inside the browser environment. Use the following checkpoints to verify completeness.

### Automated Checks
- [ ] **LINT-1**: Verify HTML and JS parsing by opening the developer console (F12) and checking for zero runtime syntax/type errors.

### Manual Visual Checkpoints
- [ ] **VERIFY-1**: Load [sdd/index.html](file:///home/kenneth-ancheta/src/github.com/agy-plugins/plugins/sdd/index.html) and confirm the interactive grid renders 35 nodes correctly color-themed (Amber for `sdd`, Blue for `git`, Red/Pink for `gh-cli`). *[Covers AC-1]*
- [ ] **VERIFY-2**: Hover over a node and confirm that its incoming/outgoing paths are highlighted, non-related nodes/edges fade, and details display in the sidebar card. *[Covers AC-2]*
- [ ] **VERIFY-3**: Hover over an active connection and confirm that the stroke dash animation triggers in the direction of flow. *[Covers AC-4]*
- [ ] **VERIFY-4**: Click a node to lock selection, then hover over a secondary node. Confirm the secondary node triggers a path preview, and the details card previews its metadata. *[Covers AC-3]*
- [ ] **VERIFY-5**: Verify clicking the map background or re-clicking the locked node clears the selection and returns the dashboard to its baseline state. *[Covers AC-3]*
- [ ] **VERIFY-6**: Select a `git` or `gh-cli` command node and verify the sidebar details card successfully renders its custom step configurations and rules. *[Covers AC-5]*
- [ ] **VERIFY-7**: Resize the browser screen to a width under `1024px` and verify the map panel displays horizontal scrollbars without wrapping or breaking the grid coordinates. *[Covers AC-6]*
- [ ] **VERIFY-8**: Use the `Tab` key to cycle through all 35 nodes. Press `Enter`/`Space` on a focused node to verify selection lock, and use Arrow keys to verify spatial directional focus movement. *[Covers Keyboard NFR]*
