#!/usr/bin/env python3
"""
Структуры данных координатора для очереди job'ов.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Dict, List, Optional

from core.job import Job
from core.task import Task
from core.job_state import JobStatus


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

    def mark_assigned(self, job_id: str, worker_id: str, now: float):
        record = self.jobs_by_id[job_id]
        record.status = JobStatus.ASSIGNED
        record.assigned_to = worker_id
        record.attempts += 1
        record.last_attempt_ts = now

    def mark_ack(self, job_id: str, now: float):
        record = self.jobs_by_id[job_id]
        record.status = JobStatus.ACKED
        record.last_attempt_ts = now

    def mark_result(self, job_id: str, success: bool, now: float):
        record = self.jobs_by_id[job_id]
        record.status = JobStatus.COMPLETED if success else JobStatus.FAILED
        record.last_attempt_ts = now
        record.next_retry_ts = now if success else now + 1.0

    def status_counters(self) -> Dict[JobStatus, int]:
        counters: Dict[JobStatus, int] = {status: 0 for status in JobStatus}
        for record in self.jobs_by_id.values():
            counters[record.status] = counters.get(record.status, 0) + 1
        return counters

    def jobs_due_for_retry(self, now: float) -> List[JobRecord]:
        due = []
        for record in self.jobs_by_id.values():
            if record.status in {JobStatus.FAILED, JobStatus.EXPIRED} and record.next_retry_ts <= now:
                due.append(record)
        return due
