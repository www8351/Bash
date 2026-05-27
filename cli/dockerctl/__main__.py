"""dockerctl entrypoint: wires the image and container command groups together."""

from __future__ import annotations

import typer

from . import __version__, containers, images

app = typer.Typer(
    help="Non-interactive Docker helper for CI/CD pipelines.",
    no_args_is_help=True,
)
app.add_typer(images.app, name="images")
app.add_typer(containers.app, name="containers")


@app.command()
def version() -> None:
    """Print the dockerctl version."""
    typer.echo(__version__)


if __name__ == "__main__":
    app()
