import os
import subprocess
import sys
from pathlib import Path


def run_cli(args, *, cwd=None):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")
    result = subprocess.run(
        [sys.executable, "-m", "obk", *args],
        capture_output=True,
        text=True,
        cwd=cwd,
        env=env,
    )
    return result

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


def test_hello_world():
    result = run_cli(["hello-world"])
    assert result.returncode == 0
    assert result.stdout.strip() == "hello world"


def test_help():
    result = run_cli(["hello-world", "-h"])
    assert result.returncode == 0
    assert "Print hello world" in result.stdout


def test_entrypoint_any_directory(tmp_path):
    result = run_cli(["hello-world"], cwd=tmp_path)
    assert result.returncode == 0
    assert result.stdout.strip() == "hello world"


def test_divide_success():
    result = run_cli(["divide", "4", "2"])
    assert result.returncode == 0
    assert result.stdout.strip() == "2.0"


def test_divide_zero_error(tmp_path):
    log = tmp_path / "obk.log"
    result = run_cli(["--logfile", str(log), "divide", "1", "0"])
    assert result.returncode == 2
    assert "[ERROR] Cannot divide by zero" in result.stderr
    assert log.exists() and log.read_text()


def test_fail_unhandled_exception(tmp_path):
    log = tmp_path / "fail.log"
    result = run_cli(["--logfile", str(log), "fail"])
    assert result.returncode == 1
    assert "[FATAL] Unexpected crash, see log" in result.stderr
    assert log.exists() and log.read_text()
