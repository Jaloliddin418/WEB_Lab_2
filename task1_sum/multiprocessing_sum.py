import time
from multiprocessing import Pool

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


def run():
    chunks = make_chunks(N, WORKERS)
    start_time = time.time()
    with Pool(WORKERS) as pool:
        parts = pool.starmap(calculate_sum, chunks)
    elapsed = time.time() - start_time

    correct = sum(parts) == N * (N + 1) // 2
    print(f"multiprocessing: результат верный = {correct}, время = {elapsed:.2f} c")
    return elapsed


if __name__ == "__main__":
    run()
