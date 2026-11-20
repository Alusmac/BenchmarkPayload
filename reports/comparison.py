import csv
from dataclasses import asdict
from pathlib import Path

from benchmark.metrics import BenchmarkResult


def save_results_to_csv(
        results: list[BenchmarkResult],
) -> None:
    """Save benchmark results to a CSV file."""

    output_file = Path(__file__).parent / "results.csv"

    with output_file.open(
            mode="w",
            newline="",
            encoding="utf-8",
    ) as file:
        fieldnames = [
            "model_name",
            "execution_time",
            "peak_memory_mb",
            "tasks_completed",
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for result in results:
            writer.writerow(asdict(result))

    print(f"\nResults saved to: {output_file}")
