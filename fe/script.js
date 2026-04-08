let chart;

async function loadData() {
    const mode = document.getElementById("mode").value;

    const res = await fetch(`http://localhost:5000/data?mode=${mode}`);
    const data = await res.json();

    if (chart) chart.destroy();

    chart = new Chart(document.getElementById("chart"), {
        type: "line",
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: "Production Power",
                    data: data.production
                },
                {
                    label: "Temperature",
                    data: data.temp
                },
                {
                    label: "Solar Radiation",
                    data: data.solar
                }
            ]
        }
    });

    // ---- TABLE ----
    const tbody = document.querySelector("#dataTable tbody");
    tbody.innerHTML = ""; // clear previous rows

    for (let i = 0; i < data.labels.length; i++) {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${data.labels[i]}</td>
            <td>${data.production[i]}</td>
            <td>${data.temp[i]}</td>
            <td>${data.solar[i]}</td>
        `;

        tbody.appendChild(row);
    }
}

// Load default data when page opens
loadData();