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
    project.mkdir()
    result = _run(["set-project-path", "--path", str(project)], env)
    assert result.returncode == 0
    cfg = tmp_path / ".config" / "obk" / "config.toml"
    assert cfg.exists()
    assert f"project_path = '{project}'" in cfg.read_text()


def test_set_project_path_windows_literal(tmp_path):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT / "src")
    env["HOME"] = str(tmp_path)
    win_arg = "C:\\Work\\obk"
    project = tmp_path / win_arg
    project.mkdir()
    result = _run(["set-project-path", "--path", win_arg], env, cwd=tmp_path)
    assert result.returncode == 0
    cfg = tmp_path / ".config" / "obk" / "config.toml"
    assert cfg.exists()
    assert "project_path = 'C:\\Work\\obk'" in cfg.read_text()


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
    assert f"project_path = '{project}'" in cfg.read_text()


def test_set_project_path_unset(tmp_path):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT / "src")
    env["HOME"] = str(tmp_path)
    project = tmp_path / "proj"
    project.mkdir()
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
    project.mkdir()
    _run(["set-project-path", "--path", str(project)], env)
    result = _run(["set-project-path", "--show"], env)
    assert result.returncode == 0
    assert str(project) in result.stdout
    assert "config" in result.stdout.lower()


def test_env_var_precedence(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    cfg = tmp_path / ".config" / "obk" / "config.toml"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    cfg.write_text(f"project_path = '{tmp_path / 'cfg'}'\n", encoding="utf-8")
    env_path = tmp_path / "env"
    env_path.mkdir()
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


def test_windows_path_env(monkeypatch, tmp_path):
    win_path = "C:\\Projects\\obk"
    (tmp_path / win_path).mkdir()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("OBK_PROJECT_PATH", win_path)
    path = cli.resolve_project_root()
    assert str(path) == win_path


def test_set_project_path_invalid(tmp_path):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT / "src")
    env["HOME"] = str(tmp_path)
    missing = tmp_path / "missing"
    result = _run(["set-project-path", "--path", str(missing)], env)
    assert result.returncode == 1
    assert f"Not a directory: {missing}" in result.stderr


def test_configured_path_missing(monkeypatch, tmp_path, capsys):
    monkeypatch.delenv("OBK_PROJECT_PATH", raising=False)
    monkeypatch.setenv("HOME", str(tmp_path))
    cfg = tmp_path / ".config" / "obk" / "config.toml"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    missing = tmp_path / "nope"
    cfg.write_text(f"project_path = '{missing}'\n", encoding="utf-8")
    with pytest.raises(typer.Exit):
        cli.resolve_project_root()
    err = capsys.readouterr().err
    assert f"Configured project path does not exist: {missing}" in err


def test_validate_all_requires_project_path(tmp_path):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT / "src")
    env["HOME"] = str(tmp_path)
    result = _run(["validate-all"], env)
    assert result.returncode == 1
    assert "No project path configured" in result.stderr
