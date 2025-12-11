#!/usr/bin/env python3
"""
Обработчики generic-задач по описанию code_ref.
Выделены отдельно, чтобы разгрузить TaskExecutor.
"""

from __future__ import annotations

from typing import Any, Dict

from core.task import (
    Task,
    TaskType,
    RangeReduceTask,
    MapTask,
    MatrixOpsTask,
    MLInferenceTask,
    MLTrainStepTask,
)
from sandbox.execution import CodeBundle, SandboxLimits, SandboxResult
import os
import logging

logger = logging.getLogger(__name__)


async def execute_generic(task: Task, job, executor) -> Dict[str, Any]:
    """Исполнение generic-задачи на основе code_ref."""
    code_ref = task.code_ref or job.input_payload.get('code_ref', {})
    input_data = job.input_payload.get('input_data', task.input_data)
    handler_type = code_ref.get('type')
    handler = code_ref.get('handler')

    if handler_type == "builtin":
        if handler == "range_reduce":
            start = input_data.get('start', 0)
            end = input_data.get('end', 0)
            operation = code_ref.get('operation', 'sum')
            rr_task = RangeReduceTask(start=start, end=end, operation=operation, chunk_size=input_data.get('chunk_size', 1))
            output = executor._execute_range_reduce(rr_task)
            return {"success": True, "output": output}

        if handler in ("map_expression", "map_reduce"):
            map_task = MapTask(
                data=input_data if isinstance(input_data, list) else [input_data],
                function=code_ref.get('function', code_ref.get('map_function', 'square')),
                params=code_ref
            )
            mapped = executor._execute_map(map_task)
            # Для map_reduce reduce будет применён на этапе combine_job_results
            return {"success": True, "output": mapped}

        if handler == "matrix_ops":
            mx_task = MatrixOpsTask(
                operation=code_ref.get('operation') or (input_data or {}).get('operation', ''),
                matrix_a=(input_data or {}).get('matrix_a', []),
                matrix_b=(input_data or {}).get('matrix_b')
            )
            output = executor._execute_matrix_ops(mx_task)
            return {"success": True, "output": output}

    if handler_type == "ml_framework":
        if handler == "ml_inference":
            ml_task = MLInferenceTask(
                model_path=code_ref.get('model_path', ''),
                input_data=input_data,
                model_type=code_ref.get('framework', 'pytorch'),
                batch_size=(task.parallel or {}).get('batch_size', 1),
                params=code_ref
            )
            output = executor._execute_ml_inference(ml_task)
            return {"success": True, "output": output}
        if handler == "ml_train_step":
            ml_task = MLTrainStepTask(
                model_path=code_ref.get('model_path', ''),
                training_data=input_data,
                batch_size=(task.parallel or {}).get('batch_size', 32),
                learning_rate=code_ref.get('learning_rate', 0.001),
                epochs=code_ref.get('epochs', 1),
                model_type=code_ref.get('framework', 'pytorch'),
                params=code_ref
            )
            output = executor._execute_ml_train_step(ml_task)
            return {"success": True, "output": output}

    if handler_type == "python_script":
        if not getattr(executor, "sandbox_executor", None):
            return {"success": False, "output": None, "error": "Sandbox executor is not configured"}
        source = code_ref.get("source")
        location = code_ref.get("location")
        if not source and location and os.path.exists(location):
            with open(location, "r", encoding="utf-8") as fh:
                source = fh.read()
        bundle = CodeBundle(
            entrypoint=code_ref.get("entry", "main.py"),
            source=source or "",
            files=code_ref.get("files", {}),
            args=code_ref.get("args", []),
            env=code_ref.get("env", {}),
            stdin=None,
        )
        limits = SandboxLimits(
            cpu_time_seconds=int(task.requirements.timeout_seconds or 30),
            memory_bytes=int(task.requirements.ram_gb * 1024 * 1024 * 1024),
        )
        result: SandboxResult = await executor.sandbox_executor.execute(job=None, code_bundle=bundle, limits=limits)
        return {
            "success": result.success,
            "output": result.stdout,
            "error": result.stderr if not result.success else None,
        }

    if handler_type in ("wasm", "container"):
        logger.warning("%s code_ref requested but not implemented; returning error", handler_type)
        return {"success": False, "output": None, "error": f"{handler_type} code_ref not implemented yet"}

    return {"success": False, "output": None, "error": f"Unsupported code_ref: {code_ref}"}
