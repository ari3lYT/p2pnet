import asyncio

from sandbox.execution import (
    CodeBundle,
    ContainerSandboxExecutor,
    ProcessSandboxExecutor,
    SandboxLimits,
    WasmSandboxExecutor,
)


def run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


def test_process_sandbox_success_and_timeout():
    executor = ProcessSandboxExecutor()
    bundle = CodeBundle(entrypoint="main.py", source="print('hello')")
    result = run(executor.execute(job=None, code_bundle=bundle, limits=SandboxLimits(wall_time_seconds=5)))
    assert result.success
    assert "hello" in result.stdout

    # timeout case
    bundle_sleep = CodeBundle(entrypoint="main.py", source="import time; time.sleep(2)")
    result_to = run(executor.execute(job=None, code_bundle=bundle_sleep, limits=SandboxLimits(wall_time_seconds=0.1)))
    assert result_to.timed_out or result_to.killed


def test_sandbox_selftest_and_fallbacks():
    proc = ProcessSandboxExecutor()
    assert run(proc.run_self_test()) is True

    container = ContainerSandboxExecutor()
    # docker may be unavailable; ensure it returns a boolean without raising
    assert isinstance(run(container.run_self_test()), bool)

    wasm = WasmSandboxExecutor()
    assert isinstance(run(wasm.run_self_test()), bool)
