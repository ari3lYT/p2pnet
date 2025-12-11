#!/usr/bin/env python3
"""
Формальное описание состояний job'а в сетевом протоколе.
"""

from enum import Enum


class JobStatus(str, Enum):
    """
    PENDING  -> ASSIGNED  (координатор создал job и готовит JOB_ASSIGN)
    ASSIGNED -> ACKED     (воркер ответил JOB_ACK со статусом accepted)
    ASSIGNED -> FAILED    (воркер отклонил job или превысился лимит попыток)
    ACKED    -> RUNNING   (воркер начал исполнение в sandbox)
    RUNNING  -> COMPLETED (воркер прислал JOB_RESULT с success=True)
    RUNNING  -> FAILED    (воркер прислал JOB_RESULT success=False или JOB_FAIL)
    ASSIGNED/RUNNING -> EXPIRED (координатор истёк таймаут ожидания)
    """

    PENDING = "pending"
    ASSIGNED = "assigned"
    ACKED = "acked"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    EXPIRED = "expired"
