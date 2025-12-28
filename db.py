import pandas as pd
from sqlalchemy import create_engine
from settings import settings

engine = create_engine(settings.DATABASE_URL)

def load_revenue_data():
    query = """
    SELECT
        month AS ds,
        department,
        revenue AS y
    FROM konecta_revenues
    ORDER BY ds
    """
    return pd.read_sql(query, engine)


def load_expense_data():
    query = """
    SELECT
        TO_DATE("Month", 'Mon-YYYY') AS ds,
        "Department" AS department,
        "Actual" AS y
    FROM konecta_budget_vs_actual
    ORDER BY ds
    """
    return pd.read_sql(query, engine)
