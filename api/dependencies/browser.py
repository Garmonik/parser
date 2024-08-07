from pyppeteer import launch
from pyppeteer.browser import Browser


async def get_browser() -> Browser:
    yield await launch(
        options={
            "args": [
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--single-process",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--no-zygote",
            ]
        },
        handleSIGINT=False,
        handleSIGTERM=False,
        handleSIGHUP=False,
    )
