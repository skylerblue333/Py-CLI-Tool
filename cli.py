"""Typer-based CLI foundation for SKYCOIN4444 services."""
import typer

app = typer.Typer(no_args_is_help=True)

@app.command()
def health():
    """Run a local health check."""
    typer.echo("ok")

@app.command()
def version():
    typer.echo("skycoin4444-cli 1.0.0")

if __name__ == "__main__":
    app()
