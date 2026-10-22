import pytest

from config import Settings


def test_settings_loaded(settings: Settings) -> None:
    assert isinstance(settings, Settings)
    assert settings.verify_ssl is True


def test_env_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("VERIFY_SSL", "false")
    custom_cfg = Settings()
    assert custom_cfg.verify_ssl is False
