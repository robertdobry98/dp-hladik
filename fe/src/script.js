let chart;
let chart2;
let chart3;

async function loadData(year) {
    const mode = document.getElementById("mode").value;
    console.log(`${year} `);

    const res = await fetch(`http://localhost:5000/data${year}?mode=${mode}`);
    const data = await res.json();

    if (chart) chart.destroy();
    if (chart2) chart2.destroy();
    if (chart3) chart3.destroy();

    chart = new Chart(document.getElementById("chart"), {
        type: "line",
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: "Production Power",
                    data: data.production
                },
            ]
        }
    });

    chart2 = new Chart(document.getElementById("chart2"), {
        type: "line",
        data: {
            labels: data.labels,
            datasets: [     
                {
                    label: "Solar Radiation",
                    data: data.solar
                }
            ]
        },
        options: {
            scales: {
                y: {
                    min: -2,
                    max: 2
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
                    data: data.temp
                },
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
loadData(2025);