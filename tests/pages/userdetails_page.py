import re

from playwright.sync_api import Page, expect

base_url = "http://127.0.0.1:8080"


class UserDetailsPage:
    def __init__(self, page: Page):
        self.page = page
        self.info_username = page.locator("//td[@id='username']")
        self.info_firstname = page.locator("//td[@id='firstname']")
        self.info_lastname = page.locator("//td[@id='lastname']")
        self.info_phone = page.locator("//td[@id='phone']")

    def verify_details(self, user):
        expect(self.page).to_have_url(f"{base_url}/user")
        expect(self.info_username).to_have_text(user["username"])
        expect(self.info_firstname).to_have_text(user["first_name"])
        expect(self.info_lastname).to_have_text(user["last_name"])
        expect(self.info_phone).to_have_text(user["phone_number"])
