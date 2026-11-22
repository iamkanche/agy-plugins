#!/usr/bin/env python3
"""Native stdlib AST, relative-import, JSON, and Graphify health check gate."""

from __future__ import annotations

import ast
import json
import os
import re
import subprocess
import sys
from pathlib import Path

JS_TS_EXTS = (".ts", ".tsx", ".mts", ".cts", ".js", ".jsx", ".mjs", ".cjs")
RESOLVE_EXTS = (".ts", ".tsx", ".d.ts", ".mts", ".cts", ".js", ".jsx", ".mjs", ".cjs", ".json", ".py", "")
SKIP_DIRS = {".git", "node_modules", "vendor", "dist", "build", ".venv", "__pycache__"}

JS_COMMENT_OR_STR_RE = re.compile(
    r"('(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\"|`(?:\\.|[^`\\])*`)"
    r"|(/\*[\s\S]*?\*/|//[^\n]*)"
)

JSONC_TRAILING_COMMA_RE = re.compile(r'("(?:\\.|[^"\\])*")|,(\s*[}\]])')

JS_IMPORT_OR_STR_RE = re.compile(
    r"""(?:^|[\s;{}()=,:?!])(?:import|export)\s*(?:[^'"`;]*?\s+from\s+)?['"]([^'"]+)['"]"""
    r"""|(?<![.\w$])(?:require|import)\s*\(\s*['"]([^'"]+)['"]\s*\)"""
    r"""|'(?:\\.|[^'\\])*'|"(?:\\.|[^"\\])*"|`(?:\\.|[^`\\])*`""",
    re.MULTILINE,
)


def strip_js_comments(src: str) -> str:
    """Remove JS/TS comments while preserving quoted strings and line numbers."""
    def _repl(m: re.Match[str]) -> str:
        if m.group(1) is not None:
            return m.group(1)
        newlines = m.group(2).count("\n")
        return "\n" * newlines if newlines else " "

    return JS_COMMENT_OR_STR_RE.sub(_repl, src)


def is_jsonc_file(path: Path) -> bool:
    """Return True for config files that allow JSON with Comments / trailing commas."""
    name = path.name.lower()
    if name.endswith(".jsonc"):
        return True
    if name.startswith(("tsconfig", "jsconfig")) and name.endswith(".json"):
        return True
    return ".vscode" in {p.lower() for p in path.parts} and name.endswith(".json")


def strip_jsonc(src: str) -> str:
    """Strip JSONC comments and trailing commas while preserving strings."""
    no_comments = strip_js_comments(src)
    return JSONC_TRAILING_COMMA_RE.sub(lambda m: m.group(1) if m.group(1) is not None else m.group(2), no_comments)


def list_repo_files(root: Path) -> list[Path]:
    """Enumerate tracked and non-ignored untracked files via git ls-files -z with os.walk fallback."""
    try:
        res = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
        paths = [root / entry for entry in res.stdout.split("\0") if entry]
        return [p for p in paths if p.is_file()]
    except (subprocess.SubprocessError, OSError):
        found: list[Path] = []
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for name in filenames:
                found.append(Path(dirpath) / name)
        return sorted(found)


def resolve_relative_module(source_file: Path, spec: str, root: Path) -> Path | None:
    """Resolve a relative module specifier against existing files under root."""
    clean_spec = spec.split("?", 1)[0].split("#", 1)[0]
    if not clean_spec:
        return None
    base = (source_file.parent / clean_spec).resolve()
    try:
        base.relative_to(root.resolve())
    except ValueError:
        return None
    if base.is_file():
        return base
    ext_fallbacks = {
        ".js": (".ts", ".tsx", ".d.ts", ".js"),
        ".jsx": (".tsx", ".jsx"),
        ".mjs": (".mts", ".d.mts", ".mjs"),
        ".cjs": (".cts", ".d.cts", ".cjs"),
    }
    if base.suffix in ext_fallbacks:
        for cand_ext in ext_fallbacks[base.suffix]:
            cand = base.parent / f"{base.stem}{cand_ext}"
            if cand.is_file():
                return cand
    for ext in RESOLVE_EXTS:
        if ext and Path(f"{base}{ext}").is_file():
            return Path(f"{base}{ext}")
    if base.is_dir():
        for idx_ext in (".ts", ".tsx", ".d.ts", ".mts", ".cts", ".js", ".jsx", ".mjs", ".cjs", ".py"):
            idx = base / f"index{idx_ext}"
            if idx.is_file():
                return idx
        init_py = base / "__init__.py"
        if init_py.is_file():
            return init_py
    return None


def _collect_assign_names(target: ast.AST, names: set[str]) -> None:
    if isinstance(target, ast.Name):
        names.add(target.id)
    elif isinstance(target, (ast.Tuple, ast.List)):
        for elt in target.elts:
            _collect_assign_names(elt, names)


