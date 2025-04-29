from playwright.async_api import async_playwright

async def html_to_pdf_with_playwright(html_path, pdf_path):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(f"file://{html_path}")  # Open the local HTML file
        await page.pdf(path=pdf_path)  # Save the PDF
        await browser.close()
    
async def ensure_playwright_installed():
    from pathlib import Path
    import subprocess

    browser_dir = Path.home() / ".cache" / "ms-playwright"
    if not browser_dir.exists() or not any(browser_dir.iterdir()):
        print("Installing Playwright browsers...")
        subprocess.run(["playwright", "install", "chromium"], check=True)

    try:
        async with async_playwright() as p:
            await p.chromium.launch(headless=True)
    except ImportError:
        print("Playwright is not installed. Please install it using 'pip install playwright'.")
        raise