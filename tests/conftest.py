from collections.abc import Iterator

import pytest

from config import Settings, get_settings
from gui.driver import GuiDriver
from gui.factory import create_driver


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()

@pytest.fixture
def driver(settings: Settings) -> Iterator[GuiDriver]:
    drv = create_driver(settings)
    yield drv
    drv.close()