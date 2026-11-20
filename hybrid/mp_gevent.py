from concurrent.futures import ProcessPoolExecutor

PROCESS_WORKERS = 2
GEVENT_WORKERS = 10


def process_worker(task_ids: list[int]) -> list[dict]:
    from gevent import monkey
    monkey.patch_all()

    import gevent
    from gevent.pool import Pool

    from benchmark.payload import run_sync_task

    pool = Pool(GEVENT_WORKERS)

    jobs = [
        pool.spawn(run_sync_task, task_id)
        for task_id in task_ids
    ]

    gevent.joinall(jobs)

    return [job.value for job in jobs]


def run_mp_gevent() -> list[dict]:
    from benchmark.payload import TASK_COUNT

    task_ids = list(range(TASK_COUNT))

    chunks = [
        task_ids[index::PROCESS_WORKERS]
        for index in range(PROCESS_WORKERS)
    ]

    with ProcessPoolExecutor(max_workers=PROCESS_WORKERS) as executor:
        results = list(executor.map(process_worker, chunks))

    return [
        result
        for batch in results
        for result in batch
    ]


if __name__ == "__main__":
    results = run_mp_gevent()

    print("Model: MP(Gevent)")
    print("Tasks completed:", len(results))
    print("Prime count:", results[0]["prime_count"])
