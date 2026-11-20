from gevent import monkey

monkey.patch_all()

import gevent
from gevent.pool import Pool

from benchmark.payload import TASK_COUNT, run_sync_task

MAX_WORKERS = 10


def run_gevent() -> list[dict]:
    """Execute tasks using gevent greenlets."""

    pool = Pool(MAX_WORKERS)

    jobs = [
        pool.spawn(run_sync_task, task_id)
        for task_id in range(TASK_COUNT)
    ]

    gevent.joinall(jobs)

    results = [job.value for job in jobs]

    return results


if __name__ == "__main__":
    results = run_gevent()
    print("Gevent tasks completed:", len(results))
    print("Prime count:", results[0]["prime_count"])
