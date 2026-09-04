---
name: ui-design-stitch
description: Generate visual UI screens, variants, and design systems using StitchMCP for system and UI design specifications.
model: flash
---

# /kanche:ui-design-stitch

**Summary.** Generate autonomous visual UI designs, screen wireframes, visual variants, and design systems via the StitchMCP server for feature and interface design specifications.

## Tools (StitchMCP)

This skill utilizes lazy-loaded StitchMCP tools:
- `create_project` — Initialize a Stitch UI project workspace.
- `generate_screen_from_text` — Generate full UI screen layouts and HTML/CSS mockups from textual feature descriptions.
- `edit_screens` — Refine generated UI screens based on feedback or design review iterations.
- `generate_variants` — Produce visual theme variants (e.g. dark/light modes, glassmorphism).
- `create_design_system` — Generate unified design tokens, typography, and color palettes.
- `apply_design_system` — Apply design system tokens to project screens.

## Workflow & Steps

1. **Initialize Project**: Call `create_project` for the feature slug if a project does not exist.
2. **Generate Design System**: Call `create_design_system` to establish token themes, typography (Google Fonts Inter/Outfit), and HSL color palettes.
3. **Generate Visual Screens**: Call `generate_screen_from_text` for each user flow screen described in `specs.md`.
4. **Produce Variants**: Call `generate_variants` to create light/dark mode and responsive layout variations.
5. **Export to `design.md`**: Embed generated screen links, visual design tokens, and layout guidelines directly into `.docs/development/{slug}/design.md`.

## Design Architecture Workflow

The `@designer` and `@architect` subagents invoke this skill to formulate UI screens, themes, and design tokens before design review.

## Done when

- Visual screens and design tokens are generated via StitchMCP.
- Visual specs and tokens are documented in `design.md`.
