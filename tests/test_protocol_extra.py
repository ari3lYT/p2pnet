from core.protocol import JobFailPayload


def test_job_fail_payload_roundtrip():
    payload = JobFailPayload(
        task_id="t",
        job_id="j",
        worker_id="w",
        reason="no_resources",
        attempt=1,
    )
    as_dict = payload.to_dict()
    restored = JobFailPayload.from_dict(as_dict)
    assert restored.reason == "no_resources"
