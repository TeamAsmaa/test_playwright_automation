from playwright.sync_api import Page, expect
import re

class ImageGeneratorLabPage:
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
        
        # iFrame elements
        self.iframe = page.locator("iframe").content_frame
        self.ai_loader = self.iframe.locator("#aiLoaderOverlay")
        self.ai_heading = self.iframe.get_by_role("heading", name="AI Image Generator")
        self.generate_image_button = self.iframe.get_by_role("button", name="Generate Image")
        self.finalize_button = self.iframe.get_by_role("button", name="Finalize Mission")

        # Final page
        self.congratulations_heading = page.get_by_role("heading", name="Congratulations!")
        

    def navigate(self, mission_url: str):
        # Wait until navigation completes (HTML ready)
        self.page.goto(mission_url, wait_until="domcontentloaded", timeout=90000)
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
        # self.page.wait_for_selector("iframe", timeout=60000)
        frame = self.page.frame_locator("iframe")

        # Wait for AI page heading
        expect(
            frame.get_by_role("heading", name="AI Image Generator")
        ).to_be_visible(timeout=60000)

        # Select Beginner from the dropdown
        level_dropdown = self.page.locator("iframe").content_frame.locator("#aiLevelSelect")
        level_dropdown.wait_for(state="visible", timeout=10000)
        level_dropdown.select_option(value="beginner")
        
        # Generate image
        generate_button = frame.get_by_role("button", name="Generate Image")
        expect(generate_button).to_be_visible(timeout=30000)
        generate_button.click()

        # Wait for Finalize button
        finalize_button = frame.get_by_role("button", name="Finalize Mission")
        expect(finalize_button).to_be_visible(timeout=60000)
        finalize_button.click()
        
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
                                             
 
