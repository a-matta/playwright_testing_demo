import re
from datetime import datetime

import pytest
from faker import Faker
from playwright.sync_api import Page, expect

fake = Faker()


@pytest.fixture
def fake_user():
    return {
        "username": str(datetime.now().timestamp()).replace(".", ""),
        "password": fake.password(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "phone_number": fake.phone_number(),
    }


base_url = "http://127.0.0.1:8080"

ui_elements = {
    "input_username": "#username",
    "input_password": "#password",
    "input_firstname": "#firstname",
    "input_lastname": "#lastname",
    "input_phone": "#phone",
    "button_register": "//input[@type='submit' and @value='Register']",
    "button_login": "//input[@type='submit' and @value='Log In']",
    "button_logout": "//a[@href='/logout' and text()='Log Out']",
    "info_username": "//td[@id='username']",
    "info_firstname": "//td[@id='firstname']",
    "info_lastname": "//td[@id='lastname']",
    "info_phone": "//td[@id='phone']",
}


def register_user(page: Page, fake_user):
    page.goto(base_url)

    expect(page).to_have_title(re.compile("index page - Demo App"))

    page.locator("//a[@href='/register' and text()='Register']").click()
    page.locator(ui_elements["input_username"]).fill(fake_user["username"])
    page.locator(ui_elements["input_password"]).fill(fake_user["password"])
    page.locator(ui_elements["input_firstname"]).fill(fake_user["first_name"])
    page.locator(ui_elements["input_lastname"]).fill(fake_user["last_name"])
    page.locator(ui_elements["input_phone"]).fill(fake_user["phone_number"])
    page.locator(ui_elements["button_register"]).click()

    error = f"User {fake_user["username"]} is already registered."
    error_element = f"//div[@class='flash' and contains(text(), '{error}')]"
    expect(page.locator(error_element)).not_to_be_visible()


def test_new_user_can_register_and_check_own_data(page: Page, fake_user):
    register_user(page, fake_user)

    assert page.url == f"{base_url}/login"
    expect(page).to_have_title(re.compile("Log In - Demo App"))
    page.locator(ui_elements["input_username"]).fill(fake_user["username"])
    page.locator(ui_elements["input_password"]).fill(fake_user["password"])
    page.locator(ui_elements["button_login"]).click()
    page.locator(ui_elements["button_logout"]).is_visible()

    expect(page).to_have_url(f"{base_url}/user")
    expect(page.locator(ui_elements["info_username"])).to_have_text(fake_user["username"])
    expect(page.locator(ui_elements["info_firstname"])).to_have_text(fake_user["first_name"])
    expect(page.locator(ui_elements["info_lastname"])).to_have_text(fake_user["last_name"])
    expect(page.locator(ui_elements["info_phone"])).to_have_text(fake_user["phone_number"])


def test_login_fails_if_username_and_password_does_not_match(page: Page, fake_user):
    register_user(page, fake_user)

    assert page.url == f"{base_url}/login"
    expect(page).to_have_title(re.compile("Log In - Demo App"))
    page.locator(ui_elements["input_username"]).fill(fake_user["username"])
    page.locator(ui_elements["input_password"]).fill("invalid-password")
    page.locator(ui_elements["button_login"]).click()
    page.locator("//p[contains(text(), 'You provided incorrect login details')]").is_visible()
