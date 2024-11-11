import pathlib
import subprocess
from importlib.metadata import version

from invoke import task

ROOT = pathlib.Path(__file__).parent.resolve().as_posix()
VERSION = version("testing_demo")


@task
def clean(context):
    """Clean the root folder. Remove all generated files/directories"""
    cmd = [
        "rm",
        "-rf",
        f"{ROOT}/.pytest_cache",
        f"{ROOT}/pytest.log",
        f"{ROOT}/report",
        f"{ROOT}/test-results",
    ]
    subprocess.run(" ".join(cmd), shell=True, check=False)


@task(pre=[clean])
def tests(context, headed=False, browser="chromium", slow_mo="0", tracing=False, video=False):
    """Run the tests in 'tests' directory.

    Args:
        headed: Run the tests in headed mode. Defaults to headless mode.
        browser: Browser to run the tests. Defaults to "chromium".
        slow_mo: Whether to run the tests in slow motion. Disabled by default.
        tracing: Whether to record a trace for failing test. Disabled by default.
        video: Whether to record a video for failing test. Disabled by default.
    """
    cmd = [
        "pytest",
        "--headed" if headed else "",
        f"--browser {browser}",
        f"--slowmo={slow_mo}",
        "--tracing=retain-on-failure" if tracing else "",
        "--video=retain-on-failure" if video else "",
        f"{ROOT}/tests",
    ]
    subprocess.run(" ".join(cmd), shell=True, check=True)


@task()
def init_db(context):
    """Initialize the DB"""
    cmd = ["flask", "--app", "testing_demo", "init-db"]
    subprocess.run(" ".join(cmd), shell=True, check=True)


@task(pre=[init_db])
def app(context):
    """Run the Flask app."""
    cmd = ["flask", "--app", "testing_demo", "run", "--host=0.0.0.0", "--port=8080"]
    subprocess.run(" ".join(cmd), shell=True, check=True)
