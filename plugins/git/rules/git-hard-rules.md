# Git Hard Rules

Always in effect for every `git` workflow:

- **Never force-push** (`--force` / `--force-with-lease`).
- **Never** use `--no-verify`.
- **Never amend a pushed commit.**
- **Never** `git reset --hard` on shared work.
- **Never commit secrets** — `.env`, credentials, `*.pem`, `*.key`, `id_rsa`, tokens.
- **Never work on a protected branch** (`main` / `master` / `develop`); create a feature
  branch first via `/git:branch-create`.
- **Never delete remote protected branches** (`main` / `master` / `develop`).
- **Keep commits atomic and focused** (avoid staging unrelated changes).
- **Every side effect is human-gated.** Before commit, push, branch-create, branch-delete, tag-create, or rebase: STOP and ask the user to confirm, showing exactly what will happen. Proceed only on an explicit yes. (Antigravity has no per-command tool scoping — run in Review-driven autonomy.)
