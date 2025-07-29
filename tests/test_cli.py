import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


def test_hello_world():
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")
    result = subprocess.run(
        [sys.executable, "-m", "obk", "hello-world"],
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )
    assert result.stdout.strip() == "hello world"


def test_help():
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")
    result = subprocess.run(
        [sys.executable, "-m", "obk", "hello-world", "-h"],
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )
    assert "Print hello world" in result.stdout


def test_entrypoint_any_directory(tmp_path):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")
    result = subprocess.run(
        [sys.executable, "-m", "obk", "hello-world"],
        capture_output=True,
        text=True,
        check=True,
        cwd=tmp_path,
        env=env,
    )
    assert result.stdout.strip() == "hello world"
