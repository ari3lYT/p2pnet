<?php
$title = "FAQ / Траблшутинг";
$active = "faq.php";
include __DIR__ . "/layout/header.php";
?>
<section>
    <h2>Частые вопросы</h2>
    <ul>
        <li><b>Нет docker/wasmtime</b> — sandbox fallback в process. Установите docker/wasmtime для жёсткой изоляции.</li>
        <li><b>Job зависает</b> — проверьте <code>timeout_seconds</code>, лимиты sandbox, логи воркера.</li>
        <li><b>Нужно больше приватности</b> — используйте <code>privacy.mode=mask</code> (map-числовые) или shard + basic verification. MPC/FHE не реализованы.</li>
        <li><b>Как поднять покрытие</b> — тесты в <code>tests/</code>, сейчас ~90%. Добавьте сценарии под <code>task.py</code> оставшиеся ветки.</li>
        <li><b>Док-сайт не открывается</b> — убедитесь, что DocumentRoot указывает на <code>docs/</code>, PHP включён, index.php разрешён.</li>
    </ul>
</section>
<section>
    <h2>Траблшутинг</h2>
    <div class="grid two not-prose">
        <div class="p-4 rounded-xl border border-slate-800 bg-slate-900/60">
            <h3 class="text-brand">Сервер/Transport</h3>
            <ul class="text-sm text-slate-200 space-y-1">
                <li>Проблемы ACK: проверьте доступность воркера, latency, таймаут assign</li>
                <li>Дубликаты результатов: ок — идемпотентность, но проверяйте репликацию</li>
                <li>Много EXPIRED: уменьшить chunk_size, повысить таймаут, увеличить воркеров</li>
            </ul>
        </div>
        <div class="p-4 rounded-xl border border-slate-800 bg-slate-900/60">
            <h3 class="text-brand">Sandbox/Изоляция</h3>
            <ul class="text-sm text-slate-200 space-y-1">
                <li>Fallback в process: проверить docker/wasmtime наличие</li>
                <li>Ошибка запуска: проверьте code_ref.files, entry, env</li>
                <li>Таймауты: уменьшить нагрузку, увеличить wall_time_seconds</li>
            </ul>
        </div>
    </div>
</section>
<?php include __DIR__ . "/layout/footer.php"; ?>
