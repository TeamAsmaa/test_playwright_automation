import os
from playwright.sync_api import Page, expect
import re

BACKEND_BASE = os.getenv("BACKEND_URL", "https://staging-backend.rgp-dev.com")

class MissionPage:
    def __init__(self, page: Page):
        self.page = page

        # Main mission elements
        self.mission_heading = page.get_by_role("heading", name="Mission Instructions")
        self.continue_button  = page.get_by_role("button", name="Continue")
        self.navbar_settings = page.locator(".navbar__setting-container")
        self.settings_button = page.locator("#navbar-setting-popover").get_by_role("button")
        
        # Mission action buttons
        self.show_model_answer_button = page.get_by_role("button", name="Show Model Answer")
        self.run_button = page.get_by_role("button", name="Run ", exact=True)
        self.finish_button = page.locator("#finish-mission-btn")               

    def navigate(self, mission_url: str):
        # Wait until navigation completes (HTML ready)
        self.page.goto(mission_url, wait_until="domcontentloaded", timeout=90000)
        # Small stabilization (helps Firefox)
        self.page.wait_for_timeout(500)
        # Now wait for mission content (UI rendered)
        expect(self.mission_heading).to_be_visible(timeout=120000)

    def start_mission(self):
    # 1. Close Mission Instructions modal 
        try:
            close_x = self.page.locator("#mission_popup").get_by_role("button").filter(has_text=re.compile(r"^$")).first
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
    def close_tutorial_overlay_if_present(self):
        overlay = self.page.locator(".mission-tutorial--modal--overlay")

        try:
            if overlay.is_visible(timeout=3000):
                print("Tutorial overlay detected — closing it")

                # Click Continue button inside overlay
                continue_btn = self.page.locator(
                    "button.mission-tutorial-btn--continue"
                )

                if continue_btn.is_visible():
                    continue_btn.click(force=True)

                # Wait for overlay to disappear
                overlay.wait_for(state="hidden", timeout=20000)

                print("Tutorial overlay closed")

        except Exception:
        # If overlay not present, ignore
            pass

    def handle_coding_step(self, mission_path: str):
        # Wait for navbar settings
        expect(self.navbar_settings).to_be_visible(timeout=30000)
        
        # # Close any open popover/overlay first
        # self.page.keyboard.press("Escape")
        # self.page.wait_for_timeout(500)
        #  CLOSE TUTORIAL OVERLAY FIRST
        self.close_tutorial_overlay_if_present()
        # Now click settings safely
        self.navbar_settings.click(force=True)
    
        # # Click settings to open popover
        # self.navbar_settings.click()
        
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
        
        # # Wait for AI-data request while clicking Run
        # self.wait_for_ai_data(mission_path)
    
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


    def wait_for_ai_data(self, mission_path: str, timeout: int = 120_000):
        # Extract mission ID from path
        mission_id = mission_path.strip("/").split("/")[-1]
        if not mission_id:
            raise ValueError(f"Invalid mission path: {mission_path}")

        # Regex for AI-data URL
        ai_data_url = re.compile(
            re.escape(f"{BACKEND_BASE}/en/missions/{mission_id}/ai-data")
        )

        # Wait for the backend request while clicking Run
        with self.page.expect_response(ai_data_url, timeout=timeout) as response_info:
            self.run_button.click()

        response = response_info.value
        assert response.ok, f"AI-data request failed: {response.url}"

    # ---------------------------------------------------------
    # FULL FLOW
    # ---------------------------------------------------------

    def complete_mission_flow(self, mission_path: str):
        self.start_mission()
        self.handle_coding_step(mission_path)
        # self.validate_completion()
                                             
 
