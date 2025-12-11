<?php
$title = "Мониторинг и метрики";
$active = "monitoring.php";
include __DIR__ . "/layout/header.php";
?>
<section>
    <h2>Метрики</h2>
    <ul>
        <li>Endpoints: <code>/metrics</code> (JSON), <code>/metrics_prom</code> (Prometheus)</li>
        <li>Содержимое: CPU/RAM usage, job statuses, средняя латентность задач</li>
    </ul>
    <p>Включите scrape в Prometheus, добавьте дашборды (CPU, RAM, active_tasks, penalties, latencies).</p>
</section>
<section>
    <h2>Логи и события</h2>
    <ul>
        <li><code>ComputeNode.event_log</code> — ack/result события</li>
        <li><code>TaskSchedulerState.to_event_list()</code> — статусы job</li>
        <li>Логи Python logging; добавьте structured logging (structlog) при необходимости</li>
    </ul>
</section>
<section>
    <h2>Дашборды</h2>
    <ul>
        <li><b>Система</b>: CPU/RAM/IO, количество воркеров, статус узлов</li>
        <li><b>Задачи</b>: активные/успешные/failed, средняя латентность, ретраи</li>
        <li><b>Sandbox</b>: доля fallback (container/wasm → process), таймауты</li>
        <li><b>Безопасность</b>: количество penalties, отклонённых задач</li>
    </ul>
</section>
<section>
    <h2>Траблшутинг по метрикам</h2>
    <ul>
        <li>Высокий timeout rate → уменьшить timeout_seconds, оптимизировать код, добавить ресурсов.</li>
        <li>Частые penalties → увеличить репликацию/verification strict, заблокировать недобросовестных воркеров.</li>
        <li>Высокий fallback sandbox → проверить docker/wasmtime, окружение воркеров.</li>
    </ul>
</section>
<?php include __DIR__ . "/layout/footer.php"; ?>
