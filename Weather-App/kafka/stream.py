from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType, DoubleType

# Initialize Spark Session
#spark = SparkSession.builder \
#   .appName("KafkaWeatherFilter") \
#    .master("local[*]") \
#    .config("spark.sql.streaming.checkpointLocation", "/tmp/kafka-checkpoint") \
#   .getOrCreate()

spark = SparkSession.builder \
    .appName("KafkaStream") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
    .getOrCreate()

# Define Schema for JSON Parsing
schema = StructType() \
    .add("city", StringType()) \
    .add("main", StructType().add("temp", DoubleType())) \
    .add("weather", StructType().add("description", StringType()))

# Read from Kafka Topic
raw_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "weather_data") \
    .option("startingOffsets", "earliest") \
    .load() \
    .show()

# Convert Kafka Value to JSON
weather_df = raw_stream.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Filter: Keep only cities where temperature > 20°C (273.15 K)
filtered_df = weather_df.filter(col("main.temp") > 293.15)

# Write Filtered Data to Another Kafka Topic
filtered_df.selectExpr("to_json(struct(*)) AS value") \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("topic", "filtered_weather_data") \
    .option("checkpointLocation", "/tmp/filtered-weather-checkpoint") \
    .start() \
    .awaitTermination() \
    .show()
