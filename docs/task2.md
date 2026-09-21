# Задача 2 - параллельный парсинг веб-страниц с сохранением в БД

## Постановка

Написать три программы (`threading`, `multiprocessing`, `async`), которые параллельно
парсят несколько веб-страниц и сохраняют данные в базу.

Требования:

- функция `parse_and_save(url)` - скачивает HTML, парсит, сохраняет заголовок в БД и
  выводит результат;
- для async - `async`/`await` и модуль `aiohttp`;
- список URL разделить на части, запустить параллельно, замерить время.

Это задача типа **I/O-bound** - программа почти всё время ждёт ответа сервера.

!!! note "Про базу данных"
    Используется SQLite - лёгкая база в одном файле `lab1.db` с таблицей `pages(url, title)`.
    Если в лабораторной №1 была своя схема, её подставляют в файл `db.py`.

---

## Что сделали

1. Составили список из 10 URL и функцию `parse_and_save(url)`.
2. Сделали три программы, обрабатывающие список разными способами.
3. Замерили каждую и сравнили с последовательным скачиванием.

**Парсинг** - это скачать страницу и вытащить из неё нужные данные. Заголовок вкладки лежит
в теге `<title>`. Библиотека **BeautifulSoup** разбирает HTML и позволяет достать этот тег.

---

## threading

На ожидании сети GIL отпускается, поэтому потоки реально помогают. Запись в базу защищена
замком, чтобы потоки не конфликтовали.

```python
db_lock = threading.Lock()


def parse_and_save(url):
    response = requests.get(url, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else "Без заголовка"
    with db_lock:
        save_page(url, title)
    return title
```

---

## multiprocessing

Каждый процесс качает свою страницу и пишет в базу через своё соединение (замок не нужен -
память у процессов разная).

```python
def run():
    with Pool(WORKERS) as pool:
        pool.map(parse_and_save, URLS)
```

!!! info "Почему слабее"
    Сеть ускоряется, но запуск процессов - дорогая операция, а задача лёгкая. Накладные
    расходы съедают часть выигрыша.

---

## async

Через `aiohttp` все запросы стартуют почти одновременно в одном потоке. Ключевой момент -
`await` на скачивании: пока одна страница грузится, стартуют остальные.

```python
async def parse_and_save(session, url):
    async with session.get(url, headers=HEADERS) as response:
        html = await response.text()
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else "Без заголовка"
    save_page(url, title)
    return title


async def main():
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[parse_and_save(session, u) for u in URLS])
```

!!! success "Почему быстрее всех"
    Все запросы стартуют разом, и время работы примерно равно времени самой медленной
    страницы, а не сумме всех. При этом не создаётся ни тяжёлых потоков, ни процессов.

---

## Результат Задачи 2

Пример замера (10 страниц, у тебя будут свои числа после запуска `task2_parsing/compare_all.py`):

| Подход | Время, с | Ускорение |
|---|---|---|
| последовательно | 4.00 | 1.00 |
| threading | 0.80 | 5.00 |
| multiprocessing | 1.10 | 3.64 |
| async | 0.60 | 6.67 |

**Вывод:** для ожидания сети помогают **async** и **threading**. Multiprocessing тоже ускоряет,
но избыточен для лёгкой сетевой задачи.
