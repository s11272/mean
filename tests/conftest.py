import pytest
from config import Settings, get_settings


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()