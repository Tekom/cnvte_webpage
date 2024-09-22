# Create the Spark Session
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType, TimestampType
from pyspark.sql.functions import to_timestamp
import uuid
import logging

spark = (
    SparkSession.builder 
    .appName("Streaming from Kafka") 
    .config("spark.streaming.stopGracefullyOnShutdown", True) 
    .config('spark.jars.packages', 'com.datastax.spark:spark-cassandra-connector_2.13:3.3.0,'
                                   'org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0')
    .config('spark.cassandra.connection.host', 'cassandra_db') 
    .config("spark.sql.shuffle.partitions", 4)
    .master("local[*]") 
    .getOrCreate()
)

spark.sparkContext.setLogLevel('WARN')
# Create the kafka_df to read from kafka
kafka_df = (
    spark
    .readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "ed-kafka:29092")
    .option("subscribe", "hamiltonev,kratos")
    .option("startingOffsets", "earliest")
    .load()
)

def generate_uuid():
    return str(uuid.uuid4())

uuid_udf = udf(generate_uuid, StringType())

# Parse value from binay to string into kafka_json_df
from pyspark.sql.functions import expr

kafka_json_df = kafka_df.withColumn("value", expr("cast(value as string)"))

# Schema of the Pyaload

from pyspark.sql.types import StringType, StructField, StructType, ArrayType, LongType

json_schema = (
    StructType(
        [
            StructField('id', StringType(), True),
            StructField('team_name', StringType(), True), 
            StructField('car_velocity', StringType(), True), 
            StructField('car_current', StringType(), True), 
            StructField('gps', StringType(), True), 
            StructField('timestamp', TimestampType(), True)
        ]
    )
)

# Apply the schema to payload to read the data
from pyspark.sql.functions import from_json,col

streaming_df = kafka_json_df.withColumn("values_json", from_json(col("value"), json_schema)).selectExpr("values_json.*")
final_df = streaming_df.select("id", "team_name", "car_velocity", "car_current", "gps", "timestamp")

# Write the output to console sink to check the output
def get_module_logger(mod_name):
    """
    To use this, do logger = get_module_logger(__name__)
    """
    logger = logging.getLogger(mod_name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger

try:
    (final_df
    .writeStream
    .format("org.apache.spark.sql.cassandra")
    .option("checkpointLocation", '/tmp/checkpoint')
    .option('keyspace', 'spark_streaming')
    .option('table', 'vehicules_data')
    .start()
    .awaitTermination())

except Exception as e:
    get_module_logger(__name__).error(f'Error in write streaming due to {e}')