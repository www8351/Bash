"""Image subcommands: pull and remove. Replaces pull_images.sh / remove_images.sh."""

from __future__ import annotations

import typer

from ._docker import DockerError, run

app = typer.Typer(help="Manage Docker images.")


@app.command()
def pull(name: str = typer.Argument(..., help="Image reference, e.g. nginx:latest")) -> None:
    """Pull an image from a registry."""
    try:
        run("pull", name)
    except DockerError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(1) from exc
    typer.echo(f"OK: pulled {name}")


@app.command("rm")
def remove(
    image_id: str = typer.Argument(..., help="Image ID or reference to remove"),
    force: bool = typer.Option(False, "--force", "-f", help="Force removal"),
) -> None:
    """Remove an image by ID or reference."""
    args = ["rmi"]
    if force:
        args.append("--force")
    args.append(image_id)
    try:
        run(*args)
    except DockerError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(1) from exc
    typer.echo(f"Removed image {image_id}")
