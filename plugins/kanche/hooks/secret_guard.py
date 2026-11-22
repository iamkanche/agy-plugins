#!/usr/bin/env python3
"""PreToolUse hook blocking writes to sensitive env/key files or live credential literals."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ENV_SECRET_RE = re.compile(r"^\.env(?:\..+)?$", re.IGNORECASE)
SAFE_ENV_RE = re.compile(r"^\.env\.(?:example|sample|template|dist)$", re.IGNORECASE)
SENSITIVE_FILENAMES = {"id_rsa", "id_ed25519", "id_ecdsa", "id_dsa"}
SENSITIVE_SUFFIXES = (".pem", ".key", ".p12", ".pfx")

SECRET_PATTERNS = [
    (re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"), "private key block"),
    (re.compile(r"\bghp_[A-Za-z0-9]{36}\b"), "GitHub personal access token"),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"), "GitHub fine-grained PAT"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key ID"),
    (re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{24,}\b"), "API secret key (sk-...)"),
    (re.compile(r"\bsk_live_[A-Za-z0-9]{16,}\b"), "Stripe live secret key"),
    (re.compile(r"\bAIza[0-9A-Za-z_-]{32,}\b"), "Google/Gemini API key"),
]


def emit(decision: str, reason: str | None = None) -> int:
    out: dict[str, str] = {"decision": decision}
    if reason:
        out["reason"] = reason
    sys.stdout.write(json.dumps(out))
    return 0


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return emit("allow")

    args = payload.get("toolCall", {}).get("args", {})
    raw_path = args.get("Path") or args.get("path") or args.get("file_path") or ""
    content = args.get("Content") or args.get("Replacement") or args.get("content") or ""

    if raw_path:
        name = Path(raw_path).name
        if (ENV_SECRET_RE.match(name) and not SAFE_ENV_RE.match(name)) or name in SENSITIVE_FILENAMES or name.lower().endswith(SENSITIVE_SUFFIXES):
            return emit("deny", f"Blocked writing sensitive credential/env file '{name}' per git-hard-rules.md.")

    if content:
        for pat, label in SECRET_PATTERNS:
            if pat.search(content):
                return emit("deny", f"Blocked writing potential {label} in '{raw_path or 'file'}' per git-hard-rules.md.")

    return emit("allow")


if __name__ == "__main__":
    sys.exit(main())
