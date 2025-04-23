from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    
    "weather_data",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
    
)


latest_weather_data = {}

'''for message in consumer:
    data = message.value
    city = data["city"]
    latest_weather_data[city] = {
        "city": city,
        "temperature": data["main"]["temp"],
        "weather_condition": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "timestamp": data["dt"]
    }
    print(f"Updated weather data for {city}: {latest_weather_data[city]}")'''

for message in consumer:
    data = message.value
    print(f"Raw data received: {data}")  # Print raw data for debugging

    # Use a default city name if the 'city' key is missing
    city = data.get("city", "Unknown City")
    
    latest_weather_data[city] = {
        "city": city,
        "temperature": data["main"]["temp"],
        "weather_condition": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "timestamp": data["dt"]
    }
    print(f"Updated weather data for {city}: {latest_weather_data[city]}")

