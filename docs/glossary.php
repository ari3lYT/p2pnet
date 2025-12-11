<?php
$title = "Глоссарий";
$active = "glossary.php";
$breadcrumbs = [
    ["label" => "Главная", "href" => "index.php"],
    ["label" => "Глоссарий"],
];
include __DIR__ . "/layout/header.php";
?>
<section class="not-prose">
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div class="p-5 rounded-2xl border border-slate-800 bg-slate-900/70 shadow">
            <h2 class="text-xl text-brand mb-3">Базовые термины</h2>
            <ul class="text-sm text-slate-200 space-y-2">
                <li><b>Task</b> — декларация вычисления (тип задачи, ресурсы, privacy, config)</li>
                <li><b>Job</b> — подзадача, полученная после шардинга Task</li>
                <li><b>JobResult</b> — результат исполнения job</li>
                <li><b>TaskType</b> — типы задач: range_reduce, map, map_reduce, matrix_ops, ml_inference, ml_train_step, generic, pipeline</li>
                <li><b>Privacy</b> — режим приватности (none/shard/mask/mpc/fhe/auto)</li>
                <li><b>zk_verify</b> — проверка результата (off/basic/strict)</li>
            </ul>
        </div>
        <div class="p-5 rounded-2xl border border-slate-800 bg-slate-900/70 shadow">
            <h2 class="text-xl text-brand mb-3">Сеть и протокол</h2>
            <ul class="text-sm text-slate-200 space-y-2">
                <li><b>MessageEnvelope</b> — оболочка для JOB_ASSIGN/ACK/RESULT/FAIL</li>
                <li><b>Transport</b> — абстракция доставки сообщений; InMemory — для тестов</li>
                <li><b>Coordinator</b> — узел, который шардингует задачи, назначает job и агрегирует результаты</li>
                <li><b>Worker</b> — узел-исполнитель, получает JOB_ASSIGN, возвращает JOB_RESULT</li>
                <li><b>SchedulerState</b> — хранит статусы job, ретраи, события</li>
            </ul>
        </div>
    </div>
</section>
<section>
    <h2>Изоляция и безопасность</h2>
    <ul>
        <li><b>Sandbox</b> — среда исполнения: process (по умолчанию), container (docker), wasm (wasmtime)</li>
        <li><b>ResourceRequirements</b> — cpu_percent, ram_gb, gpu_percent, timeout_seconds</li>
        <li><b>Config</b> — max_price, priority, retry_count, validation_required</li>
        <li><b>Verification</b> — репликация job для сравнения результатов</li>
    </ul>
</section>
<section>
    <h2>Продвинутые понятия</h2>
    <ul>
        <li><b>combine_job_results</b> — агрегатор результатов (map, reduce, generic map_reduce)</li>
        <li><b>Pipeline</b> — DAG из узлов (id, task, depends_on)</li>
        <li><b>Sandbox fallback</b> — при отсутствии docker/wasmtime откат к process</li>
        <li><b>Penalties</b> — штрафы за некорректные результаты (репутация)</li>
        <li><b>Replica jobs</b> — задачи-реплики для проверки верификации</li>
    </ul>
</section>
<?php include __DIR__ . "/layout/footer.php"; ?>
