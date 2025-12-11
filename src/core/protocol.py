#!/usr/bin/env python3
"""
Сетевые сообщения уровня job'ов и их полезная нагрузка.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Dict, Optional


class MessageType(str, Enum):
    JOB_ASSIGN = "JOB_ASSIGN"
    JOB_ACK = "JOB_ACK"
    JOB_RESULT = "JOB_RESULT"
    JOB_FAIL = "JOB_FAIL"
    WORKER_HEARTBEAT = "WORKER_HEARTBEAT"
    TASK_STATUS_UPDATE = "TASK_STATUS_UPDATE"


@dataclass
class MessageEnvelope:
    msg_type: MessageType
    msg_id: str
    src_node: str
    dst_node: str
    timestamp: float
    payload: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "msg_type": self.msg_type.value,
            "msg_id": self.msg_id,
            "src_node": self.src_node,
            "dst_node": self.dst_node,
            "timestamp": self.timestamp,
            "payload": self.payload,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MessageEnvelope":
        return cls(
            msg_type=MessageType(data["msg_type"]),
            msg_id=data["msg_id"],
            src_node=data["src_node"],
            dst_node=data["dst_node"],
            timestamp=data["timestamp"],
            payload=data.get("payload", {}),
        )

    @classmethod
    def create(cls, msg_type: MessageType, src_node: str, dst_node: str, payload: Dict[str, Any]) -> "MessageEnvelope":
        return cls(
            msg_type=msg_type,
            msg_id=str(uuid.uuid4()),
            src_node=src_node,
            dst_node=dst_node,
            timestamp=time.time(),
            payload=payload,
        )


@dataclass
class JobAssignPayload:
    task_id: str
    job_id: str
    attempt: int
    code_ref: Dict[str, Any]
    sandbox_type: str
    input_payload: Any
    requirements: Dict[str, Any]
    deadline_ts: float
    privacy: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "JobAssignPayload":
        return cls(**data)


@dataclass
class JobAckPayload:
    task_id: str
    job_id: str
    status: str  # accepted | busy | rejected
    reason: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "JobAckPayload":
        return cls(**data)


@dataclass
class JobResultPayload:
    task_id: str
    job_id: str
    success: bool
    output: Any
    error: Optional[str]
    runtime_ms: float
    worker_id: str
    attempt: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "JobResultPayload":
        return cls(**data)


@dataclass
class JobFailPayload:
    task_id: str
    job_id: str
    worker_id: str
    reason: str
    attempt: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "JobFailPayload":
        return cls(**data)
