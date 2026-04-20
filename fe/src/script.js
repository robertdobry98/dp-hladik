let chart;
let chart2;
let chart3;
let chart4;
let img;


function downloadFile() {
    const mode = document.getElementById("mode").value;
    const year = document.getElementById("config").dataset.year;
    window.location.href = `http://localhost:5000/download${year}?mode=${mode}`;
}

async function loadCorr() {

    const year = document.getElementById("config").dataset.year;
    const res = await fetch(`http://localhost:5000/corr${year}`);
    const data = await res.json();
    document.getElementById('corr-div').textContent = `Hodnoty svetelnosti a produkcie spolu korelujú na ${data.corr}%`;
    const container = document.getElementById('corr-img');
    if (!img){
        img = document.createElement('img');
        img.src = `assets/img/correlation${year}.png`;
        img.alt = `corr${year}`;
        img.style.width = '700px';
        container.appendChild(img);
    }
}

async function loadData() {
    const mode = document.getElementById("mode").value;
    const year = document.getElementById("config").dataset.year;
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
                    label: "Solar Power",
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
                label: "Solar Power",
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