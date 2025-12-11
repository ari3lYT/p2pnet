#!/usr/bin/env python3
"""
Абстракция транспорта для обмена MessageEnvelope между узлами.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Awaitable, Callable, Dict

from core.protocol import MessageEnvelope

HandlerCallable = Callable[[MessageEnvelope], Awaitable[None]]
logger = logging.getLogger(__name__)


class Transport(ABC):
    @abstractmethod
    async def send(self, dst_node: str, message: MessageEnvelope) -> None:
        raise NotImplementedError

    @abstractmethod
    def register_handler(self, node_id: str, handler: HandlerCallable) -> None:
        raise NotImplementedError


class InMemoryTransport(Transport):
    """Простейший транспорт для тестов: вызывает хендлеры в памяти."""

    def __init__(self):
        self._handlers: Dict[str, HandlerCallable] = {}

    def register_handler(self, node_id: str, handler: HandlerCallable) -> None:
        self._handlers[node_id] = handler

    async def send(self, dst_node: str, message: MessageEnvelope) -> None:
        handler = self._handlers.get(dst_node)
        if handler:
            await handler(message)
        else:
            logger.warning("Node %s is unreachable for message %s", dst_node, message.msg_id)
