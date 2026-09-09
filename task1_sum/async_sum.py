import time
import asyncio

N = 100_000_000
WORKERS = 4


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


async def calc_async(start, end):
    return calculate_sum(start, end)


async def main():
    chunks = make_chunks(N, WORKERS)
    parts = await asyncio.gather(*[calc_async(s, e) for s, e in chunks])
    return sum(parts)


def run():
    start_time = time.time()
    total = asyncio.run(main())
    elapsed = time.time() - start_time

    correct = total == N * (N + 1) // 2
    print(f"async: результат верный = {correct}, время = {elapsed:.2f} c")
    return elapsed


if __name__ == "__main__":
    run()
