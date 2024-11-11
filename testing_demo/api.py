import base64
import functools
import random

from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from testing_demo.db import get_db

bp = Blueprint("api", __name__, url_prefix="/api")


def login_required(call):
    @functools.wraps(call)
    def wrapped_call(*args, **kwargs):
        error = None
        user = None
        auth = request.authorization
        print("auth request: {}".format(auth))
        if auth:
            user = get_db().execute("SELECT * FROM user WHERE username = ?", (auth.username,)).fetchone()
        if user is None:
            error = "Invalid User"
        elif not check_password_hash(user["password"], auth.password):
            error = "Invalid Authentication"

        if error:
            return jsonify({"status": "FAILURE", "message": error}), 401
        return call(*args, **kwargs)

    return wrapped_call


def token_required(call):
    @functools.wraps(call)
    def wrapped_call(*args, **kwargs):
        headers = request.headers
        if not headers.get("token"):
            return jsonify({"status": "FAILURE", "message": "Token authentication required"}), 401

        tokens = [x[0] for x in get_db().execute("SELECT token FROM user").fetchall()]
        if headers.get("token") in tokens:
            return call(*args, **kwargs)
        else:
            return jsonify({"status": "FAILURE", "message": "Invalid Token"}), 401

    return wrapped_call


@bp.route("/auth/token", methods=(["GET"]))
@login_required
def create_token():
    username = request.authorization.username
    token = str(base64.b64encode(str(random.getrandbits(128)).encode()), "utf-8")
    get_db().execute("UPDATE user SET token = '{}' WHERE username = '{}'".format(token, username))
    get_db().commit()
    return jsonify({"status": "SUCCESS", "token": token}), 200


@bp.route("/users", methods=(["POST"]))
def create_user():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    return create_user(request)


@bp.route("/users", methods=(["GET"]))
@token_required
def users():
    """Fetch all user ids."""
    return get_all_users()


@bp.route("/users/<username>", methods=(["GET", "PUT"]))
@token_required
def username(username):
    if request.method == "GET":
        return get_specific_user(username)
    if request.method == "PUT":
        return put_specific_user(username, request)


def put_specific_user(username, request):
    allowed_fields = ("firstname", "lastname", "phone")
    if not request.is_json:
        return jsonify({"status": "FAILURE", "message": "Bad Request"}), 400

    data = request.get_json()
    print(data)
    db = get_db()
    for key, value in data.items():
        if key not in allowed_fields:
            return jsonify({"status": "FAILURE", "message": "Field update not allowed"}), 403
        db.execute("UPDATE user SET '{}' = '{}' WHERE username = '{}'".format(key, value, username))
    db.commit()
    return jsonify({"status": "SUCCESS", "message": "Updated"}), 201


def get_specific_user(username):
    try:
        query = (
            get_db()
            .execute(
                """SELECT firstname, lastname, phone FROM user
                WHERE username = '{}'""".format(
                    username
                )
            )
            .fetchall()
        )
    except:
        return jsonify({"status": "FAILURE", "message": "user not found"}), 404

    payload = {"firstname": query[0][0], "lastname": query[0][1], "phone": query[0][2]}
    return jsonify({"status": "SUCCESS", "message": "retrieval succesful", "payload": payload}), 200


def get_all_users():
    query = get_db().execute("""SELECT username FROM user""").fetchall()
    users = []
    for item in query:
        users.append(item["username"])
    return jsonify({"status": "SUCCESS", "payload": users}), 200


def create_user(user):
    try:
        validated_user = validate_new_user_data(user)
    except Exception as e:
        return jsonify({"status": "FAILURE", "message": str(e)}), 400
    print(validated_user)
    db = get_db()
    if db.execute("SELECT id FROM user WHERE username = ?", (validated_user["username"],)).fetchone() is not None:
        return jsonify({"status": "FAILURE", "message": "User exists"}), 400
    db.execute(
        """INSERT INTO user (username, password, firstname, lastname, phone)
            VALUES (?, ?, ?, ?, ?)""",
        (
            validated_user["username"],
            generate_password_hash(validated_user["password"]),
            validated_user["firstname"],
            validated_user["lastname"],
            validated_user["phone"],
        ),
    )
    db.commit()
    return jsonify({"status": "SUCCESS", "message": "Created"}), 201


def validate_new_user_data(user):
    allowed_fields = ("username", "password", "firstname", "lastname", "phone")
    if not user.is_json:
        raise AssertionError("Bad request")
    user = user.get_json()
    for key, value in user.items():
        if key not in allowed_fields:
            raise AssertionError("Invalid field")
    for field in allowed_fields:
        if field not in user:
            raise AssertionError("Field missing")
    return user
