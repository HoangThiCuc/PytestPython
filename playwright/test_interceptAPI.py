import pytest
from playwright.sync_api import Playwright, expect

from Utils.apiBase import APIUtils

fakePayload = {"data" : [], "message" : "No Orders"}

def intercep_response(route):
    route.fulfill(json = fakePayload)

def intercep_request(route):
    route.continue_(url="https://rahulshettyacademy.com/api/ecom/order/get-orders-for-customer/6711dcafae2afd4c0b9f6b66")

def test_interceptAPI(playwright:Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto('https://rahulshettyacademy.com/client')
    #page.route("https://rahulshettyacademy.com/api/ecom/order/get-orders-for-customer/*", intercep_response)
    page.route("https://rahulshettyacademy.com/api/ecom/order/get-orders-for-customer?id=*", intercep_request)
    page.get_by_placeholder('email@example.com').fill('rahulshetty@gmail.com')
    page.get_by_placeholder('enter your passsword').fill('Iamking@000')
    page.get_by_role('button', name='Login').click()
    page.get_by_role('button', name='ORDERS').click()
    #orderText = page.locator(".mt-4").text_content()
    #print(orderText)
    page.get_by_role('button', name='View').first.click()
    oderID = page.locator(".col-title")
    expect(oderID).to_contain_text("Order Id")

def test_session_storage(playwright:Playwright):
    apiUtils = APIUtils()
    token = apiUtils.get_token(playwright)

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    # script to inject token into session local storate
    page.add_init_script(f"localStorage.setItem('token', '{token}')")
    page.goto('https://rahulshettyacademy.com/client')
    page.get_by_role('button', name='ORDERS').click()
    expect(page.get_by_text("Your Orders"))
    expect(page.get_by_text("Your Orders")).to_be_visible()



