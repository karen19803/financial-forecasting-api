# Financial Forecasting API

This project implements a production-ready financial forecasting system using FastAPI and Facebook Prophet.
It provides department-level revenue and expense forecasts based on historical data stored in a PostgreSQL database.

The system supports model training, persistence, real-time forecasting, and on-demand retraining through a REST API.

---

## Architecture Overview

The system follows a clean and modular architecture:

PostgreSQL (Neon)
→ FastAPI
→ Prophet Models
→ Forecast API

Key design principles:
- Database-driven training
- Department-specific models
- SQL-side date normalization
- Model persistence using pickle
- Low-latency inference through in-memory models

---

## Data Handling

Historical data is stored in PostgreSQL tables.
Expense data contains a textual month column (e.g. `Jan-2020`), which is converted to a datetime format directly in SQL:

```sql
TO_DATE("Month", 'Mon-YYYY') AS ds
```
This ensures compatibility with Prophet without modifying the database schema.

All datasets are loaded into Pandas DataFrames using SQLAlchemy and formatted according to Prophet requirements:

- `ds`: datetime column  
- `y`: target value (revenue or actual expense)

---

## Model Training

- A separate Prophet model is trained for each department and metric.
- Total models: 10 (5 departments × revenue and expense).
- Training is performed in batch using historical data.
- Models are serialized as `.pkl` files and stored in the `models/` directory.

Training can be executed using:

```bash
python train_and_save_models.py
```
---

## API Endpoints
### Forecast
Returns future forecasts for a given department and metric.

```bash
GET /forecast
```

Query parameters:

- department: Department name
- metric: revenue or expense
- periods: Number of future months (default: 12)

Response includes predicted values and confidence intervals.

---

## Retrain
Retrains all models using the latest data from the database.

```bash
POST /retrain
```

This endpoint:

-Reloads historical data
-Retrains all Prophet models in batch
-Updates saved models and in-memory instances
-Does not require restarting the API service

---

## Exploratory Data Analysis

Exploratory Data Analysis (EDA) and data validation were performed offline using Jupyter notebooks.
These steps are not part of the production pipeline and are provided for reference in the ```bash notebooks/ ```directory.

---

## Running the Project

1. Clone the repository
2. Create a virtual environment
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Create a .env file using .env.example
5. Start the API server:
```bash
uvicorn app:app --reload
```
---

## Key Features

- Production-ready FastAPI service

- Department-level financial forecasting

- SQL-based date normalization

- Batch model training and retraining

- Persistent model storage

- Low-latency inference

- Clean separation between research and production

---

## Future Improvements

- Scheduled retraining

- Model versioning

- Model evaluation and monitoring

- Anomaly detection on incoming data

- Authentication and access control
