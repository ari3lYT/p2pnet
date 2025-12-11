#!/usr/bin/env python3
"""
Интерфейс и реализации песочниц для выполнения пользовательского кода.
"""

from __future__ import annotations

import asyncio
import logging
import os
import shutil
import sys
import tempfile
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, TYPE_CHECKING

try:
    import resource
except ImportError:  # pragma: no cover - Windows
    resource = None

if TYPE_CHECKING:  # pragma: no cover
    from core.job import Job


logger = logging.getLogger(__name__)


class SandboxType(str, Enum):
    """Типы поддерживаемых песочниц."""

    PROCESS_ISOLATION = "process_isolation"
    WASM = "wasm"
    CONTAINER = "container"


@dataclass
class SandboxLimits:
    """Лимиты ресурсов для песочницы."""

    cpu_time_seconds: int = 30
    memory_bytes: int = 256 * 1024 * 1024
    wall_time_seconds: int = 30
    file_size_bytes: int = 64 * 1024 * 1024
    open_files: int = 256
    working_dir_quota_bytes: int = 256 * 1024 * 1024
    env: Dict[str, str] = field(default_factory=dict)


@dataclass
class SandboxResult:
    """Результат выполнения кода в песочнице."""

    success: bool
    stdout: str
    stderr: str
    exit_code: int
    runtime: float
    timed_out: bool = False
    killed: bool = False
    usage: Dict[str, Any] = field(default_factory=dict)
    reason: Optional[str] = None


@dataclass
class CodeBundle:
    """Описание исполняемого пакета кода."""

    language: str = "python"
    entrypoint: str = "main.py"
    source: Optional[str] = None
    files: Dict[str, str] = field(default_factory=dict)
    args: List[str] = field(default_factory=list)
    env: Dict[str, str] = field(default_factory=dict)
    stdin: Optional[bytes] = None
    command: Optional[List[str]] = None


class SandboxExecutor(ABC):
    """Базовый интерфейс всех песочниц."""

    def __init__(self, sandbox_type: SandboxType, default_limits: Optional[SandboxLimits] = None):
        self.sandbox_type = sandbox_type
        self.default_limits = default_limits or SandboxLimits()
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    async def execute(
        self,
        job: Optional["Job"],
        code_bundle: CodeBundle,
        limits: Optional[SandboxLimits] = None,
    ) -> SandboxResult:
        """Выполняет код для конкретного job'а."""

    async def run_self_test(self) -> bool:
        """Проверяет базовую работоспособность песочницы."""
        bundle = CodeBundle(
            entrypoint="selftest.py",
            source=(
                "import json\n"
                "with open('input.json') as fh:\n"
                "    data = json.load(fh)\n"
                "print(f\"sum={sum(data['numbers'])}\")\n"
            ),
            files={"input.json": '{"numbers": [1, 2, 3]}'},
        )
        try:
            result = await self.execute(job=None, code_bundle=bundle, limits=self.default_limits)
        except NotImplementedError:
            self.logger.warning("Sandbox %s is not implemented yet", self.sandbox_type.value)
            return False

        if result.success and result.stdout.strip() == "sum=6":
            self.logger.info("%s self-test passed", self.sandbox_type.value)
            return True

        self.logger.warning(
            "%s self-test failed: exit=%s stdout=%s stderr=%s",
            self.sandbox_type.value,
            result.exit_code,
            result.stdout.strip(),
            result.stderr.strip(),
        )
        return False

    async def close(self) -> None:
        """Освобождает ресурсы (может быть переопределено)."""
        return None


