from pyspark.sql import SparkSession
from pyspark.sql.functions import expr
import json
from datetime import datetime
from time import sleep
from random import choice
from pyspark.sql.functions import from_json, col
import os
from pyspark.sql.types import StructType, StructField, StringType

# Crear sesión de Spark
spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .master("local[*]") \
    .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2') \
    .getOrCreate()

topic = "vehiculos_datos1"
print(topic)
# Leer datos de Kafka

try:
    df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:29092") \
    .option("subscribe", "vehiculos_datos1") \
    .load()

except Exception as e:
        print(f"kafka dataframe could not be created because: {e}")

# Procesar los datos (ejemplo simple: convertir los valores en strings)

schema = StructType([
        StructField("test_data", StringType(), False),
    ])

# df = df.selectExpr("CAST(value AS STRING)") \
#         .select(from_json(col('value'), schema).alias('data')).select("data.*")

print(df)
print('done')

# Escribir los datos procesados a la consola
query = df.writeStream \
    .format("console") \
    .outputMode("update") \
    .start()

print(query)
# # Mantener la ejecución del stream
#query.awaitTermination()