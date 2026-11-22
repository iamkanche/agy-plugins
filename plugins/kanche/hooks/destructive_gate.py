#!/usr/bin/env python3
"""PreToolUse safety hook enforcing kanche destructive-safety and git-hard-rules."""

from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

PROTECTED_BRANCHES = {"main", "master", "develop"}
SAFE_RM_PREFIXES = ("/tmp/", "graphify-out/.graphify_")
READ_TOOLS = {"grep", "rg", "echo", "printf", "cat", "head", "tail", "sed", "awk"}
SHELL_PREFIX_TOKENS = {"{", "}", "!", "then", "do", "else", "time"}
HEREDOC_OP_RE = re.compile(r"^-?\s*(?:'([A-Za-z0-9_]+)'|\"([A-Za-z0-9_]+)\"|\\?([A-Za-z0-9_]+))")
DB_CLI_RUNNERS = {
    "php", "artisan", "sail", "composer",
    "mysql", "mariadb", "psql", "sqlite3", "sqlcmd", "mongosh", "clickhouse-client",
    "prisma", "npx", "bunx", "pnpm", "yarn", "npm",
    "docker", "docker-compose", "podman", "kubectl",
    "rails", "rake", "bundle",
    "alembic", "knex", "sequelize", "typeorm", "drizzle-kit", "django-admin", "manage.py",
}


def _resolve_dir(base: str, target: str) -> str:
    p = Path(target).expanduser()
    if p.is_absolute() or not base:
        return str(p)
    return str(Path(base) / p)


def emit(decision: str, reason: str | None = None) -> int:
    out: dict[str, str] = {"decision": decision}
    if reason:
        out["reason"] = reason
    sys.stdout.write(json.dumps(out))
    return 0


def _find_unquoted_heredoc(line: str) -> str | None:
    """Return heredoc delimiter only when << or <<- appears outside quotes and comments."""
    in_sq = False
    in_dq = False
    escaped = False
    i = 0
    n = len(line)
    while i < n:
        ch = line[i]
        if escaped:
            escaped = False
            i += 1
            continue
        if not in_sq and ch == "\\":
            escaped = True
            i += 1
            continue
        if not in_dq and ch == "'":
            in_sq = not in_sq
            i += 1
            continue
        if not in_sq and ch == '"':
            in_dq = not in_dq
            i += 1
            continue
        if not in_sq and not in_dq:
            if ch == "#" and (i == 0 or line[i - 1].isspace() or line[i - 1] in ";|&("):
                break
            if line.startswith("<<<", i):
                i += 3
                continue
            if line.startswith("<<", i):
                m = HEREDOC_OP_RE.match(line[i + 2 :])
                if m:
                    return m.group(1) or m.group(2) or m.group(3)
                i += 2
                continue
        i += 1
    return None


def strip_heredocs(cmd: str) -> str:
    """Drop unquoted heredoc bodies so commit messages or markdown content do not trigger command rules."""
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
        terminator = _find_unquoted_heredoc(line)
    return "\n".join(kept)


def _scan_paren_sub(cmd: str, start: int) -> tuple[str, int] | None:
    """Extract balanced inner command from $(...) starting after '$('."""
    depth = 1
    sq = False
    dq = False
    esc = False
    j = start
    n = len(cmd)
    while j < n:
        ch = cmd[j]
        if esc:
            esc = False
            j += 1
            continue
        if not sq and ch == "\\":
            esc = True
            j += 1
            continue
        if not dq and ch == "'":
            sq = not sq
            j += 1
            continue
        if not sq and ch == '"':
            dq = not dq
            j += 1
            continue
        if not sq and not dq:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    return cmd[start:j], j + 1
        j += 1
    return None


