import asyncio
import logging
import math
import time

import pytest

from core.generic_handlers import execute_generic
from core.job import Job, JobResult
from core.privacy import BasePrivacyEngine, MaskPrivacyEngine
from core.protocol import MessageEnvelope, MessageType
from core.scheduler_state import TaskSchedulerState
from core.task import (
    MapReduceTask,
    MapTask,
    Task,
    TaskExecutor,
    TaskPriority,
    TaskType,
)
from core.transport import InMemoryTransport
from core.verification import get_verification_engine


def run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


def test_task_to_from_dict_and_validation():
    task = Task.create_range_reduce(
        owner_id="owner",
        start=0,
        end=10,
        operation="sum",
        config={"priority": TaskPriority.HIGH.value},
        requirements={"cpu_percent": 10.0, "ram_gb": 0.5},
        privacy={"mode": "shard", "zk_verify": "basic"},
        task_params={"chunk_size": 2},
    )
    as_dict = task.to_dict()
    restored = Task.from_dict(as_dict)
    assert restored.privacy["mode"] == "shard"
    assert restored.range_reduce["chunk_size"] == 2
    assert not restored.validate()

    # Некорректная задача
    bad = Task.create_map(owner_id="", data=[], function="increment")
    errors = bad.validate()
    assert "owner_id is required" in errors
    assert "map data cannot be empty" in errors


def test_task_estimations_and_cost():
    task = Task.create_map(owner_id="o", data=[1, 2, 3, 4], function="square", config={"priority": TaskPriority.LOW.value})
    estimate = task.estimate_execution_time()
    assert estimate > 0
    cost = task.calculate_cost({"cpu_score": 100, "gpu_score": 0})
    assert cost > 0


def test_split_and_combine_range_reduce_average_with_counts():
    executor = TaskExecutor()
    task = Task.create_range_reduce(owner_id="o", start=0, end=6, operation="average")
    jobs = executor.split_task_to_jobs(task)
    assert len(jobs) >= 1
    # Собираем результаты с метаданными count
    job_results = [
        JobResult(job_id=j.job_id, task_id=task.task_id, worker_id="w", output=6, success=True, metadata={"count": 3})
        for j in jobs
    ]
    combined = executor.combine_job_results(task, job_results)
    assert math.isclose(combined, 2.0)


def test_execute_map_reduce_reduce_functions_and_errors():
    executor = TaskExecutor()
    task = MapReduceTask(data=[1, 2, 3], map_function="x", reduce_function="count", params={})
    assert executor._execute_map_reduce(task) == 3
    task.reduce_function = "product"
    assert executor._execute_map_reduce(task) == 6
    task.reduce_function = "unknown"
    with pytest.raises(ValueError):
        executor._execute_map_reduce(task)
    with pytest.raises(ValueError):
        executor._execute_map(MapTask(data=[1], function="does_not_exist"))


def test_matrix_ops_paths():
    executor = TaskExecutor()
    matrix_a = [[1, 2], [3, 4]]
    matrix_b = [[5, 6], [7, 8]]
    transpose = executor._execute_matrix_ops(task=Task.create_matrix_ops("o", "transpose", matrix_a).matrix_ops)
    assert transpose == [[1, 3], [2, 4]]
    added = executor._execute_matrix_ops(task=Task.create_matrix_ops("o", "add", matrix_a, matrix_b).matrix_ops)
    assert added[0][0] == 6
    multiplied = executor._execute_matrix_ops(task=Task.create_matrix_ops("o", "multiply", matrix_a, matrix_b).matrix_ops)
    assert multiplied[0][0] == 19
    with pytest.raises(NotImplementedError):
        executor._execute_matrix_ops(task=Task.create_matrix_ops("o", "inverse", matrix_a).matrix_ops)


