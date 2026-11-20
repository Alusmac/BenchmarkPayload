import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from benchmark.payload import TASK_COUNT, run_sync_task

THREAD_WORKERS = 2
PROCESS_WORKERS = 2


async def run_async_batch(task_ids: list[int]) -> list[dict]:
    loop = asyncio.get_running_loop()

    with ProcessPoolExecutor(max_workers=PROCESS_WORKERS) as executor:
        tasks = [
            loop.run_in_executor(executor, run_sync_task, task_id)
            for task_id in task_ids
        ]

        results = await asyncio.gather(*tasks)

    return results


def thread_worker(task_ids: list[int]) -> list[dict]:
    return asyncio.run(run_async_batch(task_ids))


def run_thread_async_process() -> list[dict]:
    task_ids = list(range(TASK_COUNT))

    thread_chunks = [
        task_ids[index::THREAD_WORKERS]
        for index in range(THREAD_WORKERS)
    ]

    with ThreadPoolExecutor(max_workers=THREAD_WORKERS) as executor:
        results = list(executor.map(thread_worker, thread_chunks))

    return [result for batch in results for result in batch]


if __name__ == "__main__":
    results = run_thread_async_process()

    print("Model: TH(AS(MP))")
    print("Tasks completed:", len(results))
    print("Prime count:", results[0]["prime_count"])
