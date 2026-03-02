from flask import Flask, jsonify, request, send_from_directory
import pandas as pd
import os

app = Flask(
    __name__,
    static_folder="../frontend",     # points to your frontend folder
    static_url_path=""               # serve at root (“/”)
)

# Load the dataset
try:
    df = pd.read_csv("backend/karnataka_crime_merged_with_pdf_districts.csv")
    df.fillna(0, inplace=True)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
except Exception as e:
    print(f"Error loading data: {e}")
    df = pd.DataFrame()

# Serve your frontend’s index.html at root
@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

# Serve any other static file (JS, CSS, data JSON)
@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# --- API routes under /api ---

@app.route("/api/all")
def get_all():
    return df.to_json(orient="records")

@app.route("/api/district/<district>")
def by_district(district):
    result = df[df["district"] == district.upper()]
    return result.to_json(orient="records")

@app.route("/api/year/<int:year>")
def by_year(year):
    result = df[df["year"] == year]
    return result.to_json(orient="records")

@app.route("/api/top-crime-districts")
def top5():
    year = request.args.get("year", type=int)
    data = df[df["year"] == year] if year else df
    top = data.groupby("district")["total_crimes"].sum().nlargest(5)
    return top.reset_index().to_json(orient="records")

@app.route("/api/stats")
def stats():
    return jsonify({
        "total_crimes": int(df["total_crimes"].sum()),
        "years": sorted(df["year"].unique().tolist()),
        "districts": df["district"].nunique()
    })
# 🔹 Live News API route
# ========================

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "bf512b9c14514f72817d9f7155eb7f5b")

@app.route("/live-news")
def get_live_news():
    district = request.args.get("district", "Karnataka")
    query = f"crime {district}"

    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": bf512b9c14514f72817d9f7155eb7f5b,
        "pageSize": 10,
    }

    try:
        response = requests.get("https://newsapi.org/v2/everything", params=params)
        data = response.json()

        if data.get("status") != "ok":
            return jsonify({"error": "Failed to fetch news", "detail": data}), 500

        articles = data.get("articles", [])
        news_items = [{
            "title": a["title"],
            "summary": a.get("description", ""),
            "link": a["url"]
        } for a in articles]

        return jsonify(news_items)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=True)
