import os
import pickle
from fastapi import FastAPI
import pandas as pd
from prophet import Prophet
from db import load_revenue_data, load_expense_data

MODEL_DIR = "models"

app = FastAPI(title="Financial Forecasting API")

models = {}

def load_models():
    for file in os.listdir(MODEL_DIR):
        if file.endswith(".pkl"):
            with open(f"{MODEL_DIR}/{file}", "rb") as f:
                models[file.replace(".pkl", "")] = pickle.load(f)

load_models()


@app.get("/forecast")
def forecast(department: str, metric: str, periods: int = 12):
    """
    metric = revenue | expense
    """
    key = f"{department}_{metric}"
    model = models.get(key)

    if not model:
        return {"error": "Model not found"}

    future = model.make_future_dataframe(periods=periods, freq="MS")
    forecast = model.predict(future)

    return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(periods).to_dict("records")


@app.post("/retrain")
def retrain():
    revenue_df = load_revenue_data()
    expense_df = load_expense_data()

    for df, metric in [(revenue_df, "revenue"), (expense_df, "expense")]:
        for dept in df["department"].unique():
            dept_df = df[df["department"] == dept][["ds", "y"]]
            model = Prophet()
            model.fit(dept_df)

            path = f"{MODEL_DIR}/{dept}_{metric}.pkl"
            with open(path, "wb") as f:
                pickle.dump(model, f)

            models[f"{dept}_{metric}"] = model

    return {"status": "Models retrained successfully"}
