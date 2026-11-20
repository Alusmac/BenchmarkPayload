import json
import importlib
import sys

from dataclasses import asdict

from benchmark.runner import run_benchmark

MODELS = {
    "Sequential": ("strategies.sequential", "run_sequential"),
    "Threading": ("strategies.threading_model", "run_threading"),
    "Multiprocessing": (
        "strategies.multiprocessing_model",
        "run_multiprocessing",
    ),
    "Asyncio": ("strategies.asyncio_model", "run_asyncio"),
    "Gevent": ("strategies.gevent_model", "run_gevent"),

    "MP(TH(AS))": ("hybrid.mp_thread_async", "run_mp_thread_async"),
    "MP(AS(TH))": ("hybrid.mp_async_thread", "run_mp_async_thread"),
    "TH(MP(AS))": ("hybrid.th_mp_async", "run_thread_process_async"),
    "TH(AS(MP))": ("hybrid.th_async_mp", "run_thread_async_process"),
    "AS(MP(TH))": ("hybrid.as_mp_thread", "run_async_process_thread"),
    "AS(TH(MP))": ("hybrid.as_thread_mp", "run_as_thread_mp"),
    "MP(Gevent)": ("hybrid.mp_gevent", "run_mp_gevent"),
}


def main():
    model_name = sys.argv[1]

    module_name, function_name = MODELS[model_name]

    module = importlib.import_module(module_name)
    benchmark_function = getattr(module, function_name)

    result = run_benchmark(model_name, benchmark_function)

    print(json.dumps(asdict(result)))


if __name__ == "__main__":
    main()
