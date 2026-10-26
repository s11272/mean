from gui.driver import GuiDriver


class BasePage:
    def __init__(self, driver: GuiDriver) -> None:
        self.driver = driver

    def open(self, url: str) -> None:
        self.driver.open(url)

    def screenshot(self) -> bytes:
        return self.driver.screenshot() 