# API Diff: Convert SDD to Graph Engineering Workflow

## Added Commands (`/kanche:graph-*`)
- `/kanche:graph-run`: Master 10-phase Graph Engineering Workflow orchestrator.
- `/kanche:graph-continue`: Resume Graph Engineering Workflow from on-disk state.
- `/kanche:graph-steering`: Repository survey and steering guideline extraction via Knowledge Graph.
- `/kanche:graph-sync`: Domain document promotion and knowledge graph cache synchronization.
- `/kanche:graph-init`: Bootstrap graph guidelines and knowledge graph.
- `/kanche:graph-init-update`: Re-analyze repository and merge new graph findings.

## Modified Commands (Backward Compatibility Wrappers)
- `/kanche:sdd-run`: Emits forwarding notice and delegates to `/kanche:graph-run`.
- `/kanche:sdd-continue`: Emits forwarding notice and delegates to `/kanche:graph-continue`.
- `/kanche:sdd-steering`: Emits forwarding notice and delegates to `/kanche:graph-steering`.
- `/kanche:sdd-sync`: Emits forwarding notice and delegates to `/kanche:graph-sync`.
- `/kanche:sdd-init`: Emits forwarding notice and delegates to `/kanche:graph-init`.
- `/kanche:sdd-init-update`: Emits forwarding notice and delegates to `/kanche:graph-init-update`.
