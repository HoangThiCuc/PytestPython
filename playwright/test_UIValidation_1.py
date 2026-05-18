from playwright.sync_api import Page, expect


def test_UIValidationDynamicScript(page:Page):
    #iphone X, Nokia Edge -> verify 2 items are showing in cart
    page.goto('https://rahulshettyacademy.com/loginpagePractise/')
    page.get_by_label('Username:').fill("rahulshettyacademy")
    page.get_by_label('Password:').fill("Learning@830$3mK2")
    page.get_by_role("combobox").select_option("teach")
    page.get_by_role("link", name="terms and conditions").click()
    page.get_by_role("button", name="Sign In").click()
    iphoneProduct = page.locator("app-card").filter(has_text="iphone X")
    iphoneProduct.get_by_role("button", name="Add").click()
    nokiaProduct = page.locator("app-card").filter(has_text="Nokia Edge")
    nokiaProduct.get_by_role("button", name="Add").click()
    page.get_by_text(" Checkout").click()
    expect(page.locator(".media-body")).to_have_count(2)

def test_childWindowHandle(page:Page):
    page.goto('https://rahulshettyacademy.com/loginpagePractise/')
    with page.expect_popup() as newPage_info:
        #page.locator(".blinkingText").click()
        page.get_by_role("link", name="Free Access to InterviewQues/").click()
        childPage = newPage_info.value
        text = childPage.locator(".red").text_content()
        print(text)
        word = text.split("at")
        email = word[1].strip().split(" ")[0]
        assert email == "mentor@rahulshettyacademy.com"