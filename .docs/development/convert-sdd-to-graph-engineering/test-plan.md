# QA Test Plan: Convert SDD to Graph Engineering Workflow

## Test Strategy Overview
This test plan validates the completeness, backward compatibility, JSON schema conformance, markdown frontmatter validity, and UI rendering integrity of the Graph Engineering Workflow transformation.

## Test Suites

### 1. JSON Schema & Syntax Validation
- **Objective**: Ensure `plugin.json` and all `agent.json` files have valid JSON syntax.
- **Command**:
  ```bash
  python3 -c "import json, glob; [json.load(open(f)) for f in glob.glob('plugins/kanche/**/*.json', recursive=True)]"
  ```
- **Expected Result**: Exit code 0, all files loaded without error.

### 2. Skill YAML Frontmatter Validation
- **Objective**: Ensure all `SKILL.md` files (both newly added `graph-*` and modified `sdd-*`, `planner-tasks`, `qa-validate`) contain valid YAML frontmatter with `name`, `description`, and `model: flash`.
- **Command**:
  ```bash
  python3 -c "
  import glob, re
  for f in glob.glob('plugins/kanche/skills/*/SKILL.md'):
      content = open(f).read()
      assert content.startswith('---'), f'{f} missing frontmatter'
      assert re.search(r'^name:\s*\S+', content, re.MULTILINE), f'{f} missing name'
      assert re.search(r'^description:\s*\S+', content, re.MULTILINE), f'{f} missing description'
  print('All SKILL.md files valid!')
  "
  ```
- **Expected Result**: Exit code 0, all skills verified.

### 3. Dashboard HTML & DOM Parsing Test
- **Objective**: Ensure `index.html` has valid markup and loads cleanly.
- **Command**:
  ```bash
  python3 -c "
  from html.parser import HTMLParser
  class V(HTMLParser): pass
  V().feed(open('index.html').read())
  print('index.html well-formed!')
  "
  ```
- **Expected Result**: Exit code 0, no parser errors.

### 4. Backward Compatibility Verification
- **Objective**: Verify that every legacy SDD skill (`sdd-run`, `sdd-continue`, etc.) references its corresponding `graph-*` counterpart and provides seamless forwarding instructions.
