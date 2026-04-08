from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)
# Load CSV once
df = pd.read_csv("rok2025.csv")
df["Date"] = pd.to_datetime(df["Date"])
df.set_index("Date", inplace=True)
@app.route("/")
def index():
    return "INDEX"
@app.route("/data")
def get_data():
    mode = request.args.get("mode", "daily")

    if mode == "weekly":
        data = df.resample("W").agg({
            "Production_power": "sum",
            "Temp": "mean",
            "ALLSKY_SFC_SW_DWN": "mean"
        })
    elif mode == "monthly":
        data = df.resample("ME").agg({
            "Production_power": "sum",
            "Temp": "mean",
            "ALLSKY_SFC_SW_DWN": "mean"
        })
    else:
        data = df

    return jsonify({
        "labels": data.index.strftime("%Y-%m-%d").tolist(),
        "production": data["Production_power"].tolist(),
        "temp": data["Temp"].tolist(),
        "solar": data["ALLSKY_SFC_SW_DWN"].tolist()
    })


if __name__ == "__main__":
    app.run(debug=True)