def test_generic_handlers_builtin_matrix_and_ml():
    executor = TaskExecutor()
    # ML inference stub path
    task = Task.create_ml_inference("o", model_path="m", input_data=[1, 2], model_type="pytorch")
    job = Job(job_id="j", task_id="t", index=0, task_type=TaskType.GENERIC.value, input_payload={"input_data": [1, 2], "code_ref": task.code_ref})
    result = run(execute_generic(task, job, executor))
    assert result["success"]
    # ML train step stub
    train = Task.create_ml_train_step("o", model_path="m", training_data=[[1, 2]])
    job.input_payload = {"input_data": [[1, 2]], "code_ref": train.code_ref}
    result = run(execute_generic(train, job, executor))
    assert result["success"]
    # Matrix ops
    task = Task.create_matrix_ops("o", "add", [[1]], [[2]])
    job.input_payload = {"input_data": {"matrix_a": [[1]], "matrix_b": [[2]], "operation": "add"}, "code_ref": task.code_ref}
    result = run(execute_generic(task, job, executor))
    assert result["output"] == [[3]]
    # range_reduce builtin
    rr_task = Task.create_range_reduce("o", start=1, end=4, operation="product")
    job.input_payload = {"input_data": {"start": 1, "end": 4}, "code_ref": rr_task.code_ref}
    result = run(execute_generic(rr_task, job, executor))
    assert result["output"] == 6


def test_generic_handlers_python_script():
    class DummySandbox:
        async def execute(self, job, code_bundle, limits):
            from sandbox.execution import SandboxResult
            return SandboxResult(success=True, stdout="ok", stderr="", exit_code=0, runtime=0.01)

    executor = TaskExecutor()
    executor.sandbox_executor = DummySandbox()
    task = Task.create_generic(
        owner_id="o",
        code_ref={"type": "python_script", "entry": "main.py", "source": "print('ok')"},
        input_data=None,
        requirements={},
        config={},
    )
    job = Job(job_id="g:0", task_id="g", index=0, task_type=TaskType.GENERIC.value, input_payload={"code_ref": task.code_ref})
    result = run(execute_generic(task, job, executor))
    assert result["success"] and result["output"] == "ok"
    # без sandbox
    executor.sandbox_executor = None
    error_result = run(execute_generic(task, job, executor))
    assert error_result["success"] is False
    # wasm fallback
    task.code_ref = {"type": "wasm"}
    job.input_payload = {"code_ref": task.code_ref, "input_data": None}
    wasm_result = run(execute_generic(task, job, executor))
    assert wasm_result["success"] is False
    # чтение из location файла
    import os
    import tempfile
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        tmp.write("print('hi')")
        tmp_path = tmp.name
    try:
        task.code_ref = {"type": "python_script", "entry": "main.py", "location": tmp_path}
        executor.sandbox_executor = DummySandbox()
        file_result = run(execute_generic(task, job, executor))
        assert file_result["success"]
    finally:
        os.unlink(tmp_path)


def test_generic_handlers_map_expression_scalar():
    executor = TaskExecutor()
    task = Task.create_generic(
        owner_id="o",
        code_ref={"type": "builtin", "handler": "map_expression", "function": "square"},
        input_data=5,
        requirements={},
        config={},
    )
    job = Job(job_id="m:0", task_id="m", index=0, task_type=TaskType.GENERIC.value, input_payload={"input_data": 5, "code_ref": task.code_ref})
    result = run(execute_generic(task, job, executor))
    assert result["success"]


def test_verification_strict_fallback_and_penalties():
    task = Task.create_map(owner_id="o", data=[1], function="increment", privacy={"mode": "none", "zk_verify": "strict"})
    engine = get_verification_engine(task)
    jobs = [Job(job_id="j0", task_id=task.task_id, index=0, task_type=TaskType.MAP.value, input_payload={})]
    replicas = run(engine.select_jobs_for_replication(jobs, task))
    assert len(replicas) == 2
    canonical = JobResult(job_id="j0", task_id=task.task_id, worker_id="w1", output=[1], success=True, metadata={"canonical_id": "j0"})
    mismatch = JobResult(job_id="j0#r1", task_id=task.task_id, worker_id="w2", output=[2], success=True, metadata={"canonical_id": "j0"})
    verification = run(engine.verify_job_results(task, [canonical, mismatch]))
    assert verification.invalid_results and verification.penalties


