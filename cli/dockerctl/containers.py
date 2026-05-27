"""Container subcommands: list, remove, deploy.

Replaces remove_Container.sh and the deploy branches of the old menu scripts.
All non-interactive: arguments and flags only, so it is safe to call from CI.
"""

from __future__ import annotations

import typer

from ._docker import DockerError, run

app = typer.Typer(help="Manage Docker containers.")


@app.command("ls")
def list_containers(
    all_: bool = typer.Option(False, "--all", "-a", help="Include stopped containers"),
) -> None:
    """List containers (running, or all with --all)."""
    args = ["ps"]
    if all_:
        args.append("-a")
    try:
        typer.echo(run(*args, capture=True), nl=False)
    except DockerError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(1) from exc


@app.command("rm")
def remove(
    container_id: str = typer.Argument(..., help="Container ID or name to remove"),
    force: bool = typer.Option(False, "--force", "-f", help="Force removal of a running container"),
) -> None:
    """Remove a container by ID or name."""
    args = ["rm"]
    if force:
        args.append("--force")
    args.append(container_id)
    try:
        run(*args)
    except DockerError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(1) from exc
    typer.echo(f"Removed container {container_id}")


@app.command()
def deploy(
    image: str = typer.Argument(..., help="Image to run, e.g. nginx:latest"),
    name: str = typer.Option(..., "--name", "-n", help="Container name"),
    port: str = typer.Option(..., "--port", "-p", help="Port mapping host:container, e.g. 8080:80"),
) -> None:
    """Run a detached container with a name and port mapping."""
    try:
        run("run", "-d", "--name", name, "-p", port, image)
    except DockerError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(1) from exc
    typer.echo(f"Deployed {name} from {image} on {port}")
