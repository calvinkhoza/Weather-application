from kafka import KafkaProducer
import requests
import json
import time
import threading

# OpenWeatherMap API Key & Cities
API_KEY = ""
CITIES = ["Johannesburg", "Cape Town", "Durban"]

# Kafka Configuration
KAFKA_TOPIC = "weather_data"
KAFKA_BROKER = "localhost:9092"

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def fetch_and_send_weather(city):
    """Fetch weather data for a city and send it to Kafka."""
    while True:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
        response = requests.get(url)
        
        if response.status_code == 200:
            weather_data = response.json()
            weather_data["city"] = city
            producer.send(KAFKA_TOPIC, weather_data)
            print(f"Sent weather data for {city} to Kafka topic {KAFKA_TOPIC}")
        elif response.status_code == 401:
            print(f"ERROR 401: Unauthorized request for {city}. Check API key.")
            break  # Stop thread if API key is incorrect or no longer valid
        else:
            print(f"Failed to fetch data for {city}: {response.status_code}")

        time.sleep(60)


# Create and start threads for each city
threads = []
for city in CITIES:
    thread = threading.Thread(target=fetch_and_send_weather, args=(city,))
    thread.daemon = True  # Daemonize the thread so it stops with the main program
    threads.append(thread)
    thread.start()

# Keep the main thread running
for thread in threads:
    thread.join()
