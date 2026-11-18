from playwright.sync_api import sync_playwright
import time

print("Opening browser...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto('https://drive.google.com', timeout=60000)
    print("Browser opened! Google account login karo.")
    input("Login ho jaye toh yahan Enter press karo: ")
    time.sleep(3)
    context.storage_state(path='_auth_state.json')
    print("Auth state saved!")
    browser.close()
    print("Done!")
