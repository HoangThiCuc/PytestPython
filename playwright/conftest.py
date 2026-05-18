import pytest

@pytest.fixture()
def user_credentials(request):
    request.param


def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="chrome", help="Browser name for testing")
    #parser.addoption("--url_name", action="store", default="https://rahulshettyacademy.com/client", help="URL for testing")


@pytest.fixture
def browserInstance(playwright, request):
    browser_name = request.config.getoption("--browser_name")
    #url_name = request.config.getoption("url_name")
    if browser_name == "chrome":
        browser = (playwright.chromium.launch(headless=False))
    elif browser_name == "firefox":
        browser = (playwright.firefox.launch(headless=False))
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")
    context = browser.new_context()
    page = context.new_page()
    #page.goto(url_name)
    yield page
    context.close()
    browser.close()
