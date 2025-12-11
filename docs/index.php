<?php
$title = "WF P2P Compute — Обзор";
$active = "index.php";
$breadcrumbs = [
    ["label" => "Главная", "href" => "index.php"],
    ["label" => "Обзор"],
];
include __DIR__ . "/layout/header.php";
?>

<section class="not-prose">
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div class="p-5 rounded-2xl border border-slate-800 bg-slate-900/70 shadow-lg">
            <p class="text-xs uppercase tracking-widest text-slate-400 mb-2">Начните отсюда</p>
            <ul class="text-sm leading-6 text-slate-200 space-y-1">
                <li>Что это: P2P вычислительная сеть (без центрального кластера)</li>
                <li>Роли: Координатор, Воркеры, Клиент</li>
                <li>Шардинг задач, приватность, верификация, sandbox</li>
                <li><a href="glossary.php" class="text-brand hover:underline">Глоссарий</a> — ключевые термины</li>
                <li><a href="quickstart.php" class="text-brand hover:underline">Быстрый старт</a> — за 10 минут</li>
            </ul>
        </div>
        <div class="p-5 rounded-2xl border border-slate-800 bg-slate-900/70 shadow-lg">
            <p class="text-xs uppercase tracking-widest text-slate-400 mb-2">Ключевые файлы</p>
            <ul class="text-sm leading-6 text-slate-200 space-y-1">
                <li><code>src/core/task.py</code> — Task API/Executor</li>
                <li><code>src/core/node.py</code> — узел, assign/ack/result</li>
                <li><code>src/core/privacy.py</code>, <code>verification.py</code></li>
                <li><code>src/sandbox/execution.py</code> — песочницы</li>
                <li><code>tests/</code> — 51 тест, покрытие ~90%</li>
            </ul>
        </div>
        <div class="p-5 rounded-2xl border border-slate-800 bg-slate-900/70 shadow-lg">
            <p class="text-xs uppercase tracking-widest text-slate-400 mb-2">Для кого</p>
            <ul class="text-sm leading-6 text-slate-200 space-y-1">
                <li><b>Новички</b>: Overview → Quickstart → Glossary</li>
                <li><b>Разработчики</b>: Tasks, Protocol, Pipeline</li>
                <li><b>DevOps</b>: Deployment, Security, Sandbox, Monitoring</li>
                <li><b>Операторы</b>: FAQ, Troubleshooting, Metrics</li>
            </ul>
        </div>
    </div>
</section>

<section>
    <h2>Диаграмма компонентов (мермейд)</h2>
    <div class="mermaid">
        graph LR
          Client[Клиент / SDK] -->|submit task| Coord[Координатор]
          subgraph Coord
            TExec[TaskExecutor] --> Jobs[split_task_to_jobs]
            Privacy[PrivacyEngine] --> Jobs
            Verify[VerificationEngine] --> Results[JobResult]
            Sched[SchedulerState] --> Jobs
          end
          Jobs --> Worker[Воркер / ComputeNode]
          Worker --> Sandbox[Sandbox: process/container/wasm]
          Worker --> Results
          Results --> Verify
          Verify --> Combine[combine_job_results]
          Combine --> Client
    </div>
</section>

<section>
    <h2>Профиль производственного использования</h2>
    <ul>
        <li><b>Приватность</b>: shard/mask по задаче, базовая репликация (basic/strict)</li>
        <li><b>Надёжность</b>: retries на уровне executor и coordinator, статусная машина job</li>
        <li><b>Изоляция</b>: process sandbox по умолчанию, попытка container/wasm, fallback безопасен</li>
        <li><b>Наблюдаемость</b>: метрики Prometheus, event_log, cov 90%+ тестов</li>
    </ul>
</section>

<section>
    <h2>Что дальше (по нарастающей сложности)</h2>
    <ol class="space-y-2">
        <li><a class="text-brand hover:underline" href="quickstart.php">Быстрый старт</a> — запуск и первые задачи</li>
        <li><a class="text-brand hover:underline" href="glossary.php">Глоссарий</a> — термины (Task/Job/Sandbox/Privacy/Verification)</li>
        <li><a class="text-brand hover:underline" href="architecture.php">Архитектура</a> — роли, потоки, SLA</li>
        <li><a class="text-brand hover:underline" href="tasks.php">Задачи & Privacy</a> — типы задач, настройки</li>
        <li><a class="text-brand hover:underline" href="pipeline.php">Pipeline/DAG</a> — сложные графы</li>
        <li><a class="text-brand hover:underline" href="sandbox.php">Sandbox</a> — изоляция и лимиты</li>
        <li><a class="text-brand hover:underline" href="protocol.php">Протокол</a> + <a class="text-brand hover:underline" href="scheduler.php">Планировщик</a></li>
        <li><a class="text-brand hover:underline" href="deployment.php">Развертывание</a>, <a class="text-brand hover:underline" href="security.php">Безопасность</a>, <a class="text-brand hover:underline" href="monitoring.php">Мониторинг</a></li>
        <li><a class="text-brand hover:underline" href="testing.php">Тесты/CI</a>, <a class="text-brand hover:underline" href="api.php">API</a>, <a class="text-brand hover:underline" href="faq.php">FAQ</a></li>
    </ol>
</section>

<?php include __DIR__ . "/layout/footer.php"; ?>
