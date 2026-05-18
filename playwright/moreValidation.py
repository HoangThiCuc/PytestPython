from datetime import time
from tkinter import dialog

from playwright.sync_api import Page, expect


def test_UICheck(page:Page):
    page.goto('https://rahulshettyacademy.com/AutomationPractice')
    #hide/display placeholder
    expect(page.get_by_placeholder("Hide/Show Example")).to_be_visible()
    page.get_by_role("button",name="Hide").click()
    expect(page.get_by_placeholder("Hide/Show Example")).to_be_hidden()

    #alert box
    page.on("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button",name="Confirm").click()

    # mouse hover
    page.locator("#mousehover").hover()
    page.get_by_role("link",name="Top").click()

    # frame
    pageFrame = page.frame_locator("#courses-iframe")
    pageFrame.get_by_role("link",name="All Access plan").click()
    expect(pageFrame.locator("body")).to_contain_text("Happy Subscibers")

    #Check the price of rice in a table
    page.goto('https://rahulshettyacademy.com/SeleniumPractise/#/offers')
    for i in range(page.locator("th").count()):
        if (page.locator("th").nth(i).filter(has_text="Price")).count() > 0:
            priceColValue = i
            print(f"Price column value is {priceColValue} ")
            break
    riceRow = page.locator("tr").filter(has_text="Rice")
    expect(riceRow.locator("td").nth(priceColValue)).to_have_text("37")
