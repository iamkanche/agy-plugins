# /git:branch-create

**Summary.** Create and switch to a new feature branch from the up-to-date remote default branch (`origin/<default>`). The workflow delegates all branch checks and switching operations to the specialized `@git-operator` subagent (defined in `agents/git-operator/agent.json`).

## Inputs

Parse the invocation arguments:

- `<branch-name>` (positional, required) — the name of the branch to create.

If the branch name is missing, ask the user for it (do not invent one). Reject the protected names `main`/`master`/`develop` as the new branch name — ask for a different name.

## Steps

1. **Confirm this is a git repo.** If `git rev-parse --is-inside-work-tree` fails, STOP.

   ```bash
   git rev-parse --is-inside-work-tree
   ```

2. **Detect the remote default branch** (never hardcode `main`).

   ```bash
   DEFAULT=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@')
   DEFAULT=${DEFAULT:-$(git remote show origin 2>/dev/null | sed -n 's/.*HEAD branch: //p')}
   DEFAULT=${DEFAULT:-main}
   echo "$DEFAULT"
   ```

3. **Verify the new name is free.** If a branch with that name already exists, STOP and report it.

   ```bash
   NAME="<branch-name>"
   git rev-parse --verify --quiet "refs/heads/$NAME" && echo "EXISTS" || echo "free"
   ```

4. **Fetch the latest default from origin** so the branch is created from up-to-date state (never branch off a stale local default).

   ```bash
   git fetch origin "$DEFAULT"
   ```

5. **Create and switch** to the new branch from the freshly fetched remote default.

   ```bash
   git switch -c "$NAME" "origin/$DEFAULT"
   ```

6. **Report** the created branch and its base.

   ```bash
   git rev-parse --abbrev-ref HEAD
   git branch -vv
   ```

## git hard rules

Never `reset --hard` · never work on a protected branch · never branch off an out-of-date local default (always from freshly fetched `origin/<default>`).

## Done when

- A new branch named `<branch-name>` exists and is checked out.
- It was created from `origin/<default>` after a fresh fetch (not a stale local base).
- The branch name is not a protected name.
