# Git Hard Rules

- **Never Force Push**: Never use `git push --force` or `git push --force-with-lease`.
- **Never Bypass Verification**: Never use `--no-verify` on commits or pushes.
- **Never Amend Pushed Commits**: Do not amend commits that have already been pushed to a remote repository.
- **Never Hard Reset Shared Work**: Do not execute `git reset --hard` on branches shared with others or remote branches.
- **Never Commit Secrets**: Do not commit credentials, `.env` files, API keys, private key files (`.pem`, `.key`, `id_rsa`), or security tokens.
- **Protected Branch Refusal**: Never commit directly on `main`, `master`, or `develop`. Always use feature branches.
