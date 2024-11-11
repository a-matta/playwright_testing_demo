import os


def target_environment() -> str:
    """Read the environment variable 'TARGET_ENVIRONMENT'. If not found use 'local'"""
    return os.getenv("TARGET_ENVIRONMENT", "local")
