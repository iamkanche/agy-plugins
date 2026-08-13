---
name: security-scan
description: Scan codebase for secrets, dependency vulnerabilities, and security anti-patterns.
model: flash
---

# /kanche:security-scan

**Summary.** Proactively audit codebase for hardcoded secrets, exposed credentials, vulnerable dependencies, and security anti-patterns.

## Steps

1. Scan files and diffs for secrets (`.env`, private keys, hardcoded API tokens, credentials).
2. Execute project security/audit tools when available (`npm audit`, `composer audit`, `pip-audit`, `cargo audit`, `govulncheck`).
3. Scan for common OWASP patterns (unSanitized SQL queries, command execution, unsafe innerHTML usage).
4. Output detailed Security Audit Report with severity levels and mitigation steps.
