"""Small, shared parsers for Git's porcelain status output."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
import subprocess


def read_porcelain_status(worktree: Path) -> str | None:
    """Return full porcelain status, including ignored paths, or None on failure."""
    try:
        proc = subprocess.run(
            ["git", "status", "--porcelain=v1", "--ignored=matching", "-z"],
            cwd=worktree,
            check=False,
            text=True,
            capture_output=True,
            encoding="utf-8",
        )
    except (OSError, UnicodeError):
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout or ""


def porcelain_entries(status: str) -> Iterator[tuple[str, str]]:
    """Yield status-code/path pairs from NUL or line-delimited porcelain v1."""
    records = status.split("\0") if "\0" in status else status.splitlines()
    for record in records:
        if len(record) < 3 or record[2] != " ":
            continue
        yield record[:2], record[3:]


def local_data_paths(status: str) -> list[str]:
    """Return untracked and ignored paths without reading their contents."""
    return sorted(
        {path for code, path in porcelain_entries(status) if code in {"??", "!!"}}
    )
