# 0022. Explicit CLI-safe skill names

- Status: accepted
- Date: 2026-11-10

## Context

Copilot CLI discovers literal skill names from `SKILL.md`; naming the plugin
`wayfinder` does not register colon-style skill aliases. The unprefixed `context`
and `init` names also collide with client commands and personal skill copies.
See [CLI skill invocation](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills#using-agent-skills).

## Decision

Use `wayfinder-init`, `wayfinder-context`, `wayfinder-intent`,
`wayfinder-worktrees` and `wayfinder-run` as the actual skill names and matching
directory names in the [plugin manifest](../../.claude-plugin/plugin.json).
Invoke the discovered names, for example
`Use the /wayfinder-context skill to refresh and validate this repository.`
This supersedes only ADR 0020's
[unprefixed skill naming and assumed aliases](0020-wayfinder-plugin-namespace.md).

Keep the plugin identity, bundled runtime and private helper subcommands unchanged.
The external planning handoff uses its discovered skill name, `/grill-with-docs`,
without assuming a plugin-supplied alias.
Install the complete bundle; individual skill folders lack the shared helper,
runtime and assets.

## Consequences

[Plugin tests](../../tests/test_plugin.py) require matching directory/frontmatter
names and resolvable bundled resources. [Setup tests](../../tests/test_baseline.py)
require the new names in generated guidance and helper handoffs.
Users refresh the complete plugin and start a fresh session. Obsolete standalone
personal copies require reviewed manual cleanup, not automatic deletion or aliases.
Historical ADR source links receive approved mechanical path updates only;
their decisions remain unchanged.
