import typer

from pathlib import Path

from pinetext.client import PineText


app = typer.Typer(
    name="PineText",
    help="PineText CLI",
)


@app.command()
def run(
    data_dir: Path | None = typer.Option(None, "--data-dir"),
):
    client = PineText(data_dir=str(data_dir) if data_dir is not None else None)
    client.run()
