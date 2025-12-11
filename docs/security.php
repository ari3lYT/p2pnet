<?php
$title = "Безопасность";
$active = "security.php";
include __DIR__ . "/layout/header.php";
?>
<section>
    <h2>Слои</h2>
    <ul>
        <li><b>Sandbox</b>: включайте container/wasm, запрещайте сеть/FS вне рабочей директории</li>
        <li><b>Сеть</b>: добавьте TLS/mTLS поверх транспорта, ограничьте входящие узлы whitelist/ACL</li>
        <li><b>Данные</b>: privacy modes (mask/shard), лимиты размера/timeout, сигнатуры задач (позже)</li>
        <li><b>Репутация</b>: penalties при mismatch/timeout</li>
    </ul>
</section>
<section>
    <h2>Рекомендации</h2>
    <ul>
        <li>Настройте firewall: разрешайте только нужные порты координатора/воркеров</li>
        <li>Используйте отдельные сервисные аккаунты для docker/wasmtime</li>
        <li>Логируйте события безопасности, храните логи отдельно</li>
        <li>Ограничивайте payload: <code>max_task_size</code>, <code>timeout_seconds</code>, <code>allowed_file_extensions</code></li>
    </ul>
</section>
<section>
    <h2>Политики и контроль</h2>
    <ul>
        <li><b>Подписи задач</b>: добавьте HMAC/PKI подписи на Task/Job (обвязка поверх протокола).</li>
        <li><b>mTLS</b>: защитите канал обмена Envelope; верифицируйте node_id ↔ сертификат.</li>
        <li><b>Репутация</b>: penalties при mismatch/timeout; отключайте узлы при повторных нарушениях.</li>
        <li><b>Доступ к артефактам</b>: code_ref.location храните в приватных сторах (S3 presigned).</li>
    </ul>
</section>
<section>
    <h2>Лимиты и safe defaults</h2>
    <table class="w-full text-sm border border-slate-800">
        <thead class="bg-slate-900"><tr><th class="px-3 py-2 text-left">Параметр</th><th class="px-3 py-2 text-left">Рекомендация</th></tr></thead>
        <tbody>
        <tr class="border-t border-slate-800"><td class="px-3 py-2">max_task_size</td><td class="px-3 py-2">Ограничить размер входных данных (например, 10MB для публичных сетей)</td></tr>
        <tr class="border-t border-slate-800"><td class="px-3 py-2">timeout_seconds</td><td class="px-3 py-2">Устанавливать с запасом &lt; лимитов sandbox; для воркеров — wall_time_seconds</td></tr>
        <tr class="border-t border-slate-800"><td class="px-3 py-2">allowed_file_extensions</td><td class="px-3 py-2">Явный список (".py", ".json", ".csv"); запрещать исполняемые бинарники</td></tr>
        <tr class="border-t border-slate-800"><td class="px-3 py-2">sandbox network</td><td class="px-3 py-2">Выключить сеть в контейнере/wasm; только loopback для служебного</td></tr>
        </tbody>
    </table>
</section>
<?php include __DIR__ . "/layout/footer.php"; ?>
