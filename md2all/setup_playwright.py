import subprocess

def install_playwright_browsers():
    subprocess.run(["playwright", "install", "chromium"], check=True)
