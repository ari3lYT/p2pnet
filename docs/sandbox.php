<?php
$title = "Sandbox (process/container/wasm)";
$active = "sandbox.php";
include __DIR__ . "/layout/header.php";
?>
<section>
    <h2>Варианты песочниц</h2>
    <ul>
        <li><b>process_isolation</b> (дефолт): отдельный процесс, resource-лимиты CPU/память, wall-time</li>
        <li><b>container</b>: docker run без сети, лимиты CPU/mem; fallback в process при отсутствии docker</li>
        <li><b>wasm</b>: wasmtime CLI, fallback в process при отсутствии рантайма/модуля</li>
    </ul>
</section>
<section>
    <h2>Самотест</h2>
    <pre><code class="language-bash">PYTHONPATH=src python - <<'PY'
import asyncio
from sandbox.execution import ProcessSandboxExecutor
exec = ProcessSandboxExecutor()
print(asyncio.get_event_loop().run_until_complete(exec.run_self_test()))
PY</code></pre>
</section>
<section>
    <h2>Настройки</h2>
    <ul>
        <li>Переменные: <code>WF_CONTAINER_IMAGE</code> (docker образ), <code>WF_WASM_RUNTIME</code> (wasmtime)</li>
        <li>Лимиты: <code>SandboxLimits</code> — cpu_time_seconds, memory_bytes, wall_time_seconds, file_size_bytes</li>
        <li>CLI/конфиг: задайте таймауты задач в <code>ResourceRequirements</code></li>
    </ul>
</section>
<?php include __DIR__ . "/layout/footer.php"; ?>
