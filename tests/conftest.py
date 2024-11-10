from pathlib import Path

import pytest
from slugify import slugify


# Attach screenshots to the pytest-html report
# https://stackoverflow.com/questions/71418173/pytests-html-reporter-doesnt-take-show-screenshot-in-the-test-reports-for-pyte/71428174#71428174
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield

    report_dir = "report"  # The directory where the pytest-html report is stored
    screenshots = "screenshots"  # The directory inside report_dir where the screenshots are stored
    Path(f"{report_dir}/{screenshots}").mkdir(exist_ok=True, parents=True)

    report = outcome.get_result()
    extra = getattr(report, "extras", [])
    if report.when == "call":
        screenshot_file_name = f"{slugify(item.nodeid)}.png"
        if report.failed and "page" in item.funcargs:
            page = item.funcargs["page"]
            # absolute path is needed to dump the screenshot
            page.screenshot(path=f"{report_dir}/{screenshots}/{screenshot_file_name}")
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            # add the screenshots to the html report. use path relative to screenshot
            extra.append(pytest_html.extras.png(f"{screenshots}/{screenshot_file_name}"))
        report.extras = extra
