import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from benchmark.payload import TASK_COUNT, run_sync_task

PROCESS_WORKERS = 2
THREAD_WORKERS = 2


def thread_worker(task_ids: list[int]) -> list[dict]:
    with ThreadPoolExecutor(max_workers=THREAD_WORKERS) as executor:
        return list(executor.map(run_sync_task, task_ids))


async def run_process_batch(task_ids: list[int]) -> list[dict]:
    loop = asyncio.get_running_loop()

    chunks = [
        task_ids[index::PROCESS_WORKERS]
        for index in range(PROCESS_WORKERS)
    ]

    with ProcessPoolExecutor(max_workers=PROCESS_WORKERS) as executor:
        tasks = [
            loop.run_in_executor(executor, thread_worker, chunk)
            for chunk in chunks
        ]

        results = await asyncio.gather(*tasks)

    return [result for batch in results for result in batch]


def run_async_process_thread() -> list[dict]:
    task_ids = list(range(TASK_COUNT))
    return asyncio.run(run_process_batch(task_ids))


if __name__ == "__main__":
    results = run_async_process_thread()

    print("Model: AS(MP(TH))")
    print("Tasks completed:", len(results))
    print("Prime count:", results[0]["prime_count"])
