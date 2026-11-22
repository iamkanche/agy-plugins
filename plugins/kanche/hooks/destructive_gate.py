#!/usr/bin/env python3
"""PreToolUse safety hook enforcing kanche destructive-safety and git-hard-rules."""

from __future__ import annotations

import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

PROTECTED_BRANCHES = {"main", "master", "develop"}
SAFE_RM_PREFIXES = ("/tmp/", "graphify-out/.graphify_")
READ_TOOLS = {"grep", "rg", "echo", "printf", "cat", "head", "tail", "sed", "awk"}


def emit(decision: str, reason: str | None = None) -> int:
    out: dict[str, str] = {"decision": decision}
    if reason:
        out["reason"] = reason
    sys.stdout.write(json.dumps(out))
    return 0


def strip_heredocs(cmd: str) -> str:
    """Drop heredoc bodies so commit messages or markdown content do not trigger command rules."""
    lines = cmd.splitlines()
    if not lines:
        return cmd
    kept: list[str] = []
    terminator: str | None = None
    for line in lines:
        if terminator is not None:
            if line.strip() == terminator:
                terminator = None
            continue
        kept.append(line)
        m = re.search(r"<<-?\s*['\"]?([A-Za-z0-9_]+)['\"]?", line)
        if m:
            terminator = m.group(1)
    return "\n".join(kept)


