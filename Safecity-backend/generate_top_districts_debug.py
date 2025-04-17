import psycopg2
import pandas as pd
import os
import json
import re

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="crime_dashboard",
    user="postgres",
    password="Shiva@88",  # <-- Replace with your actual password
    host="localhost",
    port="5432"
)

# Load data
df = pd.read_sql("SELECT district, year, total_crimes_against_women FROM crimes", conn)
conn.close()

# Debug print: total rows fetched
print(f"✅ Total rows fetched from DB: {len(df)}")

# Clean district names
df['district'] = df['district'].apply(lambda x: re.sub(r'[^a-zA-Z\\s]', '', x).strip().upper())

# Convert totals to numeric and filter out zeros
df['total_crimes_against_women'] = pd.to_numeric(df['total_crimes_against_women'], errors='coerce').fillna(0)
df = df[df['total_crimes_against_women'] > 0]

# Debug print: after filtering
print(f"✅ Rows with total_crimes > 0: {len(df)}")
print("📌 Sample cleaned data:")
print(df.head())

# Group and find top districts
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
    print(f"🏆 Top 5 districts for {year}:")
    print(top)
    
    result[str(year)] = [
        {"district": row['district'], "total": int(row['total_crimes_against_women'])}
        for _, row in top.iterrows()
    ]

# Save result to JSON
os.makedirs("data", exist_ok=True)
with open("data/top_crime_districts.json", "w") as f:
    json.dump(result, f, indent=2)

print("✅ Done! File saved to data/top_crime_districts.json")
