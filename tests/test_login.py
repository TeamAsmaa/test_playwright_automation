import pytest
from playwright.sync_api import sync_playwright, Page
from pages.login_page import LoginPage

# -----------------------------
# Test: Successful login
# -----------------------------
def test_login_success(page: Page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("CV_teacher1", "123456")

    # Assert dashboard loaded
    assert page.url == "https://codingville-staging.rgp-dev.com/teacher/dashboard"
    print("Login successful")

# -----------------------------
# Test: Invalid credentials
# -----------------------------
def test_login_invalid_credentials(page: Page):
    login_page = LoginPage(page)
    login_page.navigate()

    # Expect RuntimeError for failed login
    with pytest.raises(RuntimeError) as e:
        login_page.login("wrong_user", "wrong_pass")

    assert "Login failed" in str(e.value)
    print("Invalid credentials correctly blocked")