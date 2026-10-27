from pathlib import Path

from pytest_bdd import given, parsers, scenarios, then, when

from db.client import DbClient
from example.login_page import LoginPage
from gui.driver import GuiDriver

FEATURE_FILE = Path(__file__).resolve().parents[2] / "features" / "example" / "login.feature"
scenarios(str(FEATURE_FILE))


@given("the user opens the login page", target_fixture="login_page")
def open_login_page(driver: GuiDriver) -> LoginPage:
    page = LoginPage(driver)
    page.open_login()
    return page


@when(parsers.parse('the user logs in as "{username}" with password "{password}"'))
def login_user(login_page: LoginPage, username: str, password: str) -> None:
    login_page.login(username, password)


@then(parsers.parse('the flash message "{expected_text}" is displayed'))
def verify_flash_message(login_page: LoginPage, expected_text: str) -> None:
    assert login_page.is_flash_visible()
    assert login_page.get_flash_text() == expected_text

@given(parsers.parse('an active user "{username}" exists in the database'))
def seed_active_user(db_client: DbClient, username: str) -> None:
    db_client.execute(
        "CREATE TABLE IF NOT EXISTS users "
        "(username VARCHAR(50) PRIMARY KEY, is_active BOOLEAN)"
    )
    db_client.execute("DELETE FROM users WHERE username = :u", {"u": username})
    db_client.execute(
        "INSERT INTO users (username, is_active) VALUES (:u, :a)",
        {"u": username, "a": True},
    )


@then(parsers.parse('the user "{username}" is active in the database'))
def verify_user_in_db(db_client: DbClient, username: str) -> None:
    row = db_client.fetch_one(
        "SELECT username, is_active FROM users WHERE username = :u",
        {"u": username},
    )
    assert row is not None
    assert bool(row["is_active"]) is True