import asyncio

from core.pipeline import run_pipeline
from core.task import Task, TaskExecutor


def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


def test_pipeline_with_dependency_map_to_map_reduce():
    executor = TaskExecutor()
    # node1: map squares
    map_task = Task.create_map(owner_id="o", data=[1, 2, 3], function="square")
    # node2: map_reduce sum, data пустое — будет подставлено из зависимости
    mr_task = Task.create_map_reduce(owner_id="o", data=[], map_function="x", reduce_function="sum")

    pipeline_task = Task.create_pipeline(
        owner_id="o",
        nodes=[
            {"id": "step1", "task": map_task.to_dict(), "depends_on": []},
            {"id": "step2", "task": mr_task.to_dict(), "depends_on": ["step1"]},
        ],
    )

    result = _run(run_pipeline(pipeline_task, executor))
    # ensure run completed and result aggregated
    assert result["success"]
    assert result["result"] in (9, 14)


def test_pipeline_cycle_fails():
    executor = TaskExecutor()
    node_a = Task.create_map(owner_id="o", data=[1], function="square")
    node_b = Task.create_map_reduce(owner_id="o", data=[], map_function="x", reduce_function="sum")
    pipeline_task = Task.create_pipeline(
        owner_id="o",
        nodes=[
            {"id": "a", "task": node_a.to_dict(), "depends_on": ["b"]},
            {"id": "b", "task": node_b.to_dict(), "depends_on": ["a"]},
        ],
    )
    result = _run(run_pipeline(pipeline_task, executor))
    assert result["success"] is False
