# Databricks notebook source
import base64
import datetime
import hashlib
import hmac
import json

import pyspark
import pyspark.sql.functions as F
import requests
from pyspark.sql import DataFrame
from pyspark.sql.streaming import StreamingQueryListener
from pyspark.sql.types import (
    DoubleType,
    FloatType,
    IntegerType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)

# COMMAND ----------

#remove previously ingested bronze stream
dbutils.fs.rm("/FileStore/bronze",recurse= True)

# COMMAND ----------

# set schema 

data_schema = StructType(
    [
        StructField("NAME", StringType(), False),
        StructField("COUNTY", StringType(), False),
        StructField("AREA", IntegerType(), True),
        StructField("POPULATION", IntegerType(), True),
        StructField("CABIN_CONSTRUCTION", DoubleType(), True),
        StructField("ECO_RIVER_WATER", DoubleType(), False),
    ]
)


# COMMAND ----------

#data1= spark.read.load("/FileStore/raw_data/dataset_1.csv", sep = ";", header = True, format = "csv", schema = data_schema)

# COMMAND ----------

#paths for raw and bronze datasets

dataset_raw_path = "/FileStore/raw_data/dataset*.csv"
dataset_bronze_path = "/FileStore/bronze/data"
dataset_bronze_checkpointh_path = "/FileStore/bronze/checkpoint/data"

# COMMAND ----------

# function to be applied to each batch of the stream

def make_bronze_data(raw_df: DataFrame, batchId: int) -> None:
    
    # add ingestion timestamp column
    bronze_df = raw_df.withColumn(
        "ingestion_tmsp",
        F.date_format(
            F.from_utc_timestamp(F.current_timestamp(), "Europe/Rome"),
            "yyyy-MM-dd HH:mm",
        ),
    )
    
    
    # reduce number of partitions to one
    bronze_df = bronze_df.coalesce(1)

    # store the bronze dataset
    (
        bronze_df.write.mode("append")
        .option("mergeSchema", False)
        .format("delta")
        .save(dataset_bronze_path)
    )
    
    

# COMMAND ----------

# read raw stream

read_raw_data = (
    spark.readStream.format("csv")
    .option("header", True)
    .option("sep", ";")
    .schema(data_schema)
    .option("enforceSchema", False)
    .option("maxFilesPerTrigger", 1)
    .load(dataset_raw_path)
)

# COMMAND ----------

# write stream
write_bronze_data = (
    read_raw_data.writeStream.foreachBatch(make_bronze_data)
    .trigger(availableNow=True)
    .option("checkpointLocation", dataset_bronze_checkpointh_path)
    .queryName("bronzing_data")
    .start()
)

# COMMAND ----------

time.sleep(60)

# load the delta lake resulting from the bronzing 
bronze_df = spark.read.load(dataset_bronze_path, format ="delta", versionAsOf = 1)

# let's have a look at it
bronze_df.display()

# COMMAND ----------


