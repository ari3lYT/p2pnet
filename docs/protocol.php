<?php
$title = "Протокол и транспорт";
$active = "protocol.php";
include __DIR__ . "/layout/header.php";
?>
<section>
    <h2>MessageEnvelope</h2>
    <p><code>core/protocol.php</code> — оболочка сообщения: <code>msg_type</code>, <code>msg_id</code>, <code>src_node</code>, <code>dst_node</code>, <code>timestamp</code>, <code>payload</code>.</p>
</section>
<section>
    <h2>Payload'ы</h2>
    <ul>
        <li><b>JOB_ASSIGN</b>: task_id, job_id, attempt, code_ref, sandbox_type, input_payload, requirements, deadline_ts, privacy</li>
        <li><b>JOB_ACK</b>: task_id, job_id, status</li>
        <li><b>JOB_RESULT</b>: task_id, job_id, success, output, error, runtime_ms, worker_id, attempt</li>
        <li><b>JOB_FAIL</b>: task_id, job_id, worker_id, reason, attempt</li>
    </ul>
    <div class="mermaid">
        sequenceDiagram
          autonumber
          Coordinator->>Worker: JOB_ASSIGN
          Worker-->>Coordinator: JOB_ACK
          Worker->>Worker: run in sandbox
          Worker-->>Coordinator: JOB_RESULT / JOB_FAIL
          Coordinator-->>Coordinator: verify + combine
    </div>
</section>
<section>
    <h2>Transport</h2>
    <ul>
        <li><code>core/transport.py</code> — интерфейс + InMemoryTransport (тесты/локально)</li>
        <li>Для прод — оборачивайте Envelope в свой P2P/RPC слой с mTLS</li>
    </ul>
</section>
<section>
    <h2>Таблица полей и инвариантов</h2>
    <table class="w-full text-sm border border-slate-800">
        <thead class="bg-slate-900">
        <tr><th class="px-3 py-2 text-left">Тип</th><th class="px-3 py-2 text-left">Обязательно</th><th class="px-3 py-2 text-left">Назначение</th><th class="px-3 py-2 text-left">Инварианты</th></tr>
        </thead>
        <tbody>
        <tr class="border-t border-slate-800"><td class="px-3 py-2">JOB_ASSIGN</td><td class="px-3 py-2">Да</td><td class="px-3 py-2">Назначение job</td><td class="px-3 py-2">deadline_ts > now; attempt >=1</td></tr>
        <tr class="border-t border-slate-800"><td class="px-3 py-2">JOB_ACK</td><td class="px-3 py-2">Да</td><td class="px-3 py-2">Принятие job</td><td class="px-3 py-2">status in {accepted,busy,rejected}</td></tr>
        <tr class="border-t border-slate-800"><td class="px-3 py-2">JOB_RESULT</td><td class="px-3 py-2">Да</td><td class="px-3 py-2">Результат выполнения</td><td class="px-3 py-2">success XOR error; runtime_ms >=0</td></tr>
        <tr class="border-t border-slate-800"><td class="px-3 py-2">JOB_FAIL</td><td class="px-3 py-2">Да</td><td class="px-3 py-2">Не смог стартовать</td><td class="px-3 py-2">reason in {no_resources, invalid_code,...}</td></tr>
        </tbody>
    </table>
</section>
<section>
    <h2>Практические советы</h2>
    <ul>
        <li>Серилизация: используйте JSON без двоичных данных, код/артефакты храните по ссылке (code_ref.location).</li>
        <li>Безопасность: добавьте подписи сообщений и TLS поверх транспорта; верифицируйте <code>src_node</code>.</li>
        <li>Идемпотентность: JOB_RESULT с тем же <code>job_id</code> должен быть безопасен (дубликаты игнорируются).</li>
        <li>Ретраи: координация по <code>attempt</code>; при EXPIRED/FAILED — переназначение на другой воркер.</li>
    </ul>
</section>
<?php include __DIR__ . "/layout/footer.php"; ?>
