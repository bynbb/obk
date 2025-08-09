import os
import subprocess
import sys
from pathlib import Path

import pytest
import typer

import obk.cli as cli

PYTHON = sys.executable
REPO_ROOT = Path(__file__).resolve().parents[1]


def _run(args, env, cwd=None):
    return subprocess.run(
        [PYTHON, "-m", "obk", *args],
        capture_output=True,
        text=True,
        env=env,
        cwd=cwd,
        check=False,
    )


def test_set_project_path_via_path(tmp_path):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT / "src")
    env["HOME"] = str(tmp_path)
    project = tmp_path / "proj"
    result = _run(["set-project-path", "--path", str(project)], env)
    assert result.returncode == 0
    cfg = tmp_path / ".config" / "obk" / "config.toml"
    assert cfg.exists()
    assert f"project_path = \"{project}\"" in cfg.read_text()


def test_set_project_path_here(tmp_path):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT / "src")
    env["HOME"] = str(tmp_path)
    project = tmp_path / "here"
    project.mkdir()
    result = _run(["set-project-path", "--here"], env, cwd=project)
    assert result.returncode == 0
    cfg = tmp_path / ".config" / "obk" / "config.toml"
    assert cfg.exists()
    assert f"project_path = \"{project}\"" in cfg.read_text()


def test_set_project_path_unset(tmp_path):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT / "src")
    env["HOME"] = str(tmp_path)
    project = tmp_path / "proj"
    _run(["set-project-path", "--path", str(project)], env)
    cfg = tmp_path / ".config" / "obk" / "config.toml"
    assert cfg.exists()
    result = _run(["set-project-path", "--unset"], env)
    assert result.returncode == 0
    assert not cfg.exists()


def test_set_project_path_show(tmp_path):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT / "src")
    env["HOME"] = str(tmp_path)
    project = tmp_path / "proj"
    _run(["set-project-path", "--path", str(project)], env)
    result = _run(["set-project-path", "--show"], env)
    assert result.returncode == 0
    assert str(project) in result.stdout
    assert "config" in result.stdout.lower()


def test_env_var_precedence(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    cfg = tmp_path / ".config" / "obk" / "config.toml"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    cfg.write_text(f"project_path = \"{tmp_path / 'cfg'}\"\n", encoding="utf-8")
    env_path = tmp_path / "env"
    monkeypatch.setenv("OBK_PROJECT_PATH", str(env_path))
    assert cli.resolve_project_root() == env_path


def test_resolve_project_root_unset(monkeypatch, capsys, tmp_path):
    monkeypatch.delenv("OBK_PROJECT_PATH", raising=False)
    monkeypatch.setenv("HOME", str(tmp_path))
    cfg = tmp_path / ".config" / "obk" / "config.toml"
    if cfg.exists():
        cfg.unlink()
    with pytest.raises(typer.Exit):
        cli.resolve_project_root()
    out = capsys.readouterr().err
    assert "No project path configured" in out


def test_windows_path_env(monkeypatch):
    win_path = "C:\\Projects\\obk"
    monkeypatch.setenv("OBK_PROJECT_PATH", win_path)
    path = cli.resolve_project_root()
    assert str(path) == win_path
