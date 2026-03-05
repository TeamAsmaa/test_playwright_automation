from playwright.sync_api import Playwright
from pages.login_page import LoginPage


def test_auth_setup(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("CV_teacher1", "123456")

    # # Save authenticated state
    # context.storage_state(path="storage_state.json")

    browser.close()