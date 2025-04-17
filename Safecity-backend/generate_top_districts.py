
import psycopg2
import pandas as pd
import os
import json

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="crime_dashboard",
    user="postgres",
    password="Shiva@88",  # <-- replace with your password
    host="localhost",
    port="5432"
)

# Load data into a DataFrame
df = pd.read_sql("SELECT district, year, total_crimes_against_women FROM crimes", conn)
conn.close()

# Clean data
df['total_crimes_against_women'] = pd.to_numeric(df['total_crimes_against_women'], errors='coerce').fillna(0)

# Prepare top 5 districts by year
result = {}
for year in sorted(df['year'].unique()):
    year_df = df[df['year'] == year]
    top = (
        year_df.groupby('district')['total_crimes_against_women']
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )
    result[str(year)] = [
        {"district": row['district'], "total": int(row['total_crimes_against_women'])}
        for _, row in top.iterrows()
    ]

# Output path
os.makedirs("data", exist_ok=True)
with open("data/top_crime_districts.json", "w") as f:
    json.dump(result, f, indent=2)

print("✅ top_crime_districts.json generated successfully!")
