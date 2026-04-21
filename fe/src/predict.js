async function getPrediction() {
    const day = document.getElementById("day").value;
    const month = document.getElementById("month").value;
    const solar = document.getElementById("solar").value;
    const temp = document.getElementById("temp").value;
    if ( day<1 || day>31){
        document.getElementById('predict-result').textContent = "Nespravne zadany vstup!"
        return;
    }else if (month<1 || month>12){
        document.getElementById('predict-result').textContent = "Nespravne zadany vstup!"
        return;
    }else if (temp<-20 || temp>50){
        document.getElementById('predict-result').textContent = "Nespravne zadany vstup!"
        return;
    }else if (solar<=0 || solar>2){
        document.getElementById('predict-result').textContent = "Nespravne zadany vstup!"
        return;
    }
    const res = await fetch(`http://localhost:5000/predict?solar=${solar}&temp=${temp}&month=${month}&day=${day}`);
    const data = await res.json();
    document.getElementById('predict-result').textContent = `Vo vybrany den bude produkcia priblizne ${data.predictedValue} kW`;
}