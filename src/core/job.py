#!/usr/bin/env python3
"""
Job abstraction for splitting high-level tasks into sub tasks.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional

from core.job_state import JobStatus


class TaskStatus(Enum):
    PENDING = "pending"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


@dataclass
class Job:
    """Подзадача, которая передается воркеру для исполнения."""

    job_id: str
    task_id: str
    index: int
    task_type: str
    input_payload: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    status: JobStatus = JobStatus.PENDING
    attempts: int = 0
    max_attempts: int = 3
    assigned_worker: Optional[str] = None
    canonical_id: Optional[str] = None


@dataclass
class JobResult:
    """Результат выполнения подзадачи."""

    job_id: str
    task_id: str
    worker_id: str
    output: Any
    success: bool
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
