import asyncio

from benchmark.payload import TASK_COUNT, run_async_task


async def run_asyncio() -> list[dict]:
    """Execute tasks using asyncio."""

    tasks = [
        run_async_task(task_id)
        for task_id in range(TASK_COUNT)
    ]

    results = await asyncio.gather(*tasks)

    return results
