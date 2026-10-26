from config import Settings
from gui.driver import GuiDriver
from gui.playwright_driver import PlaywrightDriver
from gui.selenium_driver import SeleniumDriver


def create_driver(settings: Settings) -> GuiDriver:
    engine = settings.gui_engine.lower()
    if engine == "playwright":
        return PlaywrightDriver(headless=settings.headless)
    if engine == "selenium":
        return SeleniumDriver(headless=settings.headless)
    raise ValueError(f"Unsupported GUI engine: {settings.gui_engine}")