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
    r.submit_registration()
    return r


def login_user(page: Page, fake_user):
    l = LoginPage(page)
    l.navigate()
    l.input_username(fake_user["username"])
    l.input_password(fake_user["password"])
    l.login()
    return l


def test_new_user_can_register_and_check_own_data(page: Page, fake_user):
    r = register_user(page, fake_user)
    r.verify_registration_success(fake_user["username"])
    l = login_user(page, fake_user)
    l.verify_login_success()
    ud = UserDetailsPage(page)
    ud.verify_details(fake_user)


def test_login_fails_if_username_and_password_does_not_match(page: Page, fake_user):
    r = register_user(page, fake_user)
    r.verify_registration_success(fake_user["username"])
    l = login_user(page, {**fake_user, "password": "invalid-password"})
    l.verify_login_failure()


def test_duplicate_username_registration_is_not_allowed(page: Page, fake_user):
    register_user(page, fake_user)
    r = register_user(page, fake_user)
    r.verify_registration_error_username_is_registered(fake_user["username"])
