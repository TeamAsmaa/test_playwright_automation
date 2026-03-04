from playwright.sync_api import Page, expect, TimeoutError

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://codingville-staging.rgp-dev.com/auth/login"
        self.username_input = page.get_by_role("textbox", name="Email/Username")
        self.password_input = page.get_by_role("textbox", name="Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.ok_button = page.get_by_role("button", name="Ok")

    def navigate(self):
        self.page.goto(self.url)

    def login(self, username: str, password: str) -> None:
        """
        Fill credentials, submit, handle the 'Ok' popup if it appears,
        and wait for dashboard redirect.
        """
        # Wait for form to be ready
        self.username_input.wait_for(state="visible", timeout=20000)
        self.username_input.fill(username)
        
        self.password_input.fill(password)
        
        self.login_button.click()

        try:
            # First try: direct redirect to dashboard
            self.page.wait_for_url(
                "https://codingville-staging.rgp-dev.com/teacher/dashboard",
                timeout=25000
            )
            print("→ Dashboard loaded directly")
            return

        except TimeoutError:
            # If no direct redirect → check for 'Ok' button
            try:
                expect(self.ok_button).to_be_visible(timeout=12000)
                print("→ Ok button appeared — clicking it")
                self.ok_button.click()

                # After clicking Ok → wait again for dashboard
                self.page.wait_for_url(
                    "https://codingville-staging.rgp-dev.com/teacher/dashboard",
                    timeout=15000
                )
                print("→ Dashboard loaded after clicking Ok")
                return

            except Exception as e:
                self.page.screenshot(path="login-failed.png")
                raise RuntimeError(
                    "Login failed:\n"
                    "- No dashboard redirect\n"
                    "- Could not find or click 'Ok' button\n"
                    f"Current URL: {self.page.url}"
                ) from e


