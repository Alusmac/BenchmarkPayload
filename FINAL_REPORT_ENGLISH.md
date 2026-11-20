
# Architectural Benchmarking and Analysis of Concurrency Models in Python

## 1. Aim of the Work

The aim of this practical work is to investigate and compare the performance of different concurrency models in Python when executing a mixed workload that combines Input/Output (I/O-bound) operations and CPU-intensive (CPU-bound) operations.

The main objective is to determine how different parallel and asynchronous execution models affect program execution time and memory consumption.

## 2. Objectives

The following tasks were completed:

1. Implement basic concurrency models.
2. Implement seven hybrid architectures.
3. Create a unified benchmarking system.
4. Measure execution time and peak memory consumption.
5. Perform repeated runs to obtain median results.
6. Create a comparison table.
7. Analyze the results and identify the most efficient models.

## 3. Theoretical Background

The following Python concurrency technologies were investigated.

**Sequential Execution**

Tasks are executed one after another. Each new task starts only after the previous task has finished.

**Threading**

Uses multiple threads within a single process. It is particularly useful for I/O-bound tasks because threads can perform other operations while waiting for I/O operations to complete.

**Multiprocessing**

Uses multiple independent processes. It allows CPU-bound tasks to run in parallel because each process has its own Python interpreter.

**Asyncio**

Provides asynchronous programming using an event loop, coroutines, and `await`. It allows many I/O operations to be coordinated without creating a separate thread for each operation.

**Gevent**

A library for cooperative multitasking based on greenlets. When one greenlet waits for an I/O operation, execution can be transferred to another greenlet.

**Hybrid Models**

Combine several concurrency approaches, such as multiprocessing, threading, and asynchronous execution. Their efficiency depends on the workload and the overhead introduced by coordination.

## 4. Experimental Setup

All models were tested using the same workload.

| Parameter | Value |
|---|---:|
| Number of tasks | 100 |
| I/O delay | 0.1 seconds |
| CPU workload | Counting prime numbers up to 20,000 |
| Number of repetitions | 3 |
| Total benchmark runs | 36 |
| Programming language | Python |
| IDE | PyCharm |
| Operating system | macOS |

The `time.perf_counter()` function was used to measure execution time.

The `psutil` library was used to monitor memory consumption by tracking the RSS (Resident Set Size) of the main process and its child processes.

Each model was executed three times. The median value was used as the final result.

## 5. Implemented Models

### 5.1. Basic Models

Five basic concurrency models were implemented:

1. Sequential.
2. Threading.
3. Multiprocessing.
4. Asyncio.
5. Gevent.

### 5.2. Hybrid Models

Seven hybrid combinations were implemented:

| No. | Model | Architecture |
|---|---|---|
| 1 | MP(TH(AS)) | Processes → Threads → Asyncio |
| 2 | MP(AS(TH)) | Processes → Asyncio → Threads |
| 3 | TH(MP(AS)) | Threads → Processes → Asyncio |
| 4 | TH(AS(MP)) | Threads → Asyncio → Processes |
| 5 | AS(MP(TH)) | Asyncio → Processes → Threads |
| 6 | AS(TH(MP)) | Asyncio → Threads → Processes |
| 7 | MP(Gevent) | Processes → Gevent |

In total, 12 concurrency models were implemented and tested.

## 6. Experimental Results

The following table presents the median results obtained from three runs of each model.

| Model | Execution Time (s) | Memory (MB) | Completed Tasks |
|---|---:|---:|---:|
| Sequential | 11.4746 | 27.20 | 100 |
| Threading | 1.1662 | 26.25 | 100 |
| Multiprocessing | 2.8651 | 156.05 | 100 |
| Asyncio | 0.7235 | 25.28 | 100 |
| Gevent | 1.5672 | 33.62 | 100 |
| MP(TH(AS)) | 0.4193 | 97.89 | 100 |
| MP(AS(TH)) | 2.8855 | 98.30 | 100 |
| TH(MP(AS)) | 0.3093 | 152.47 | 100 |
| TH(AS(MP)) | 2.8826 | 153.03 | 100 |
| AS(MP(TH)) | 2.8445 | 97.05 | 100 |
| AS(TH(MP)) | 1.5173 | 277.98 | 100 |
| MP(Gevent) | 0.8865 | 110.22 | 100 |

All 12 models successfully completed all 100 tasks.

## 7. Analysis of the Results

