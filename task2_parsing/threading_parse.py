import time
import threading
import requests
from bs4 import BeautifulSoup

from db import URLS, HEADERS, init_db, clear_db, save_page, show_db

db_lock = threading.Lock()


def parse_and_save(url):
    response = requests.get(url, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else "Без заголовка"
    with db_lock:
        save_page(url, title)
    print(f"{url} -> {title}")
    return title


def run():
    init_db()
    clear_db()
    start_time = time.time()
    threads = [threading.Thread(target=parse_and_save, args=(u,)) for u in URLS]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    elapsed = time.time() - start_time
    print(f"\nthreading: время = {elapsed:.2f} c")
    return elapsed


if __name__ == "__main__":
    run()
    show_db()
