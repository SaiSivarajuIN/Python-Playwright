import base64
import configparser
import logging
import os
import pytest
import pytest_html

# Ensure project root is on sys.path so `pageObjects` can be imported
# regardless of how pytest is invoked (cwd, pythonpath, etc.)

config = configparser.ConfigParser()
config.read("properties.ini")

url = config["settings"]["url"]


@pytest.fixture(scope="function", autouse=True)
def log_test_status(request):
    """
    An autouse fixture to automatically log the status of each test.
    """
    logging.info(f"--- Starting test: {request.node.name} ---")
    yield

    setup_report = getattr(request.node, "rep_setup", None)
    call_report = getattr(request.node, "rep_call", None)
    if (setup_report and setup_report.failed) or (call_report and call_report.failed):
        logging.error(f"--- Test finished: {request.node.name} [FAILED] ---")
    else:
        logging.info(f"--- Test finished: {request.node.name} [PASSED] ---")


@pytest.fixture(scope="session")
def testData(request):
    return request.param


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when != "call" or not rep.failed:
        return

    if pytest_html is None:
        return

    page = getattr(item, "_page", None)
    if page is None and "browserInstance" in getattr(item, "funcargs", {}):
        page = item.funcargs["browserInstance"]

    if page is None:
        return

    try:
        report_path = item.config.getoption("htmlpath") or "reports/report.html"
        screenshot_dir = os.path.join(os.path.dirname(report_path) or ".", "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)
        safe_name = item.nodeid.replace("::", "_").replace("/", "_").replace("\\", "_").replace(" ", "_")
        screenshot_file = os.path.join(screenshot_dir, f"{safe_name}.png")
        page.screenshot(path=screenshot_file, full_page=True)

        with open(screenshot_file, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode("utf-8")

        extras = list(getattr(rep, "extras", []))
        extras.append(pytest_html.extras.image(f"data:image/png;base64,{encoded}", name="Failure Screenshot"))
        rep.extras = extras
    except Exception:
        logging.exception("Failed to capture screenshot for %s", item.nodeid)


def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="chrome", help="select the browsr")


@pytest.fixture
def browserInstance(request):
    from playwright.sync_api import sync_playwright

    browser_name = request.config.getoption("--browser_name")

    with sync_playwright() as playwright:
        if browser_name == "chrome":
            browser = playwright.chromium.launch(headless=True)
        elif browser_name == "firefox":
            browser = playwright.firefox.launch(headless=False)
        elif browser_name == "edge":
            browser = playwright.chromium.launch(channel="msedge", headless=False)
        elif browser_name == "webKit":
            browser = playwright.webkit.launch(headless=False)
        else:
            # default fallback
            browser = playwright.chromium.launch(headless=False)

        new_context = browser.new_context()
        # start tracing for this context
        try:
            new_context.tracing.start(screenshots=True, snapshots=True, sources=True)
        except Exception:
            # tracing may not be supported in older playwright versions; continue without tracing
            pass

        page = new_context.new_page()
        request.node._page = page
        page.goto(url)
        yield page

        # ensure test-results dir exists and export trace
        try:
            os.makedirs("test-results", exist_ok=True)
            trace_path = f"test-results/{request.node.name}-trace.zip"
            new_context.tracing.stop(path=trace_path)
        except Exception:
            # if tracing was not started or export fails, log and continue teardown
            logging.warning("Tracing export failed or not supported.")

        new_context.close()
        browser.close()
