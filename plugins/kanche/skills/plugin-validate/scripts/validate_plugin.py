#!/usr/bin/env python3
"""Antigravity 2.0 plugin schema, frontmatter, hooks, rules, agents, skills, and catalog validator."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ALLOWED_PLUGIN_KEYS = {
    "name",
    "displayName",
    "version",
    "description",
    "logo",
    "suggestedPrompts",
    "author",
    "homepage",
    "repository",
    "disabled",
}

VALID_NATIVE_TOOLS = {
    "read_file",
    "edit_file",
    "write_file",
    "run_command",
    "manage_task",
    "search_web",
    "call_mcp_tool",
    "list_resources",
    "read_resource",
    "ask_question",
    "invoke_subagent",
    "send_message",
}

VALID_TRIGGERS = {"always_on", "model_decision", "glob", "manual"}


def parse_frontmatter(text: str) -> tuple[dict[str, object], bool]:
    """Parse simple YAML frontmatter key/value pairs without external deps."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, False
    end_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break
    if end_idx is None:
        return {}, False

    data: dict[str, object] = {}
    for line in lines[1:end_idx]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k = k.strip()
        v = v.strip()
        if v.startswith("[") and v.endswith("]"):
            items = [x.strip().strip("'\"") for x in v[1:-1].split(",") if x.strip()]
            data[k] = items
        elif v.lower() == "true":
            data[k] = True
        elif v.lower() == "false":
            data[k] = False
        else:
            data[k] = v.strip("'\"")
    return data, True


