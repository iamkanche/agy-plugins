# Fix SDD UI Containers — Technical Design

<!-- schema: design | written by /sdd:design -->

## Approach
To resolve the grid and flex layout column blowouts, we need to ensure that the flex children (`.content-area` in `index.html` and `.details-area` in `plugins/sdd/index.html`) can shrink below their minimum content sizes when space is constrained.
1. **Grid Column Definition:**
   Modify the main grid layout in both `index.html` and `plugins/sdd/index.html`:
   Change `grid-template-columns: 320px 1fr;` to `grid-template-columns: 320px minmax(0, 1fr);`. This ensures that the second column track allows shrinking down to 0, rather than maintaining a minimum content width based on wide children (like the SVG map or long code snippets).
2. **Details / Content Area styling:**
   Add `min-width: 0;` to `.content-area` in `index.html` and `.details-area` in `plugins/sdd/index.html` as a safety measure for flex child shrinking.
3. **SVG container wrapper styling:**
   Ensure `.map-scroll-wrapper` container has `max-width: 100%;` and `overflow-x: auto;` to handle local scrollbar constraints smoothly.

## Architecture context
Files modified:
- `index.html` (root)
- `plugins/sdd/index.html`

## Components
| Component | Responsibility | New/Modified |
|---|---|---|
| `index.html` | Root registry dashboard layout | Modified |
| `plugins/sdd/index.html` | SDD inspector dashboard layout | Modified |

## Interfaces
No new APIs or endpoints.

## Data / schema changes
No database or schema changes.

## Sequence
No complex asynchronous sequence. Page layout styling changes are resolved immediately by the browser rendering engine upon parsing the modified style declarations.

## Alternatives considered
- Hardcoding percentages or media query break-points for the SVG size. Rejected: It breaks the visual rendering of the map nodes and requires coordinates updates. Allowing horizontal scroll containers inside a flexbox with `min-width: 0` is the standard, cleanest solution.

## Risks
None identified.
