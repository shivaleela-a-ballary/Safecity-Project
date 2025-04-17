
import psycopg2
import pandas as pd
import json
from sklearn.cluster import KMeans
import os

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="crime_dashboard",
    user="postgres",
    password="Shiva@88",  # <-- Replace with your actual password
    host="localhost",
    port="5432"
)

# Load lat/lon data
query = '''
    SELECT latitude, longitude
    FROM crimes
    WHERE latitude IS NOT NULL AND longitude IS NOT NULL
'''
df = pd.read_sql(query, conn)
conn.close()

# Drop rows with invalid lat/lon
df = df.dropna()

# Cluster with KMeans
kmeans = KMeans(n_clusters=5, random_state=42)
df['cluster'] = kmeans.fit_predict(df[['latitude', 'longitude']])

# Count points per cluster
result = (
    df.groupby('cluster')
    .agg({'latitude': 'mean', 'longitude': 'mean', 'cluster': 'count'})
    .rename(columns={'cluster': 'count'})
    .reset_index()
)

# Format result
output = []
for _, row in result.iterrows():
    output.append({
        "cluster": int(row['cluster']),
        "lat": round(row['latitude'], 6),
        "lon": round(row['longitude'], 6),
        "count": int(row['count'])
    })

# Save to JSON
os.makedirs("data", exist_ok=True)
with open("data/crime_clusters.json", "w") as f:
    json.dump(output, f, indent=2)

print("✅ crime_clusters.json saved.")
