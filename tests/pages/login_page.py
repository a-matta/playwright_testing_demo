import re

from playwright.sync_api import Page, expect

from ..global_vars import base_url


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username = page.locator("#username")
        self.password = page.locator("#password")
        self.login_button = page.locator("//input[@type='submit' and @value='Log In']")
        self.logout_button = page.locator("//a[@href='/logout' and text()='Log Out']")
        self.incorrect_login = page.locator("//p[contains(text(), 'You provided incorrect login details')]")

    def navigate(self):
        self.page.goto(f"{base_url}/login")
        expect(self.page).to_have_title(re.compile("Log In - Demo App"))

    def input_username(self, username):
        self.username.fill(username)

    def input_password(self, password):
        self.password.fill(password)

    def login(self):
        self.login_button.click()

    def verify_login_success(self):
        self.logout_button.is_visible()
        expect(self.incorrect_login).not_to_be_visible()

    def verify_login_failure(self):
        expect(self.logout_button).not_to_be_visible()
        self.incorrect_login.is_visible()
