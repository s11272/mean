from collections.abc import Iterator

import pytest
from sqlalchemy import Engine, create_engine

from config import Settings, get_settings
from db.client import DbClient
from gui.driver import GuiDriver
from gui.factory import create_driver
from integrations.qtest.plugin import QTestPlugin


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()

@pytest.fixture
def driver(settings: Settings) -> Iterator[GuiDriver]:
    drv = create_driver(settings)
    yield drv
    drv.close()

@pytest.fixture(scope="session")
def db_engine(settings: Settings) -> Iterator[Engine]:
    engine = create_engine(settings.db_url)
    yield engine
    engine.dispose()

@pytest.fixture
def db_client(db_engine: Engine) -> DbClient:
    return DbClient(db_engine)

def pytest_configure(config: pytest.Config) -> None:
    settings = get_settings()
    config.pluginmanager.register(QTestPlugin(settings), "qtest_plugin")