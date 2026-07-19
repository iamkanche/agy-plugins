# Specs: Specialized SDD Subagents

## Context
Currently, the Software Development Document (SDD) lifecycle workflow plugin has no defined subagents. This forces the parent workspace agent to execute all planning, design, coding, review, and validation tasks directly, which can lead to context pollution and limits the modularity of specialized tasks. This work exists to define specialized subagents for each key role in the SDD phase model, ensuring that each phase's skills (specs, design, tasks, build, validate, review, sync) are delegated to dedicated, role-specific subagents.

## Scope
### In-Scope
1. Define specialized subagents under the `plugins/sdd/` directory.
2. Group the SDD skills into 5 logical role-based subagents:
   - `sdd-analyst`: Handles feature interrogation, specs drafting, and specs review (`grill`, `specs`, `specs-review`).
   - `sdd-architect`: Handles architecture design and design review (`design`, `design-review`).
   - `sdd-planner`: Handles guideline bootstrap, repository updates, tasks drafting, and tasks review (`init`, `init-update`, `steering`, `tasks`, `tasks-review`).
   - `sdd-coder`: Handles code implementation and implementation code review (`build`, `build-review`).
   - `sdd-validator`: Handles validation, deployment/alignment actions, and overall workflow run control (`validate`, `sync`, `continue`, `run`).
3. Add the subagents to the `plugins/sdd/plugin.json` manifest structure so that `agy plugin install` registers them correctly.
4. Set up specialized system prompts, permissions, and tool-access configurations for each subagent in separate `agent.json` files.
5. Reference the subagents in the descriptions of their relevant skills in the `index.html` main registry dashboard.

### Out of Scope / Non-goals
- Modifying the underlying execution engine of the Google Antigravity SDK or CLI.
- Automatically migrating existing running SDD workflows to use these subagents midway through execution (this is for new or restarted workflow invocations).
- Creating new backend command-line executors for the agents.

## User stories
- **As a Developer**, I want the SDD plugin to have specialized subagents for analysis, architecture, planning, coding, and validation, so that each task is handled by a focused agent with minimal unnecessary context and appropriate tool privileges.
- **As an Antigravity Agent**, I want to register and spawn specialized subagents from the `sdd` plugin automatically when executing steps in the SDD phase model.

## Acceptance criteria
1. **Validation of Manifest (plugin.json)**:
   - The file `plugins/sdd/plugin.json` must declare an `agents` array containing the paths to all 5 specialized subagent configurations.
2. **Subagent Configuration Files**:
   - The files `plugins/sdd/agents/{agent-name}/agent.json` must exist for all 5 subagents.
   - Each configuration must specify the correct `name`, a clear `description`, a targeted `system_prompt`, and correct boolean flags for `enable_write_tools`, `enable_mcp_tools`, and `enable_subagent_tools`.
3. **Write Tool Permission Boundaries**:
   - `sdd-coder` and `sdd-planner` must have `enable_write_tools: true`.
   - `sdd-analyst`, `sdd-architect`, and `sdd-validator` must have `enable_write_tools: false`.
4. **Registry Dashboard View**:
   - The main registry dashboard `index.html` must be updated to display descriptions showing delegation to the new subagents for the relevant `sdd` commands.
5. **Successful Plugin Reinstallation**:
   - Running `agy plugin install /home/kenneth-ancheta/src/github.com/agy-plugins` must process all 5 agents under the `sdd` plugin and display `✔ agents      : 5 processed` without errors.

## Data model
- **Plugin Manifest Schema** (existing, updated):
  - Adds the `agents` array under the `sdd` plugin definition in `plugins/sdd/plugin.json`:
    ```json
    "agents": [
      "agents/sdd-analyst/agent.json",
      "agents/sdd-architect/agent.json",
      "agents/sdd-planner/agent.json",
      "agents/sdd-coder/agent.json",
      "agents/sdd-validator/agent.json"
    ]
    ```
- **Subagent Manifest Schema** (new files):
  - A JSON structure with keys: `name`, `description`, `system_prompt`, `enable_write_tools` (boolean), `enable_mcp_tools` (boolean), `enable_subagent_tools` (boolean).

## NFR (non-functional requirements)
- **Security / Safety**: Subagents with read-only roles (analyst, architect, validator) must not be granted write tools to prevent unintended workspace edits.
- **Zero-runtime-overhead**: Subagent registration must only occur during plugin installation time; execution is dynamically delegated via the Antigravity SDK.

## Open questions
- None. All major assumptions from the Grill stage have been folded into the Scope and Acceptance Criteria.