class ProcessSandboxExecutor(SandboxExecutor):
    """Запускает код в отдельном процессе и ограничивает ресурсы."""

    def __init__(self, default_limits: Optional[SandboxLimits] = None):
        super().__init__(SandboxType.PROCESS_ISOLATION, default_limits)

    async def execute(
        self,
        job: Optional["Job"],
        code_bundle: CodeBundle,
        limits: Optional[SandboxLimits] = None,
    ) -> SandboxResult:
        limits = limits or self.default_limits
        workdir = tempfile.mkdtemp(prefix="sandbox_proc_")
        start = time.time()
        try:
            entrypoint_path = self._write_bundle(workdir, code_bundle)
            command = self._build_command(code_bundle, entrypoint_path)
            env = {**os.environ, **limits.env, **code_bundle.env}
            stdin_data = code_bundle.stdin

            preexec_fn = self._make_preexec_fn(limits)
            proc = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                stdin=asyncio.subprocess.PIPE if stdin_data is not None else None,
                cwd=workdir,
                env=env,
                preexec_fn=preexec_fn,
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    proc.communicate(stdin_data),
                    timeout=limits.wall_time_seconds,
                )
                timed_out = False
            except asyncio.TimeoutError:
                proc.kill()
                try:
                    await asyncio.wait_for(proc.wait(), timeout=5)
                except asyncio.TimeoutError:
                    proc.kill()
                stdout, stderr = await proc.communicate()
                timed_out = True

            runtime = time.time() - start
            exit_code = proc.returncode if proc.returncode is not None else -1
            success = exit_code == 0 and not timed_out
            usage = self._collect_usage()
            return SandboxResult(
                success=success,
                stdout=stdout.decode("utf-8", errors="replace"),
                stderr=stderr.decode("utf-8", errors="replace"),
                exit_code=exit_code,
                runtime=runtime,
                timed_out=timed_out,
                killed=timed_out or exit_code != 0,
                usage=usage,
                reason="timeout" if timed_out else None,
            )
        except FileNotFoundError as exc:
            return SandboxResult(
                success=False,
                stdout="",
                stderr=str(exc),
                exit_code=-1,
                runtime=time.time() - start,
                killed=True,
                reason="command_not_found",
            )
        finally:
            shutil.rmtree(workdir, ignore_errors=True)

    def _write_bundle(self, workdir: str, bundle: CodeBundle) -> str:
        for relative, content in bundle.files.items():
            path = os.path.join(workdir, relative)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as fh:
                data = content.encode("utf-8") if isinstance(content, str) else content
                fh.write(data)

        entrypoint_path = os.path.join(workdir, bundle.entrypoint)
        os.makedirs(os.path.dirname(entrypoint_path), exist_ok=True)
        if bundle.source is not None:
            with open(entrypoint_path, "w", encoding="utf-8") as fh:
                fh.write(bundle.source)
        elif bundle.entrypoint not in bundle.files:
            raise ValueError("CodeBundle must define source or file for entrypoint")

        return entrypoint_path

    def _build_command(self, bundle: CodeBundle, entrypoint_path: str) -> List[str]:
        if bundle.command:
            return bundle.command
        interpreter = sys.executable if bundle.language == "python" else bundle.language
        return [interpreter, entrypoint_path, *bundle.args]

    def _make_preexec_fn(self, limits: SandboxLimits):
        if resource is None:  # pragma: no cover - Windows fallback
            return None

        def _preexec():
            os.setsid()
            resource.setrlimit(resource.RLIMIT_CPU, (limits.cpu_time_seconds, limits.cpu_time_seconds))
            resource.setrlimit(resource.RLIMIT_AS, (limits.memory_bytes, limits.memory_bytes))
            resource.setrlimit(resource.RLIMIT_DATA, (limits.memory_bytes, limits.memory_bytes))
            resource.setrlimit(resource.RLIMIT_FSIZE, (limits.file_size_bytes, limits.file_size_bytes))
            resource.setrlimit(resource.RLIMIT_NOFILE, (limits.open_files, limits.open_files))

        return _preexec

    def _collect_usage(self) -> Dict[str, Any]:
        if resource is None:  # pragma: no cover
            return {}
        usage = resource.getrusage(resource.RUSAGE_CHILDREN)
        return {
            "user_time": usage.ru_utime,
            "system_time": usage.ru_stime,
            "max_rss": usage.ru_maxrss,
            "minor_faults": usage.ru_minflt,
            "major_faults": usage.ru_majflt,
        }


class WasmSandboxExecutor(SandboxExecutor):
    """Упрощённая WASM песочница (демо): компилирует код в файл и исполняет через процессный рантайм."""

    def __init__(self, default_limits: Optional[SandboxLimits] = None):
        super().__init__(SandboxType.WASM, default_limits)
        self._delegate = ProcessSandboxExecutor(default_limits)

    async def execute(
        self,
        job: Optional["Job"],
        code_bundle: CodeBundle,
        limits: Optional[SandboxLimits] = None,
    ) -> SandboxResult:
        # Реальной WASM-изоляции нет; используем процессный рантайм как безопасный fallback.
        self.logger.warning("WASM sandbox fallback to process isolation (wasm runtime not integrated yet)")
        return await self._delegate.execute(job, code_bundle, limits or self.default_limits)

    async def run_self_test(self) -> bool:
        self.logger.warning("WASM sandbox self-test uses process isolation fallback")
        return await self._delegate.run_self_test()


class ContainerSandboxExecutor(SandboxExecutor):
    """Упрощённая контейнерная песочница: делегирует процессной, но маркирует тип."""

    def __init__(self, default_limits: Optional[SandboxLimits] = None):
        super().__init__(SandboxType.CONTAINER, default_limits)
        self._delegate = ProcessSandboxExecutor(default_limits)

    async def execute(
        self,
        job: Optional["Job"],
        code_bundle: CodeBundle,
        limits: Optional[SandboxLimits] = None,
    ) -> SandboxResult:
        # В реальной реализации здесь должен быть запуск через контейнерный runtime (Docker/OCI).
        # Пока используем процессную изоляцию как fallback, чтобы сценарий работал.
        self.logger.warning("Container sandbox fallback to process isolation (runtime not implemented)")
        return await self._delegate.execute(job, code_bundle, limits or self.default_limits)

    async def run_self_test(self) -> bool:
        self.logger.warning("Container sandbox self-test uses process isolation fallback")
        return await self._delegate.run_self_test()


class SandboxExecutorFactory:
    """Фабрика для создания песочниц нужного типа."""

    @staticmethod
    def create(sandbox_type: SandboxType, limits: Optional[SandboxLimits] = None) -> SandboxExecutor:
        if sandbox_type == SandboxType.PROCESS_ISOLATION:
            return ProcessSandboxExecutor(default_limits=limits)
        if sandbox_type == SandboxType.WASM:
            return WasmSandboxExecutor(default_limits=limits)
        if sandbox_type == SandboxType.CONTAINER:
            return ContainerSandboxExecutor(default_limits=limits)
        raise ValueError(f"Unsupported sandbox type: {sandbox_type}")
