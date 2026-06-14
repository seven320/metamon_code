import os

from src import env_loader


def _make_env_files(tmp_path):
    env_dir = tmp_path / "env"
    env_dir.mkdir()
    (env_dir / ".env").write_text("X_FROM=prod\n")
    (env_dir / ".env.dev").write_text("X_FROM=dev\n")


class Test_load_env:
    def test_loads_prod_by_default(self, tmp_path, monkeypatch):
        _make_env_files(tmp_path)
        monkeypatch.chdir(tmp_path)
        monkeypatch.delenv("APP_ENV", raising=False)
        assert env_loader.load_env() == os.path.join("env", ".env")

    def test_loads_dev_when_app_env_dev(self, tmp_path, monkeypatch):
        _make_env_files(tmp_path)
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("APP_ENV", "dev")
        assert env_loader.load_env() == os.path.join("env", ".env.dev")

    def test_non_dev_value_falls_back_to_prod(self, tmp_path, monkeypatch):
        _make_env_files(tmp_path)
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("APP_ENV", "staging")
        assert env_loader.load_env() == os.path.join("env", ".env")

    def test_missing_file_returns_none(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        monkeypatch.delenv("APP_ENV", raising=False)
        assert env_loader.load_env() is None
