#!/usr/bin/env python3
"""
Privacy engines that transform tasks and job results according to privacy mode.
"""

from __future__ import annotations

import logging
import random
from typing import TYPE_CHECKING, Any, List

from core.job import Job, JobResult
from core.task import Task, TaskType

if TYPE_CHECKING:  # pragma: no cover
    pass

logger = logging.getLogger(__name__)


class BasePrivacyEngine:
    """Базовый privacy-движок, не меняющий поведение."""

    def __init__(self, executor: Any):
        self.executor = executor

    async def prepare_task(self, task: Task) -> Task:
        return task

    async def before_job_assign(self, task: Task, job: Job) -> Job:
        return job

    async def after_job_result(self, task: Task, job_result: JobResult) -> JobResult:
        return job_result

    async def finalize_task_result(self, task: Task, job_results: List[JobResult]):
        return self.executor.combine_job_results(task, job_results)


class ShardPrivacyEngine(BasePrivacyEngine):
    """Режим shard полагается на базовый шардинг задач."""

    async def prepare_task(self, task: Task) -> Task:
        logger.debug("Task %s is running in shard mode", task.task_id)
        return task


class MaskPrivacyEngine(BasePrivacyEngine):
    """Простая маскировка входных данных (поддержка только для map-задач)."""

    async def prepare_task(self, task: Task) -> Task:
        if task.task_type != TaskType.MAP or not task.map or not task.map.data:
            logger.warning(
                "Mask privacy mode is supported only for map tasks. Fallback to shard."
            )
            return task

        permutation = list(range(len(task.map.data)))
        random.shuffle(permutation)
        shuffled = [task.map.data[idx] for idx in permutation]
        task.map.data = shuffled
        task.metadata["mask_permutation"] = permutation
        logger.debug(
            "Task %s masked with permutation of %d elements",
            task.task_id,
            len(permutation),
        )
        return task

    async def finalize_task_result(self, task: Task, job_results: List[JobResult]):
        shuffled_result = await super().finalize_task_result(task, job_results)
        permutation = task.metadata.get("mask_permutation")
        if not permutation or not isinstance(shuffled_result, list):
            return shuffled_result

        restored = [None] * len(permutation)
        for shuffled_idx, original_idx in enumerate(permutation):
            restored[original_idx] = shuffled_result[shuffled_idx]
        return restored


def get_privacy_engine(task: Task, executor: Any) -> BasePrivacyEngine:
    mode = (task.privacy or {}).get("mode", "none").lower()
    if mode == "shard":
        return ShardPrivacyEngine(executor)
    if mode == "mask":
        return MaskPrivacyEngine(executor)
    if mode not in ("none", "auto"):
        logger.warning("Privacy mode '%s' is not implemented, using default.", mode)
    return BasePrivacyEngine(executor)
