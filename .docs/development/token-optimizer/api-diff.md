# API Delta: Token Optimizer Agents & Global Token Optimization

- **Feature:** Token Optimizer Agents & Global Token Optimization
- **Slug:** `token-optimizer`
- **Domain:** `optimizer`

## New Agent Definition
- Path: `plugins/kanche/agents/token-optimizer/agent.json`
- Schema:
  ```json
  {
    "name": "token-optimizer",
    "description": "Specialized subagent for LLM prompt distillation, context window efficiency, token budgeting, and instruction compaction.",
    "model": "flash",
    "system_prompt": "...",
    "enable_write_tools": false,
    "tools": ["read_file", "view_file", "grep_search", "list_dir"]
  }
  ```

## New Skill Contract
- Skill: `/kanche:token-optimize`
- Path: `plugins/kanche/skills/token-optimize/SKILL.md`
- Inputs:
  - `<target-path>` (optional positional): Path to file or directory to optimize.
  - `--auto-apply`: Apply changes directly to disk.
  - `--budget=<number>`: Optional target token budget limit.
  - `--format=text|json`: Output format (default text).
- Output: Structured token reduction statistics and optimized output.

## New Rule Definition
- Path: `plugins/kanche/rules/token-optimization.md`
- Core guidelines for telegraphic instruction engineering, anti-bloat principles, deduplication, and context caching.

## Modified Manifests & Showcase
- `plugins/kanche/plugin.json`: Team count updated from 16 to 17 agents; keywords and description updated.
- `README.md`: Agent catalog updated with `@token-optimizer`; skill catalog updated with `/kanche:token-optimize`.
- `index.html`: Added card for `@token-optimizer` and skill entry for `/kanche:token-optimize`.
