import shutil
import subprocess
from pathlib import Path

import pytest

from scripts.helper import BUNDLE, main

FIXTURE = Path(__file__).parent / "fixtures" / "npm-typescript"


def install_npm(root, cache, *, offline=False):
    executable = shutil.which("npm")
    if executable is None:
        pytest.fail("npm integration tests require Node.js and npm on PATH")
    args = [
        executable,
        "ci",
        "--include=dev",
        "--ignore-scripts",
        "--no-audit",
        "--no-fund",
        "--cache",
        str(cache),
    ]
    if offline:
        args.append("--offline")
    result = subprocess.run(args, cwd=root, capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.fixture(scope="module")
def npm_cache(tmp_path_factory):
    cache = tmp_path_factory.mktemp("npm cache")
    seed = tmp_path_factory.mktemp("npm seed")
    shutil.copytree(
        FIXTURE, seed, dirs_exist_ok=True, ignore=shutil.ignore_patterns("node_modules", "dist")
    )
    install_npm(seed, cache)
    return cache


@pytest.fixture
def npm_repository(repo_factory, commit):
    root = repo_factory(verify="npm run verify")
    shutil.copytree(
        FIXTURE, root, dirs_exist_ok=True, ignore=shutil.ignore_patterns("node_modules", "dist")
    )
    item = root / "docs/work/wi-01.md"
    item.write_text(
        item.read_text().replace("wi-01.txt", "src/sum.ts")
        + "\nRequires Node.js and npm. Run `npm ci` in each worktree before verification.\n"
    )
    assert main(["init", "--path", str(root)]) == 0
    commit(root, ".")
    return root


def create_worktree(root, capsys):
    assert main(["worktrees", "--path", str(root), "--approve", "--yes"]) == 0
    capsys.readouterr()
    assert main(["worktrees", "--path", str(root), "--create", "--yes"]) == 0
    paths = [
        Path(line.removeprefix("created "))
        for line in capsys.readouterr().out.splitlines()
        if line.startswith("created ")
    ]
    assert len(paths) == 1
    return paths[0]


def source_worker(command, expression):
    source = (
        f"export function sum(left: number, right: number): number {{\n  return {expression};\n}}\n"
    )
    return (
        command(f"from pathlib import Path; Path('src/sum.ts').write_text({source!r})")
        + " {prompt}"
    )


def failure_log(output):
    paths = [
        line.strip().removeprefix("log: ")
        for line in output.splitlines()
        if line.strip().startswith("log: ")
    ]
    assert len(paths) == 1
    return Path(paths[0]).read_text()


@pytest.mark.parametrize("force", [False, True])
def test_init_preserves_existing_npm_typescript_project(tmp_path, force):
    root = tmp_path / "npm project"
    shutil.copytree(FIXTURE, root, ignore=shutil.ignore_patterns("node_modules", "dist"))
    original = {
        path.relative_to(root): path.read_bytes() for path in root.rglob("*") if path.is_file()
    }
    args = [
        "uv",
        "run",
        "--project",
        str(BUNDLE),
        "--locked",
        "python",
        str(BUNDLE / "scripts/helper.py"),
        "init",
        "--path",
        str(root),
    ]
    if force:
        args.append("--force")
    result = subprocess.run(args, cwd=root, capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stdout + result.stderr
    assert (root / "AGENTS.md").is_file()
    assert original == {name: (root / name).read_bytes() for name in original}
    for name in ("node_modules", "pyproject.toml", "uv.lock", ".venv"):
        assert not (root / name).exists()


def test_npm_worktree_requires_its_own_dependencies(npm_repository, npm_cache, command, capsys):
    root = npm_repository
    original = (root / "src/sum.ts").read_bytes()
    install_npm(root, npm_cache, offline=True)
    worktree = create_worktree(root, capsys)
    assert not (worktree / "node_modules").exists()
    args = [
        "run",
        "--path",
        str(root),
        "--yes",
        "--runner-command",
        source_worker(command, "right + left"),
    ]
    assert main(args) == 1
    failed = capsys.readouterr().out
    assert "wi-01 [failed]" in failed
    assert "verification failed (npm run verify)" in failed
    assert "node_modules/typescript" in failure_log(failed)

    install_npm(worktree, npm_cache, offline=True)
    assert main(args) == 0
    assert "wi-01 [done]" in capsys.readouterr().out
    assert (worktree / "dist/sum.js").is_file()
    assert (root / "src/sum.ts").read_bytes() == original
    assert not (root / "dist").exists()
    for name in ("package.json", "package-lock.json", "tsconfig.json"):
        assert (worktree / name).read_bytes() == (root / name).read_bytes()


@pytest.mark.parametrize(
    "expression,diagnostic", [('"wrong"', "TS2322"), ("left - right", "AssertionError")]
)
def test_npm_type_errors_and_test_failures_block_completion(
    npm_repository, npm_cache, command, capsys, expression, diagnostic
):
    root = npm_repository
    worktree = create_worktree(root, capsys)
    install_npm(worktree, npm_cache, offline=True)
    assert (
        main(
            [
                "run",
                "--path",
                str(root),
                "--yes",
                "--runner-command",
                source_worker(command, expression),
            ]
        )
        == 1
    )
    output = capsys.readouterr().out
    assert "wi-01 [failed]" in output
    assert "wi-01 [done]" not in output
    assert "verification failed (npm run verify)" in output
    assert diagnostic in failure_log(output)
