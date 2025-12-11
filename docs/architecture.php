<?php
$title = "Архитектура";
$active = "architecture.php";
$breadcrumbs = [
    ["label" => "Главная", "href" => "index.php"],
    ["label" => "Архитектура"],
];
include __DIR__ . "/layout/header.php";
?>
<section>
    <h2>Компоненты</h2>
    <ul>
        <li><b>Task</b> (core/task.py) — декларативное описание вычислений</li>
        <li><b>Job</b> (core/job.py) — подзадача после шардинга</li>
        <li><b>SchedulerState</b> — состояния/ретраи</li>
        <li><b>PrivacyEngine</b> — none/shard/mask</li>
        <li><b>VerificationEngine</b> — off/basic/strict</li>
        <li><b>Sandbox</b> — process, container, wasm</li>
        <li><b>Transport/Protocol</b> — MessageEnvelope + payload'ы</li>
    </ul>
</section>
<section>
    <h2>Поток задачи</h2>
    <div class="mermaid">
        sequenceDiagram
          autonumber
          participant C as Client/SDK
          participant S as Scheduler
          participant P as Privacy
          participant W as Worker
          participant V as Verification
          C->>S: submit task (Task)
          S->>P: prepare_task
          P-->>S: Task'
          S->>S: split_task_to_jobs
          S->>W: JOB_ASSIGN
          W-->>S: JOB_ACK
          W->>W: sandbox execute
          W-->>S: JOB_RESULT
          S->>V: verify_job_results
          V-->>S: valid_results
          S-->>C: final result
    </div>
</section>
<section>
    <h2>Роли и ответственность</h2>
    <div class="grid two not-prose">
        <div class="p-4 rounded-xl border border-slate-800 bg-slate-900/60">
            <h3>Координатор</h3>
            <ul class="text-sm text-slate-200 space-y-1">
                <li>Валидация и шардинг задачи</li>
                <li>Назначение job'ов воркерам</li>
                <li>Верификация (replica) и агрегация</li>
                <li>Учёт репутации/penalties</li>
            </ul>
        </div>
        <div class="p-4 rounded-xl border border-slate-800 bg-slate-900/60">
            <h3>Воркер</h3>
            <ul class="text-sm text-slate-200 space-y-1">
                <li>Принимает JOB_ASSIGN, подтверждает JOB_ACK</li>
                <li>Выполняет в sandbox (process/container/wasm)</li>
                <li>Возвращает JOB_RESULT</li>
                <li>Не знает полной задачи при privacy shard/mask</li>
            </ul>
        </div>
    </div>
</section>
<section>
    <h2>Слои надёжности</h2>
    <ul>
        <li><b>Статусы Job</b>: pending → assigned → acked → running → completed/failed/expired</li>
        <li><b>Retries</b>: в executor и в assign_single_job_to_worker с timeout</li>
        <li><b>Verification</b>: basic/strict — репликация, сравнение output</li>
        <li><b>Sandbox fallback</b>: container/wasm → process, чтобы задача не падала из-за окружения</li>
    </ul>
</section>
<?php include __DIR__ . "/layout/footer.php"; ?>
