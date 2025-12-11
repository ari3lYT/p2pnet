<?php
$title = "Pipeline / DAG";
$active = "pipeline.php";
include __DIR__ . "/layout/header.php";
?>
<section>
    <h2>Pipeline задачи</h2>
    <p>Тип <code>PIPELINE</code> объединяет узлы с зависимостями. Исполнение послойное (зависимости → готовые узлы).</p>
    <pre><code class="language-python">pipeline = Task.create_pipeline(
    owner_id="o",
    nodes=[
        {"id": "step1", "task": Task.create_map("o", [1,2,3], "square").to_dict()},
        {"id": "step2", "task": Task.create_map_reduce("o", [], "x", "sum").to_dict(), "depends_on": ["step1"]},
    ],
)</code></pre>
    <div class="mermaid">
        graph LR
          A[step1 map square] --> B[step2 map_reduce sum]
    </div>
</section>
<section>
    <h2>Best practices</h2>
    <ul>
        <li>Готовьте данные на ранних узлах, передавайте через <code>input_data</code></li>
        <li>Делайте шардинг на map-узлах, reduce — в конце</li>
        <li>Следите за лимитами по времени/памяти на каждом узле</li>
    </ul>
</section>
<?php include __DIR__ . "/layout/footer.php"; ?>
