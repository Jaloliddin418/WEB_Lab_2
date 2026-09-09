import time

from threading_sum import run as run_threading
from multiprocessing_sum import run as run_multiprocessing
from async_sum import run as run_async
from threading_sum import N, WORKERS, calculate_sum


def run_sequential():
    start_time = time.time()
    total = calculate_sum(1, N)
    elapsed = time.time() - start_time
    correct = total == N * (N + 1) // 2
    print(f"последовательно: результат верный = {correct}, время = {elapsed:.2f} c")
    return elapsed


def main():
    print(f"N = {N}, частей = {WORKERS}\n")
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


if __name__ == "__main__":
    main()
