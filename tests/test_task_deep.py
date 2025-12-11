import asyncio

import pytest

from core.job import Job, JobResult
from core.job_state import JobStatus
from core.task import (
    MapTask,
    RangeReduceTask,
    ResourceRequirements,
    Task,
    TaskConfig,
    TaskExecutor,
    TaskPriority,
    TaskType,
)


def run(coro):
    return asyncio.get_event_loop_policy().new_event_loop().run_until_complete(coro)


def test_task_factories_and_get_task_data():
    rr = Task.create_range_reduce("o", 1, 5, "min")
    mp = Task.create_map("o", [1, 2], "filter", task_params={"function": lambda x: x > 1})
    mr = Task.create_map_reduce("o", [1, 2], "square", "sum")
    mx = Task.create_matrix_ops("o", "transpose", [[1, 2], [3, 4]])
    ml_inf = Task.create_ml_inference("o", "model", [1], "onnx")
    ml_train = Task.create_ml_train_step("o", "model", [[1, 2]], task_params={"epochs": 2})

    assert rr.get_task_data()["operation"] == "min"
    assert mp.get_task_data()["function"] == "filter"
    assert mr.get_task_data()["reduce_function"] == "sum"
    assert mx.get_task_data()["operation"] == "transpose"
    assert ml_inf.get_task_data()["model_type"] == "onnx"
    assert ml_train.get_task_data()["epochs"] == 2
    # валидация ошибок
    bad_matrix = Task.create_matrix_ops("o", "add", [], [])
    errors = bad_matrix.validate()
    assert "matrix_a cannot be empty" in errors
    bad_ml = Task.create_ml_inference("o", "", [], "pytorch")
    assert any("model_path" in e for e in bad_ml.validate())
    bad_train = Task.create_ml_train_step("o", "", [])
    assert any("model_path" in e or "training_data" in e for e in bad_train.validate())


def test_task_from_dict_with_status():
    original = Task(
        task_id="t",
        task_type=TaskType.MAP,
        owner_id="o",
        created_at=1.0,
        requirements=ResourceRequirements(),
        config=TaskConfig(priority=TaskPriority.HIGH),
        map=MapTask(data=[1], function="square"),
    )
    original.status = JobStatus.COMPLETED
    data = original.to_dict()
    restored = Task.from_dict(data)
    from core.job import TaskStatus
    assert restored.status == TaskStatus.COMPLETED


def test_executor_split_generic_modes():
    executor = TaskExecutor()
    task = Task.create_generic(
        "o",
        {"type": "builtin", "handler": "map_expression", "function": "square"},
        [1, 2, 3],
        parallel={"mode": "map", "chunk_size": 2},
    )
    jobs = executor.split_task_to_jobs(task)
    assert len(jobs) == 2
    task.parallel = {"mode": "single"}
    jobs_single = executor.split_task_to_jobs(task)
    assert len(jobs_single) == 1
    # fallback single job snapshot
    no_parallel = Task.create_generic("o", {"type": "builtin", "handler": "matrix_ops", "operation": "add"}, {"matrix_a": [[1]], "matrix_b": [[2]]})
    single_jobs = executor.split_task_to_jobs(no_parallel)
    assert single_jobs[0].input_payload.get("input_data") is not None


def test_executor_safe_execute_job_error_path():
    executor = TaskExecutor()
    bad_task = Task.create_generic("o", {"type": "unsupported"}, None)
    job = Job(job_id="x:0", task_id="x", index=0, task_type=TaskType.GENERIC.value, input_payload={"code_ref": {"type": "unsupported"}})
    result = run(executor._safe_execute_job(bad_task, job))
    assert result.success is False
    assert "Unsupported" in (result.error or "")


def test_execute_direct_and_helpers():
    executor = TaskExecutor()
    rr_task = Task.create_range_reduce("o", 1, 4, "product")
    direct = executor._execute_direct(rr_task)
    assert direct["result"] == 6
    # map helpers
    assert executor._increment_map([1, 2]) == [2, 3]
    assert executor._sum_range([1, 2, 3]) == 6
    # range reduce variations
    assert executor._execute_range_reduce(RangeReduceTask(start=0, end=3, operation="average")) == 1.0
    assert executor._execute_range_reduce(RangeReduceTask(start=0, end=3, operation="min")) == 0
    assert executor._execute_range_reduce(RangeReduceTask(start=0, end=3, operation="max")) == 2


def test_execute_ml_paths_and_costs():
    executor = TaskExecutor()
    task = Task.create_map("o", [1, 2, 3], "increment", config={"priority": TaskPriority.HIGH.value})
    cost = task.calculate_cost({"cpu_score": 50, "gpu_score": 0})
    assert cost > 0
    assert task.estimate_execution_time() > 0
    # map transform/filter
    t_map = MapTask(data=[1, 2, 3], function="transform", params={"function": lambda x: x * 2})
    assert executor._execute_map(t_map) == [2, 4, 6]
    f_map = MapTask(data=[1, 2, 3], function="filter", params={"function": lambda x: x > 1})
    assert executor._execute_map(f_map) == [2, 3]


def test_combine_job_results_generic_map_reduce_product():
    executor = TaskExecutor()
    task = Task.create_generic(
        owner_id="o",
        code_ref={"type": "builtin", "handler": "map_reduce", "reduce_function": "product", "map_function": "x"},
        input_data=[1, 2, 3, 4],
        parallel={"mode": "map_reduce", "chunk_size": 2},
        requirements={},
        config={},
    )
    results = [
        JobResult(job_id="j1", task_id=task.task_id, worker_id="w", output=[1, 2], success=True, metadata={"canonical_id": "j1"}),
        JobResult(job_id="j2", task_id=task.task_id, worker_id="w", output=[3, 4], success=True, metadata={"canonical_id": "j2"}),
    ]
    assert executor.combine_job_results(task, results) == 24


def test_execute_job_with_task_snapshot_path():
    executor = TaskExecutor()
    task = Task.create_map("o", [1, 2], "increment")
    snapshot = task.to_dict()
    job = Job(
        job_id="snap:0",
        task_id=task.task_id,
        index=0,
        task_type="unknown",
        input_payload={"task_snapshot": snapshot},
    )
    result = run(executor._execute_job(task, job))
    assert result.success is False
    assert "attribute" in (result.error or "")


def test_scheduler_to_event_and_counters():
    from core.scheduler_state import TaskSchedulerState
    scheduler = TaskSchedulerState()
    task = Task.create_map("o", [1], "increment")
    job = Job(job_id="evt:0", task_id=task.task_id, index=0, task_type=TaskType.MAP.value, input_payload={})
    scheduler.register_jobs_for_task(task, [job])
    scheduler.mark_assigned(job.job_id, "worker", now=0)
    scheduler.mark_result(job.job_id, success=True, now=1)
    events = scheduler.to_event_list()
    assert events and events[0]["job_id"] == job.job_id
    counters = scheduler.status_counters()
    from core.job_state import JobStatus
    assert counters[JobStatus.COMPLETED] >= 1


def test_matrix_helpers_and_notimplemented():
    executor = TaskExecutor()
    a = [[1, 2], [3, 4]]
    b = [[1, 0], [0, 1]]
    assert executor._matrix_multiply(a, b)[0][0] == 1
    with pytest.raises(NotImplementedError):
        executor._matrix_decompose(a)
    assert executor._pytorch_inference("model", [1])["predictions"]
    assert executor._tensorflow_inference("model", [1])["predictions"]
