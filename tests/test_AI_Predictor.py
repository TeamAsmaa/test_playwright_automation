from playwright.sync_api import Page, expect
import pytest
from pages.AI_Predictor_Lab_page import AIPredictorLabPage


MISSION_URLS = [
    # Discover Canada adventture 2
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1459/3719",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1459/3718",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1459/3726",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1459/3717",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1459/3725"
    # Add more URLs here
]
@pytest.mark.parametrize("mission_url", MISSION_URLS)
def test_complete_mission(logged_in_page: Page, mission_url: str):
    mission_page = AIPredictorLabPage(logged_in_page)

    # Step 1: Navigate directly to mission
    mission_page.navigate(mission_url)

    # Step 2: Start mission 
    mission_page.complete_mission_flow()  

    print("Mission completed successfully")