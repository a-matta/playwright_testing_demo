from datetime import datetime

import pytest
from faker import Faker
from playwright.sync_api import Page

from .pages.login_page import LoginPage
from .pages.registration_page import RegisterPage
from .pages.userdetails_page import UserDetailsPage

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


def register_user(page: Page, fake_user):
    r = RegisterPage(page)
    r.navigate()
    r.input_username(fake_user["username"])
    r.input_password(fake_user["password"])
    r.input_firstname(fake_user["first_name"])
    r.input_lastname(fake_user["last_name"])
    r.input_phone(fake_user["phone_number"])
    r.submit_registration(fake_user["username"])


def login_user(page: Page, fake_user, success=True):
    l = LoginPage(page)
    l.navigate()
    l.input_username(fake_user["username"])
    l.input_password(fake_user["password"])
    l.login(success=success)


def test_new_user_can_register_and_check_own_data(page: Page, fake_user):
    register_user(page, fake_user)
    login_user(page, fake_user)
    ud = UserDetailsPage(page)
    ud.verify_details(fake_user)


def test_login_fails_if_username_and_password_does_not_match(page: Page, fake_user):
    register_user(page, fake_user)
    login_user(page, fake_user, success=False)
    page.locator("//p[contains(text(), 'You provided incorrect login details')]").is_visible()
