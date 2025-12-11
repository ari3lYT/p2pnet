import pytest

from core.job import Job
from core.node import ComputeNode
from core.protocol import MessageEnvelope, MessageType
from core.task import Task, TaskPriority, TaskType
from core.transport import InMemoryTransport


@pytest.mark.asyncio
async def test_inmemory_transport_dispatch():
    transport = InMemoryTransport()
    received = []

    async def handler(envelope: MessageEnvelope):
        received.append(envelope)

    transport.register_handler("node-b", handler)
    envelope = MessageEnvelope.create(
        MessageType.WORKER_HEARTBEAT,
        src_node="node-a",
        dst_node="node-b",
        payload={"status": "alive"},
    )
    await transport.send("node-b", envelope)
    assert len(received) == 1
    assert received[0].msg_type == MessageType.WORKER_HEARTBEAT


@pytest.mark.asyncio
async def test_single_job_assignment_between_nodes():
    transport = InMemoryTransport()
    coordinator = ComputeNode(host="127.0.0.1", port=6000, transport=transport)
    worker = ComputeNode(host="127.0.0.1", port=6001, transport=transport)

    task = Task.create_map(
        owner_id=coordinator.node_id,
        data=[1, 2, 3],
        function="increment",
        config={"max_price": 0.1, "priority": TaskPriority.NORMAL.value},
        requirements={"cpu_percent": 10.0, "ram_gb": 0.1, "timeout_seconds": 10},
    )
    job = Job(
        job_id=f"{task.task_id}:0",
        task_id=task.task_id,
        index=0,
        task_type=TaskType.MAP.value,
        input_payload={"function": "increment", "data": [1, 2, 3], "params": {"increment": 1}},
    )

    result_payload = await coordinator.assign_single_job_to_worker(worker.node_id, job, task)
    assert result_payload.success is True
    assert result_payload.output == [2, 3, 4]


@pytest.mark.asyncio
async def test_job_retry_on_failure():
    transport = InMemoryTransport()
    coordinator = ComputeNode(host="127.0.0.1", port=6002, transport=transport)
    worker = ComputeNode(host="127.0.0.1", port=6003, transport=transport)

    task = Task.create_map(
        owner_id=coordinator.node_id,
        data=[1],
        function="increment",
        requirements={"cpu_percent": 10.0, "ram_gb": 0.1, "timeout_seconds": 5},
        config={"max_price": 0.1, "priority": TaskPriority.NORMAL.value},
    )
    job = Job(
        job_id=f"{task.task_id}:0",
        task_id=task.task_id,
        index=0,
        task_type=TaskType.MAP.value,
        input_payload={"function": "increment", "data": [1], "params": {"increment": 1}},
        max_attempts=2,
    )

    worker.simulate_fail_once.add(job.job_id)
    result_payload = await coordinator.assign_single_job_to_worker(worker.node_id, job, task)
    assert result_payload.success is True
    assert result_payload.output == [2]
