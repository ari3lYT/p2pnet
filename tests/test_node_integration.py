import asyncio

import pytest

from core.job import Job, JobStatus
from core.node import ComputeNode
from core.protocol import JobResultPayload, MessageEnvelope, MessageType
from core.task import Task, TaskPriority, TaskType
from core.transport import InMemoryTransport


def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@pytest.mark.asyncio
async def test_node_timeout_and_penalty():
    transport = InMemoryTransport()
    coordinator = ComputeNode(host="127.0.0.1", port=7000, transport=transport)
    worker_id = "missing-worker"

    task = Task.create_map(
        owner_id=coordinator.node_id,
        data=[1],
        function="increment",
        requirements={"cpu_percent": 10.0, "ram_gb": 0.1, "timeout_seconds": 0.1},
        config={"priority": TaskPriority.NORMAL.value},
    )
    job = Job(
        job_id=f"{task.task_id}:0",
        task_id=task.task_id,
        index=0,
        task_type=TaskType.MAP.value,
        input_payload={"function": "increment", "data": [1], "params": {"increment": 1}},
        max_attempts=1,
    )

    with pytest.raises(RuntimeError):
        await coordinator.assign_single_job_to_worker(worker_id, job, task, sandbox_type="process_isolation")
    record = coordinator.scheduler_state.jobs_by_id[job.job_id]
    assert record.status in {JobStatus.FAILED, JobStatus.EXPIRED}
    assert coordinator.reputation["penalties"] >= 1


@pytest.mark.asyncio
async def test_node_assign_without_transport_raises():
    node = ComputeNode(host="127.0.0.1", port=7010, transport=None)
    task = Task.create_map(owner_id=node.node_id, data=[1], function="increment")
    job = Job(job_id=f"{task.task_id}:0", task_id=task.task_id, index=0, task_type=TaskType.MAP.value, input_payload={"data": [1]})
    with pytest.raises(RuntimeError):
        await node.assign_single_job_to_worker("worker", job, task)


@pytest.mark.asyncio
async def test_node_idempotent_job_result():
    transport = InMemoryTransport()
    coordinator = ComputeNode(host="127.0.0.1", port=7001, transport=transport)
    worker = ComputeNode(host="127.0.0.1", port=7002, transport=transport)

    task = Task.create_map(
        owner_id=coordinator.node_id,
        data=[1, 2],
        function="increment",
        config={"priority": TaskPriority.NORMAL.value},
        requirements={"cpu_percent": 10.0, "ram_gb": 0.1, "timeout_seconds": 5},
    )
    job = Job(
        job_id=f"{task.task_id}:0",
        task_id=task.task_id,
        index=0,
        task_type=TaskType.MAP.value,
        input_payload={"function": "increment", "data": [1, 2], "params": {"increment": 1}},
    )

    # normal execution
    result_payload = await coordinator.assign_single_job_to_worker(worker.node_id, job, task)
    assert result_payload.success is True

    # duplicate JOB_RESULT should not break
    from core.protocol import MessageEnvelope, MessageType
    envelope = MessageEnvelope.create(
        MessageType.JOB_RESULT,
        src_node=worker.node_id,
        dst_node=coordinator.node_id,
        payload=result_payload.to_dict(),
    )
    await coordinator._handle_job_result(envelope)
    record = coordinator.scheduler_state.jobs_by_id[job.job_id]
    assert record.status == JobStatus.COMPLETED


@pytest.mark.asyncio
async def test_node_job_result_failure_records_reputation():
    transport = InMemoryTransport()
    node = ComputeNode(host="127.0.0.1", port=7005, transport=transport)
    # stub reputation manager
    class DummyRep:
        def __init__(self):
            self.events = []
        async def add_event(self, event):
            self.events.append(event)
    rep = DummyRep()
    node.reputation_manager = rep
    # подменяем модуль reputation.system, чтобы импорт прошел
    import sys
    import types
    dummy_reputation = types.ModuleType("reputation.system")
    class DummyEvent:
        def __init__(self, *args, **kwargs):
            pass
    class DummyType:
        MALICIOUS_BEHAVIOR = "malicious"
    dummy_reputation.ReputationEvent = DummyEvent
    dummy_reputation.ReputationEventType = DummyType
    sys.modules["reputation.system"] = dummy_reputation
    payload = JobResultPayload(
        task_id="t",
        job_id="j",
        success=False,
        output=None,
        error="fail",
        runtime_ms=0.0,
        worker_id="w",
        attempt=1,
    )
    envelope = MessageEnvelope.create(
        MessageType.JOB_RESULT,
        src_node="w",
        dst_node=node.node_id,
        payload=payload.to_dict(),
    )
    await node._handle_job_result(envelope)
    assert rep.events  # reputation event added