def extract_command_substitutions(cmd: str) -> list[str]:
    """Extract active $(...) and backtick substitutions outside single-quoted spans."""
    subs: list[str] = []
    in_sq = False
    in_dq = False
    escaped = False
    i = 0
    n = len(cmd)
    while i < n:
        ch = cmd[i]
        if escaped:
            escaped = False
            i += 1
            continue
        if not in_sq and ch == "\\":
            escaped = True
            i += 1
            continue
        if not in_dq and ch == "'":
            in_sq = not in_sq
            i += 1
            continue
        if not in_sq and ch == '"':
            in_dq = not in_dq
            i += 1
            continue
        if in_sq:
            i += 1
            continue
        if not in_dq and ch == "#" and (i == 0 or cmd[i - 1] in " \t\n;|(&"):
            nl = cmd.find("\n", i)
            if nl == -1:
                break
            i = nl + 1
            continue
        if cmd.startswith("$(", i):
            res = _scan_paren_sub(cmd, i + 2)
            if res is not None:
                inner, end = res
                subs.append(inner)
                i = end
                continue
        if ch == "`":
            j = i + 1
            bt_esc = False
            while j < n:
                bc = cmd[j]
                if bt_esc:
                    bt_esc = False
                    j += 1
                    continue
                if bc == "\\":
                    bt_esc = True
                    j += 1
                    continue
                if bc == "`":
                    inner = re.sub(r"\\([`$\\])", r"\1", cmd[i + 1 : j])
                    subs.append(inner)
                    i = j + 1
                    break
                j += 1
            else:
                i += 1
            continue
        i += 1
    return subs


def split_segments(cmd: str) -> list[list[str]]:
    """Split shell command into token lists per && / || / ; / | / ( / ) / newline segment."""
    segments: list[list[str]] = []
    for raw_line in cmd.splitlines():
        if not raw_line.strip():
            continue
        try:
            lexer = shlex.shlex(raw_line, posix=True, punctuation_chars=";&|()")
            lexer.whitespace_split = True
            tokens = list(lexer)
        except ValueError:
            tokens = raw_line.split()

        cur: list[str] = []
        for tok in tokens:
            if tok in {"&&", "||", ";", "|", "&", "(", ")"}:
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
            repo_dir = _resolve_dir(repo_dir, tokens[i + 1])
            i += 2
        elif t.startswith("-C") and len(t) > 2:
            repo_dir = _resolve_dir(repo_dir, t[2:])
            i += 1
        elif t == "--work-tree" and i + 1 < len(tokens):
            repo_dir = _resolve_dir(repo_dir, tokens[i + 1])
            i += 2
        elif t.startswith("--work-tree="):
            repo_dir = _resolve_dir(repo_dir, t.split("=", 1)[1])
            i += 1
        elif t == "--git-dir" and i + 1 < len(tokens):
            gd = Path(_resolve_dir(repo_dir, tokens[i + 1]))
            repo_dir = str(gd.parent if gd.name == ".git" else gd)
            i += 2
        elif t.startswith("--git-dir="):
            gd = Path(_resolve_dir(repo_dir, t.split("=", 1)[1]))
            repo_dir = str(gd.parent if gd.name == ".git" else gd)
            i += 1
        elif t == "-c" and i + 1 < len(tokens):
            i += 2
        elif t.startswith("-"):
            i += 1
        else:
            return t, tokens[i + 1 :], repo_dir
    return None, [], repo_dir


def parse_git_subargs(args: list[str], value_opts: set[str] | None = None) -> tuple[list[str], list[str], list[str]]:
    """Parse git subcommand args into (short_flags, long_flags, pos_args) respecting option values and --."""
    val_opts = value_opts or set()
    short_flags: list[str] = []
    long_flags: list[str] = []
    pos_args: list[str] = []
    i = 0
    while i < len(args):
        tok = args[i]
        if tok == "--":
            pos_args.extend(args[i + 1 :])
            break
        if tok.startswith("--"):
            long_flags.append(tok)
            if "=" not in tok and tok in val_opts and i + 1 < len(args):
                i += 2
                continue
            i += 1
            continue
        if tok.startswith("-") and tok != "-":
            j = 1
            consumed_next = False
            while j < len(tok):
                ch = tok[j]
                short_flags.append(ch)
                if f"-{ch}" in val_opts:
                    if j == len(tok) - 1 and i + 1 < len(args):
                        consumed_next = True
                    break
                j += 1
            i += 2 if consumed_next else 1
            continue
        pos_args.append(tok)
        i += 1
    return short_flags, long_flags, pos_args


def is_safe_rm_target(target: str) -> bool:
    if not target or ".." in Path(target).parts or "*" in target or "?" in target:
        return False
    norm = os.path.normpath(target)
    if norm == "/tmp":
        return False
    return (norm.startswith("/tmp/") and len(norm) > len("/tmp/")) or norm.startswith("graphify-out/.graphify_")


