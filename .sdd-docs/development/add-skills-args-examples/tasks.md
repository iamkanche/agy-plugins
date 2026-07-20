# Tasks: Add Command Arguments/Usage Samples in Connections Dashboard

## Phase 4 — Build Tasks
- [ ] **[T-4.1]** Edit `loadCommandDetails(cmdName)` in `plugins/sdd/index.html` to append the usage snippet markup to `headerSection.innerHTML` if `data.usage` exists.
- [ ] **[T-4.2]** Add `usage` properties to all commands inside the `commandData` object in `plugins/sdd/index.html` (lines 612–800).
- [ ] **[T-4.3]** Add `usage` properties to all commands inside the `gitAndGhCliData` object in `plugins/sdd/index.html` (lines 803–971).

## Phase 5 — Verification Tasks
- [ ] **[T-5.1]** Verify no syntax errors in `plugins/sdd/index.html` (valid Javascript structure).
- [ ] **[T-5.2]** Open `plugins/sdd/index.html` (or inspect it) to confirm that the `usage` strings are correctly escaped and formatted.
