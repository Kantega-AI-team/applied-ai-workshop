# Databricks notebook source
# load required packages

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

import time

# COMMAND ----------

#remove previously ingested bronze stream
dbutils.fs.rm("/FileStore/bronze/external_data",recurse= True)
dbutils.fs.rm("/FileStore/bronze/checkpoint/external_data",recurse= True)

# COMMAND ----------

#external_data1= spark.read.load("/FileStore/raw_data/external_dataset_1.csv", sep = ";", header = True, format = "csv")

# COMMAND ----------

# set schema 

external_data_schema = StructType(
    [
        StructField("NAME", StringType(), False),
        StructField("temp", DoubleType(), False),
    ]
)



# COMMAND ----------

#paths for raw and bronze datasets

external_dataset_raw_path = "/FileStore/raw_data/external_dataset*.csv"
external_dataset_bronze_path = "/FileStore/bronze/external_data"
external_dataset_bronze_checkpointh_path = "/FileStore/bronze/checkpoint/external_data"

# COMMAND ----------

# function to be applied to each batch of the stream

def make_bronze_external_data(raw_df: DataFrame, batchId: int) -> None:
    
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
        .save(external_dataset_bronze_path)
    )
    
    

# COMMAND ----------

# read raw stream

read_raw_external_data = (
    spark.readStream.format("csv")
    .option("header", True)
    .option("sep", ";")
    .schema(external_data_schema)
    .option("enforceSchema", False)
    .option("maxFilesPerTrigger", 1)
    .load(external_dataset_raw_path)
)

# COMMAND ----------

# write stream
write_bronze_external_data = (
    read_raw_external_data.writeStream.foreachBatch(make_bronze_external_data)
    .trigger(availableNow=True)
    .option("checkpointLocation", external_dataset_bronze_checkpointh_path)
    .queryName("bronzing_external_data")
    .start()
)

# COMMAND ----------

time.sleep(60)

# load the delta lake resulting from the bronzing 
bronze_df = spark.read.load(external_dataset_bronze_path, format ="delta", versionAsOf = 1)

# let's have a look at it
bronze_df.display()
