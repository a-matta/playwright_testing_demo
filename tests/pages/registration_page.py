import re

from playwright.sync_api import Page, expect

base_url = "http://127.0.0.1:8080"


class RegisterPage:
    def __init__(self, page: Page):
        self.page = page
        self.register_link = page.locator("//a[@href='/register' and text()='Register']")
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.firstname_input = page.locator("#firstname")
        self.lastname_input = page.locator("#lastname")
        self.phone_input = page.locator("#phone")
        self.register_submit = page.locator("//input[@type='submit' and @value='Register']")

    def navigate(self):
        self.page.goto(base_url)
        expect(self.page).to_have_title(re.compile("index page - Demo App"))
        self.register_link.click()

    def input_username(self, username):
        self.username_input.fill(username)

    def input_password(self, password):
        self.password_input.fill(password)

    def input_firstname(self, firstname):
        self.firstname_input.fill(firstname)

    def input_lastname(self, lastname):
        self.lastname_input.fill(lastname)

    def input_phone(self, phone):
        self.phone_input.fill(phone)

    def submit_registration(self):
        self.register_submit.click()
