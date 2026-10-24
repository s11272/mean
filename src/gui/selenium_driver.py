from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from src.gui.driver import GuiDriver


class SeleniumDriver(GuiDriver):
    def __init__(self, headless: bool = True) -> None:
        opts = Options()
        if headless:
            opts.add_argument("--headless=new")
        self._driver = webdriver.Chrome(options=opts)
        self._driver.implicitly_wait(5)

    def open(self, url: str) -> None:
        self._driver.get(url)

    def click(self, selector: str) -> None:
        self._driver.find_element(By.XPATH, selector).click()

    def fill(self, selector: str, value: str) -> None:
        el = self._driver.find_element(By.XPATH, selector)
        el.clear()
        el.send_keys(value)

    def get_text(self, selector: str) -> str:
        return self._driver.find_element(By.XPATH, selector).text

    def is_visible(self, selector: str) -> bool:
        els = self._driver.find_elements(By.XPATH, selector)
        return bool(els and els[0].is_displayed())

    def screenshot(self) -> bytes:
        return self._driver.get_screenshot_as_png()

    def close(self) -> None:
        self._driver.quit()