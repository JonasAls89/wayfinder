# 0020. Wayfinder public plugin namespace

- Status: accepted
- Date: 2026-11-10

## Context

Short workflow names can collide with client commands or independently installed
skills. The product connects intent to reviewed, verified work; Wayfinder names
that purpose without changing the execution contract.

## Decision

Rename the [plugin](../../.claude-plugin/plugin.json) to `wayfinder`, superseding
only the public name in [ADR 0017](0017-skills-first-intent-workflow.md).
Keep the five skill names unprefixed and distribute the complete bundle, so
plugin-aware clients expose `/wayfinder:init`, `/wayfinder:context`,
`/wayfinder:intent`, `/wayfinder:worktrees` and `/wayfinder:run`.
Update active guidance, generated assets and helper handoffs to those commands.

This is a public namespace change, not a runtime migration. Keep the Git
repository URL, [Python package](../../pyproject.toml),
[execution storage](../../src/wayfinder/execution.py) and
[managed context markers](../../src/wayfinder/guardrails.py) unchanged.
Renaming those internals would add unrelated migration and import changes.

## Consequences

Users install Wayfinder as a separate plugin identity and explicitly disable or
uninstall an old installation. No aliases, duplicate standalone skills or
automatic cleanup are added. Existing repository setup is still preserved;
skipped files need reviewed edits to adopt the new command references.
See the [installation guidance](../../README.md#install).
