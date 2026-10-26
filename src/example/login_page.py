from pathlib import Path

from pages.base_page import BasePage


class LoginPage(BasePage):
    DEMO_URL = (Path(__file__).resolve().parent / "demo_login.html").as_uri()

    USERNAME_INPUT = "//input[@id='username']"
    PASSWORD_INPUT = "//input[@id='password']"
    SUBMIT_BTN = "//button[@id='login-btn']"
    FLASH_MSG = "//div[@id='flash']"

    def open_login(self) -> None:
        self.open(self.DEMO_URL)

    def login(self, username: str, password: str) -> None:
        self.driver.fill(self.USERNAME_INPUT, username)
        self.driver.fill(self.PASSWORD_INPUT, password)
        self.driver.click(self.SUBMIT_BTN)

    def get_flash_text(self) -> str:
        return self.driver.get_text(self.FLASH_MSG)

    def is_flash_visible(self) -> bool:
        return self.driver.is_visible(self.FLASH_MSG)