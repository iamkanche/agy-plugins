# System Design Specification: Human-Gated PR Merge Workflow

## System Architecture

### Component Updates
1. **`.sdd-docs/settings.json`**:
   - `auto_merge`: boolean set to `false`.
2. **`.sdd-docs/product/memory.md`**:
   - Durable rule documenting mandatory human gating for PR merging when `auto_merge: false`.
3. **`plugins/sdd/skills/run/SKILL.md`**:
   - Phase P9 workflow updated to evaluate `auto_merge` parameter from `settings.json`.
4. **`plugins/gh-cli/skills/pr-merge/SKILL.md`**:
   - Step 4 (Gate) updated to check both `mode=auto` AND `auto_merge: true` before bypassing interactive prompts.
5. **`plugins/sdd/rules/workflow-gating.md`**:
   - Gating rule updated to reflect PR merge confirmation exception under `auto_merge: false`.

## Data Flow
```
[ P9 Execution ] -> [ Check auto_merge in settings.json ]
                         |
           +-------------+-------------+
           |                           |
    (auto_merge: true)          (auto_merge: false)
           |                           |
   [ Execute PR Merge ]      [ Prompt User (default_api:ask_question) ]
                                       |
                                +------+------+
                                |             |
                             (Yes)           (No)
                                |             |
                      [ Execute Merge ]  [ Abort Merge ]
```
