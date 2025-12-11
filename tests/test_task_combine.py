import pytest

from core.task import Task, TaskExecutor, TaskPriority


@pytest.mark.parametrize(
    "operation, data, expected",
    [
        ("sum", [1, 2, 3], 6),
        ("product", [1, 2, 3], 6),
        ("min", [3, 1, 2], 1),
        ("max", [3, 1, 2], 3),
        ("average", [1, 2, 3, 4], 2.5),
    ],
)
def test_combine_range_reduce(operation, data, expected):
    executor = TaskExecutor()
    task = Task.create_range_reduce(
        owner_id="t",
        start=0,
        end=len(data),
        operation=operation,
        requirements={"cpu_percent": 1.0, "ram_gb": 0.1},
        config={"priority": TaskPriority.NORMAL.value},
        task_params={"chunk_size": 2},
    )
    # Имитация результатов job'ов
    from core.job import JobResult

    job_results = []
    for i, v in enumerate(data):
        job_results.append(
            JobResult(
                job_id=f"{task.task_id}:{i}",
                task_id=task.task_id,
                worker_id="w",
                output=v,
                success=True,
            )
        )
    combined = executor.combine_job_results(task, job_results)
    assert combined == expected


def test_combine_generic_map_reduce_sum():
    executor = TaskExecutor()
    task = Task.create_map_reduce(
        owner_id="t",
        data=[1, 2, 3],
        map_function="x",
        reduce_function="sum",
        requirements={"cpu_percent": 1.0, "ram_gb": 0.1},
        config={"priority": TaskPriority.NORMAL.value},
    )
    from core.job import JobResult

    job_results = [
        JobResult(job_id="j1", task_id=task.task_id, worker_id="w", output=[1, 2, 3], success=True),
    ]
    combined = executor.combine_job_results(task, job_results)
    assert combined == 6
