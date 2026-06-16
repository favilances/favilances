from playwright.sync_api import sync_playwright
from PIL import Image
import io

import os

SVGS = [
    "dark_mode.svg",
    "light_mode.svg",
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for filename in SVGS:
        path = os.path.abspath(filename)
        page = browser.new_page(viewport={"width": 1200, "height": 850})
        page.goto(f"file://{path}", wait_until="networkidle")

        frames = []
        for _ in range(30):
            page.wait_for_timeout(100)
            frames.append(page.screenshot())

        name = filename.replace(".svg", ".webp")
        images = [Image.open(io.BytesIO(f)) for f in frames]
        images[0].save(
            name,
            save_all=True,
            append_images=images[1:],
            duration=100,
            loop=0,
        )
        print(f"Saved {name}")
        page.close()

    browser.close()