### 7.1. Execution Time Comparison

The best execution time was achieved by **TH(MP(AS))**, with a result of 0.3093 seconds.

The second-best result was achieved by MP(TH(AS)), with 0.4193 seconds.

The slowest model was Sequential, with an execution time of 11.4746 seconds.

Therefore, the fastest hybrid model completed the workload approximately 37 times faster than sequential execution.

### 7.2. Memory Consumption Comparison

The lowest memory consumption was recorded by Asyncio — 25.28 MB.

The highest memory consumption was recorded by AS(TH(MP)) — 277.98 MB.

This can be explained by the additional overhead associated with creating and coordinating nested threads and processes.

It is important to note that RSS is a measure of resident process memory. Summing RSS values may count shared memory pages more than once, so it should not be considered an exact measurement of unique physical RAM usage.

### 7.3. Best Balance Between Performance and Memory

When both execution time and memory consumption are considered, MP(TH(AS)) demonstrates an interesting result:

- Execution time: 0.4193 seconds.
- Memory consumption: 97.89 MB.

It is approximately 35.6% slower than the fastest model but uses approximately 35.8% less memory.

Therefore, MP(TH(AS)) can be considered a reasonable compromise between execution speed and memory consumption in this experiment.

## 8. Analytical Questions and Answers

**1. Which model is best suited for mixed I/O + CPU workloads?**

According to the experimental results, TH(MP(AS)) achieved the fastest execution time of 0.3093 seconds.

It combines threading, multiprocessing, and asynchronous execution.

However, MP(TH(AS)) provides a better compromise between execution speed and memory consumption.

**2. Why can some hybrid combinations be inefficient?**

Each additional concurrency layer introduces overhead, including process and thread creation, context switching, synchronization, and data transfer.

For example, AS(TH(MP)) demonstrated the highest memory consumption — 277.98 MB.

Therefore, a more complex architecture does not necessarily provide better performance.

**3. Why is Multiprocessing not always faster than Threading?**

Multiprocessing introduces additional overhead related to process creation, inter-process communication, and data serialization.

For relatively small computational tasks, these costs can outweigh the benefits of parallel execution.

In our experiment, Threading achieved 1.1662 seconds, while Multiprocessing required 2.8651 seconds.

**4. How does the GIL affect CPU-bound tasks?**

In standard GIL-enabled CPython builds, the Global Interpreter Lock prevents multiple threads within the same process from executing Python bytecode simultaneously.

Therefore, multiprocessing is generally more effective for CPU-bound tasks because each process has its own Python interpreter and GIL.

For I/O-bound tasks, threading and asyncio can be more efficient because other operations can proceed while waiting for I/O.

**5. Why did Asyncio achieve a good result?**

Asyncio efficiently coordinates multiple I/O operations without creating a separate thread for every task.

In our experiment, asynchronous waiting allowed the total execution time to be significantly reduced compared with sequential execution.

However, synchronous CPU-intensive code inside a coroutine blocks the event loop while the computation is running.

## 9. Limitations of the Experiment

The following limitations should be considered when interpreting the results:

1. Only 100 tasks and one workload configuration were tested.
2. The CPU workload was relatively small: counting prime numbers up to 20,000.
3. Results depend on the computer's hardware and current system load.
4. Only three repetitions were performed for each model.
5. Hybrid models use different levels of parallelism and create different numbers of child processes.
6. RSS monitoring uses periodic sampling, so short-lived memory peaks may be missed, and shared memory pages may be counted more than once.

Future experiments could include increasing the number of tasks, increasing CPU workload, testing different numbers of workers, and performing more repetitions.

## 10. Conclusions

During this practical work, 12 Python concurrency models were implemented and investigated: five basic models and seven hybrid models.

A unified benchmarking system was developed to automate model execution, measure execution time and memory consumption, perform repeated runs, and generate a comparison table in CSV format.

The experiment demonstrated that the fastest model for the selected mixed workload was **TH(MP(AS))**, with an execution time of 0.3093 seconds.

The lowest memory consumption was achieved by **Asyncio**, with 25.28 MB.

The **MP(TH(AS))** model demonstrated a good compromise between execution speed and memory consumption.

The experiment confirms that the choice of a concurrency model depends on the workload type, task complexity, number of workers, and coordination overhead.

**Main conclusion:** There is no universally best concurrency model. The most efficient architecture depends on the specific requirements of an application and should be selected based on actual performance measurements.