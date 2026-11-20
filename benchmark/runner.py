import time
import asyncio
import inspect
import threading
import psutil
from collections.abc import Callable
from benchmark.metrics import BenchmarkResult


def run_benchmark(model_name: str,benchmark_function: Callable,) -> BenchmarkResult:
    """Measure execution time and peak memory of a process tree."""

    process = psutil.Process()
    stop_event = threading.Event()

    peak_memory = 0

    def monitor_memory():
        nonlocal peak_memory

        while not stop_event.is_set():
            total_memory = 0

            try:
                processes = [process]
                processes.extend(process.children(recursive=True))

                for child in processes:
                    try:
                        total_memory += child.memory_info().rss
                    except psutil.Error:
                        continue

                peak_memory = max(peak_memory, total_memory)

            except psutil.Error:
                pass

            stop_event.wait(0.01)

    monitor = threading.Thread(
        target=monitor_memory,
        daemon=True,
    )

    monitor.start()

    try:
        start_time = time.perf_counter()

        result = benchmark_function()

        if inspect.isawaitable(result):
            result = asyncio.run(result)

        end_time = time.perf_counter()

    finally:
        stop_event.set()
        monitor.join()

    execution_time = end_time - start_time
    peak_memory_mb = peak_memory / (1024 ** 2)

    return BenchmarkResult(
        model_name=model_name,
        execution_time=execution_time,
        peak_memory_mb=peak_memory_mb,
        tasks_completed=len(result),
    )
