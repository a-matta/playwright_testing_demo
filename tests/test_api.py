import base64
import logging
from typing import Generator

import pytest
from playwright.sync_api import APIRequestContext, Playwright

from .environment import base_url
from .libraries.api_utils import create_user, get_all_users, get_auth_token, get_user_details, update_user


@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    request_context = playwright.request.new_context(base_url=f"{base_url}/api/")
    yield request_context
    request_context.dispose()


def test_new_user_can_be_registered_and_its_data_fetched(fake_user, api_request_context: APIRequestContext):
    response = create_user(api_request_context, fake_user)
    assert response["status"] == "SUCCESS"
    response = get_auth_token(api_request_context, fake_user["username"], fake_user["password"])
    token = response["token"]
    expected = {
        "firstname": fake_user["firstname"],
        "lastname": fake_user["lastname"],
        "phone": fake_user["phone"],
    }
    response = get_user_details(api_request_context, token, fake_user["username"])
    assert response["status"] == "SUCCESS"
    assert response["payload"] == expected


def test_token_fetching_fails_if_username_passwords_do_not_match(fake_user, api_request_context: APIRequestContext):
    response = create_user(api_request_context, fake_user)
    assert response["status"] == "SUCCESS"
    response = get_auth_token(api_request_context, fake_user["username"], "invalid_password")
    assert response["status"] == "FAILURE"


def test_duplicate_username_registration_is_not_allowed(fake_user, api_request_context: APIRequestContext):
    response = create_user(api_request_context, fake_user)
    assert response["status"] == "SUCCESS"

    new_user = {
        "username": fake_user["username"],
        "password": "password",
        "firstname": "firstname",
        "lastname": "lastname",
        "phone": "11111111",
    }
    response = create_user(api_request_context, new_user)
    assert response["status"] == "FAILURE"
    assert response["message"] == "User exists"


def test_user_details_cannot_be_fetched_without_token(fake_user, api_request_context: APIRequestContext):
    response = create_user(api_request_context, fake_user)
    assert response["status"] == "SUCCESS"
    response = get_user_details(api_request_context, "", fake_user["username"])
    assert response["status"] == "FAILURE"
    assert response["message"] == "Token authentication required"


def test_users_list_cannot_be_fetched_without_token(api_request_context: APIRequestContext):
    response = get_all_users(api_request_context, "")
    assert response["status"] == "FAILURE"
    assert response["message"] == "Token authentication required"


def test_users_list_contains_newly_created_user(fake_user, api_request_context: APIRequestContext):
    response = create_user(api_request_context, fake_user)
    assert response["status"] == "SUCCESS"
    response = get_auth_token(api_request_context, fake_user["username"], fake_user["password"])
    token = response["token"]
    response = get_all_users(api_request_context, token)
    assert response["status"] == "SUCCESS"
    assert fake_user["username"] in response["payload"]


def test_user_information_can_be_updated(fake_user, api_request_context: APIRequestContext):
    response = create_user(api_request_context, fake_user)
    assert response["status"] == "SUCCESS"
    response = get_auth_token(api_request_context, fake_user["username"], fake_user["password"])
    token = response["token"]
    response = update_user(
        api_request_context,
        token,
        fake_user["username"],
        firstname="firstname",
        lastname="lastname",
        phone="11111111",
    )
    assert response["status"] == "SUCCESS"
    expected = {
        "firstname": "firstname",
        "lastname": "lastname",
        "phone": "11111111",
    }
    response = get_user_details(api_request_context, token, fake_user["username"])
    assert response["status"] == "SUCCESS"
    assert response["payload"] == expected
