from benchmark.payload import TASK_COUNT, run_sync_task


def run_sequential() -> list[dict]:
    """Execute all tasks sequentially."""

    results = []

    for task_id in range(TASK_COUNT):
        result = run_sync_task(task_id)
        results.append(result)

    return results
