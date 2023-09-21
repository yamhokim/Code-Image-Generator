from playwright.sync_api import sync_playwright

# 'url' is the URL that playwright's browser shpuld visit
# 'session_data' is the data stored in your own session, this needs to be transferred to be worked with
def take_screenshot_from_url(url, session_data):
    with sync_playwright() as playwright:   # Using a context manager to wrap playwright code, ensures python sets up and tears down playwright instance properly
        webkit = playwright.webkit  # Create headless webkit browser
        browser = webkit.launch()   # launch the webkit browser
        browser_context = browser.new_context(device_scale_factor=2)    # set up new context for browser, and increae deviec_scale_factor at 2 to ensure pictures aren't pixelated
        browser_context.add_cookies([session_data]) # Add session info to the browser
        page = browser_context.new_page()   # open a new page in the browser_context, like a new browser window
        page.goto(url)  # visit the target url
        screenshot_bytes = page.locator(".code").screenshot()   # Take a ss of the image, this returns a buffer with the image
        browser.close()
        return screenshot_bytes # Return the image buffer
    
