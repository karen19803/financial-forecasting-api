import pandas as pd
import psycopg2
from sqlalchemy import create_engine


# 1. Load CSV
df = pd.read_csv("konecta_budget_vs_actual.csv")  

# 2. Connect to Neon Postgres
engine = create_engine(
    "postgresql+psycopg2://neondb_owner:npg_JxagX98GlRvV@" 
    "ep-dark-mode-a4hxz46r-pooler.us-east-1.aws.neon.tech/neondb"
    "?sslmode=require&channel_binding=require"
)

# 3. Upload to Neon (replace = drop + recreate, append = add rows)
df.to_sql(
    "konecta_budget_vs_actual",   # change to your table name
    engine,
    if_exists="replace",  # or "append"
    index=False
)

print("Uploaded successfully!")
