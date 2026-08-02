# System Design: gh-cli-pr-review-format

## Approach
Update the instructional prompt within `plugins/kanche/skills/gh-cli-pr-review/SKILL.md` to strictly enforce the new formatting rules. The changes will redefine how the review summary, severity summary table, and inline comments are structured. Since this is an agent skill, the "implementation" is simply refining the prompt template in the markdown file.

## Architecture context
This affects the PR Review Loop of the Loop Engineering Framework within the Kanche plugin. The skill acts as an AI prompt layer before calling `@gh-operator`.

## Components
- `plugins/kanche/skills/gh-cli-pr-review/SKILL.md`: 
  - **Modifications**: Rewrite steps 5 and 6 to include explicit instructions and Markdown templates for the `# Summary`, `## Review Summary`, and `### inline comments` sections. The score heuristic and table format with color emojis (`🔴`, `🟡`, `🟢`) will be explicitly defined.

## Interfaces
- **Output Format (PR Comment Body)**:
  - `# Summary`: Short description, severity score (out of 10 based on findings heuristic), total files touched, total lines modified.
  - `## Review Summary`: ASCII table `| Severity | Count | Category |`.
  - `### inline comments`: Formatted file and line indicators, followed by the exact suggestion blocks (already partially defined, but will be standardized).

## Data changes
No database or state changes. The review document structure mapped in the specs will be rendered as markdown text.

## Alternatives
- **Using a separate template formatting script**: We could use a script to reformat a JSON output from the agent into Markdown. 
  *Rejected* because Kanche relies on LLMs' text generation capabilities and adding a script increases complexity for a simple Markdown structure change.

## Risks
- **Risk**: The AI might hallucinate the formatting, fail to render the ASCII table correctly, or miscalculate the "severity score" out of 10.
- **Mitigation**: Provide a strict, verbatim example in the `SKILL.md` prompt, including the table headers, the emojis, and a clear instruction on how to calculate the severity score heuristically.
