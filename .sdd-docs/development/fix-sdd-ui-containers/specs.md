# Fix SDD UI Containers — Specification

<!-- schema: specs | written by /sdd:specs -->

## Context
The Antigravity plugins marketplace registry dashboard (`index.html`) and the SDD workflow inspector page (`plugins/sdd/index.html`) display command grids, pipeline steps, and interactive connection maps. On smaller viewports or with wide content (e.g. the 1300px connection map), grid and flex items blow out layout bounds, causing unwanted horizontal scrolling on the entire page body instead of local scroll containers.

## Scope
- **In scope:**
  - Fix grid layout column blowouts in `index.html` and `plugins/sdd/index.html` by setting proper minimum widths (`min-width: 0`) and grid column limits (`minmax(0, 1fr)`).
  - Ensure the SVG connection map container scrolls locally and does not expand its parent containers.
  - Ensure pipeline step containers scroll locally without blowing out the dashboard layout grid.
- **Out of scope:**
  - Redesigning the registry dashboard or SDD inspector UI styling theme (keep the existing glassmorphic design).
  - Modifying SVG path coordinates or command metadata.

## User stories
- As an Antigravity developer using the dashboard on a laptop or tablet, I want the page grid layout to remain within the screen viewport, so that I don't have to scroll the entire page horizontally to view the sidebar or content.
- As a mobile user, I want the page to adjust to single-column layout cleanly, with scrollable components (like maps and pipelines) scrolling locally.

## Acceptance criteria
1. Given a desktop or laptop browser window, when index.html is loaded, then the grid layout stays confined to the window viewport, and no horizontal scrollbar appears on the main body.
2. Given the SDD inspector page (`plugins/sdd/index.html`), when the interactive map or pipeline container overflows, then horizontal scrollbars are constrained to their respective panels, and the main layout does not blow out.
3. Given viewport width under 1024px, when the layout collapses to a single column, then the content container respects the width and does not overflow the page body.

## Data model
No schema or data model modifications.

## Non-functional requirements
- Maintain a highly responsive, modern glassmorphic look.
- Zero external CSS/JS dependencies added.
- No visual regressions for existing dashboard components.

## Open questions
_Resolved in grill-me: We will apply CSS min-width: 0 rules on main content/details containers and use minmax(0, 1fr) for grid template columns to prevent blowout without altering page width or breaking layout flow._
