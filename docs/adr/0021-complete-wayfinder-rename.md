# 0021. Complete Wayfinder rename

- Status: accepted
- Date: 2026-11-10

## Context

The public-only rename in [ADR 0020](0020-wayfinder-plugin-namespace.md) left
different names for the plugin and its implementation. A partial runtime rename
then moved the package without updating its startup check and internal imports,
preventing the context commit hook from starting.

## Decision

Use `wayfinder` for the [plugin](../../.claude-plugin/plugin.json),
[Python project](../../pyproject.toml), [runtime package](../../src/wayfinder/)
and [GitHub repository](https://github.com/JonasAls89/wayfinder).
The [helper](../../scripts/helper.py) resolves only that bundled package.

Use `.wayfinder/execution/` for approvals, locks, worktree ownership, run state
and logs, and `.wayfinder/BRIEF.md` for worktree briefs. The
[execution checks](../../src/wayfinder/execution.py) continue excluding runtime
state from design inputs and execution-owned files from implementation scope.
Use `wayfinder:context` for the
[managed context markers](../../src/wayfinder/guardrails.py), including generated
[context documents](../../skills/wayfinder-init/assets/docs/CONTEXT.md.j2).
Reviewed plans remain in `docs/work/`; no runtime plan directory is generated.

This supersedes ADR 0020's internal-name preservation policy. Existing ADR names
and source links are mechanically refreshed with explicit user approval; their
other decisions remain unchanged.

## Consequences

Install the complete current bundle. Existing repositories need reviewed
guidance and marker edits plus a fresh execution approval; previous state is not
automatically imported or removed. No compatibility package, command aliases or
migration layer is introduced, consistent with the
[current-only policy](0018-current-workflow-only.md).
