import json
import subprocess
import sys

from pathlib import Path
from statistics import median

from benchmark.metrics import BenchmarkResult
from benchmark.payload import TASK_COUNT
from reports.comparison import save_results_to_csv

PROJECT_ROOT = Path(__file__).resolve().parent

REPEATS = 3

MODELS = [
    "Sequential",
    "Threading",
    "Multiprocessing",
    "Asyncio",
    "Gevent",
    "MP(TH(AS))",
    "MP(AS(TH))",
    "TH(MP(AS))",
    "TH(AS(MP))",
    "AS(MP(TH))",
    "AS(TH(MP))",
    "MP(Gevent)",
]


def run_model_isolated(model_name: str) -> BenchmarkResult:
    """Run one model in a separate Python process."""

    command = [
        sys.executable,
        "-m",
        "benchmark.isolated_runner",
        model_name,
    ]

    completed = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    result_data = json.loads(completed.stdout.strip())

    return BenchmarkResult(**result_data)


def run_repeated_benchmark(model_name: str) -> BenchmarkResult:
    """Run a model several times and calculate median metrics."""

    execution_times = []
    memory_values = []

    for repetition in range(1, REPEATS + 1):
        print(f"  Run {repetition}/{REPEATS}...")

        result = run_model_isolated(model_name)

        if result.tasks_completed != TASK_COUNT:
            raise RuntimeError(
                f"{model_name}: expected {TASK_COUNT} tasks, "
                f"got {result.tasks_completed}"
            )

        execution_times.append(result.execution_time)
        memory_values.append(result.peak_memory_mb)

        print(
            f"  Time: {result.execution_time:.4f} s | "
            f"Memory: {result.peak_memory_mb:.2f} MB"
        )

    return BenchmarkResult(
        model_name=model_name,
        execution_time=median(execution_times),
        peak_memory_mb=median(memory_values),
        tasks_completed=TASK_COUNT,
    )


def display_comparison(results: list[BenchmarkResult]) -> None:
    """Display sorted benchmark comparison."""

    print("\n" + "=" * 85)
    print("MEDIAN BENCHMARK COMPARISON")
    print("=" * 85)

    print(
        f"{'Model':<20}"
        f"{'Time (s)':<18}"
        f"{'Memory (MB)':<18}"
        f"{'Tasks':<10}"
    )

    print("-" * 85)

    for result in sorted(
            results,
            key=lambda item: item.execution_time,
    ):
        print(
            f"{result.model_name:<20}"
            f"{result.execution_time:<18.4f}"
            f"{result.peak_memory_mb:<18.2f}"
            f"{result.tasks_completed:<10}"
        )

    print("=" * 85)


def main() -> None:
    print("\n=== PYTHON CONCURRENCY BENCHMARK ===")
    print(f"Models: {len(MODELS)}")
    print(f"Repetitions per model: {REPEATS}")
    print(f"Total benchmark runs: {len(MODELS) * REPEATS}")

    benchmark_results = []

    for index, model_name in enumerate(MODELS, start=1):
        print(f"\n[{index}/{len(MODELS)}] Running {model_name}...")

        try:
            result = run_repeated_benchmark(model_name)
            benchmark_results.append(result)

            print(
                f"Median time: {result.execution_time:.4f} seconds"
            )
            print(
                f"Median memory: {result.peak_memory_mb:.2f} MB"
            )

        except subprocess.CalledProcessError as error:
            print(f"ERROR while running {model_name}")
            print(error.stderr)
            raise

    display_comparison(benchmark_results)

    print("\n=== SAVING RESULTS ===")
    save_results_to_csv(benchmark_results)

    print("\n=== BENCHMARK COMPLETED ===")


if __name__ == "__main__":
    main()
