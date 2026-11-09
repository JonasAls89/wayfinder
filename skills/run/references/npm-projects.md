# npm and JavaScript/TypeScript projects

## Runtime boundary

The [helper](../../../scripts/helper.py) uses the plugin's bundled Python sources
and uv environment, even when the target repository has no Python manifest.
Users still need the plugin's Python/uv prerequisites and the target project's
Node.js/npm toolchain. [Init](../../init/SKILL.md) proposes changes from existing
project tooling; it does not generate an application or install its dependencies.

## Project-owned verification

The [runner](../../../src/automagic/runner.py) executes the documented
`verify_command` at the worktree root. When the project defines a `verify` npm
script, the handoff can use:

```toml
verify_command = "npm run verify"
```

Declare a committed repository document containing that exact command in
`verify_sources`. Let the npm script compose the project's existing lint,
type-check, build and test commands as appropriate. The helper does not interpret
shell chains such as `&&` in `verify_command`; put them inside the npm script.
For nested packages or npm workspaces, document a root-level command using the
project's actual workspace/package layout rather than assuming a directory.

## Prepare every worktree explicitly

[Worktree creation](../../../src/automagic/worktrees.py) checks out committed
files; it does not copy `node_modules` or install project dependencies.

1. Record the required runtimes, documented setup command and working directory
   in the work item, with evidence among its declared repository sources.
2. Present and confirm dependency setup before executing it in each created
   worktree. With a matching committed npm lockfile, the project's documented
   command may be [`npm ci`](https://docs.npmjs.com/cli/v10/commands/npm-ci/),
   which installs without rewriting the manifest or lockfile. Respect existing
   project npm configuration and required install flags.
3. Keep dependencies and generated output ignored. Propose necessary ignore-rule
   edits before snapshot approval, rather than broadening approved file scope
   during execution. Missing tools or failed installs block launch.
4. Repeat setup for newly created worktrees and refresh dependencies when their
   committed lockfile changes, including after prerequisite integration.
   Changes to reviewed inputs require a new approved snapshot.

Dependency installation remains a separately confirmed setup step, not an
automatic helper action. Review changes and make implementation commits manually.

## Regression coverage

The [locked fixture](../../../tests/fixtures/npm-typescript/package.json) and
[integration tests](../../../tests/test_npm.py) cover manifest/tooling preservation,
per-worktree dependency setup, real TypeScript compilation and JavaScript tests.
Missing dependencies, type errors and failing tests cannot count as completion.
The tests use fake workers, not real Copilot agents. The compiler download uses a
private temporary npm cache; subsequent worktree installs run offline.
