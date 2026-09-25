---
name: token-optimize
description: Audit, distill, and compress prompts, skills, and agent instructions to maximize context efficiency and token savings.
model: flash
---

# /kanche:token-optimize

**Summary.** Audit and compress prompt templates, SKILL.md documents, agent system prompts, and rule files to maximize context efficiency, reduce token expenditure, and accelerate inference. The workflow delegates analysis to the specialized `@token-optimizer` subagent (defined in `agents/token-optimizer/agent.json`) and strictly complies with `rules/token-optimization.md`.

## Inputs

Parse invocation arguments:

- `<target-path>` (positional, optional) — file path or directory to audit and optimize. Defaults to modified diff or whole plugin prompt set.
- `--auto-apply` — automatically write the optimized, compressed content back to disk. Defaults to dry-run (read-only audit).
- `--budget=<number>` — target maximum token limit for the target file/prompt.
- `--format=text|json` — output report format (default: `text`).

## Steps

1. **Scan Target Files.** Locate specified files or gather all prompts in target path. Compute baseline metrics (character count, estimated tokens using ~4 chars/token heuristic or native tokenizer).
2. **Detect Token Inefficiencies.** Identify:
   - Conversational padding, throat-clearing, and polite preamble phrases.
   - Repeated/redundant rule restatements that can reference centralized rules in `rules/`.
   - Verbose prose that can be converted into telegraphic directives or compact markdown tables.
   - Cache-hostile dynamic prefixes before static invariant rules.
3. **Execute Distillation.** Apply compaction strategies per `rules/token-optimization.md`:
   - Enforce telegraphic imperative style.
   - Retain 100% of CLI arguments, option flags, input requirements, and output schemas.
   - Retain verbatim all human confirmation gates (`default_api:ask_question`) and destructive action warnings (`rules/destructive-safety.md`).
4. **Safety & Semantic Invariance Check.** Verify:
   - Zero lost CLI options or parameters.
   - Zero altered safety gates or review verdict structures.
   - Valid YAML frontmatter and JSON/Markdown syntax.
5. **Apply or Emit Report.**
   - If `--auto-apply` is active, write optimized files to disk.
   - Emit audit report summarizing: original tokens, optimized tokens, tokens saved, percentage reduction, and semantic verification status.

## Report Schema (Text or JSON)

```text
=== Token Optimization Report ===
Target: <path>
Original Estimated Tokens: <count>
Optimized Estimated Tokens: <count>
Savings: <saved> tokens (<percentage>%)
Safety Invariants Verified: PASS
Status: [Dry-run / Applied]
```

## Rules

- Read-only by default. Requires `--auto-apply` to write modifications to disk.
- Never truncate or weaken human confirmation gates (`ask_question`), destructive command warnings, or review interfaces.
- Follow `rules/token-optimization.md` and `rules/output-language.md`.

## Done when

- Target files are audited and compressed with measurable token savings (≥15%).
- Zero semantic or functional regressions introduced.
- All safety invariants remain intact.
