import os
import re
import pytest
from playwright.sync_api import sync_playwright

def sanitize_filename(name: str) -> str:
    # Replace invalid Windows filename characters with "_"
    return re.sub(r'[<>:"/\\|?*\[\]]', "_", name)

@pytest.fixture(scope="function")
def logged_in_page(request):
    # Parent folder for all runs
    parent_dir = "runs"
    os.makedirs(parent_dir, exist_ok=True)

    # Unique folder per test
    test_dir = os.path.join(parent_dir, sanitize_filename(request.node.name))
    os.makedirs(test_dir, exist_ok=True)

    # Paths for video and trace inside this test folder
    video_dir = os.path.join(test_dir, "videos")
    os.makedirs(video_dir, exist_ok=True)
    trace_file = os.path.join(test_dir, "trace.zip")

    # Launch Playwright
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        storage_state="storage_state.json",
        record_video_dir=video_dir,
        record_video_size={"width": 1024, "height": 768},
    )

    # Start tracing
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()

    try:
        yield page  # run the test
    finally:
        # Stop tracing and save to test folder
        context.tracing.stop(path=trace_file)
        context.close()
        browser.close()
        p.stop()