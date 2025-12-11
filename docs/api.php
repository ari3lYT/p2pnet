<?php
$title = "API / Swagger";
$active = "api.php";
include __DIR__ . "/layout/header.php";
?>
<section>
    <h2>Основные интерфейсы</h2>
    <ul>
        <li><code>Task</code>: фабрики <code>create_map</code>/<code>create_range_reduce</code>/<code>create_generic</code>/<code>create_pipeline</code></li>
        <li><code>TaskExecutor.execute(task)</code>: полный pipeline с privacy/verification</li>
        <li><code>ComputeNode.assign_single_job_to_worker</code>: отправка Job через транспорт</li>
    </ul>
</section>
<section>
    <h2>Swagger / REST (рекомендация)</h2>
    <p>В текущем коде REST/Swagger не развёрнуты, но можно добавить FastAPI/Flask gateway, экспортировать схемы Task/Job. Минимальный OpenAPI-концепт:</p>
    <pre><code class="language-yaml">openapi: 3.0.3
info:
  title: WF Compute API
  version: 0.1.0
paths:
  /tasks:
    post:
      summary: Submit task
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Task'
      responses:
        '200':
          description: Task accepted
  /tasks/{task_id}:
    get:
      summary: Get task status</code></pre>
    <p>Готовый Swagger UI можно положить как статический HTML/JS (например, swagger-ui-dist) и читать openapi.json, если добавите REST-прослойку.</p>
</section>
<section>
    <h2>Структуры данных</h2>
    <table class="w-full text-sm border border-slate-800">
        <thead class="bg-slate-900"><tr><th class="px-3 py-2 text-left">Класс</th><th class="px-3 py-2 text-left">Ключевые поля</th><th class="px-3 py-2 text-left">Назначение</th></tr></thead>
        <tbody>
        <tr class="border-t border-slate-800"><td class="px-3 py-2">Task</td><td class="px-3 py-2">task_type, requirements, config, privacy, code_ref/input_data/parallel</td><td class="px-3 py-2">Декларация задачи</td></tr>
        <tr class="border-t border-slate-800"><td class="px-3 py-2">Job</td><td class="px-3 py-2">job_id, task_id, input_payload, metadata</td><td class="px-3 py-2">Подзадача после шардинга</td></tr>
        <tr class="border-t border-slate-800"><td class="px-3 py-2">JobResult</td><td class="px-3 py-2">output, success, error, metadata</td><td class="px-3 py-2">Результат исполнения</td></tr>
        </tbody>
    </table>
</section>
<section>
    <h2>Примеры вызовов</h2>
    <pre><code class="language-python"># submit generic task
task = Task.create_generic(
    owner_id="o",
    code_ref={"type": "builtin", "handler": "map_expression", "function": "square"},
    input_data=[1,2,3],
    privacy={"mode": "mask", "zk_verify": "basic"}
)
result = await TaskExecutor().execute(task)
print(result["result"])
</code></pre>
</section>
<?php include __DIR__ . "/layout/footer.php"; ?>
