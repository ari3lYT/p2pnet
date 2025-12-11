<?php
$title = "Задачи, Privacy и Верификация";
$active = "tasks.php";
include __DIR__ . "/layout/header.php";
?>
<section>
    <h2>Типы задач (TaskType)</h2>
    <div class="grid two not-prose">
        <div class="p-4 rounded-xl border border-slate-800 bg-slate-900/50">
            <h3 class="text-lg text-brand">Базовые</h3>
            <ul class="text-sm text-slate-200 space-y-1">
                <li>RANGE_REDUCE — диапазоны: sum/product/min/max/average</li>
                <li>MAP — трансформация коллекций</li>
                <li>MAP_REDUCE — map + reduce (sum/product/count/...)</li>
                <li>MATRIX_OPS — add/multiply/transpose</li>
            </ul>
        </div>
        <div class="p-4 rounded-xl border border-slate-800 bg-slate-900/50">
            <h3 class="text-lg text-brand">Продвинутые</h3>
            <ul class="text-sm text-slate-200 space-y-1">
                <li>ML_INFERENCE — инференс по модели</li>
                <li>ML_TRAIN_STEP — шаг обучения (data-parallel)</li>
                <li>GENERIC — произвольный code_ref (python/wasm/container)</li>
                <li>PIPELINE — DAG из узлов</li>
            </ul>
        </div>
    </div>
    <pre><code class="language-python">task = Task.create_map(
    owner_id="user123",
    data=[1,2,3],
    function="increment",
    privacy={"mode": "shard", "zk_verify": "basic"},
    config={"priority": TaskPriority.NORMAL.value},
)</code></pre>
</section>

<section>
    <h2>Privacy</h2>
    <div class="grid two not-prose">
        <div class="p-4 rounded-xl border border-slate-800 bg-slate-900/50">
            <h3 class="text-brand">Режимы</h3>
            <ul class="text-sm text-slate-200 space-y-1">
                <li><b>none</b> — без приватности</li>
                <li><b>shard</b> — каждый воркер видит только свой chunk</li>
                <li><b>mask</b> — перестановка/маскирование (map числовых)</li>
                <li><b>auto/mpc/fhe</b> — задел, откат к mask/shard при недоступности</li>
            </ul>
        </div>
        <div class="p-4 rounded-xl border border-slate-800 bg-slate-900/50">
            <h3 class="text-brand">Верификация</h3>
            <ul class="text-sm text-slate-200 space-y-1">
                <li><b>off</b> — доверие + репутация</li>
                <li><b>basic</b> — репликация подзадач, сравнение output</li>
                <li><b>strict</b> — усиленная репликация (zk позже), фокус на корректности</li>
            </ul>
        </div>
    </div>
</section>

<section>
    <h2>Таблица настроек</h2>
    <table class="w-full text-sm border border-slate-800">
        <thead class="bg-slate-900">
            <tr>
                <th class="px-3 py-2 text-left">Поле</th>
                <th class="px-3 py-2 text-left">Назначение</th>
                <th class="px-3 py-2 text-left">Значения</th>
            </tr>
        </thead>
        <tbody>
            <tr class="border-t border-slate-800">
                <td class="px-3 py-2"><code>privacy.mode</code></td>
                <td class="px-3 py-2">Базовый режим приватности</td>
                <td class="px-3 py-2">none | shard | mask | mpc | fhe | auto</td>
            </tr>
            <tr class="border-t border-slate-800">
                <td class="px-3 py-2"><code>privacy.zk_verify</code></td>
                <td class="px-3 py-2">Проверка корректности результата</td>
                <td class="px-3 py-2">off | basic | strict</td>
            </tr>
            <tr class="border-t border-slate-800">
                <td class="px-3 py-2"><code>requirements.timeout_seconds</code></td>
                <td class="px-3 py-2">Жёсткий таймаут исполнения job</td>
                <td class="px-3 py-2">Целое число секунд</td>
            </tr>
            <tr class="border-t border-slate-800">
                <td class="px-3 py-2"><code>config.retry_count</code></td>
                <td class="px-3 py-2">Количество ретраев</td>
                <td class="px-3 py-2">Целое число</td>
            </tr>
        </tbody>
    </table>
</section>

<section>
    <h2>Практические паттерны</h2>
    <ul>
        <li>Для публичных задач: <b>shard</b> + <b>basic</b> verification, chunk_size <= 1000</li>
        <li>Для конфиденциальных map: <b>mask</b> + <b>strict</b>, мелкие чанки</li>
        <li>Для тяжёлых ML: <b>shard</b> по батчам, <b>basic</b> на контрольных подзадачах</li>
        <li>Для диапазонных сумм: <b>shard</b>, <b>off/basic</b> по SLA</li>
    </ul>
</section>

<?php include __DIR__ . "/layout/footer.php"; ?>
