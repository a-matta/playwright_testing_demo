import re

from playwright.sync_api import Page, expect

from ..environment import base_url


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username = page.locator("#username")
        self.password = page.locator("#password")
        self.login_button = page.locator("//input[@type='submit' and @value='Log In']")
        self.logout_button = page.locator("//a[@href='/logout' and text()='Log Out']")

    def navigate(self):
        self.page.goto(f"{base_url}/login")
        expect(self.page).to_have_title(re.compile("Log In - Demo App"))

    def input_username(self, username):
        self.username.fill(username)

    def input_password(self, password):
        self.password.fill(password)

    def login(self, success=True):
        self.login_button.click()
        if success:
            self.logout_button.is_visible()
