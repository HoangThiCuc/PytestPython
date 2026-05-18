import time

#import playwright
from playwright.sync_api import Page, Playwright,expect


def test_playwrightBasics(playwright):
    browser = playwright.webkit.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto('https://rahulshettyacademy.com')

def test_playwrightShortCut(page:Page):
    page.goto('https://rahulshettyacademy.com')

def test_coreLocators(page:Page):
    page.goto('https://rahulshettyacademy.com/loginpagePractise/')
    page.get_by_label('Username:').fill("rahulshettyacademy")  #get_by_label only work if the input is wrap inside the label tag
                                                        # or input's id is refered to the "for" atrribute in the label
    page.get_by_label('Password:').fill("Learning@830$3mK2")
    #page.get_by_label('Password:').fill("Learning") # incorrect password
    page.get_by_role("combobox").select_option("teach")
    page.get_by_role("link", name="terms and conditions").click()
    # page.locator("#terms").check() / page.locator(".text-info").check()
    page.get_by_role("button", name="Sign In").click()
    expect(page.get_by_text("Incorrect username/password.")).to_be_visible()
    #time.sleep(5)

def test_firefoxBrowser(playwright:Playwright):
    firefoxBrowser = playwright.firefox.launch(headless=False)
    page = firefoxBrowser.new_page()
    page.goto('https://rahulshettyacademy.com/loginpagePractise/')
    page.get_by_label('Username:').fill("rahulshettyacademy")
    page.get_by_label('Password:').fill("Learning") # incorrect password
    page.get_by_role("combobox").select_option("teach")
    page.get_by_role("link", name="terms and conditions").click()
    page.get_by_role("button", name="Sign In").click()
    expect(page.get_by_text("Incorrect username/password.")).to_be_visible()