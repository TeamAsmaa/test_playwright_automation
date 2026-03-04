from playwright.sync_api import Page, expect
import re

class AIPredictorLabPage:
    def __init__(self, page: Page):
        self.page = page

        # Main mission elements
        self.mission_heading = page.get_by_role("heading", name="Mission Instructions")
        self.continue_button = page.get_by_role("button", name="Continue")
        self.navbar_settings = page.locator(".navbar__setting-container")
        self.settings_button = page.locator("#navbar-setting-popover").get_by_role(
            "button"
        )

        # Mission action buttons
        self.show_model_answer_button = page.get_by_role(
            "button", name="Show Model Answer"
        )
        self.run_button = page.get_by_role("button", name="Run ", exact=True)
        self.finish_button = page.locator("#finish-mission-btn")

        # Final page
        self.congratulations_heading = page.get_by_role(
            "heading", name="Congratulations!"
        )

    def navigate(self, mission_url: str):
        # Wait until navigation completes (HTML ready)
        self.page.goto(mission_url, wait_until="domcontentloaded", timeout=90000)
        # Now wait for mission content (UI rendered)
        expect(self.mission_heading).to_be_visible(timeout=120000)

    def start_mission(self):
        # 1. Close Mission Instructions modal
        try:
            close_x = (
                self.page.locator("#mission_popup")
                .get_by_role("button")
                .filter(has_text=re.compile(r"^$"))
                .first
            )
            close_x.wait_for(state="visible", timeout=8000)
            close_x.click()
            close_x.wait_for(state="hidden", timeout=5000)
            print("Closed Mission Instructions modal")
        except Exception as e:
            print(f"No Mission Instructions modal found: {e}")

        # 2. Click Continue if present
        try:
            self.continue_button.wait_for(state="visible", timeout=5000)
            self.continue_button.click()
            print("Clicked Continue")
        except Exception as e:
            print(f"Continue button not found or clickable: {e}")

        # self.page.wait_for_timeout(1000)

    def handle_coding_step(self):
        expect(self.navbar_settings).to_be_visible(timeout=30000)

        # Close any open popover/overlay first
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(500)

        # Click settings to open popover
        self.navbar_settings.click()
        self.page.wait_for_timeout(500)

        # Wait for Show Model Answer and click it
        expect(self.show_model_answer_button).to_be_visible(timeout=10000)
        self.show_model_answer_button.click()

        # Wait for popover to close
        self.show_model_answer_button.wait_for(state="hidden", timeout=10000)
        self.page.wait_for_timeout(500)

        # Dismiss any lingering overlay before clicking Run
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(500)

        # Click Run
        expect(self.run_button).to_be_visible(timeout=30000)
        self.run_button.scroll_into_view_if_needed()
        self.run_button.click()
        self.page.wait_for_timeout(5000)

        # Click CONTINUE FLYING.. for each drone stop
        while True:
            try:
                self.finish_button.wait_for(state="visible", timeout=30000)
                self.finish_button.click()
                self.finish_button.wait_for(state="hidden", timeout=15000)
                print("Clicked Continue Flying..")
            except Exception:
                print("No more Continue Flying buttons — drone finished")
                break

    # ---------------------------------------------------------
    # HANDLE IFRAME STEP (AI Generator)
    # ---------------------------------------------------------

    def handle_iframe_step(self):
    # Wait for iframe to appear
        expect(self.page.locator("iframe").first).to_be_visible(timeout=60000)

    # Click "Got it" inside the iframe
        frame = self.page.frame_locator("iframe").first
        expect(frame.get_by_role("button", name="Got it")).to_be_visible(timeout=60000)
        frame.get_by_role("button", name="Got it").click()
        print("Clicked Got it")

    # 🔍 Search for "Finalize Mission" in all frames AND main page
        finalize_clicked = False

    # 1. Check main page
        try:
            btn = self.page.get_by_role("button", name="Finalize Mission")
            if btn.count() > 0:
                expect(btn).to_be_visible(timeout=60000)
                btn.click()
                print("Clicked Finalize Mission on main page")
                finalize_clicked = True
        except:

            pass

    # 2. Check all frames
        if not finalize_clicked:
            for f in self.page.frames:
                try:
                    btn = f.get_by_role("button", name="Finalize Mission")
                    if btn.count() > 0:
                        expect(btn).to_be_visible(timeout=60000)
                        btn.click()
                        print(f"Clicked Finalize Mission in frame: {f.url}")
                        finalize_clicked = True
                        break
                except:
                    pass

        if not finalize_clicked:
            raise Exception("Could not find 'Finalize Mission' button anywhere!")
    # ---------------------------------------------------------
    # FINAL VALIDATION
    # ---------------------------------------------------------

    def validate_completion(self):
        expect(self.congratulations_heading).to_be_visible(timeout=60000)

    # ---------------------------------------------------------
    # FULL FLOW
    # ---------------------------------------------------------

    def complete_mission_flow(self):
        self.start_mission()
        self.handle_coding_step()
        self.handle_iframe_step()
        self.validate_completion()
