# Specifications

## Context
Currently, the `/kanche:gh-cli-pr-review` skill outputs PR review results using a standard markdown table layout. To improve readability and standardize the presentation for developers, the output format needs to be updated to a specific custom structured format. This format includes a high-level summary, a categorized ASCII-style table of review severities, and properly formatted inline comments with actionable code suggestions.

## Scope
**In-scope:**
- Modify the formatting template of `/kanche:gh-cli-pr-review` to match the target custom layout.
- Implement the `# Summary` section with a short description, severity score, total files, and total lines.
- Implement the `## Review Summary` section with a specific ASCII-style table (Severity, Count, Category) and color emojis.
- Implement the `### inline comments` section detailing file paths, line numbers, issue descriptions, code suggestions, and explanations.

**Out of scope / non-goals:**
- Modifying the underlying code review logic, rules engine, or the criteria for flagging issues.
- Changes to any other skills or plugins outside of `gh-cli-pr-review`.
- Modifying how the skill posts to GitHub APIs beyond the formatting of the text payload.

## User stories
As a developer reviewing a Pull Request, I want the automated review output to be formatted with clear summaries, categorized severity counts, and structured inline code suggestions, so that I can quickly understand the impact of the issues and apply suggested fixes seamlessly.

## Acceptance criteria
1. **Summary Generation**: When `/kanche:gh-cli-pr-review` executes, its output must begin with a `# Summary` section containing a short summary sentence, a severity score (e.g., 6/10), the total number of files affected, and the total lines of code reviewed.
2. **Review Summary Table**: The output must include a `## Review Summary` section formatted as an ASCII table showing columns for `Severity`, `Count`, and `Category`, specifically using the indicators `🔴 HIGH`, `🟡 MEDIUM`, and `🟢 LOW`.
3. **Inline Comments Formatting**: The output must include a `### inline comments` section that clearly points to specific files and line numbers.
4. **Suggestion Blocks**: Each inline comment must follow the exact format: 
   - `[<SEVERITY>] <Short description>`
   - `Issue: <description of what is wrong>`
   - `Suggestion:` followed by a markdown code block tagged with `suggestion` containing the replacement code.
   - `Why: <explanation>`
5. **No Regression**: The underlying review findings must remain accurate and only the formatting of the text should change.

## Data model
- **PR Review Output Document Structure**:
  - `SummaryData`: string `description`, integer `severityScore` (out of 10), integer `totalFiles`, integer `totalLines`.
  - `ReviewSummaryTable`: array of objects `{ severity: string, count: integer, category: string }`.
  - `InlineComment`: object `{ file: string, lineRange: string, severity: enum(HIGH, MEDIUM, LOW), shortDescription: string, issue: string, suggestion: string, explanation: string }`.

## NFR (non-functional requirements)
- **Compatibility**: The generated output must be valid Markdown that renders correctly in GitHub's web UI.
- **Performance**: The template formatting process should add negligible overhead (e.g., < 100ms) to the existing review generation execution time.

## Open questions
- Are there specific formulas for calculating the overall "Severity: N/10" score? 
  *Assumption if unanswered: The score will be derived heuristically based on the counts of HIGH/MEDIUM/LOW issues.*
- Should "total files" and "total lines of code" represent the entire PR diff or only the specific files reviewed by the agent? 
  *Assumption if unanswered: It will represent the specific files/lines modified in the PR diff that were reviewed.*
