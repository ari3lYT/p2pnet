import pytest

from core.task import Task, TaskExecutor, TaskPriority


@pytest.mark.asyncio
async def test_split_and_execute_map():
    executor = TaskExecutor()
    task = Task.create_map(
        owner_id="tester",
        data=[1, 2, 3],
        function="increment",
        requirements={"cpu_percent": 10.0, "ram_gb": 0.1},
        config={"priority": TaskPriority.NORMAL.value},
    )
    jobs = executor.split_task_to_jobs(task)
    assert len(jobs) == 1
    result = await executor.execute(task)
    assert result["success"]
    assert result["result"] == [2, 3, 4]


@pytest.mark.asyncio
async def test_split_and_execute_range_reduce():
    executor = TaskExecutor()
    task = Task.create_range_reduce(
        owner_id="tester",
        start=1,
        end=6,
        operation="sum",
        requirements={"cpu_percent": 10.0, "ram_gb": 0.1},
        config={"priority": TaskPriority.NORMAL.value},
        task_params={"chunk_size": 2},
    )
    jobs = executor.split_task_to_jobs(task)
    assert len(jobs) >= 1
    result = await executor.execute(task)
    assert result["success"]
    assert result["result"] == sum(range(1, 6))


@pytest.mark.asyncio
async def test_pipeline_execution():
    executor = TaskExecutor()
    step1 = Task.create_map(
        owner_id="tester",
        data=[1, 2],
        function="increment",
        requirements={"cpu_percent": 5.0, "ram_gb": 0.1},
        config={"priority": TaskPriority.NORMAL.value},
    )
    step2 = Task.create_map_reduce(
        owner_id="tester",
        data=[],
        map_function="x",
        reduce_function="sum",
        requirements={"cpu_percent": 5.0, "ram_gb": 0.1},
        config={"priority": TaskPriority.NORMAL.value},
    )
    pipeline = Task.create_pipeline(
        owner_id="tester",
        nodes=[
            {"id": "s1", "task": step1.to_dict()},
            {"id": "s2", "depends_on": ["s1"], "task": step2.to_dict()},
        ],
        config={"priority": TaskPriority.NORMAL.value},
    )
    result = await executor.execute(pipeline)
    assert result["success"]
    assert result["result"] == sum([2, 3])


@pytest.mark.asyncio
async def test_generic_map_reduce():
    executor = TaskExecutor()
    task = Task.create_map_reduce(
        owner_id="tester",
        data=[1, 2, 3],
        map_function="x",
        reduce_function="sum",
        requirements={"cpu_percent": 10.0, "ram_gb": 0.1},
        config={"priority": TaskPriority.NORMAL.value},
    )
    result = await executor.execute(task)
    assert result["success"]
    assert result["result"] == 6
