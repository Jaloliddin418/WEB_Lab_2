import time
import asyncio
import aiohttp
from bs4 import BeautifulSoup

from db import URLS, HEADERS, init_db, clear_db, save_page, show_db


async def parse_and_save(session, url):
    async with session.get(url, headers=HEADERS) as response:
        html = await response.text()
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else "Без заголовка"
    save_page(url, title)
    print(f"{url} -> {title}")
    return title


async def main():
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[parse_and_save(session, u) for u in URLS])


def run():
    init_db()
    clear_db()
    start_time = time.time()
    asyncio.run(main())
    elapsed = time.time() - start_time
    print(f"\nasync: время = {elapsed:.2f} c")
    return elapsed


if __name__ == "__main__":
    run()
    show_db()
