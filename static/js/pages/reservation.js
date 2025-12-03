document.addEventListener("DOMContentLoaded", () => {
    const dateInput = document.getElementById("id_date");
    if (!dateInput) return;

    const today = new Date().toISOString().split("T")[0];

    dateInput.value = today;
    dateInput.min = today;
});

document.addEventListener("DOMContentLoaded", () => {
    const dateInput = document.getElementById("id_date");
    const closed = JSON.parse(dateInput.dataset.closedWeekdays);

    dateInput.addEventListener("change", () => {
        const selected = new Date(dateInput.value);
        let weekday = selected.getDay();

        // djangoの曜日設定に合わせる (0=月曜, 6=日曜)
        weekday = (weekday + 6) % 7; 
        console.log("closed raw =", dateInput.dataset.closedWeekdays);
        console.log("closed parsed =", closed);

        if (closed.includes(weekday)) {
            alert("この日は休業日です");
            dateInput.value = "";
        }
    });
});

