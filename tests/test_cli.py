from typer.testing import CliRunner
from obk.cli import app

runner = CliRunner()

def test_hello_default():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Hello, world!" in result.output

def test_hello_custom():
    result = runner.invoke(app, ["--name", "Alice"])
    assert result.exit_code == 0
    assert "Hello, Alice!" in result.output
