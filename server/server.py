from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)
CORS(app)
# Load CSV once
df = pd.read_csv("rok2025.csv")
df["Date"] = pd.to_datetime(df["Date"])
df.set_index("Date", inplace=True)
df["Production_power"] = df["Production_power"] / 1000
df=df.round(2)
# df["ALLSKY_SFC_SW_DWN"] = df["ALLSKY_SFC_SW_DWN"] * 1000

df2 = pd.read_csv("rok2024.csv")
df2["Date"] = pd.to_datetime(df2["Date"])
df2.set_index("Date", inplace=True)
df2["Production_power"] = df2["Production_power"] / 1000
df2=df2.round(2)
# df2["ALLSKY_SFC_SW_DWN"] = df2["ALLSKY_SFC_SW_DWN"] * 1000


@app.route('/corr2024')
def correlation2024():
    corr = df2["Production_power"].corr(df2["ALLSKY_SFC_SW_DWN"])
    # plt.scatter(df2["ALLSKY_SFC_SW_DWN"], df2["Production_power"])
    # plt.xlabel("Solar Power (W/m²)")
    # plt.ylabel("Production Power (kW)")
    # plt.title("2024")
    # plt.savefig("correlation2024.png", dpi=300, bbox_inches="tight")
    # plt.close()
    return jsonify({ "corr" : corr})

@app.route('/corr2025')
def correlation2025():
    corr = df["Production_power"].corr(df["ALLSKY_SFC_SW_DWN"])
    # plt.scatter(df["ALLSKY_SFC_SW_DWN"], df["Production_power"])
    # plt.xlabel("Solar Power (W/m²)")
    # plt.ylabel("Production Power (kW)")
    # plt.title("2025")
    # plt.savefig("correlation2025.png", dpi=300, bbox_inches="tight")
    # plt.close()
    return jsonify({ "corr" : corr})

@app.route("/")
def index():
    return "INDEX"

@app.route("/data2025")
def get_data():
    mode = request.args.get("mode", "daily")
    if mode == "weekly":
        data = df.resample("W").agg({
            "Production_power": "mean",
            "Temp": "mean",
            "ALLSKY_SFC_SW_DWN": "mean"
        })
    elif mode == "monthly":
        data = df.resample("ME").agg({
            "Production_power": "mean",
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


@app.route("/data2024")
def get_data2():
    mode = request.args.get("mode", "daily")
    if mode == "weekly":
        data = df2.resample("W").agg({
            "Production_power": "mean",
            "Temp": "mean",
            "ALLSKY_SFC_SW_DWN": "mean"
        })
    elif mode == "monthly":
        data = df2.resample("ME").agg({
            "Production_power": "mean",
            "Temp": "mean",
            "ALLSKY_SFC_SW_DWN": "mean"
        })
    else:
        data = df2
    return jsonify({
        "labels": data.index.strftime("%Y-%m-%d").tolist(),
        "production": data["Production_power"].tolist(),
        "temp": data["Temp"].tolist(),
        "solar": data["ALLSKY_SFC_SW_DWN"].tolist()
    })


if __name__ == "__main__":
    app.run(debug=True)