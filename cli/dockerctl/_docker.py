"""Thin wrapper around the `docker` CLI.

Centralises subprocess handling so the command modules stay focused on intent.
Bash scraped `docker search`/`$?`; here we call docker directly and surface its
exit code and stderr as a typed exception.
"""

from __future__ import annotations

import shutil
import subprocess


class DockerError(RuntimeError):
    """Raised when a docker invocation fails or docker is unavailable."""


def _docker_bin() -> str:
    path = shutil.which("docker")
    if path is None:
        raise DockerError("docker CLI not found on PATH")
    return path


def run(*args: str, capture: bool = False) -> str:
    """Run `docker <args>`.

    With capture=False, output streams to the terminal (good for `pull`/`up`).
    With capture=True, stdout is returned as text (good for `ps`/`inspect`).
    Raises DockerError on non-zero exit.
    """
    cmd = [_docker_bin(), *args]
    try:
        result = subprocess.run(
            cmd,
            check=True,
            text=True,
            capture_output=capture,
        )
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or "").strip() or f"exit code {exc.returncode}"
        raise DockerError(f"`docker {' '.join(args)}` failed: {detail}") from exc
    return result.stdout if capture else ""
