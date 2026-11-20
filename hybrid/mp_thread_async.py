import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from benchmark.payload import (
    TASK_COUNT,
    run_async_task,
)

PROCESS_WORKERS = 2
THREAD_WORKERS = 2


async def run_async_batch(task_ids: list[int]) -> list[dict]:
    """Execute a batch of tasks using asyncio."""

    tasks = [
        run_async_task(task_id)
        for task_id in task_ids
    ]

    return await asyncio.gather(*tasks)


def run_thread_batch(task_ids: list[int]) -> list[dict]:
    """Run an asyncio event loop inside a thread."""

    return asyncio.run(run_async_batch(task_ids))


def process_worker(task_ids: list[int]) -> list[dict]:
    """Create a thread pool inside a process."""

    chunks = [
        task_ids[index::THREAD_WORKERS]
        for index in range(THREAD_WORKERS)
    ]

    with ThreadPoolExecutor(
            max_workers=THREAD_WORKERS
    ) as executor:
        results = list(
            executor.map(run_thread_batch, chunks)
        )

    return [
        result
        for batch in results
        for result in batch
    ]


def run_mp_thread_async() -> list[dict]:
    """Execute tasks using MP(TH(AS))."""

    task_ids = list(range(TASK_COUNT))

    process_chunks = [
        task_ids[index::PROCESS_WORKERS]
        for index in range(PROCESS_WORKERS)
    ]

    with ProcessPoolExecutor(
            max_workers=PROCESS_WORKERS
    ) as executor:
        results = list(
            executor.map(process_worker, process_chunks)
        )

    return [
        result
        for batch in results
        for result in batch
    ]


if __name__ == "__main__":
    results = run_mp_thread_async()

    print("Model: MP(TH(AS))")
    print("Tasks completed:", len(results))
    print("Prime count:", results[0]["prime_count"])