def unwrap_command_with_cwd(raw_tokens: list[str], cwd: str = "") -> tuple[list[str], str]:
    """Strip leading VAR=val assignments, shell keywords, and wrapper commands, returning (tokens, effective_cwd)."""
    tokens = list(raw_tokens)
    cur_cwd = cwd
    while tokens:
        head = tokens[0]
        if head in SHELL_PREFIX_TOKENS:
            tokens.pop(0)
            continue
        name = Path(head).name
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", head):
            tokens.pop(0)
            continue
        if name in {"env", "sudo", "command", "nohup", "exec"}:
            tokens.pop(0)
            value_flags = {"-u", "--unset", "-g", "-p"}
            while tokens and (
                (tokens[0].startswith("-") and tokens[0] != "--")
                or (name in {"env", "sudo"} and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", tokens[0]))
            ):
                tok = tokens.pop(0)
                if not tok.startswith("-"):
                    continue
                if name == "env":
                    if tok in {"-C", "--chdir"} and tokens:
                        cur_cwd = _resolve_dir(cur_cwd, tokens.pop(0))
                        continue
                    if tok.startswith("--chdir="):
                        cur_cwd = _resolve_dir(cur_cwd, tok.split("=", 1)[1])
                        continue
                    if tok.startswith("-C") and len(tok) > 2:
                        cur_cwd = _resolve_dir(cur_cwd, tok[2:])
                        continue
                    split_arg: str | None = None
                    if tok == "--split-string" and tokens:
                        split_arg = tokens.pop(0)
                    elif tok.startswith("--split-string="):
                        split_arg = tok.split("=", 1)[1]
                    elif tok.startswith("-") and not tok.startswith("--") and "S" in tok[1:]:
                        s_idx = tok.index("S", 1)
                        if s_idx + 1 < len(tok):
                            split_arg = tok[s_idx + 1 :]
                        elif tokens:
                            split_arg = tokens.pop(0)
                    if split_arg is not None:
                        try:
                            split_toks = shlex.split(split_arg)
                        except ValueError:
                            split_toks = split_arg.split()
                        tokens = split_toks + tokens
                        continue
                if name == "sudo":
                    if tok in {"-D", "--chdir"} and tokens:
                        cur_cwd = _resolve_dir(cur_cwd, tokens.pop(0))
                        continue
                    if tok.startswith("--chdir="):
                        cur_cwd = _resolve_dir(cur_cwd, tok.split("=", 1)[1])
                        continue
                    if tok == "-C" and tokens:
                        tokens.pop(0)
                        continue
                if name in {"env", "sudo"} and tok in value_flags and tokens:
                    tokens.pop(0)
            if tokens and tokens[0] == "--":
                tokens.pop(0)
            continue
        if name == "timeout":
            tokens.pop(0)
            while tokens and tokens[0].startswith("-") and tokens[0] != "--":
                flag = tokens.pop(0)
                if flag in {"-k", "-s", "--kill-after", "--signal"} and tokens:
                    tokens.pop(0)
            if tokens and tokens[0] == "--":
                tokens.pop(0)
            if tokens:
                tokens.pop(0)  # duration argument
            continue
        break
    return tokens, cur_cwd


def unwrap_command_tokens(raw_tokens: list[str]) -> list[str]:
    """Strip leading VAR=val assignments, shell keywords, and wrapper commands."""
    tokens, _ = unwrap_command_with_cwd(raw_tokens)
    return tokens


def evaluate_command(cmd: str, cwd: str) -> tuple[str, str | None]:
    stripped = strip_heredocs(cmd)
    segments = split_segments(stripped)

    # Track worst decision: deny > force_ask > allow
    ask_reasons: list[str] = []

    for sub_cmd in extract_command_substitutions(stripped):
        sub_dec, sub_reason = evaluate_command(sub_cmd, cwd)
        if sub_dec == "deny":
            return "deny", sub_reason
        if sub_dec == "force_ask" and sub_reason:
            ask_reasons.append(sub_reason)

    effective_cwd = cwd
    for raw_tokens in segments:
        tokens, seg_cwd = unwrap_command_with_cwd(raw_tokens, effective_cwd)
        if not tokens:
            continue
        prog = Path(tokens[0]).name

        if prog == "cd":
            cd_target: str | None = None
            for t in tokens[1:]:
                if t == "--":
                    continue
                if t.startswith("-") and t != "-":
                    continue
                cd_target = t
                break
            if cd_target == "-":
                pass
            elif cd_target is None:
                effective_cwd = str(Path.home())
            else:
                effective_cwd = _resolve_dir(seg_cwd, cd_target)
            continue

        # Skip read/search utilities unless they shouldn't matter
        if prog in READ_TOOLS:
            continue

        # Evaluate `eval ...` recursively
        if prog == "eval" and len(tokens) > 1:
            eval_args = tokens[2:] if tokens[1] == "--" else tokens[1:]
            if eval_args:
                eval_cmd = eval_args[0] if len(eval_args) == 1 else shlex.join(eval_args)
                ev_dec, ev_reason = evaluate_command(eval_cmd, seg_cwd)
                if ev_dec == "deny":
                    return "deny", ev_reason
                if ev_dec == "force_ask" and ev_reason:
                    ask_reasons.append(ev_reason)
                continue

        # Inspect nested shell invocations like `bash -c -- "git reset --hard"` or `bash <<< "git push --force"`
        if prog in {"bash", "sh", "zsh", "dash"}:
            t_idx = 1
            while t_idx < len(tokens):
                htok = tokens[t_idx]
                if htok == "<<<" and t_idx + 1 < len(tokens):
                    hs_dec, hs_reason = evaluate_command(tokens[t_idx + 1], seg_cwd)
                    if hs_dec == "deny":
                        return "deny", hs_reason
                    if hs_dec == "force_ask" and hs_reason:
                        ask_reasons.append(hs_reason)
                    t_idx += 2
                    continue
                if htok.startswith("<<<") and len(htok) > 3:
                    hs_dec, hs_reason = evaluate_command(htok[3:], seg_cwd)
                    if hs_dec == "deny":
                        return "deny", hs_reason
                    if hs_dec == "force_ask" and hs_reason:
                        ask_reasons.append(hs_reason)
                t_idx += 1

            has_c = False
            script_idx: int | None = None
            idx = 1
            while idx < len(tokens):
                arg = tokens[idx]
                if arg == "--":
                    if has_c and idx + 1 < len(tokens):
                        script_idx = idx + 1
                    break
                if arg == "<<<":
                    idx += 2
                    continue
                if arg.startswith("<<<"):
                    idx += 1
                    continue
                if arg in {"-o", "+o"} and idx + 1 < len(tokens):
                    idx += 2
                    continue
                if (arg.startswith("-") or arg.startswith("+")) and arg not in {"-", "+"}:
                    if arg.startswith("-") and not arg.startswith("--") and "c" in arg[1:]:
                        has_c = True
                    idx += 1
                    continue
                if has_c:
                    script_idx = idx
                break
            if script_idx is not None:
                nested_dec, nested_reason = evaluate_command(tokens[script_idx], seg_cwd)
                if nested_dec == "deny":
                    return "deny", nested_reason
                if nested_dec == "force_ask" and nested_reason:
                    ask_reasons.append(nested_reason)

        joined = " ".join(tokens)

        # DB / Schema destructive patterns (scoped to DB/migration/container runners)
        if prog in DB_CLI_RUNNERS:
            if re.search(r"\bmigrate:(fresh|reset)\b", joined, re.IGNORECASE):
                return "deny", "Blocked destructive database reset (migrate:fresh / migrate:reset) per destructive-safety.md."
            if re.search(r"\bdrop\s+(database|table)\b", joined, re.IGNORECASE):
                return "deny", "Blocked destructive SQL DROP DATABASE/TABLE command per destructive-safety.md."

        # Git rules
        if prog == "git":
            sub, args, repo_dir = parse_git_command(tokens, seg_cwd)
            if sub == "push":
                push_val_opts = {"--repo", "-o", "--push-option", "--receive-pack", "--exec"}
                short_flags, long_flags, pos_args = parse_git_subargs(args, push_val_opts)
                has_repo_opt = any(lf == "--repo" or lf.startswith("--repo=") for lf in long_flags)
                refspecs = pos_args if has_repo_opt else pos_args[1:]
                is_force = (
                    "--force" in long_flags
                    or "--mirror" in long_flags
                    or any(lf == "--force-with-lease" or lf.startswith("--force-with-lease=") for lf in long_flags)
                    or "f" in short_flags
                    or any(r.startswith("+") for r in refspecs)
                )
                if is_force:
                    return "deny", "Blocked force push (--force / -f / --force-with-lease / --mirror / +refspec) per git-hard-rules.md."
                if "--no-verify" in long_flags:
                    return "deny", "Blocked git push --no-verify per git-hard-rules.md."
                branch = current_git_branch(repo_dir)
                targets_protected = any(
                    r.lstrip("+").split(":")[-1].removeprefix("refs/heads/") in PROTECTED_BRANCHES
                    for r in refspecs
                )
                is_delete = "--delete" in long_flags or "d" in short_flags or any(r.startswith(":") for r in refspecs)
                if targets_protected or (branch in PROTECTED_BRANCHES and not is_delete):
                    return "deny", "Blocked direct push or remote deletion on protected branch per git-hard-rules.md."
                ask_reasons.append("git push requires explicit human confirmation.")
            elif sub == "commit":
                commit_val_opts = {
                    "-m", "--message", "-F", "--file", "-C", "--reuse-message",
                    "-c", "--reedit-message", "--fixup", "--squash", "-t", "--template",
                    "--author", "--date", "--cleanup", "-u", "--untracked-files",
                    "-S", "--gpg-sign", "--pathspec-from-file",
                }
                short_flags, long_flags, _ = parse_git_subargs(args, commit_val_opts)
                if "--no-verify" in long_flags or "n" in short_flags:
                    return "deny", "Blocked git commit --no-verify (-n) per git-hard-rules.md."
                branch = current_git_branch(repo_dir)
                if branch in PROTECTED_BRANCHES:
                    return "deny", f"Blocked direct git commit on protected branch '{branch}' per git-hard-rules.md."
                ask_reasons.append("git commit requires explicit human confirmation.")
            elif sub == "reset":
                _, long_flags, _ = parse_git_subargs(args)
                if "--hard" in long_flags:
                    return "deny", "Blocked git reset --hard per git-hard-rules.md."
            elif sub == "stash":
                _, _, pos_args = parse_git_subargs(args)
                if pos_args:
                    if pos_args[0] == "clear":
                        return "deny", "Blocked git stash clear (bulk discard) per git-stash skill."
                    if pos_args[0] == "drop":
                        ask_reasons.append("git stash drop requires explicit human confirmation.")
            elif sub == "merge":
                _, long_flags, _ = parse_git_subargs(args, {"-m", "--message", "-F", "--file", "-s", "--strategy", "-X", "--strategy-option", "--cleanup", "-S", "--gpg-sign"})
                if "--abort" not in long_flags and "--continue" not in long_flags and "--quit" not in long_flags:
                    ask_reasons.append("git merge mutates branch history and requires explicit human confirmation.")
            elif sub == "rm":
                ask_reasons.append("git rm deletes tracked files and requires explicit human confirmation.")
            elif sub == "rebase":
                _, long_flags, _ = parse_git_subargs(args, {"--onto", "-s", "--strategy", "-X", "--strategy-option", "--exec", "-x", "--autosquash"})
                if "--abort" not in long_flags and "--continue" not in long_flags and "--skip" not in long_flags:
                    ask_reasons.append("git rebase rewrites history and requires explicit human confirmation.")
            elif sub == "branch":
                branch_val_opts = {
                    "-m", "-M", "-c", "-C", "--format", "--sort", "--contains",
                    "--no-contains", "--merged", "--no-merged", "--points-at",
                    "--set-upstream-to", "-u",
                }
                short_flags, long_flags, _ = parse_git_subargs(args, branch_val_opts)
                if "--delete" in long_flags or "d" in short_flags or "D" in short_flags:
                    ask_reasons.append("git branch deletion requires explicit human confirmation.")
            elif sub == "tag":
                tag_val_opts = {
                    "-m", "-F", "-u", "--local-user", "--cleanup", "--format",
                    "--sort", "--contains", "--no-contains", "--merged", "--no-merged", "--points-at",
                }
                short_flags, long_flags, _ = parse_git_subargs(args, tag_val_opts)
                if "--delete" in long_flags or "d" in short_flags:
                    ask_reasons.append("git tag deletion requires explicit human confirmation.")

        # GitHub CLI rules
        elif prog == "gh" and len(tokens) >= 3 and tokens[1] == "pr" and tokens[2] == "merge":
            ask_reasons.append("gh pr merge requires explicit human confirmation.")

        # Recursive rm rules
        elif prog == "rm":
            short_flags: list[str] = []
            long_flags: list[str] = []
            targets: list[str] = []
            after_sep = False
            for t in tokens[1:]:
                if after_sep:
                    targets.append(t)
                elif t == "--":
                    after_sep = True
                elif t.startswith("--"):
                    long_flags.append(t)
                elif t.startswith("-") and t != "-":
                    short_flags.append(t[1:])
                else:
                    targets.append(t)
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
