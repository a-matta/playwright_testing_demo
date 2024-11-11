import base64
import logging

from playwright.sync_api import APIRequestContext


def get_auth_token(api_request_context: APIRequestContext, username: str, password: str):
    """Fetch authorisation token and return the JSON response"""
    auth_header = "Basic " + base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("utf-8")
    response = api_request_context.get(
        "./auth/token",
        headers={"content-type": "application/json", "Authorization": auth_header},
    ).json()
    logging.info(response)
    return response


def create_user(api_request_context: APIRequestContext, user):
    """Create a user and return the JSON response"""
    response = api_request_context.post(
        "./users",
        data=user,
        headers={"content-type": "application/json"},
    ).json()
    logging.info(response)
    return response


def get_user_details(api_request_context: APIRequestContext, token: str, username: str):
    """Get user details and return the JSON response"""
    url = f"./users/{username}"
    response = api_request_context.get(
        url,
        headers={"Token": token},
    ).json()
    logging.info(response)
    return response


def get_all_users(api_request_context: APIRequestContext, token: str):
    """Get all users and return the JSON response"""
    url = f"./users"
    response = api_request_context.get(
        url,
        headers={"Token": token},
    ).json()
    logging.info(response)
    return response


def update_user(api_request_context: APIRequestContext, token: str, username: str, **data):
    """Update the user and return the JSON response"""
    url = f"./users/{username}"
    response = api_request_context.put(
        url,
        headers={"Token": token, "content-type": "application/json"},
        data=data,
    ).json()
    logging.info(response)
    return response
