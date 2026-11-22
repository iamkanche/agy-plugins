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
        m = re.search(r"(?<!<)<<-?(?!<)\s*['\"]?([A-Za-z0-9_]+)['\"]?", line)
        if m:
            terminator = m.group(1)
    return "\n".join(kept)


def split_segments(cmd: str) -> list[list[str]]:
    """Split shell command into token lists per && / || / ; / | / newline segment."""
    segments: list[list[str]] = []
    for raw_line in cmd.splitlines():
        if not raw_line.strip():
            continue
        try:
            lexer = shlex.shlex(raw_line, posix=True, punctuation_chars=";&|")
            lexer.whitespace_split = True
            tokens = list(lexer)
        except ValueError:
            tokens = raw_line.split()

        cur: list[str] = []
        for tok in tokens:
            if tok in {"&&", "||", ";", "|", "&"}:
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
    if ".." in Path(target).parts or "*" in target or "?" in target:
        return False
    if target.rstrip("/") == "/tmp":
        return False
    return any(target.startswith(prefix) and len(target) > len(prefix) for prefix in SAFE_RM_PREFIXES)


def unwrap_command_tokens(raw_tokens: list[str]) -> list[str]:
    """Strip leading VAR=val assignments and wrapper commands (env, sudo, command, nohup, exec, timeout)."""
    tokens = list(raw_tokens)
    while tokens:
        head = tokens[0]
        name = Path(head).name
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", head):
            tokens.pop(0)
            continue
        if name in {"env", "sudo", "command", "nohup", "exec"}:
            tokens.pop(0)
            while tokens and tokens[0].startswith("-") and tokens[0] != "--":
                flag = tokens.pop(0)
                if name in {"env", "sudo"} and flag in {"-u", "--unset", "-C", "-g"} and tokens:
                    tokens.pop(0)
            continue
        if name == "timeout":
            tokens.pop(0)
            while tokens and tokens[0].startswith("-") and tokens[0] != "--":
                flag = tokens.pop(0)
                if flag in {"-k", "-s", "--kill-after", "--signal"} and tokens:
                    tokens.pop(0)
            if tokens:
                tokens.pop(0)  # duration argument
            continue
        break
    return tokens


def evaluate_command(cmd: str, cwd: str) -> tuple[str, str | None]:
    stripped = strip_heredocs(cmd)
    segments = split_segments(stripped)

    # Track worst decision: deny > force_ask > allow
    ask_reasons: list[str] = []

    for raw_tokens in segments:
        tokens = unwrap_command_tokens(raw_tokens)
        if not tokens:
            continue
        prog = Path(tokens[0]).name

        # Skip read/search utilities unless they shouldn't matter
        if prog in READ_TOOLS:
            continue

        # Inspect nested shell invocations like `bash -c "git reset --hard"`
        if prog in {"bash", "sh", "zsh"}:
            for idx, arg in enumerate(tokens[1:], start=1):
                is_c = arg == "-c" or (arg.startswith("-") and not arg.startswith("--") and "c" in arg[1:])
                if is_c and idx + 1 < len(tokens):
                    nested_dec, nested_reason = evaluate_command(tokens[idx + 1], cwd)
                    if nested_dec == "deny":
                        return "deny", nested_reason
                    if nested_dec == "force_ask" and nested_reason:
                        ask_reasons.append(nested_reason)
                    break

        joined = " ".join(tokens)

        # DB / Schema destructive patterns
        if re.search(r"\bmigrate:(fresh|reset)\b", joined, re.IGNORECASE):
            return "deny", "Blocked destructive database reset (migrate:fresh / migrate:reset) per destructive-safety.md."
        if re.search(r"\bdrop\s+(database|table)\b", joined, re.IGNORECASE):
            return "deny", "Blocked destructive SQL DROP DATABASE/TABLE command per destructive-safety.md."

        # Git rules
        if prog == "git":
            sub, args, repo_dir = parse_git_command(tokens, cwd)
            short_flags = [a[1:] for a in args if a.startswith("-") and not a.startswith("--") and a != "-"]
            if sub == "push":
                pos_args = [a for a in args if not a.startswith("-")]
                is_force = (
                    "--force" in args
                    or any(a == "--force-with-lease" or a.startswith("--force-with-lease=") for a in args)
                    or any("f" in sf for sf in short_flags)
                    or any(a.startswith("+") for a in pos_args[1:])
                )
                if is_force:
                    return "deny", "Blocked force push (--force / -f / --force-with-lease / +refspec) per git-hard-rules.md."
                if "--no-verify" in args:
                    return "deny", "Blocked git push --no-verify per git-hard-rules.md."
                branch = current_git_branch(repo_dir)
                targets_protected = any(
                    a.lstrip("+").split(":")[-1].removeprefix("refs/heads/") in PROTECTED_BRANCHES
                    for a in pos_args[1:]
                )
                is_delete = "--delete" in args or "-d" in args or any(a.startswith(":") for a in pos_args[1:])
                if targets_protected or (branch in PROTECTED_BRANCHES and not is_delete):
                    return "deny", "Blocked direct push or remote deletion on protected branch per git-hard-rules.md."
                ask_reasons.append("git push requires explicit human confirmation.")
            elif sub == "commit":
                if "--no-verify" in args or any("n" in sf for sf in short_flags):
                    return "deny", "Blocked git commit --no-verify (-n) per git-hard-rules.md."
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
            short_flags = [t[1:] for t in tokens[1:] if t.startswith("-") and not t.startswith("--") and t != "-"]
            long_flags = [t for t in tokens[1:] if t.startswith("--")]
            targets = [t for t in tokens[1:] if not t.startswith("-")]
            has_r = any("r" in sf.lower() for sf in short_flags) or "--recursive" in long_flags
            if has_r:
                if not targets or not all(is_safe_rm_target(t) for t in targets):
                    ask_reasons.append("Recursive rm outside /tmp/<subpath> or graphify-out/.graphify_* requires explicit human confirmation.")

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
