from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = "bf512b9c14514f72817d9f7155eb7f5b"  # replace with your real key

@app.route("/live-news", methods=["GET"])
def get_crime_news():
    district = request.args.get("district", "Karnataka")
    query = f"crime {district}"
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={bf512b9c14514f72817d9f7155eb7f5b}&pageSize=5&language=en"

    try:
        response = requests.get(url)
        data = response.json()

        articles = [{
            "title": a["title"],
            "summary": a.get("description", ""),
            "link": a["url"]
        } for a in data.get("articles", [])]

        return jsonify(articles)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
