from concurrent.futures import ProcessPoolExecutor
from benchmark.payload import TASK_COUNT, run_sync_task

MAX_WORKERS = 4


def run_multiprocessing() -> list[dict]:
    """Execute tasks using multiple processes."""

    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        results = list(
            executor.map(run_sync_task, range(TASK_COUNT))
        )

    return results
