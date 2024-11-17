function toggleSelection(day) {
    const checkbox = document.getElementById(`checkbox-${day}`);
    checkbox.checked = !checkbox.checked;

    const cell = document.getElementById(`day-${day}`);
    if (checkbox.checked) {
        cell.classList.add("selected");
    } else {
        cell.classList.remove("selected");
    }
}
