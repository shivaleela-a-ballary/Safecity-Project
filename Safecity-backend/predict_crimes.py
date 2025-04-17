
import psycopg2
import pandas as pd
import json
from sklearn.linear_model import LinearRegression
import os

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="crime_dashboard",
    user="postgres",
    password="Shiva@88",  # <-- Replace with your actual password
    host="localhost",
    port="5432"
)

# Query past crime totals
query = '''
    SELECT district, year, total_crimes_against_women
    FROM crimes
    WHERE total_crimes_against_women IS NOT NULL
    ORDER BY district, year
'''
df = pd.read_sql(query, conn)
conn.close()

# Forecast 2024 total crimes for each district
predictions = []
for district in df['district'].unique():
    ddf = df[df['district'] == district]
    if len(ddf['year'].unique()) < 3:
        continue  # skip if not enough data

    X = ddf[['year']]
    y = ddf['total_crimes_against_women']
    model = LinearRegression()
    model.fit(X, y)

    y_pred = model.predict([[2024]])
    predictions.append({
        "district": district,
        "year": 2024,
        "predicted_total": int(round(y_pred[0]))
    })

# Save to JSON
os.makedirs("data", exist_ok=True)
with open("data/crime_predictions.json", "w") as f:
    json.dump(predictions, f, indent=2)

print("✅ crime_predictions.json saved.")
