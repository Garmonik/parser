import asyncio
import json
import logging
from parser.base import BaseParser
from typing import List

from bs4 import BeautifulSoup
from pyppeteer.browser import Browser
from pyppeteer.errors import PageError, TimeoutError

import utils.html
import utils.urls


class DataParser(BaseParser):
    def __init__(self, links: list[str], browser: Browser):
        self.links = links
        self.browser = browser
        self.data = []

    async def start(self) -> str:
        tasks = (
            asyncio.create_task(self.scrape_url(url)) for url in self.links
        )
        results = await asyncio.gather(*tasks)
        await self.process_results(results)
        await self.browser.close()
        return await self.format_response()

    async def scrape_url(self, url_to_parse: str) -> dict:
        logging_msg = "Не удалось получить данные с %s"
        try:
            response = await self.send_request(url_to_parse)
            if response is None:
                logging.warning(logging_msg % url_to_parse)

            soup = BeautifulSoup(response, "lxml").find("body")
            processed_page = await utils.html.remove_html_tags(soup)
            return {
                "data": processed_page,
            }
        except (PageError, TimeoutError):
            logging.warning(logging_msg % url_to_parse)

    async def process_results(self, results: List[dict]):
        for result in results:
            if data := result.get("data"):
                self.data.append(data)

    async def format_response(self) -> str:
        return json.dumps(self.data, ensure_ascii=False)