def init_exports_name(init_file: Path, name: str, cache: dict[Path, set[str] | None]) -> bool:
    """Check whether __init__.py defines, imports, or dynamically exports `name` at module scope."""
    if init_file not in cache:
        try:
            tree = ast.parse(init_file.read_text(encoding="utf-8"), filename=str(init_file))
        except (SyntaxError, OSError):
            cache[init_file] = None
            return True
        names: set[str] = set()
        dynamic = False

        def _collect(stmts: list[ast.stmt]) -> None:
            nonlocal dynamic
            for node in stmts:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    if node.name == "__getattr__":
                        dynamic = True
                        return
                    names.add(node.name)
                elif isinstance(node, ast.Assign):
                    for tgt in node.targets:
                        _collect_assign_names(tgt, names)
                elif isinstance(node, ast.AnnAssign):
                    _collect_assign_names(node.target, names)
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    for alias in node.names:
                        if alias.name == "*":
                            dynamic = True
                            return
                        names.add(alias.asname or alias.name.split(".")[0])
                elif isinstance(node, ast.If):
                    _collect(node.body)
                    _collect(node.orelse)
                elif isinstance(node, (ast.With, ast.AsyncWith)):
                    _collect(node.body)
                elif hasattr(ast, "TryStar") and isinstance(node, ast.TryStar):  # Python 3.11+
                    _collect(node.body)
                    _collect(node.orelse)
                    _collect(node.finalbody)
                    for h in node.handlers:
                        _collect(h.body)
                elif isinstance(node, ast.Try):
                    _collect(node.body)
                    _collect(node.orelse)
                    _collect(node.finalbody)
                    for h in node.handlers:
                        _collect(h.body)

        _collect(tree.body)
        cache[init_file] = None if dynamic else names
    exported = cache[init_file]
    return exported is None or name in exported


def resolve_python_relative(source_file: Path, level: int, module: str | None, root: Path) -> Path | None:
    """Resolve a Python relative import (`from .foo import bar`)."""
    pkg_dir = source_file.parent
    for _ in range(max(0, level - 1)):
        pkg_dir = pkg_dir.parent
    target = pkg_dir / module.replace(".", "/") if module else pkg_dir
    for candidate in (Path(f"{target}.py"), target / "__init__.py"):
        if candidate.is_file():
            try:
                candidate.resolve().relative_to(root.resolve())
                return candidate.resolve()
            except ValueError:
                return None
    return None


def check_graphify_extraction(root: Path) -> tuple[list[str], str]:
    """Audit graphify-out/.graphify_extract.json if present."""
    extract_path = root / "graphify-out" / ".graphify_extract.json"
    if not extract_path.is_file():
        return [], "not present (skipped)"

    try:
        from graphify.diagnostics import diagnose_extraction  # type: ignore

        extraction = json.loads(extract_path.read_text(encoding="utf-8"))
        summary = diagnose_extraction(extraction, directed=False, root=str(root))
        issues = []
        for key, label in (
            ("dangling_endpoint_edges", "dangling-endpoint edges"),
            ("missing_endpoint_edges", "missing-endpoint edges"),
            ("self_loop_edges", "self-loop edges"),
        ):
            count = summary.get(key, 0)
            if count:
                issues.append(f"{extract_path}: {count} {label}")
        return issues, "checked via graphify.diagnostics"
    except Exception:
        try:
            data = json.loads(extract_path.read_text(encoding="utf-8"))
            node_ids = {n.get("id") for n in data.get("nodes", []) if isinstance(n, dict)}
            issues = []
            for idx, edge in enumerate(data.get("edges", [])):
                src, dst = edge.get("source"), edge.get("target")
                if not src or not dst:
                    issues.append(f"{extract_path}: edge[{idx}] missing endpoint")
                elif src == dst:
                    issues.append(f"{extract_path}: edge[{idx}] self-loop on {src}")
                elif src not in node_ids or dst not in node_ids:
                    issues.append(f"{extract_path}: edge[{idx}] dangling endpoint ({src} -> {dst})")
            return issues, "checked via JSON fallback"
        except Exception as exc:
            return [f"{extract_path}: failed to parse extraction JSON ({exc})"], "error"


def find_cycles(graph: dict[Path, set[Path]], root: Path) -> list[str]:
    """Detect directed cycles using 3-color DFS."""
    state: dict[Path, int] = {}
    stack: list[Path] = []
    cycles: list[str] = []
    seen_cycles: set[tuple[str, ...]] = set()
    resolved_root = root.resolve()

    def _rel_label(p: Path) -> str:
        try:
            return str(p.relative_to(resolved_root))
        except ValueError:
            return str(p)

    def dfs(node: Path) -> None:
        state[node] = 1
        stack.append(node)
        for nxt in sorted(graph.get(node, ())):
            st = state.get(nxt, 0)
            if st == 0:
                dfs(nxt)
            elif st == 1 and nxt in stack:
                idx = stack.index(nxt)
                cyc = [_rel_label(p) for p in stack[idx:]] + [_rel_label(nxt)]
                norm = tuple(sorted(cyc[:-1]))
                if norm not in seen_cycles:
                    seen_cycles.add(norm)
                    cycles.append(" -> ".join(cyc))
        stack.pop()
        state[node] = 2

    for node in sorted(graph):
        if state.get(node, 0) == 0:
            dfs(node)
    return cycles


