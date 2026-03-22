#!/usr/bin/env python3
"""Helpers for generating human-readable Git push summaries for demos."""

from __future__ import annotations

import argparse
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = REPO_ROOT / "docs" / "push-summaries" / "latest.md"
SUMMARY_RELATIVE_PATH = DEFAULT_OUTPUT.relative_to(REPO_ROOT).as_posix()


class GitSummaryError(RuntimeError):
    """Raised when git state is not suitable for summary generation."""


@dataclass
class PushContext:
    local_ref: str
    local_sha: str
    remote_ref: str
    remote_sha: str


def rev_parse(revision: str) -> str:
    return run_git(["rev-parse", revision])


def run_git(args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "git command failed"
        raise GitSummaryError(message)
    return result.stdout.strip()


def parse_push_line(line: str) -> PushContext:
    parts = line.strip().split()
    if len(parts) != 4:
        raise GitSummaryError(
            "Expected pre-push input in the form: <local ref> <local sha> <remote ref> <remote sha>."
        )
    return PushContext(*parts)


def commit_subjects(commit_range: str) -> list[str]:
    if not commit_range:
        return []
    output = run_git(["log", "--format=%h %s", commit_range])
    return [line for line in output.splitlines() if line]


def changed_files(diff_range: str) -> list[str]:
    output = run_git(["diff", "--name-only", diff_range])
    return [line for line in output.splitlines() if line and line != SUMMARY_RELATIVE_PATH]


def diff_stat(diff_range: str) -> str:
    output = run_git(["diff", "--stat", diff_range, "--", ".", f":(exclude){SUMMARY_RELATIVE_PATH}"])
    return output or "(No diff stat available after excluding generated summary file)"


def unified_diff_excerpt(diff_range: str, limit: int = 120) -> list[str]:
    output = run_git(["diff", "--unified=1", diff_range, "--", ".", f":(exclude){SUMMARY_RELATIVE_PATH}"])
    lines = output.splitlines()
    return lines[:limit]


def remote_exists(remote_sha: str) -> bool:
    if not remote_sha or remote_sha == "0" * 40:
        return False
    try:
        run_git(["cat-file", "-e", f"{remote_sha}^{{commit}}"])
        return True
    except GitSummaryError:
        return False


def commit_changed_files(commit_sha: str) -> list[str]:
    output = run_git(["diff-tree", "--no-commit-id", "--name-only", "-r", commit_sha])
    return [line for line in output.splitlines() if line]


def is_summary_only_commit(commit_sha: str) -> bool:
    files = commit_changed_files(commit_sha)
    return bool(files) and all(path == SUMMARY_RELATIVE_PATH for path in files)


def effective_local_sha(context: PushContext) -> str:
    local_sha = context.local_sha
    if not remote_exists(local_sha):
        return local_sha

    if is_summary_only_commit(local_sha):
        try:
            return rev_parse(f"{local_sha}^")
        except GitSummaryError:
            return local_sha

    return local_sha


def build_ranges(context: PushContext) -> tuple[str, str]:
    local_sha = effective_local_sha(context)
    if remote_exists(context.remote_sha):
        return (f"{context.remote_sha}..{local_sha}", f"{context.remote_sha}..{local_sha}")
    base = run_git(["hash-object", "-t", "tree", "/dev/null"])
    return (local_sha, f"{base}..{local_sha}")


def render_summary(context: PushContext) -> str:
    commit_range, diff_range = build_ranges(context)
    subjects = commit_subjects(commit_range)
    files = changed_files(diff_range)
    stat = diff_stat(diff_range)
    excerpt = unified_diff_excerpt(diff_range)

    commit_lines = "\n".join(f"- {line}" for line in subjects) if subjects else "- No commits detected"
    file_lines = "\n".join(f"- `{path}`" for path in files) if files else "- No file changes detected"
    excerpt_block = "\n".join(excerpt) if excerpt else "(No diff excerpt available)"

    return f"""# Push Summary

## Push Context

- Local ref: `{context.local_ref}`
- Local sha: `{context.local_sha}`
- Remote ref: `{context.remote_ref}`
- Remote sha: `{context.remote_sha}`

## Commits In This Push

{commit_lines}

## Files Changed

{file_lines}

## Diff Stat

```text
{stat}
```

## Diff Excerpt

```diff
{excerpt_block}
```
"""


def write_summary(output_path: Path, content: str) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    return output_path


def stdin_lines() -> list[str]:
    import sys

    data = sys.stdin.read()
    return [line for line in data.splitlines() if line.strip()]


def summary_for_push_line(push_line: str, output_path: Path | None = None) -> Path:
    context = parse_push_line(push_line)
    content = render_summary(context)
    return write_summary(output_path or DEFAULT_OUTPUT, content)


def summary_for_stdin(output_path: Path | None = None) -> Path:
    lines = stdin_lines()
    if not lines:
        raise GitSummaryError("No push refs were provided on stdin.")
    return summary_for_push_line(lines[0], output_path=output_path)


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a Markdown summary for an upcoming git push.")
    parser.add_argument(
        "--push-line",
        help="A single pre-push line: <local ref> <local sha> <remote ref> <remote sha>.",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Where to write the Markdown summary file.",
    )
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    output_path = Path(args.output)
    try:
        if args.push_line:
            path = summary_for_push_line(args.push_line, output_path=output_path)
        else:
            path = summary_for_stdin(output_path=output_path)
    except GitSummaryError as exc:
        print(f"git-summary error: {exc}")
        return 1

    print(f"Wrote push summary to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
