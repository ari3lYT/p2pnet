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
    """
    Исполнение pipeline/DAG с учётом depends_on.
    Узлы без зависимостей запускаются параллельно.
    """
    nodes = {node["id"]: node for node in (task.pipeline or {}).get("nodes", []) if "id" in node}
    results: Dict[str, Any] = {}
    completed = set()

    async def run_node(node_id: str, node_def: Dict[str, Any]):
        deps = set(node_def.get("depends_on", []))
        node_task_data = node_def.get("task", {})
        if isinstance(node_task_data, Task):
            node_task = node_task_data
        else:
            node_task = Task.from_dict(node_task_data)
        node_task.input_data = node_task.input_data or {dep: results.get(dep) for dep in deps}
        result = await executor.execute(node_task)
        results[node_id] = result.get("result")
        completed.add(node_id)

    # Топологические слои
    while len(completed) < len(nodes):
        ready = []
        for node_id, node in nodes.items():
            if node_id in completed:
                continue
            deps = set(node.get("depends_on", []))
            if deps.issubset(completed):
                ready.append((node_id, node))
        if not ready:
            break  # цикл или отсутствие прогресса
        await asyncio.gather(*(run_node(nid, ndef) for nid, ndef in ready))

    final_output = results[max(results.keys(), default=None, key=lambda x: x)] if results else None
    return executor._build_response(task, final_output, 0.0)
