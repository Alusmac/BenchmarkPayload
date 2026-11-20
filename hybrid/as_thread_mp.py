import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from benchmark.payload import TASK_COUNT, run_sync_task

THREAD_WORKERS = 2
PROCESS_WORKERS = 2


def process_worker(task_ids: list[int]) -> list[dict]:
    with ProcessPoolExecutor(max_workers=PROCESS_WORKERS) as executor:
        return list(executor.map(run_sync_task, task_ids))


async def run_thread_batch(task_ids: list[int]) -> list[dict]:
    loop = asyncio.get_running_loop()

    chunks = [
        task_ids[index::PROCESS_WORKERS]
        for index in range(PROCESS_WORKERS)
    ]

    with ThreadPoolExecutor(max_workers=PROCESS_WORKERS) as executor:
        tasks = [
            loop.run_in_executor(executor, process_worker, chunk)
            for chunk in chunks
        ]

        results = await asyncio.gather(*tasks)

    return [result for batch in results for result in batch]


async def run_async_thread_process() -> list[dict]:
    task_ids = list(range(TASK_COUNT))

    chunks = [
        task_ids[index::THREAD_WORKERS]
        for index in range(THREAD_WORKERS)
    ]

    with ThreadPoolExecutor(max_workers=THREAD_WORKERS) as executor:
        loop = asyncio.get_running_loop()

        tasks = [
            loop.run_in_executor(executor, run_thread_batch_sync, chunk)
            for chunk in chunks
        ]

        results = await asyncio.gather(*tasks)

    return [result for batch in results for result in batch]


def run_thread_batch_sync(task_ids: list[int]) -> list[dict]:
    return asyncio.run(run_thread_batch(task_ids))


def run_as_thread_mp() -> list[dict]:
    return asyncio.run(run_async_thread_process())


if __name__ == "__main__":
    results = run_as_thread_mp()

    print("Model: AS(TH(MP))")
    print("Tasks completed:", len(results))
    print("Prime count:", results[0]["prime_count"])