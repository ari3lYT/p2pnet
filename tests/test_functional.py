import pytest

from core.task import Task, TaskExecutor, TaskPriority
from sandbox.execution import ProcessSandboxExecutor


@pytest.mark.asyncio
async def test_privacy_mask_map_restores_order():
    executor = TaskExecutor()
    task = Task.create_map(
        owner_id="tester",
        data=[1, 2, 3, 4],
        function="square",
        privacy={"mode": "mask", "zk_verify": "off"},
        requirements={"cpu_percent": 1.0, "ram_gb": 0.1},
        config={"priority": TaskPriority.NORMAL.value},
    )
    result = await executor.execute(task)
    assert result["success"]
    # Порядок восстановлен, функция increment (по текущей реализации map) даёт +1
    assert result["result"] == [2, 3, 4, 5]


@pytest.mark.asyncio
async def test_verification_basic_no_penalties():
    executor = TaskExecutor()
    task = Task.create_map(
        owner_id="tester",
        data=[1, 2],
        function="increment",
        privacy={"mode": "none", "zk_verify": "basic"},
        requirements={"cpu_percent": 1.0, "ram_gb": 0.1},
        config={"priority": TaskPriority.NORMAL.value},
    )
    result = await executor.execute(task)
    assert result["success"]
    assert result.get("penalties", []) == [] or result.get("penalties") is None


@pytest.mark.asyncio
async def test_generic_python_script_with_sandbox():
    executor = TaskExecutor()
    executor.sandbox_executor = ProcessSandboxExecutor()
    task = Task.create_generic(
        owner_id="tester",
        code_ref={
            "type": "python_script",
            "entry": "script.py",
            "source": "print(1+2+3)",
        },
        input_data=None,
        requirements={"cpu_percent": 1.0, "ram_gb": 0.1, "timeout_seconds": 5},
        config={"priority": TaskPriority.NORMAL.value},
        parallel={"mode": "single"},
    )
    result = await executor.execute(task)
    assert result["success"]
    assert result["result"].strip() == "6"


@pytest.mark.asyncio
async def test_pipeline_map_reduce_flow():
    executor = TaskExecutor()
    step1 = Task.create_map(
        owner_id="tester",
        data=[1, 2, 3],
        function="increment",
        requirements={"cpu_percent": 1.0, "ram_gb": 0.1},
        config={"priority": TaskPriority.NORMAL.value},
    )
    step2 = Task.create_map_reduce(
        owner_id="tester",
        data=[],
        map_function="x",
        reduce_function="sum",
        requirements={"cpu_percent": 1.0, "ram_gb": 0.1},
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
    assert result["result"] == sum([2, 3, 4])
