import psycopg2
import pandas as pd
import os
import json
import re

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="crime_dashboard",
    user="postgres",
    password="Shiva@88",  # <-- Replace with your PostgreSQL password
    host="localhost",
    port="5432"
)

# Load data
df = pd.read_sql("SELECT * FROM crimes", conn)
conn.close()

# Output folder
output_dir = "district_summaries"
os.makedirs(output_dir, exist_ok=True)

# Generate JSON summaries
for district in df['district'].unique():
    ddf = df[df['district'] == district]

    totals_by_year = ddf.groupby('year')['total_crimes_against_women'].sum().to_dict()

    crime_types = {
        "murder": ddf['murder'].sum(),
        "rape": ddf['rape'].sum(),
        "kidnapping": ddf['kidnapping_abduction'].sum(),
        "dowry": ddf['dowry_deaths'].sum(),
        "cruelty": ddf['cruelty_by_husband'].sum()
    }
    top_crimes = sorted(crime_types, key=crime_types.get, reverse=True)[:3]

    trend = [{"year": int(y), "total": int(t)} for y, t in totals_by_year.items()]

    lat = float(ddf['latitude'].iloc[0])
    lon = float(ddf['longitude'].iloc[0])

    summary = {
        "district": district,
        "location": [lat, lon],
        "totals_by_year": totals_by_year,
        "top_crimes": top_crimes,
        "trend": trend
    }

    safe_name = re.sub(r'[^a-zA-Z0-9_]', '', district.replace(" ", "_").upper())
    filename = f"summary_{safe_name}.json"
    with open(os.path.join(output_dir, filename), "w") as f:
        json.dump(summary, f, indent=2)

print("✅ District summaries generated successfully.")
