# Задача 1 - различия между threading, multiprocessing и async

## Постановка

Написать три программы на Python, каждая своим подходом (`threading`, `multiprocessing`,
`async`), которые считают сумму всех чисел от 1 до N. Разделить вычисления на несколько
параллельных подзадач и сравнить время.

Требования:

- в каждой программе функция `calculate_sum()`;
- разбить задачу на несколько подзадач и выполнять параллельно;
- замерить и сравнить время.

Это задача типа **CPU-bound** - процессор занят на 100%, ждать нечего.

!!! note "Про число N"
    В задании N = 10 000 000 000 000 (10 трлн), но пройти такой цикл в Python - это около
    90 часов. Поэтому в коде N = 100 000 000 (100 млн): время измеримое, а правильность
    проверяется формулой Гаусса `N * (N + 1) / 2`.

---

## Что сделали

1. Написали функцию `calculate_sum(start, end)` - складывает числа в заданном диапазоне.
2. Разбили весь диапазон на 4 равные части (`make_chunks`), чтобы считать их параллельно.
3. Сделали три программы, запускающие эти 4 куска разными способами.
4. Замерили каждую и сравнили с обычным последовательным подсчётом.

Общая для всех трёх программ основа:

```python
def make_chunks(n, parts):
    step = n // parts
    chunks = []
    start = 1
    for i in range(parts):
        end = n if i == parts - 1 else start + step - 1
        chunks.append((start, end))
        start = end + 1
    return chunks


def calculate_sum(start, end):
    total = 0
    for i in range(start, end + 1):
        total += i
    return total
```

---

## threading

Каждый поток считает свой кусок и кладёт результат в общий список по своему индексу
(вернуть значение напрямую поток не может).

```python
def run():
    chunks = make_chunks(N, WORKERS)
    results = [0] * WORKERS

    def worker(idx, start, end):
        results[idx] = calculate_sum(start, end)

    threads = [threading.Thread(target=worker, args=(i, s, e))
               for i, (s, e) in enumerate(chunks)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return sum(results)
```

`start()` запускает потоки, `join()` заставляет главную программу дождаться всех.

!!! warning "Почему не ускорится"
    Из-за GIL потоки делят один «нож». Для чистых вычислений время выйдет почти как у
    обычного цикла.

---

## multiprocessing

`Pool(4)` создаёт 4 отдельных процесса, `starmap` раздаёт им куски и собирает результаты.

```python
def run():
    chunks = make_chunks(N, WORKERS)
    with Pool(WORKERS) as pool:
        parts = pool.starmap(calculate_sum, chunks)
    return sum(parts)
```

!!! success "Почему ускорится"
    У каждого процесса свой интерпретатор и своё ядро - GIL обойдён, куски считаются
    по-настоящему параллельно. Это единственный из трёх способов, который реально ускоряет
    вычисления.

!!! danger "Обязательная защита на Windows"
    Запуск процессов должен быть под `if __name__ == "__main__":`. На Windows дочерние
    процессы заново импортируют файл, и без этой строки они бесконечно порождали бы сами
    себя.

---

## async

Корутины запускаются через `asyncio.gather`, но внутри - чистые вычисления без `await`.

```python
async def calc_async(start, end):
    return calculate_sum(start, end)


async def main():
    chunks = make_chunks(N, WORKERS)
    parts = await asyncio.gather(*[calc_async(s, e) for s, e in chunks])
    return sum(parts)
```

!!! warning "Почему не ускорится"
    Событийный цикл работает в одном потоке. Раз паузы на ожидании (`await`) нет, корутины
    выполняются одна за другой, как обычный цикл. Async создан для ожиданий, а не для
    вычислений.

---

## Результат Задачи 1

Пример замера (2 ядра, у тебя будут свои числа после запуска `task1_sum/compare_all.py`):

| Подход | Время, с | Ускорение |
|---|---|---|
| последовательно | 3.20 | 1.00 |
| threading | 3.30 | 0.97 |
| multiprocessing | 1.80 | 1.78 |
| async | 3.25 | 0.98 |

**Вывод:** для тяжёлых вычислений помогает только **multiprocessing**. Потоки и async упираются
в GIL.
