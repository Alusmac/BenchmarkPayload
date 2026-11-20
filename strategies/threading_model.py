from concurrent.futures import ThreadPoolExecutor

from benchmark.payload import TASK_COUNT, run_sync_task

MAX_WORKERS = 10


def run_threading() -> list[dict]:
    """Execute tasks using a thread pool."""

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        results = list(
            executor.map(run_sync_task, range(TASK_COUNT))
        )

    return results
