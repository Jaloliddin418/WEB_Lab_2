import time
import requests
from bs4 import BeautifulSoup

from db import URLS, HEADERS, init_db, clear_db, save_page, show_db
from threading_parse import run as run_threading
from multiprocessing_parse import run as run_multiprocessing
from async_parse import run as run_async


def run_sequential():
    init_db()
    clear_db()
    start_time = time.time()
    for url in URLS:
        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string.strip() if soup.title and soup.title.string else "Без заголовка"
        save_page(url, title)
        print(f"{url} -> {title}")
    elapsed = time.time() - start_time
    print(f"\nпоследовательно: время = {elapsed:.2f} c")
    return elapsed


def main():
    print(f"Страниц для парсинга: {len(URLS)}\n")
    times = {
        "последовательно": run_sequential(),
        "threading": run_threading(),
        "multiprocessing": run_multiprocessing(),
        "async": run_async(),
    }

    base = times["последовательно"]
    print("\n{:<18}{:>10}{:>14}".format("Подход", "Время, с", "Ускорение"))
    print("-" * 42)
    for name, t in times.items():
        print("{:<18}{:>10.2f}{:>14.2f}".format(name, t, base / t))

    show_db()


if __name__ == "__main__":
    main()
