# Steering Rules

- **Feature Branching**: All modifications must be committed on feature branches checked out from the default branch.
- **Explicit Human Gates**: Gated confirmations are required for all repository-modifying actions (commits, pushes, pull request creations, and posting API reviews).
- **Autonomy & Decisions**: The AI is empowered to decide the best approaches for implementation, design, and specifications autonomously, but must explicitly list all key design decisions in the respective documentation files.
- **No Force-Pushes**: Force-pushing (`--force`, `--force-with-lease`) is strictly prohibited.
- **No Verification Bypass**: Bypassing pre-commit hooks (`--no-verify`) is strictly prohibited.
