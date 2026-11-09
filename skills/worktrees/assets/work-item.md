# Work item

```toml
id = "wi-01"
title = "REPLACE with a deliverable"
depends_on = []
files = ["REPLACE with exact repository-relative file paths"]
est_lines = 0
acceptance_criteria = ["REPLACE with observable acceptance criteria"]
verify_command = "REPLACE with the exact documented command"
verify_sources = ["REPLACE with the repository document containing that command"]
```

## Scope

Describe only the approved work this item delivers.

## Environment and verification

List required runtimes, dependency setup commands and their working directories,
using evidence in `verify_sources` or selected design sources. Describe setup
needed in each worktree before `verify_command` can run. Keep dependencies and
build output ignored, and preserve reviewed manifests and lockfiles.

## Rationale and provenance

Explain how it implements the settled design. Link the relevant intent and
decision documents, using paths relative to this work-item document.
The zero estimate and placeholder paths intentionally make this template
unexecutable until filled in and reviewed.
