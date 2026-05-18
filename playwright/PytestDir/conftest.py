import pytest

@pytest.fixture(scope='session')
def preSetupWork():
    print("I setup browser instance")
    yield
    print("I teardown browser instance")


@pytest.fixture()
def user_credentials(request):
    request.param