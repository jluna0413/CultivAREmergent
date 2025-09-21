from pathlib import Path
from playwright.sync_api import sync_playwright

OUT_DIR = Path(__file__).parent.parent / "screenshots"
OUT_DIR.mkdir(parents=True, exist_ok=True)

URLS = [
    ("/marketing/", "marketing"),
    ("/marketing/blog", "blog"),
]

VIEWPORT = {"width": 1400, "height": 900}

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport=VIEWPORT)

    for path, name in URLS:
        for theme in ("light", "dark"):
            url = f"http://127.0.0.1:5000{path}"
            page.goto(url, wait_until="networkidle")
            # Set theme by updating data-theme on documentElement
            if theme == "dark":
                page.evaluate("() => document.documentElement.setAttribute('data-theme','dark')")
            else:
                page.evaluate("() => document.documentElement.removeAttribute('data-theme')")
            # small delay to let CSS transitions settle
            page.wait_for_timeout(300)
            out_file = OUT_DIR / f"{name}_{theme}.png"
            page.screenshot(path=str(out_file), full_page=True)
            print(f"Saved {out_file}")

    browser.close()