def main() -> int:
    target = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    if not target.is_dir():
        print(f"Graph Health: FAIL — target directory not found: {target}")
        return 1

    files = list_repo_files(target)
    syntax_errors: list[str] = []
    dangling_imports: list[str] = []
    dep_graph: dict[Path, set[Path]] = {}
    init_export_cache: dict[Path, set[str] | None] = {}

    for path in files:
        rel = path.relative_to(target)
        suffix = path.suffix.lower()

        if suffix in {".json", ".jsonc"}:
            try:
                raw_json = path.read_text(encoding="utf-8")
                parsed_src = strip_jsonc(raw_json) if is_jsonc_file(path) else raw_json
                json.loads(parsed_src)
            except Exception as exc:
                syntax_errors.append(f"{rel}:1 invalid JSON ({exc})")
            continue

        if suffix == ".py":
            try:
                src = path.read_text(encoding="utf-8")
                tree = ast.parse(src, filename=str(rel))
            except SyntaxError as exc:
                syntax_errors.append(f"{rel}:{exc.lineno or 1} Python SyntaxError: {exc.msg}")
                continue
            except OSError as exc:
                syntax_errors.append(f"{rel}:1 read error: {exc}")
                continue

            resolved_src = path.resolve()
            dep_graph.setdefault(resolved_src, set())
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.level > 0:
                    if node.module:
                        target_mod = resolve_python_relative(path, node.level, node.module, target)
                        if target_mod is None:
                            mod_label = "." * node.level + node.module
                            dangling_imports.append(f"{rel}:{node.lineno} dangling Python relative import '{mod_label}'")
                        else:
                            dep_graph[resolved_src].add(target_mod)
                    else:
                        for alias in node.names:
                            if alias.name == "*":
                                target_mod = resolve_python_relative(path, node.level, None, target)
                            else:
                                target_mod = resolve_python_relative(path, node.level, alias.name, target)
                                if target_mod is None:
                                    init_mod = resolve_python_relative(path, node.level, None, target)
                                    if init_mod is not None and init_exports_name(init_mod, alias.name, init_export_cache):
                                        target_mod = init_mod
                            if target_mod is None:
                                mod_label = "." * node.level + alias.name
                                dangling_imports.append(f"{rel}:{node.lineno} dangling Python relative import '{mod_label}'")
                            else:
                                dep_graph[resolved_src].add(target_mod)
            continue

        if suffix in JS_TS_EXTS:
            try:
                src = path.read_text(encoding="utf-8")
            except OSError as exc:
                syntax_errors.append(f"{rel}:1 read error: {exc}")
                continue

            cleaned_src = strip_js_comments(src)
            resolved_src = path.resolve()
            dep_graph.setdefault(resolved_src, set())
            for match in JS_IMPORT_OR_STR_RE.finditer(cleaned_src):
                spec = match.group(1) or match.group(2)
                if not spec or not spec.startswith("."):
                    continue
                start_pos = match.start(1) if match.group(1) is not None else match.start(2)
                lineno = cleaned_src[:start_pos].count("\n") + 1
                target_mod = resolve_relative_module(path, spec, target)
                if target_mod is None:
                    dangling_imports.append(f"{rel}:{lineno} dangling JS/TS import '{spec}'")
                else:
                    dep_graph[resolved_src].add(target_mod)

    cycles = find_cycles(dep_graph, target)
    graphify_issues, graphify_status = check_graphify_extraction(target)
    total_blockers = len(syntax_errors) + len(dangling_imports) + len(cycles) + len(graphify_issues)

    print("=== Kanche Graph Health Diagnostics ===")
    print(f"Target: {target}")
    print(f"Files scanned: {len(files)}")
    print(f"Syntax errors: {len(syntax_errors)}")
    print(f"Dangling relative imports: {len(dangling_imports)}")
    print(f"Circular dependencies: {len(cycles)}")
    print(f"Graphify extraction: {graphify_status} ({len(graphify_issues)} issues)")

    for label, items in (
        ("Syntax Errors", syntax_errors),
        ("Dangling Imports", dangling_imports),
        ("Circular Dependencies", cycles),
        ("Graphify Issues", graphify_issues),
    ):
        if items:
            print(f"\n{label}:")
            for item in items:
                print(f"  - {item}")

    if total_blockers == 0:
        print("\nGraph Health: OK (0 syntax errors, 0 dangling edges, 0 circular dependencies)")
        return 0
    print(f"\nGraph Health: FAIL ({total_blockers} blocker(s) detected)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
