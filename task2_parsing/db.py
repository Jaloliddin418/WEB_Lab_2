import os
import sqlite3

DB = os.path.join(os.path.dirname(__file__), "lab1.db")

URLS = [
    "https://example.com",
    "https://www.python.org",
    "https://en.wikipedia.org/wiki/Python_(programming_language)",
    "https://en.wikipedia.org/wiki/Concurrency_(computer_science)",
    "https://en.wikipedia.org/wiki/Thread_(computing)",
    "https://en.wikipedia.org/wiki/Process_(computing)",
    "https://docs.python.org/3/library/asyncio.html",
    "https://docs.python.org/3/library/threading.html",
    "https://docs.python.org/3/library/multiprocessing.html",
    "https://www.iana.org/",
]

HEADERS = {"User-Agent": "Mozilla/5.0"}


def init_db():
    conn = sqlite3.connect(DB)
    conn.execute('''CREATE TABLE IF NOT EXISTS pages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        url TEXT,
                        title TEXT)''')
    conn.commit()
    conn.close()


def clear_db():
    conn = sqlite3.connect(DB)
    conn.execute("DELETE FROM pages")
    conn.commit()
    conn.close()


def save_page(url, title):
    conn = sqlite3.connect(DB, timeout=15)
    conn.execute("INSERT INTO pages (url, title) VALUES (?, ?)", (url, title))
    conn.commit()
    conn.close()


def show_db():
    conn = sqlite3.connect(DB)
    rows = conn.execute("SELECT id, url, title FROM pages").fetchall()
    conn.close()
    print("\nСодержимое базы данных:")
    for row in rows:
        print(row)
