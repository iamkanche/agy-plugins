# Token Optimization & Context Efficiency Policy

Universal rules for context window efficiency, instruction compression, and token budget management across all skills, agent definitions, workflows, and prompts. Enforced globally by `@token-optimizer`.

## 1. Response Formatting & Communication Rules
- **Short & Direct:** Make responses concise, actionable, and strictly direct. State conclusions, findings, or code changes immediately without throat-clearing.
- **Bullets Over Paragraphs:** Use crisp bullet points (`- `) and compact Markdown tables wherever possible instead of dense multi-line prose paragraphs.
- **Zero Conversational Padding:** Disallow pleasantries, polite filler ("Sure, I can help with that...", "As an AI..."), and conversational meta-commentary ("Let's delve into...").
- **Bottom Line Up Front (BLUF):** Present verdicts, conclusions, and action items first; supporting details second.
- **Surgical Diffs:** Output only the minimal necessary code or text changes. Never rewrite unchanged files.

## 2. Telegraphic Directives in Prompts & Skills
- **Imperative Syntax:** Use strong, active verbs ("Run...", "Check...", "Extract...", "Format...") instead of passive or explanatory narrative.
- **Concise Constraints:** State operational boundaries directly without philosophical justifications.
- **Single Source of Truth:** Do not duplicate universal rules inline across skills. Reference `rules/destructive-safety.md`, `rules/token-optimization.md`, or `rules/git-hard-rules.md`.

## 3. Prompt Caching Optimization
- **Stable Prefix Ordering:** Place static, reusable instructions, invariants, and role descriptions at the beginning of prompts. Keep dynamic variables and session-specific payloads at the end to maximize LLM prompt-caching hit rates.
- **Consistent Tokens:** Maintain exact identical wording for invariant headers, schema blocks, and error guards across skills to maximize prefix caching.

## 4. Structured Compact Machine Formats
- **Machine-Readable Fenced Blocks:** Prefer compact key-value blocks (e.g. `review-verdict`) or dense JSON over long conversational explanations.
- **Tabular Summaries:** Use compact tables for multi-attribute listings.

## 5. Non-Negotiable Safety Invariants
- **Never Truncate Gating:** Token optimization must NEVER strip or bypass mandatory human confirmation prompts (`default_api:ask_question`), destructive command warnings, or review interfaces.
- **Contract Fidelity:** Preserve all required CLI options, flags, and return formats verbatim.