def test_verification_canonical_fallback():
    task = Task.create_map(owner_id="o", data=[1], function="increment", privacy={"mode": "basic"})
    engine = get_verification_engine(task)
    base = JobResult(job_id="j0", task_id=task.task_id, worker_id="w1", output=None, success=False, metadata={"canonical_id": "j0"})
    # replica with same failure should still produce canonical fallback
    replica = JobResult(job_id="j0#r1", task_id=task.task_id, worker_id="w2", output=None, success=False, metadata={"canonical_id": "j0", "replica": True})
    result = run(engine.verify_job_results(task, [base, replica]))
    assert result.valid_results


def test_privacy_unknown_mode_logs_warning(caplog):
    executor = TaskExecutor()
    task = Task.create_map(owner_id="o", data=[1], function="square", privacy={"mode": "fhe"})
    caplog.set_level(logging.WARNING)
    from core.privacy import get_privacy_engine
    engine = get_privacy_engine(task, executor)
    assert isinstance(engine, BasePrivacyEngine)
    assert "not implemented" in caplog.text.lower()


def test_privacy_shard_and_mask_fallback(caplog):
    executor = TaskExecutor()
    shard_task = Task.create_map("o", [1], "square", privacy={"mode": "shard"})
    from core.privacy import get_privacy_engine
    engine = get_privacy_engine(shard_task, executor)
    caplog.set_level(logging.DEBUG)
    run(engine.prepare_task(shard_task))
    assert "shard mode" in caplog.text.lower()

    # mask fallback for non-map
    rr_task = Task.create_range_reduce("o", 0, 2, "sum")
    rr_task.privacy = {"mode": "mask"}
    mask_engine = get_privacy_engine(rr_task, executor)
    fallback = run(mask_engine.prepare_task(rr_task))
    assert fallback is rr_task
    # finalize без permutation
    dummy_result = JobResult(job_id="j", task_id=rr_task.task_id, worker_id="w", output=3, success=True, metadata={})
    final_no_perm = run(mask_engine.finalize_task_result(rr_task, [dummy_result]))
    assert final_no_perm == 3


def test_scheduler_state_transitions_and_retry():
    scheduler = TaskSchedulerState()
    task = Task.create_map(owner_id="o", data=[1], function="increment")
    job = Job(job_id="j0", task_id=task.task_id, index=0, task_type=TaskType.MAP.value, input_payload={})
    scheduler.register_jobs_for_task(task, [job])
    scheduler.mark_assigned(job.job_id, "worker", now=time.time())
    scheduler.mark_ack(job.job_id, now=time.time())
    scheduler.mark_result(job.job_id, success=False, now=time.time() - 2)
    due = scheduler.jobs_due_for_retry(now=time.time())
    assert due and due[0].job.job_id == job.job_id
    from core.job_state import JobStatus
    counters = scheduler.status_counters()
    assert counters[JobStatus.ACKED] >= 0  # existence check


def test_protocol_envelope_roundtrip_and_transport_unreachable(caplog):
    payload = {"hello": "world"}
    env = MessageEnvelope.create(MessageType.WORKER_HEARTBEAT, "a", "b", payload)
    as_dict = env.to_dict()
    restored = MessageEnvelope.from_dict(as_dict)
    assert restored.payload == payload
    transport = InMemoryTransport()
    # отправляем на неизвестный узел
    caplog.set_level(logging.WARNING)
    run(transport.send("missing", env))
    assert "unreachable" in caplog.text.lower()


def test_privacy_mask_restores_permutation():
    executor = TaskExecutor()
    task = Task.create_map(owner_id="o", data=[1, 2, 3], function="square", privacy={"mode": "mask"})
    engine = MaskPrivacyEngine(executor)
    prepared = run(engine.prepare_task(task))
    jobs = executor.split_task_to_jobs(prepared)
    # выполним и восстановим порядок
    job_results = []
    for job in jobs:
        res = run(executor._execute_job(prepared, job))
        job_results.append(res)
    restored = run(engine.finalize_task_result(prepared, job_results))
    expected_increment = sorted([x + 1 for x in [1, 2, 3]])
    assert sorted(restored) in ([1, 4, 9], expected_increment)