def split_segments(cmd: str) -> list[list[str]]:
    """Split shell command into token lists per && / || / ; / | / newline segment."""
    segments: list[list[str]] = []
    try:
        lexer = shlex.shlex(cmd, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        tokens = cmd.split()

    cur: list[str] = []
    for tok in tokens:
        if tok in {"&&", "||", ";", "|", "&", "\n"}:
            if cur:
                segments.append(cur)
                cur = []
        else:
            cur.append(tok)
    if cur:
        segments.append(cur)
    return segments


def current_git_branch(repo_dir: str) -> str | None:
    if not repo_dir:
        return None
    for args in (["rev-parse", "--abbrev-ref", "HEAD"], ["symbolic-ref", "--short", "HEAD"]):
        try:
            res = subprocess.run(
                ["git", "-C", repo_dir, *args],
                capture_output=True,
                text=True,
                timeout=2,
                check=True,
            )
            val = res.stdout.strip()
            if val and val != "HEAD":
                return val
        except (subprocess.SubprocessError, OSError):
            continue
    return None


def parse_git_command(tokens: list[str], cwd: str) -> tuple[str | None, list[str], str]:
    """Extract (subcommand, args, effective_repo_dir) from a git invocation."""
    repo_dir = cwd
    i = 1
    while i < len(tokens):
        t = tokens[i]
        if t == "-C" and i + 1 < len(tokens):
            p = Path(tokens[i + 1])
            repo_dir = str(p if p.is_absolute() else Path(cwd) / p) if cwd else str(p)
            i += 2
        elif t.startswith("-C") and len(t) > 2:
            p = Path(t[2:])
            repo_dir = str(p if p.is_absolute() else Path(cwd) / p) if cwd else str(p)
            i += 1
        elif t in {"-c", "--git-dir", "--work-tree"} and i + 1 < len(tokens):
            i += 2
        elif t.startswith("-"):
            i += 1
        else:
            return t, tokens[i + 1 :], repo_dir
    return None, [], repo_dir


def is_safe_rm_target(target: str) -> bool:
    if ".." in Path(target).parts:
        return False
    return any(target.startswith(prefix) for prefix in SAFE_RM_PREFIXES)


def evaluate_command(cmd: str, cwd: str) -> tuple[str, str | None]:
    stripped = strip_heredocs(cmd)
    segments = split_segments(stripped)

    # Track worst decision: deny > force_ask > allow
    ask_reasons: list[str] = []

    for tokens in segments:
        if not tokens:
            continue
        prog = Path(tokens[0]).name

        # Skip read/search utilities unless they shouldn't matter
        if prog in READ_TOOLS:
            continue

        joined = " ".join(tokens)

        # DB / Schema destructive patterns
        if re.search(r"\bmigrate:(fresh|reset)\b", joined, re.IGNORECASE):
            return "deny", "Blocked destructive database reset (migrate:fresh / migrate:reset) per destructive-safety.md."
        if re.search(r"\bdrop\s+(database|table)\b", joined, re.IGNORECASE):
            return "deny", "Blocked destructive SQL DROP DATABASE/TABLE command per destructive-safety.md."

        # Git rules
        if prog == "git":
            sub, args, repo_dir = parse_git_command(tokens, cwd)
            if sub == "push":
                if "--force" in args or "--force-with-lease" in args or "-f" in args:
                    return "deny", "Blocked force push (--force / -f / --force-with-lease) per git-hard-rules.md."
                if "--no-verify" in args:
                    return "deny", "Blocked git push --no-verify per git-hard-rules.md."
                branch = current_git_branch(repo_dir)
                if branch in PROTECTED_BRANCHES and "--delete" not in args and not any(a.startswith(":") for a in args):
                    return "deny", f"Blocked direct git push on protected branch '{branch}' per git-hard-rules.md."
                ask_reasons.append("git push requires explicit human confirmation.")
            elif sub == "commit":
                if "--no-verify" in args:
                    return "deny", "Blocked git commit --no-verify per git-hard-rules.md."
                branch = current_git_branch(repo_dir)
                if branch in PROTECTED_BRANCHES:
                    return "deny", f"Blocked direct git commit on protected branch '{branch}' per git-hard-rules.md."
                ask_reasons.append("git commit requires explicit human confirmation.")
            elif sub == "reset" and "--hard" in args:
                return "deny", "Blocked git reset --hard per git-hard-rules.md."
            elif sub == "stash" and args:
                if args[0] == "clear":
                    return "deny", "Blocked git stash clear (bulk discard) per git-stash skill."
                if args[0] == "drop":
                    ask_reasons.append("git stash drop requires explicit human confirmation.")
            elif sub == "rebase":
                if "--abort" not in args and "--continue" not in args and "--skip" not in args:
                    ask_reasons.append("git rebase rewrites history and requires explicit human confirmation.")
            elif sub == "branch" and ("-d" in args or "-D" in args):
                ask_reasons.append("git branch deletion requires explicit human confirmation.")
            elif sub == "tag" and ("-d" in args or "--delete" in args):
                ask_reasons.append("git tag deletion requires explicit human confirmation.")

        # GitHub CLI rules
        elif prog == "gh" and len(tokens) >= 3 and tokens[1] == "pr" and tokens[2] == "merge":
            ask_reasons.append("gh pr merge requires explicit human confirmation.")

        # Recursive rm rules
        elif prog == "rm":
            flags = [t for t in tokens[1:] if t.startswith("-") and t != "--"]
            targets = [t for t in tokens[1:] if not t.startswith("-")]
            has_r = any("r" in f.lower() or f == "--recursive" for f in flags)
            has_f = any("f" in f.lower() or f == "--force" for f in flags)
            if has_r and (has_f or "--recursive" in flags):
                if not targets or not all(is_safe_rm_target(t) for t in targets):
                    ask_reasons.append("Recursive rm outside /tmp/ or graphify-out/.graphify_* requires explicit human confirmation.")

    if ask_reasons:
        return "force_ask", " ".join(dict.fromkeys(ask_reasons))
    return "allow", None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return emit("allow")

    args = payload.get("toolCall", {}).get("args", {})
    cmd = args.get("CommandLine") or args.get("command") or ""
    cwd = payload.get("cwd") or ""
    if not cmd:
        return emit("allow")

    decision, reason = evaluate_command(cmd, cwd)
    return emit(decision, reason)


if __name__ == "__main__":
    sys.exit(main())
