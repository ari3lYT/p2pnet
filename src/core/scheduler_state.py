#!/usr/bin/env python3
"""
Структуры данных координатора для очереди job'ов.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Dict, List, Optional

from core.job import Job
from core.job_state import JobStatus
from core.task import Task

logger = logging.getLogger(__name__)


@dataclass
class JobRecord:
    job: Job
    status: JobStatus
    assigned_to: Optional[str]
    attempts: int
    last_attempt_ts: float
    next_retry_ts: float


class TaskSchedulerState:
    def __init__(self):
        self.jobs_by_id: Dict[str, JobRecord] = {}
        self.jobs_by_task: Dict[str, List[str]] = {}

    def register_jobs_for_task(self, task: Task, jobs: List[Job]):
        now = time.time()
        self.jobs_by_task.setdefault(task.task_id, [])
        for job in jobs:
            record = JobRecord(
                job=job,
                status=JobStatus.PENDING,
                assigned_to=None,
                attempts=0,
                last_attempt_ts=0.0,
                next_retry_ts=now,
            )
            self.jobs_by_id[job.job_id] = record
            self.jobs_by_task[task.task_id].append(job.job_id)
            logger.debug("Job %s registered for task %s", job.job_id, task.task_id)

    def mark_assigned(self, job_id: str, worker_id: str, now: float):
        record = self.jobs_by_id[job_id]
        record.status = JobStatus.ASSIGNED
        record.assigned_to = worker_id
        record.attempts += 1
        record.last_attempt_ts = now
        logger.debug("Job %s assigned to %s (attempt %d)", job_id, worker_id, record.attempts)

    def mark_ack(self, job_id: str, now: float):
        record = self.jobs_by_id[job_id]
        record.status = JobStatus.ACKED
        record.last_attempt_ts = now
        logger.debug("Job %s acked by worker %s", job_id, record.assigned_to)

    def mark_result(self, job_id: str, success: bool, now: float):
        record = self.jobs_by_id[job_id]
        record.status = JobStatus.COMPLETED if success else JobStatus.FAILED
        record.last_attempt_ts = now
        record.next_retry_ts = now if success else now + 1.0
        logger.debug("Job %s result status=%s", job_id, "success" if success else "failed")

    def to_event_list(self) -> List[Dict]:
        events = []
        for rec in self.jobs_by_id.values():
            events.append({
                "job_id": rec.job.job_id,
                "task_id": rec.job.task_id,
                "status": rec.status.value,
                "attempts": rec.attempts,
                "assigned_to": rec.assigned_to,
                "last_attempt_ts": rec.last_attempt_ts,
            })
        return events

    def status_counters(self) -> Dict[JobStatus, int]:
        counters: Dict[JobStatus, int] = dict.fromkeys(JobStatus, 0)
        for record in self.jobs_by_id.values():
            counters[record.status] = counters.get(record.status, 0) + 1
        return counters

    def jobs_due_for_retry(self, now: float) -> List[JobRecord]:
        due = []
        for record in self.jobs_by_id.values():
            if record.status in {JobStatus.FAILED, JobStatus.EXPIRED} and record.next_retry_ts <= now:
                due.append(record)
        return due
