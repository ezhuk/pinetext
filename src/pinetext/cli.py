import sys
from pathlib import Path
from typing import Annotated

import typer

from pinetext.client import PineText

app = typer.Typer(
    name="PineText",
    help="PineText CLI",
)


@app.command()
def run(
    path: Annotated[
        Path | None,
        typer.Argument(help="Directory containing documents"),
    ] = None,
    text: Annotated[
        str | None,
        typer.Argument(help="Optional one-shot question"),
    ] = None,
    name: Annotated[
        str | None,
        typer.Option("--name", help="Assistant name"),
    ] = None,
    model: Annotated[
        str | None,
        typer.Option(None, "--model", help="Model name"),
    ] = None,
):
    if text is None and not sys.stdin.isatty():
        text = sys.stdin.read().strip() or None
    client = PineText(name=name, model=model)
    client.run(path, text)
