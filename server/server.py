from flask import Flask, request, jsonify, Response
from waitress import serve
from flask_cors import CORS
import pandas as pd
import prediction, io
app = Flask(__name__)
CORS(app)
df = pd.read_csv("rok2025.csv")
df["Date"] = pd.to_datetime(df["Date"])
df.set_index("Date", inplace=True)
df["Production_power"] = df["Production_power"] / 1000
df=df.round(2)

df2 = pd.read_csv("rok2024.csv")
df2["Date"] = pd.to_datetime(df2["Date"])
df2.set_index("Date", inplace=True)
df2["Production_power"] = df2["Production_power"] / 1000
df2=df2.round(2)


@app.route("/download2025")
def download_file2025():
    print('/download2025')
    output=io.StringIO()
    mode = request.args.get("mode", "daily")
    if mode == "weekly":
        data = df.resample("W").agg({
            "Production_power": "mean",
            "Temp": "mean",
            "Solar_Power": "mean"
        }).round(2)
    elif mode == "monthly":
        data = df.resample("ME").agg({
            "Production_power": "mean",
            "Temp": "mean",
            "Solar_Power": "mean"
        }).round(2)
    else:
        data = df
    data.to_csv(output, index=False)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=prehlad2025.csv"}
    )


@app.route("/download2024")
def download_file2024():
    print('/download2024')
    output=io.StringIO()
    mode = request.args.get("mode", "daily")
    if mode == "weekly":
        data = df2.resample("W").agg({
            "Production_power": "mean",
            "Temp": "mean",
            "Solar_Power": "mean"
        }).round(2)
    elif mode == "monthly":
        data = df2.resample("ME").agg({
            "Production_power": "mean",
            "Temp": "mean",
            "Solar_Power": "mean"
        }).round(2)
    else:
        data = df2
    data.to_csv(output, index=False)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=prehlad2024.csv"}
    )


@app.route('/corr2024')
def correlation2024():
    print('/corr2024')
    corr = df2["Production_power"].corr(df2["Solar_Power"])
    corr = (corr*100).round(2)
    return jsonify({"corr" : corr})

@app.route('/corr2025')
def correlation2025():
    print('/corr2025')
    corr = df["Production_power"].corr(df["Solar_Power"])
    corr = (corr*100).round(2)
    return jsonify({ "corr" : corr})

@app.route("/")
def index():
    return "INDEX"

@app.route("/data2025")
def get_data():
    print('/data2025')
    mode = request.args.get("mode", "daily")
    if mode == "weekly":
        data = df.resample("W").agg({
            "Production_power": "mean",
            "Temp": "mean",
            "Solar_Power": "mean"
        }).round(2)
    elif mode == "monthly":
        data = df.resample("ME").agg({
            "Production_power": "mean",
            "Temp": "mean",
            "Solar_Power": "mean"
        }).round(2)
    else:
        data = df
    return jsonify({
        "labels": data.index.strftime("%Y-%m-%d").tolist(),
        "production": data["Production_power"].tolist(),
        "temp": data["Temp"].tolist(),
        "solar": data["Solar_Power"].tolist()
    })


@app.route("/data2024")
def get_data2():
    print('/data2024')
    mode = request.args.get("mode", "daily")
    if mode == "weekly":
        data = df2.resample("W").agg({
            "Production_power": "mean",
            "Temp": "mean",
            "Solar_Power": "mean"
        }).round(2)

    elif mode == "monthly":
        data = df2.resample("ME").agg({
            "Production_power": "mean",
            "Temp": "mean",
            "Solar_Power": "mean"
        }).round(2)
    else:
        data = df2
    return jsonify({
        "labels": data.index.strftime("%Y-%m-%d").tolist(),
        "production": data["Production_power"].tolist(),
        "temp": data["Temp"].tolist(),
        "solar": data["Solar_Power"].tolist()
    })


@app.route("/predict", methods=['GET'])
def predict():
    print('/predict')
    solar = request.args.get('solar')
    temp = request.args.get('temp')
    day = request.args.get('day')
    month = request.args.get('month')
    model = prediction.trainModel()
    new_data = pd.DataFrame({
    "Solar_Power": [solar],
    "Temp": [temp],
    "day_of_year": [day],
    "month" : [month]
    })
    value = prediction.predictValues(data=new_data, model=model)
    return jsonify({"predictedValue" : round(value/1000,2) })


if __name__ == "__main__":
    print("program started")
    serve(app, host="0.0.0.0", port=5000)