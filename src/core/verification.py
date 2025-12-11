#!/usr/bin/env python3
"""
Verification engines that provide job replication and result validation.
"""

from __future__ import annotations

import copy
import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Tuple

from core.job import Job, JobResult
from core.task import Task

logger = logging.getLogger(__name__)


@dataclass
class VerificationResult:
    valid_results: List[JobResult]
    invalid_results: List[JobResult]
    penalties: List[Tuple[str, str]]


class VerificationEngine:
    async def select_jobs_for_replication(self, jobs: List[Job], task: Task) -> List[Job]:
        return []

    async def verify_job_results(self, task: Task, job_results: List[JobResult]) -> VerificationResult:
        return VerificationResult(
            valid_results=job_results,
            invalid_results=[],
            penalties=[]
        )


class OffVerificationEngine(VerificationEngine):
    """Не проводит дополнительных проверок."""

    pass


class BasicReplicationVerificationEngine(VerificationEngine):
    """Реплицирует задачи и сравнивает результаты."""

    def __init__(self, replicas: int = 1):
        self.replicas = max(1, replicas)

    async def select_jobs_for_replication(self, jobs: List[Job], task: Task) -> List[Job]:
        replicated: List[Job] = []
        for job in jobs:
            for replica_idx in range(self.replicas):
                replica = Job(
                    job_id=f"{job.job_id}#r{replica_idx + 1}",
                    task_id=job.task_id,
                    index=job.index,
                    task_type=job.task_type,
                    input_payload=copy.deepcopy(job.input_payload),
                    metadata={
                        **job.metadata,
                        "replica": True,
                        "replica_index": replica_idx + 1,
                    },
                    max_attempts=1
                )
                replica.canonical_id = job.canonical_id or job.job_id
                replicated.append(replica)

        if replicated:
            logger.debug("Scheduled %d replica jobs for verification", len(replicated))
        return replicated

    async def verify_job_results(self, task: Task, job_results: List[JobResult]) -> VerificationResult:
        grouped: Dict[str, List[JobResult]] = defaultdict(list)
        for result in job_results:
            canonical_id = result.metadata.get('canonical_id') or result.job_id.split('#')[0]
            grouped[canonical_id].append(result)

        valid_results: List[JobResult] = []
        invalid_results: List[JobResult] = []
        penalties: List[Tuple[str, str]] = []

        for canonical_id, results in grouped.items():
            if not results:
                continue

            canonical = next((res for res in results if res.success and not res.metadata.get('replica')), None)
            if not canonical:
                canonical = results[0]
            valid_results.append(canonical)

            for replica in results:
                if replica is canonical:
                    continue
                if replica.output != canonical.output or replica.success != canonical.success:
                    invalid_results.append(replica)
                    penalties.append((replica.worker_id, f"Mismatch for job {canonical_id}"))

        if penalties:
            logger.warning("Verification penalties detected: %s", penalties)

        return VerificationResult(
            valid_results=valid_results,
            invalid_results=invalid_results,
            penalties=penalties
        )


def get_verification_engine(task: Task) -> VerificationEngine:
    mode = (task.privacy or {}).get("zk_verify", "off").lower()
    if mode == "basic":
        return BasicReplicationVerificationEngine()
    if mode == "strict":
        # Пока используем ту же реализацию, но логируем о недоступности ZK
        logger.warning("Strict verification requested, falling back to basic replication")
        return BasicReplicationVerificationEngine(replicas=2)
    return OffVerificationEngine()
