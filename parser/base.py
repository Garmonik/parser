from typing import Optional

from pyppeteer.browser import Browser
from pyppeteer.page import Page

DefaultNavigationTimeout = 15_000
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/118.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "referer": "https://www.google.com/",
}


class BaseParser:
    browser: Browser

    async def get_page(self) -> Page:
        page = await self.browser.newPage()
        page.setDefaultNavigationTimeout(DefaultNavigationTimeout)
        await page.setExtraHTTPHeaders(HEADERS)
        return page

    async def send_request(self, url: str) -> Optional[str]:
        page = await self.get_page()
        response = await page.goto(url)
        if response.ok:
            return await page.content()
