
function toggleSelection(day) {
    const cell = document.getElementById(`day-${day}`);
    const checkbox = document.getElementById(`checkbox-${day}`);

    // 初期状態のクラスを取得
    const classes = ["green", "yellow", "red"];
    const symbols = { green: "〇", yellow: "△", red: "×" };

    // 現在のクラスを取得し、次のクラスを決定
    let currentClass = classes.find(cls => cell.classList.contains(cls)) || "green";
    let nextClass = classes[(classes.indexOf(currentClass) + 1) % classes.length];

    // クラスを更新
    cell.classList.remove(currentClass);
    cell.classList.add(nextClass);

    // マークを更新
    cell.textContent = String(day) +"\n"+ symbols[nextClass];

    // チェックボックスの状態を更新 (CSV出力用)
    checkbox.value = nextClass;
    checkbox.checked = nextClass !== "green";
}
