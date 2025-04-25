import os
from playwright.sync_api import sync_playwright

def html_to_pdf_with_playwright(html_path, output_pdf_path):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"file://{os.path.abspath(html_path)}", wait_until='networkidle')
        page.pdf(path=output_pdf_path, format="A4")
        browser.close()

    
def ensure_playwright_installed():
    from pathlib import Path
    import subprocess

    browser_dir = Path.home() / ".cache" / "ms-playwright"
    if not browser_dir.exists() or not any(browser_dir.iterdir()):
        print("Installing Playwright browsers...")
        subprocess.run(["playwright", "install", "chromium"], check=True)

    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            p.chromium.launch(headless=True).close()
    except Exception as e:
        print("Reinstalling Playwright browsers due to error:", e)
        subprocess.run(["playwright", "install", "chromium"], check=True)
