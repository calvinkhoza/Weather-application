from flask import Flask, jsonify
import threading

# Initialize Flask app
app = Flask(__name__)

# Shared dictionary to store the latest weather data
latest_weather_data = {}

# API endpoint to get the latest weather data
@app.route("/weather", methods=["GET"])
def get_weather():
    return jsonify(latest_weather_data)

# Function to run the Flask app
def run_flask_app():
    app.run(host="0.0.0.0", port=5000)

# Start the Flask app in a separate thread
flask_thread = threading.Thread(target=run_flask_app)
flask_thread.daemon = True
flask_thread.start()