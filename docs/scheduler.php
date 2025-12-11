<?php
$title = "Планировщик / Jobs";
$active = "scheduler.php";
include __DIR__ . "/layout/header.php";
?>
<section>
    <h2>Статусы Job</h2>
    <ul>
        <li>PENDING → ASSIGNED → ACKED → RUNNING → COMPLETED/FAILED/EXPIRED</li>
        <li>Поле <code>attempts</code>, <code>next_retry_ts</code>, <code>assigned_to</code></li>
    </ul>
    <pre><code class="language-python"># регистрация
scheduler.register_jobs_for_task(task, jobs)
# назначение
scheduler.mark_assigned(job_id, worker, now)
scheduler.mark_ack(job_id, now)
scheduler.mark_result(job_id, success, now)
# ретраи
due = scheduler.jobs_due_for_retry(now)</code></pre>
</section>
<section>
    <h2>Ретраи и идемпотентность</h2>
    <ul>
        <li>Executor: повторяет job, пока <code>max_attempts</code></li>
        <li>Node.assign_single_job_to_worker: retry loop + timeout</li>
        <li>Идемпотентность JOB_RESULT: будущие дубликаты просто обновят статус</li>
    </ul>
</section>
<section>
    <h2>Диаграмма переходов</h2>
    <div class="mermaid">
        stateDiagram-v2
          [*] --> PENDING
          PENDING --> ASSIGNED
          ASSIGNED --> ACKED: JOB_ACK accepted
          ASSIGNED --> FAILED: ACK rejected/busy
          ACKED --> RUNNING
          RUNNING --> COMPLETED: JOB_RESULT success
          RUNNING --> FAILED: JOB_RESULT fail
          ASSIGNED --> EXPIRED: timeout
          RUNNING --> EXPIRED: timeout
    </div>
</section>
<section>
    <h2>Практические рекомендации</h2>
    <ul>
        <li><b>max_attempts</b>: подбирайте по SLA и объёму пула; для критичных задач ≥2.</li>
        <li><b>timeout_seconds</b>: лучше меньше, чем wall-time sandbox; избегайте подвисаний.</li>
        <li><b>penalties</b>: при EXPIRED/FAILED учитывайте репутацию узлов; держите черный список.</li>
        <li><b>репликация</b>: для strict/basic — планируйте отдельные ресурсы под дубли.</li>
    </ul>
</section>
<?php include __DIR__ . "/layout/footer.php"; ?>
