let chart;
let chart2;
let chart3;
let chart4;

async function loadData() {
    const mode = document.getElementById("mode").value;
    const year = document.getElementById("config").dataset.year;
    console.log(year); 
    const res = await fetch(`http://localhost:5000/data${year}?mode=${mode}`);
    const data = await res.json();
    if (chart) chart.destroy();
    if (chart2) chart2.destroy();
    if (chart3) chart3.destroy();
    if (chart4) chart4.destroy();
    chart = new Chart(document.getElementById("chart"), {
        type: "line",
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: "Production Power",
                    data: data.production,
                    borderColor: "blue"
                },
            ]
        },
    });
    chart2 = new Chart(document.getElementById("chart2"), {
        type: "line",
        data: {
            labels: data.labels,
            datasets: [     
                {
                    label: "Solar Radiation",
                    data: data.solar,
                    borderColor: "orange"
                }
            ]
        },
        options: {
            scales: {
                y: {
                    min: 0,
                    max: 1.5
                }
            }

        }
    });
    chart3 = new Chart(document.getElementById("chart3"), {
        type: "line",
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: "Temperature",
                    data: data.temp,
                    borderColor: "red"
                },
            ]
        }
        });
    chart4 = new Chart(document.getElementById("chart4"), {
    type: "line",
    data: {
        labels: data.labels,
        datasets: [
            {
                label: "Production Power",
                data: data.production,
                borderColor: "blue"
            },
            {
                label: "Temperature",
                data: data.temp,
                borderColor: "red"
            },
            {
                label: "Solar Radiation",
                data: data.solar,
                borderColor: "orange"
            }
        ]
    },
    options: {
            scales: {
                y: {
                    min: -5,
                    max: 45
                }
            }

        }
}
);
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