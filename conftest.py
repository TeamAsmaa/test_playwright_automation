# import os
# import re
# import shutil
# import pytest
# from playwright.sync_api import sync_playwright

# def sanitize_filename(name: str) -> str:
#     """Replace invalid Windows filename characters with '_'"""
#     return re.sub(r'[<>:"/\\|?*\[\]]', "_", name)

# @pytest.fixture(scope="function")
# def page(request):
#     """
#     Fresh Playwright page for login tests, with tracing and video recording.
#     Only keeps the last run for each test case.
#     """
#     # Folder per test (fixed, overwrites old run)
#     test_dir = os.path.join("runs", sanitize_filename(request.node.name))

#     # Remove old run for this test
#     if os.path.exists(test_dir):
#         shutil.rmtree(test_dir)
#     os.makedirs(test_dir, exist_ok=True)

#     video_dir = os.path.join(test_dir, "videos")
#     os.makedirs(video_dir, exist_ok=True)

#     trace_file = os.path.join(test_dir, "trace.zip")

#     # Launch Playwright
#     p = sync_playwright().start()
#     browser = p.chromium.launch(headless=False)
#     context = browser.new_context(
#         record_video_dir=video_dir,
#         record_video_size={"width": 1024, "height": 768}
#     )

#     # Start tracing
#     context.tracing.start(screenshots=True, snapshots=True, sources=True)

#     page = context.new_page()

#     yield page  # test handles login

#     # Stop tracing
#     context.tracing.stop(path=trace_file)

#     # Cleanup
#     context.close()
#     browser.close()
#     p.stop()
import os
import re
import shutil
import pytest
from playwright.sync_api import sync_playwright

def sanitize_filename(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*\[\]]', "_", name)

# -----------------------------
# Fixture to run tests on multiple browsers
# -----------------------------
@pytest.fixture(params=["chromium"], scope="function")
def page(request):
    """
    Fresh Playwright page for login tests, with tracing/video.
    Parametrized to run on Chromium and Firefox.
    Only keeps the last run per test case.
    """
    browser_name = request.param
    test_dir = os.path.join("runs", sanitize_filename(request.node.name) + f"_{browser_name}")

    # Remove old run
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir, exist_ok=True)

    video_dir = os.path.join(test_dir, "videos")
    os.makedirs(video_dir, exist_ok=True)
    trace_file = os.path.join(test_dir, "trace.zip")

    # Launch Playwright
    p = sync_playwright().start()
    browser = getattr(p, browser_name).launch(headless=False)
    context = browser.new_context(
        record_video_dir=video_dir,
        record_video_size={"width": 1024, "height": 768},
    )

    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()

    yield page  # test will handle login

    context.tracing.stop(path=trace_file)
    context.close()
    browser.close()
    p.stop()
