<?php
$title = "Быстрый старт";
$active = "quickstart.php";
$breadcrumbs = [
    ["label" => "Главная", "href" => "index.php"],
    ["label" => "Быстрый старт"],
];
include __DIR__ . "/layout/header.php";
?>
<section>
    <h2>Путь для новичка (до первой задачи)</h2>
    <ol class="text-slate-200 space-y-1">
        <li>Подготовьте окружение (Python 3.11, venv)</li>
        <li>Поставьте зависимости</li>
        <li>Гоните тесты + смоук</li>
        <li>Запустите демо-узел</li>
        <li>Отправьте свою первую задачу (map)</li>
    </ol>
    <pre><code class="language-bash">python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# тесты + покрытие
PYTHONPATH=src pytest --cov --cov-report=term-missing

# смоук
bash scripts/smoke.sh

# демо-узел
PYTHONPATH=src python examples/basic_usage.py</code></pre>
</section>

<section>
    <h2>Отправка первой задачи</h2>
    <pre><code class="language-python">from core.task import Task, TaskPriority
from core.task import TaskExecutor

task = Task.create_map(
    owner_id="me",
    data=[1,2,3],
    function="increment",
    privacy={"mode": "shard", "zk_verify": "basic"},
    config={"priority": TaskPriority.NORMAL.value},
)

result = TaskExecutor()
import asyncio
print(asyncio.run(result.execute(task)))</code></pre>
</section>

<section>
    <h2>Готовимся к прод</h2>
    <ul>
        <li>Включите container/wasm sandbox (docker/wasmtime), задайте лимиты.</li>
        <li>Для публичных задач: privacy=shard/mask, zk_verify=basic.</li>
        <li>Настройте метрики (/metrics, /metrics_prom) и сбор логов.</li>
    </ul>
</section>
<?php include __DIR__ . "/layout/footer.php"; ?>
