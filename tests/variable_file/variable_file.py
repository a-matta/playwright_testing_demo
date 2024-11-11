import json
import logging
import pathlib
from os import path
from typing import Any

from .env_vars import target_environment

TESTS_FOLDER = (pathlib.Path(__file__) / ".." / "..").resolve().as_posix()
TARGET_ENVIRONMENTS = ("dev", "local")


def get_variables() -> dict[str, Any]:
    """Read common variables, patch them with target environment variables and return them"""
    variables = _common_vars()
    variables.update(_get_env_config())
    return variables


def _get_env_config() -> dict[str, Any]:
    """Read the variables from the target environment configuration file"""
    environment = target_environment()
    if environment not in TARGET_ENVIRONMENTS:
        raise ValueError(f"Target environment should be in {TARGET_ENVIRONMENTS}")
    return _get_config(environment)


def _common_vars() -> dict[str, Any]:
    """Read the common variables applicable to all environments"""
    return _get_config("common")


def _get_config(config_name: str) -> dict[str, Any]:
    """Loads the file with given config name as json and returns the dictionary"""
    file_path = path.abspath(path.join(TESTS_FOLDER, "config", f"{config_name}.json"))
    logging.info(f"loading file {file_path}")
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)
