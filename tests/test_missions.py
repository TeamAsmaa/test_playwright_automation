from playwright.sync_api import Page, expect
import pytest
from pages.login_page import LoginPage
from pages.Mission_Page import MissionPage


MISSION_URLS = [
    # Discover Canada adventture 1
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1460/3727",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1460/3729",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1460/3730",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1460/3731",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1460/3732",
     
    # Discover Canada adventture 2
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1459/3719",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1459/3718",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1459/3726",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1459/3717",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1459/3725",
     
    # Discover Canada adventture 3
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1461/3728",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1461/3733",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1461/3734",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1461/3735",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1461/3736",
     
    # Discover Canada adventture 4
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1462/3744",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1462/3745",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1462/3746",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1462/3747",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1462/3748",
     
    # Discover Canada adventture 5
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1464/3750",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1464/3753",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1464/3756",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1464/3757",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1464/3758",
     
    # Discover Canada adventture 6
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1463/3749",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1463/3751",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1463/3752",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1463/3754",
     "https://codingville-staging.rgp-dev.com/workspaces/journey/blocks/168/1463/3755",
]
@pytest.mark.parametrize("mission_url", MISSION_URLS)
def test_complete_mission(page: Page, mission_url: str):
     # -----------------------------
    # Step 1: Login first
    # -----------------------------
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("CV_teacher1", "123456")
    
    # Ensure dashboard is loaded
    assert page.url == "https://codingville-staging.rgp-dev.com/teacher/dashboard"
    print("✅ Logged in successfully")

    # -----------------------------
    # Step 2: Complete mission
    # -----------------------------
    
    mission_page = MissionPage(page)

    # Step 1: Navigate directly to mission
    mission_page.navigate(mission_url)

    # Step 2: Start mission 
    mission_page.complete_mission_flow(mission_url)  

    print("Mission completed successfully")