import playwright
import pytest
from pytest_bdd import given, when, then, parsers, scenarios

from Utils.apiBase import APIUtils
from pageObjects.LoginPage import LoginPage

scenarios('features/orderTransaction.feature')

@pytest.fixture
def shared_data():
    return{}

@given(parsers.parse('place the item order with {username} and {password}'))
def place_item_order(playwright, username, password, shared_data):
    apiUtils = APIUtils()
    user_credentials = {}
    user_credentials['userEmail'] = username
    user_credentials['password'] = password
    orderId = apiUtils.createOrder(playwright, user_credentials)
    shared_data['order_id'] = orderId

@given('the user is on landing page')
def user_on_landing_page(browserInstance, shared_data):
    loginPage = LoginPage(browserInstance)
    loginPage.navigateToLoginPage()
    shared_data['login_page'] = loginPage

@when(parsers.parse('I login to portal with {username} and {password}'))
def login_to_portal(username, password, shared_data):
    login_page = shared_data['login_page']
    dashboardPage = login_page.login(username, password)
    shared_data['dashboard_page'] = dashboardPage

@when('navigate to orders page')
def navigate_to_order_page(shared_data):
    dashboardPage = shared_data['dashboard_page']
    orderPage = dashboardPage.selectOrderNavLink()
    shared_data['order_page'] = orderPage


@when('select the orderID')
def select_order_id(shared_data):
    orderPage = shared_data['order_page']
    orderId = shared_data['order_id']
    orderDetail = orderPage.viewOrder(orderId)
    shared_data['order_detail'] = orderDetail

@then('order message is successfuly displayed')
def order_message_successfully_displayed(shared_data):
    orderDetail = shared_data['order_detail']
    orderDetail.getOrderDetail()