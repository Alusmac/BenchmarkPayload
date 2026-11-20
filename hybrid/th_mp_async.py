import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from benchmark.payload import TASK_COUNT, run_async_task

THREAD_WORKERS = 2
PROCESS_WORKERS = 2


async def run_async_batch(task_ids: list[int]) -> list[dict]:
    tasks = [run_async_task(task_id) for task_id in task_ids]
    return await asyncio.gather(*tasks)


def process_worker(task_ids: list[int]) -> list[dict]:
    return asyncio.run(run_async_batch(task_ids))


def run_process_batch(task_ids: list[int]) -> list[dict]:
    chunks = [
        task_ids[index::PROCESS_WORKERS]
        for index in range(PROCESS_WORKERS)
    ]

    with ProcessPoolExecutor(max_workers=PROCESS_WORKERS) as executor:
        results = list(executor.map(process_worker, chunks))

    return [result for batch in results for result in batch]


def run_thread_process_async() -> list[dict]:
    task_ids = list(range(TASK_COUNT))

    thread_chunks = [
        task_ids[index::THREAD_WORKERS]
        for index in range(THREAD_WORKERS)
    ]

    with ThreadPoolExecutor(max_workers=THREAD_WORKERS) as executor:
        results = list(executor.map(run_process_batch, thread_chunks))

    return [result for batch in results for result in batch]


if __name__ == "__main__":
    results = run_thread_process_async()

    print("Model: TH(MP(AS))")
    print("Tasks completed:", len(results))
    print("Prime count:", results[0]["prime_count"])
