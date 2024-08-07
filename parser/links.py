import asyncio
from parser.base import BaseParser
from typing import List
from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup, ResultSet
from pyppeteer.browser import Browser
from pyppeteer.errors import PageError, TimeoutError

import utils.html
import utils.urls


class LinksParser(BaseParser):
    def __init__(self, initial_url: str, browser: Browser):
        self.initial_url = initial_url
        self.domain = "/".join(initial_url.split("/")[:3])
        self.visited = {initial_url}
        self.error = set()
        self.browser = browser

    async def start(self) -> set[str]:
        to_scrape = {self.initial_url}
        while len(to_scrape) > 0:
            tasks = (
                asyncio.create_task(self.scrape_url(url)) for url in to_scrape
            )
            results = await asyncio.gather(*tasks)
            to_scrape = await self.process_results(results)

        await self.browser.close()
        return await self.format_response()

    async def scrape_url(self, url_to_parse: str) -> dict:
        try:
            response = await self.send_request(url_to_parse)
            if response is None:
                return {"not_reachable_url": url_to_parse}

            soup = BeautifulSoup(response, "lxml").find("body")
            links = await self.get_links(soup.find_all("a"))
            return {
                "links": links,
            }
        except (PageError, TimeoutError):
            return {"not_reachable_url": url_to_parse}

    async def get_links(self, a_tags: ResultSet) -> tuple:
        links = ()
        for a_tag in a_tags:
            url_href = a_tag.get("href")
            if url_href and "#" not in url_href:
                parsed_url = urlparse(url_href)
                query_params = parse_qs(parsed_url.query)
                if not query_params and not await utils.urls.is_file_url(
                    url_href
                ):
                    if self.initial_url in url_href:
                        links += (url_href,)
                    elif url_href.startswith("/"):
                        links += (self.domain + url_href,)
        return links

    async def process_results(self, results: List[dict]) -> set:
        to_scrape = set()

        for result in results:
            not_reachable_url = result.get("not_reachable_url")
            if not_reachable_url is None:
                new_links = (
                    url for url in result["links"] if url not in self.visited
                )
                to_scrape.update(new_links)
                self.visited.update(result["links"])
            else:
                self.error.update(not_reachable_url)
        return to_scrape

    async def format_response(self) -> set[str]:
        return self.visited - self.error
