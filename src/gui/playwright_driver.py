from playwright.sync_api import sync_playwright

from gui.driver import GuiDriver


class PlaywrightDriver(GuiDriver):
    def __init__(self, headless: bool = True) -> None:
        self._pw = sync_playwright().start()
        self._browser = self._pw.chromium.launch(headless=headless)
        self._page = self._browser.new_page()

    def open(self, url: str) -> None:
        self._page.goto(url)

    def click(self, selector: str) -> None:
        self._page.click(selector)

    def fill(self, selector: str, value: str) -> None:
        self._page.fill(selector, value)

    def get_text(self, selector: str) -> str:
        return self._page.locator(selector).inner_text()

    def is_visible(self, selector: str) -> bool:
        return self._page.locator(selector).is_visible()

    def screenshot(self) -> bytes:
        return self._page.screenshot()

    def close(self) -> None:
        self._browser.close()
        self._pw.stop()