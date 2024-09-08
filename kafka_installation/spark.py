# Create the Spark Session
from pyspark.sql import SparkSession

spark = (
    SparkSession 
    .builder 
    .appName("Streaming from Kafka") 
    .config("spark.streaming.stopGracefullyOnShutdown", True) 
    .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0')
    .config("spark.sql.shuffle.partitions", 4)
    .master("local[*]") 
    .getOrCreate()
)

# Create the kafka_df to read from kafka

kafka_df = (
    spark
    .readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "ed-kafka:29092")
    .option("subscribe", "device-data")
    .option("startingOffsets", "earliest")
    .load()
)

# View schema for raw kafka_df
kafka_df.printSchema()
#kafka_df.show()

# Parse value from binay to string into kafka_json_df
from pyspark.sql.functions import expr

kafka_json_df = kafka_df.withColumn("value", expr("cast(value as string)"))

# Schema of the Pyaload

from pyspark.sql.types import StringType, StructField, StructType, ArrayType, LongType

json_schema = (
    StructType(
    [StructField('customerId', StringType(), True), 
    StructField('data', StructType(
        [StructField('devices', 
                     ArrayType(StructType([ 
                        StructField('deviceId', StringType(), True), 
                        StructField('measure', StringType(), True), 
                        StructField('status', StringType(), True), 
                        StructField('temperature', LongType(), True)
                    ]), True), True)
        ]), True), 
    StructField('eventId', StringType(), True), 
    StructField('eventOffset', LongType(), True), 
    StructField('eventPublisher', StringType(), True), 
    StructField('eventTime', StringType(), True)
    ])
)


# Apply the schema to payload to read the data
from pyspark.sql.functions import from_json,col

streaming_df = kafka_json_df.withColumn("values_json", from_json(col("value"), json_schema)).selectExpr("values_json.*")

# To the schema of the data, place a sample json file and change readStream to read 
streaming_df.printSchema()
#streaming_df.show(truncate=False)

# Lets explode the data as devices contains list/array of device reading
from pyspark.sql.functions import explode

exploded_df = streaming_df.withColumn("data_devices", explode("data.devices"))


# Check the schema of the exploded_df, place a sample json file and change readStream to read 
exploded_df.printSchema()
#exploded_df.show(truncate=False)

# Flatten the exploded df
from pyspark.sql.functions import col

flattened_df = (
    exploded_df
    .drop("data")
    .withColumn("deviceId", col("data_devices.deviceId"))
    .withColumn("measure", col("data_devices.measure"))
    .withColumn("status", col("data_devices.status"))
    .withColumn("temperature", col("data_devices.temperature"))
    .drop("data_devices")
)

# Check the schema of the flattened_df, place a sample json file and change readStream to read 
flattened_df.printSchema()
#flattened_df.show(truncate=False)

# Write the output to console sink to check the output

(flattened_df
 .writeStream
 .format("console")
 .outputMode("append")
 .option("checkpointLocation", "checkpoint_dir_kafka")
 .start()
 .awaitTermination())