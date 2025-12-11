#!/usr/bin/env python3
"""
Вспомогательный модуль для исполнения pipeline/DAG задач.
"""

from __future__ import annotations

from typing import Any, Dict
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from core.task import Task


async def run_pipeline(task: "Task", executor) -> Dict[str, Any]:
    """Последовательное исполнение pipeline/DAG (упрощённый режим)."""
    nodes = (task.pipeline or {}).get('nodes', [])
    previous_result = None
    for node in nodes:
        node_task_data = node.get('task', {})
        if isinstance(node_task_data, Task):
            node_task = node_task_data
        else:
            node_task = Task.from_dict(node_task_data)
        if previous_result is not None and node_task.input_data is None:
            node_task.input_data = previous_result
        result = await executor.execute(node_task)
        previous_result = result.get('result')
    return executor._build_response(task, previous_result, 0.0)
