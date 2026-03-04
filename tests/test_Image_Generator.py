from playwright.sync_api import Page, expect
import pytest
from pages.Image_Generator_Lab_Page import ImageGeneratorLabPage


MISSION_URLS = [
    # Discover Canada adventture 1
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1460/3727",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1460/3729",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1460/3730",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1460/3731",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1460/3732"
    # Add more URLs here
]
@pytest.mark.parametrize("mission_url", MISSION_URLS)
def test_complete_mission(logged_in_page: Page, mission_url: str):
    mission_page = ImageGeneratorLabPage(logged_in_page)

    # Step 1: Navigate directly to mission
    mission_page.navigate(mission_url)

    # Step 2: Start mission 
    mission_page.complete_mission_flow()  

    print("Mission completed successfully")