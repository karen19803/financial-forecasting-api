import os
import pickle
from prophet import Prophet
from db import load_revenue_data, load_expense_data

MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

def train_models(df, metric_name):
    departments = df["department"].unique()

    for dept in departments:
        dept_df = df[df["department"] == dept][["ds", "y"]]

        model = Prophet()
        model.fit(dept_df)

        model_path = f"{MODEL_DIR}/{dept}_{metric_name}.pkl"
        with open(model_path, "wb") as f:
            pickle.dump(model, f)

        print(f"Saved {model_path}")


if __name__ == "__main__":
    revenue_df = load_revenue_data()
    expense_df = load_expense_data()

    train_models(revenue_df, "revenue")
    train_models(expense_df, "expense")
