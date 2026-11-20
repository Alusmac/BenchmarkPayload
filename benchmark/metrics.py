from dataclasses import dataclass


@dataclass
class BenchmarkResult:
    """Store benchmark results for one concurrency model."""

    model_name: str
    execution_time: float
    peak_memory_mb: float
    tasks_completed: int

    def display(self) -> None:
        """Display benchmark results."""

        print(f"\nModel: {self.model_name}")
        print(f"Execution Time: {self.execution_time:.4f} seconds")
        print(f"Peak Memory: {self.peak_memory_mb:.2f} MB")
        print(f"Tasks Completed: {self.tasks_completed}")
