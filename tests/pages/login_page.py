import re

from playwright.sync_api import Page, expect

base_url = "http://127.0.0.1:8080"


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username = page.locator("#username")
        self.password = page.locator("#password")
        self.login_button = page.locator("//input[@type='submit' and @value='Log In']")

    def navigate(self):
        self.page.goto(f"{base_url}/login")
        expect(self.page).to_have_title(re.compile("Log In - Demo App"))

    def input_username(self, username):
        self.username.fill(username)

    def input_password(self, password):
        self.password.fill(password)

    def login(self):
        self.login_button.click()
