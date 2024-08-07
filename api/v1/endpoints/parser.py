import parser
import time

from fastapi import APIRouter, Depends
from pyppeteer.browser import Browser

from api.dependencies.browser import get_browser
from schemas.urls import DataUrls, ParseUrl

router = APIRouter()


@router.post("/links/")
async def parse_links(url: ParseUrl, browser: Browser = Depends(get_browser)):
    start = time.time()
    links_parser = parser.LinksParser(url.url, browser)
    result = await links_parser.start()
    process_time = time.time() - start
    return {"time": process_time, "result": result}


@router.post("/data/")
async def parse_data(urls: DataUrls, browser: Browser = Depends(get_browser)):
    start = time.time()
    data_parser = parser.DataParser(urls.urls, browser)
    result = await data_parser.start()
    process_time = time.time() - start
    return {"time": process_time, "result": result}
