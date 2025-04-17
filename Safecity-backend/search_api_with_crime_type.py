
from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


# PostgreSQL connection
def get_connection():
    return psycopg2.connect(
        dbname="crime_dashboard",
        user="postgres",
        password="Shiva@88",  # <-- Replace with your password
        host="localhost",
        port="5432"
    )

@app.route('/api/crimes', methods=['GET'])
def search_crimes():
    district = request.args.get('district', '').strip().upper()
    start_year = request.args.get('start_year')
    end_year = request.args.get('end_year')
    crime_type = request.args.get('crime_type', '').strip().lower()

    if not start_year or not end_year:
        return jsonify({"error": "Please provide both start_year and end_year"}), 400

    allowed_crimes = [
        "murder", "rape", "kidnapping_abduction",
        "dowry_deaths", "cruelty_by_husband", "total_crimes_against_women"
    ]
    if crime_type and crime_type not in allowed_crimes:
        return jsonify({"error": f"Invalid crime_type. Choose from: {', '.join(allowed_crimes)}"}), 400

    conn = get_connection()
    cur = conn.cursor()

    # Build dynamic query
    select_fields = "district, year"
    sum_fields = ", ".join([f"SUM({crime_type})" if crime_type else f"SUM({col})"
                            for col in allowed_crimes if not crime_type or col == crime_type])
    full_query = f"SELECT {select_fields}, {sum_fields} FROM crimes WHERE year BETWEEN %s AND %s"
    params = [start_year, end_year]

    if district != "ALL":
        full_query += " AND UPPER(district) LIKE %s"
        params.append(f"%{district}%")

    full_query += " GROUP BY district, year ORDER BY year"

    cur.execute(full_query, params)
    rows = cur.fetchall()
    conn.close()

    if not rows:
        return jsonify({"error": "No data found"}), 404

    results = []
    for row in rows:
        base = {"district": row[0], "year": row[1]}
        if crime_type:
            base[crime_type] = int(row[2])
        else:
            for i, crime in enumerate(allowed_crimes):
                base[crime] = int(row[i + 2])
        results.append(base)

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
@app.route('/predict', methods=['GET'])
def predict_crimes():
    import pandas as pd
    from statsmodels.tsa.arima.model import ARIMA

    df = pd.read_csv("karnataka_crime_merged_with_pdf_districts.csv")
    predictions = []

    for district in df['district'].unique():
        df_d = df[df['district'] == district].sort_values('year')
        try:
            series = df_d.groupby('year')['total_crimes_against_women'].sum()
            model = ARIMA(series, order=(1, 1, 1))
            model_fit = model.fit()
            forecast = model_fit.forecast(steps=1)
            predictions.append({
                "district": district,
                "total_predicted": round(float(forecast[0]), 2)
            })
        except:
            continue

    predictions = sorted(predictions, key=lambda x: x["total_predicted"], reverse=True)[:10]
    return jsonify(predictions)
