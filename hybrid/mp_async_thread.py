import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from benchmark.payload import TASK_COUNT, run_sync_task

PROCESS_WORKERS = 2
THREAD_WORKERS = 2


async def run_thread_batch(task_ids: list[int]) -> list[dict]:
    """Execute tasks using threads inside asyncio."""

    loop = asyncio.get_running_loop()

    with ThreadPoolExecutor(
            max_workers=THREAD_WORKERS
    ) as executor:
        tasks = [
            loop.run_in_executor(
                executor,
                run_sync_task,
                task_id,
            )
            for task_id in task_ids
        ]

        results = await asyncio.gather(*tasks)

    return results


def process_worker(task_ids: list[int]) -> list[dict]:
    """Run asyncio inside a process."""

    return asyncio.run(run_thread_batch(task_ids))


def run_mp_async_thread() -> list[dict]:
    """Execute tasks using MP(AS(TH))."""

    task_ids = list(range(TASK_COUNT))

    chunks = [
        task_ids[index::PROCESS_WORKERS]
        for index in range(PROCESS_WORKERS)
    ]

    with ProcessPoolExecutor(
            max_workers=PROCESS_WORKERS
    ) as executor:
        results = list(
            executor.map(process_worker, chunks)
        )

    return [
        result
        for batch in results
        for result in batch
    ]


if __name__ == "__main__":
    results = run_mp_async_thread()

    print("Model: MP(AS(TH))")
    print("Tasks completed:", len(results))
    print("Prime count:", results[0]["prime_count"])
