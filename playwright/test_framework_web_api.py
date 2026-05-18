import json
import pytest
from playwright.sync_api import Playwright

from Utils.apiBase import APIUtils
from pageObjects.LoginPage import LoginPage

# json file -> until -> access into test
with open('data/credentials.json') as f:
    test_data = json.load(f)
    user_credentials_list = test_data['user_credentials']


@pytest.mark.parametrize('user_credentials', user_credentials_list)
def test_e2e_web_api(playwright: Playwright, browserInstance, user_credentials):
    # browser = playwright.chromium.launch(headless=False)
    # context = browser.new_context()
    # page = context.new_page()

    userEmail = user_credentials["userEmail"]
    userPassword = user_credentials["password"]
    # create an order -> get order ID
    apiUtils = APIUtils()
    orderId = apiUtils.createOrder(playwright, user_credentials)
    #login

    loginPage = LoginPage(browserInstance)

    loginPage.navigateToLoginPage()
    dashboardPage = loginPage.login(userEmail, userPassword)

    #Verify order
    orderPage = dashboardPage.selectOrderNavLink()
    orderDetail = orderPage.viewOrder(orderId)
    orderDetail.getOrderDetail()