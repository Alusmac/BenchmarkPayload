import asyncio
import time

TASK_COUNT = 100
IO_DELAY = 0.1
CPU_LIMIT = 20_000


def count_primes(limit: int) -> int:
    """Count prime numbers below the given limit."""
    count = 0

    for number in range(2, limit):
        is_prime = True

        for divisor in range(2, int(number ** 0.5) + 1):
            if number % divisor == 0:
                is_prime = False
                break

        if is_prime:
            count += 1

    return count


def run_sync_task(task_id: int) -> dict:
    """Execute one synchronous benchmark task."""

    time.sleep(IO_DELAY)

    prime_count = count_primes(CPU_LIMIT)

    return {
        "task_id": task_id,
        "prime_count": prime_count,
    }


async def run_async_task(task_id: int) -> dict:
    """Execute one asynchronous benchmark task."""

    await asyncio.sleep(IO_DELAY)

    prime_count = count_primes(CPU_LIMIT)

    return {
        "task_id": task_id,
        "prime_count": prime_count,
    }
