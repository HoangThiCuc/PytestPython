import pytest


@pytest.fixture(scope='module')
def preWork():
    print("I setup module instance")
    return "pass"

@pytest.fixture(scope='function')
def secondPreWork():
    print("I setup function instance")
    yield
    print("tear down validation")

@pytest.mark.smoke
def test_secondCheck(preWork, secondPreWork):
    print('test 2')

@pytest.mark.skip
def test_thirdCheck(preWork):
    print('test 3')
    assert preWork == "pahss"