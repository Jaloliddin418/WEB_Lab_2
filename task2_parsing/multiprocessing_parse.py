import time
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool

from db import URLS, HEADERS, init_db, clear_db, save_page, show_db

WORKERS = 4


def parse_and_save(url):
    response = requests.get(url, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else "Без заголовка"
    save_page(url, title)
    print(f"{url} -> {title}")
    return title


def run():
    init_db()
    clear_db()
    start_time = time.time()
    with Pool(WORKERS) as pool:
        pool.map(parse_and_save, URLS)
    elapsed = time.time() - start_time
    print(f"\nmultiprocessing: время = {elapsed:.2f} c")
    return elapsed


if __name__ == "__main__":
    run()
    show_db()
