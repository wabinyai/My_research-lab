from flask import Flask, render_template, request, jsonify
from utils import get_pm25_data

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_pm25_data", methods=["POST"])
def get_pm25_data_route():
    latitude = request.json["latitude"]
    longitude = request.json["longitude"]
    pm25_data = get_pm25_data(latitude, longitude)
    return jsonify(pm25_data)

if __name__ == "__main__":
    app.run(debug=True)
