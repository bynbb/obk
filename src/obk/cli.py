from typer import Typer, echo

app = Typer(add_completion=False)

@app.command()
def hello(name: str = "world"):
    """A stub command that prints a friendly greeting."""
    echo(f"Hello, {name}!")
