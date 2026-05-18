import pytest

@pytest.fixture()
def user_credentials(request):
    request.param