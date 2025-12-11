<?php
$title = "Тесты и CI";
$active = "testing.php";
include __DIR__ . "/layout/header.php";
?>
<section>
    <h2>Локальный прогон</h2>
    <pre><code class="language-bash">PYTHONPATH=src pytest --cov --cov-report=term-missing
ruff check src tests
black --check src tests
bash scripts/smoke.sh</code></pre>
    <p>51 тест, покрытие ~90%. Узлы/transport/sandbox/pipeline/verification/privacy/task покрыты.</p>
</section>
<section>
    <h2>CI</h2>
    <ul>
        <li><code>.github/workflows/ci.yml</code>: ruff, black, pytest+cov, smoke</li>
        <li>Python 3.11; зависимые пакеты из <code>requirements.txt</code></li>
        <li>Результаты: cov report, статический анализ</li>
    </ul>
</section>
<section>
    <h2>Что покрывают тесты</h2>
    <ul>
        <li>Executor: map/range_reduce/map_reduce/matrix_ops/ml/generic</li>
        <li>Privacy: none/shard/mask, реставрация порядка</li>
        <li>Verification: basic/strict репликация, penalties</li>
        <li>Transport: InMemory, JOB_ASSIGN/RESULT потоки</li>
        <li>Sandbox: process timeout/success, container/wasm fallback</li>
        <li>Pipeline: deps и циклы</li>
        <li>Scheduler: стейты, retries, idempotent result</li>
    </ul>
</section>
<section>
    <h2>Рекомендации для прод</h2>
    <ul>
        <li>Добавьте нагрузочные тесты (Locust/k6) для десятков воркеров</li>
        <li>Chaos-тесты: drop/delay пакеты, симуляция падения воркеров</li>
        <li>Security-тесты: лимиты размера payload, фуззинг входных данных</li>
        <li>Расширьте coverage для <code>core/task.py</code> оставшихся веток</li>
    </ul>
</section>
<?php include __DIR__ . "/layout/footer.php"; ?>
