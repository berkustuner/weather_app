from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "Berk Üstüner"

@app.route("/weather")
def weather():
    city = request.args.get("city", "istanbul")
    api_key = "c27ffba3d514472ea4bfa7091b0a7e9d"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Şehir bulunamadı"}), 404

    data = response.json()
    return jsonify({
        "city": city,
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

