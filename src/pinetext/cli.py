import sys
import typer

from pathlib import Path

from pinetext.client import PineText


app = typer.Typer(
    name="PineText",
    help="PineText CLI",
)


@app.command()
def run(
    path: Path | None = typer.Argument(None, help="Directory containinig documents"),
    text: str | None = typer.Argument(None, help="Optional one-shot question"),
    name: str | None = typer.Option(None, "--name", help="Assistant name"),
    model: str | None = typer.Option(None, "--model", help="Model name"),
):
    if text is None and not sys.stdin.isatty():
        text = sys.stdin.read().strip() or None
    client = PineText(name=name, model=model)
    client.run(path, text)
