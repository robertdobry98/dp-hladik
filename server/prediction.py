import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import random
def trainModel():
    df = pd.read_csv("data-merged.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df["day_of_year"] = df["Date"].dt.dayofyear
    df["month"] = df["Date"].dt.month
    X = df[["Solar_Power", "Temp", "day_of_year", "month"]]
    y = df["Production_power"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.15, random_state=42
    )
    model = RandomForestRegressor()
    model.fit(X_train, y_train)
    return model

def predictValues(data, model):
    return model.predict(data)[0]