def validate(repo_root: Path) -> tuple[list[str], list[str], dict[str, int]]:
    errors: list[str] = []
    warnings: list[str] = []

    plugin_dir = repo_root / "plugins" / "kanche" if (repo_root / "plugins" / "kanche" / "plugin.json").is_file() else repo_root
    if not (plugin_dir / "plugin.json").is_file():
        return [f"plugin.json not found under {plugin_dir}"], warnings, {}

    # 1. plugin.json
    try:
        manifest = json.loads((plugin_dir / "plugin.json").read_text(encoding="utf-8"))
        unknown = sorted(set(manifest.keys()) - ALLOWED_PLUGIN_KEYS)
        if unknown:
            errors.append(f"plugin.json: unsupported top-level keys {unknown}")
        if not manifest.get("name"):
            errors.append("plugin.json: missing 'name'")
        if not manifest.get("description"):
            errors.append("plugin.json: missing 'description'")
        logo = manifest.get("logo")
        if logo and not (plugin_dir / logo).is_file():
            errors.append(f"plugin.json: logo path missing: {logo}")
        prompts = manifest.get("suggestedPrompts", [])
        if isinstance(prompts, list) and len(prompts) > 3:
            warnings.append(f"plugin.json: suggestedPrompts has {len(prompts)} entries (>3 ignored by UI)")
    except Exception as exc:
        errors.append(f"plugin.json: invalid JSON ({exc})")

    # 2. hooks.json
    hooks_path = plugin_dir / "hooks.json"
    if hooks_path.is_file():
        try:
            hooks_data = json.loads(hooks_path.read_text(encoding="utf-8"))
            for hook_name, spec in hooks_data.items():
                if not isinstance(spec, dict):
                    errors.append(f"hooks.json: hook '{hook_name}' must be an object")
                    continue
                for ev in ("PreToolUse", "PostToolUse", "SessionStart", "PreInvocation", "PostInvocation", "Stop"):
                    for entry in spec.get(ev, []):
                        handlers = entry.get("hooks", [entry]) if ev in ("PreToolUse", "PostToolUse") else [entry]
                        for h in handlers:
                            cmd = h.get("command", "")
                            for rel_match in re.findall(r"\./[A-Za-z0-9_./-]+", cmd):
                                target_script = plugin_dir / rel_match[2:]
                                if not target_script.is_file():
                                    errors.append(f"hooks.json ({hook_name}): missing script {rel_match}")
        except Exception as exc:
            errors.append(f"hooks.json: invalid JSON ({exc})")
    else:
        warnings.append("hooks.json: not present")

    # 3. agents/*.md
    agents_dir = plugin_dir / "agents"
    agent_files = sorted(agents_dir.glob("*.md")) if agents_dir.is_dir() else []
    agent_names: set[str] = set()
    for af in agent_files:
        fm, has_fm = parse_frontmatter(af.read_text(encoding="utf-8"))
        if not has_fm:
            errors.append(f"agents/{af.name}: missing YAML frontmatter")
            continue
        if fm.get("name") != af.stem:
            errors.append(f"agents/{af.name}: frontmatter name '{fm.get('name')}' != '{af.stem}'")
        if not fm.get("description"):
            errors.append(f"agents/{af.name}: missing description")
        if fm.get("subagent") is not True or fm.get("mainAgent") is not False:
            errors.append(f"agents/{af.name}: must set subagent: true and mainAgent: false")
        tools = fm.get("tools")
        if not isinstance(tools, list) or not tools:
            errors.append(f"agents/{af.name}: missing or empty tools list")
        else:
            invalid_tools = [t for t in tools if t not in VALID_NATIVE_TOOLS]
            if invalid_tools:
                errors.append(f"agents/{af.name}: invalid tool name(s) {invalid_tools}")
        agent_names.add(af.stem)

    legacy_agent_jsons = sorted(agents_dir.glob("*/agent.json")) if agents_dir.is_dir() else []
    if legacy_agent_jsons:
        warnings.append(f"agents/: {len(legacy_agent_jsons)} legacy agent.json file(s) still present")

    # 4. rules/*.md
    rules_dir = plugin_dir / "rules"
    rule_files = sorted(rules_dir.glob("*.md")) if rules_dir.is_dir() else []
    for rf in rule_files:
        raw = rf.read_text(encoding="utf-8")
        byte_len = len(raw.encode("utf-8"))
        if byte_len > 24000:
            errors.append(f"rules/{rf.name}: exceeds 24,000 byte cap ({byte_len} bytes)")
        fm, has_fm = parse_frontmatter(raw)
        if rf.name in ("AGENTS.md", "GEMINI.md"):
            if has_fm:
                errors.append(f"rules/{rf.name}: must NOT contain frontmatter")
        else:
            if not has_fm or fm.get("trigger") not in VALID_TRIGGERS:
                errors.append(f"rules/{rf.name}: missing or invalid trigger frontmatter ({fm.get('trigger')})")
            if fm.get("trigger") == "model_decision" and not fm.get("description"):
                errors.append(f"rules/{rf.name}: trigger=model_decision requires description")

    # 5. skills/*/SKILL.md
    skills_dir = plugin_dir / "skills"
    skill_files = sorted(skills_dir.glob("*/SKILL.md")) if skills_dir.is_dir() else []
    skill_names: set[str] = set()
    for sf in skill_files:
        sdir = sf.parent.name
        raw = sf.read_text(encoding="utf-8")
        fm, has_fm = parse_frontmatter(raw)
        if not has_fm:
            errors.append(f"skills/{sdir}/SKILL.md: missing YAML frontmatter")
            continue
        if fm.get("name") != sdir:
            errors.append(f"skills/{sdir}/SKILL.md: name '{fm.get('name')}' != directory '{sdir}'")
        if not fm.get("description"):
            errors.append(f"skills/{sdir}/SKILL.md: missing description")
        if "model" in fm:
            errors.append(f"skills/{sdir}/SKILL.md: non-standard 'model:' key in frontmatter")
        if "{NNN}_{slug}" in raw and sdir != "plugin-validate":
            errors.append(f"skills/{sdir}/SKILL.md: contains legacy '{{NNN}}_{{slug}}' path")
        if "/git:" in raw and sdir != "plugin-validate":
            errors.append(f"skills/{sdir}/SKILL.md: contains legacy '/git:' command reference")
        if "agent.json" in raw and sdir != "plugin-validate":
            errors.append(f"skills/{sdir}/SKILL.md: contains stale 'agent.json' reference")
        skill_names.add(sdir)

    # 6. index.html parity (when checking repo root)
    index_path = repo_root / "index.html"
    if index_path.is_file():
        html = index_path.read_text(encoding="utf-8")
        if "@laravel-expert" in html:
            errors.append("index.html: contains legacy '@laravel-expert' reference")
        if "agent.json" in html:
            errors.append("index.html: contains stale 'agent.json' reference")

        kanche_skills_in_html = set(re.findall(r'name:\s*"/kanche:([a-z0-9-]+)"', html))
        missing_in_html = sorted(skill_names - kanche_skills_in_html)
        extra_in_html = sorted(kanche_skills_in_html - skill_names)
        if missing_in_html:
            errors.append(f"index.html: missing skills from catalog: {missing_in_html}")
        if extra_in_html:
            errors.append(f"index.html: unknown skills in catalog: {extra_in_html}")

        agents_block_match = re.search(r"const agentsData = \[(.*?)\];", html, re.DOTALL)
        if agents_block_match:
            html_agents = set(re.findall(r'name:\s*"([a-z0-9-]+)"', agents_block_match.group(1)))
            missing_agents = sorted(agent_names - html_agents)
            extra_agents = sorted(html_agents - agent_names)
            if missing_agents:
                errors.append(f"index.html: missing agents from agentsData: {missing_agents}")
            if extra_agents:
                errors.append(f"index.html: unknown agents in agentsData: {extra_agents}")
        else:
            errors.append("index.html: could not locate agentsData array")

    stats = {
        "agents": len(agent_files),
        "rules": len(rule_files),
        "skills": len(skill_files),
    }
    return errors, warnings, stats


def main() -> int:
    target = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    errors, warnings, stats = validate(target)

    print("=== Kanche Plugin Validation Report ===")
    print(f"Target: {target}")
    if stats:
        print(f"Inventory: {stats['agents']} agents, {stats['rules']} rules, {stats['skills']} skills")
    print(f"Errors: {len(errors)} | Warnings: {len(warnings)}")

    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"  - [WARN] {w}")
    if errors:
        print("\nErrors:")
        for e in errors:
            print(f"  - [ERROR] {e}")
        return 1

    print("\nPlugin Validation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
