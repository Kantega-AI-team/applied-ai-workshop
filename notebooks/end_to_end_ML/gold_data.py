# Databricks notebook source
# import required packages

import delta.tables as T
import pyspark
import pyspark.sql.functions as F
from dateutil import relativedelta
from pyspark.sql import DataFrame
from pyspark.sql.types import (DateType, DecimalType, DoubleType, IntegerType,
                               StringType, TimestampType)
from pyspark.sql.window import Window

import time

# COMMAND ----------

#remove previously ingested silver stream
dbutils.fs.rm("/FileStore/gold/data",recurse= True)
dbutils.fs.rm("/FileStore/gold/checkpoint/data",recurse= True)

# COMMAND ----------

# read and write directories

dataset_silver_path = "/FileStore/silver/data"
external_dataset_silver_path = "/FileStore/silver/external_data"
dataset_gold_path = "/FileStore/gold/data"
dataset_gold_checkpointh_path = "/FileStore/gold/checkpoint/data"

# COMMAND ----------

def make_gold_data(silver_data: DataFrame, batchId: int) -> None:
    
    # load silver external data as a static delta table 
    external_data_silver = spark.read.load(external_dataset_silver_path, format = "delta")
    
    
    #join data_silver and external_datasilver
    gold_data = (
        
        silver_data.alias("internal")
        .join(
            external_data_silver.alias("external"),
            silver_data.name == external_data_silver.name,
            "leftouter",
        )
        .select("internal.*", "external.temperature", "external.weather")
        .drop("ingestion_tmsp", "name") #for privacy 
    )
    
    # save the gold data
    
    (
        gold_data.write.mode("append")
        .option("mergeSchema", False)
        .format("delta")
        .save(dataset_gold_path)
    )

# COMMAND ----------

# read silver data stream

read_silver_data = (
    spark.readStream.format("delta")
    .option("enforceSchema", False)
    .option("maxFilesPerTrigger", 1)
    .load(dataset_silver_path)
)

# COMMAND ----------

# write silver stream

write_gold_data = (
    read_silver_data.writeStream.foreachBatch(make_gold_data)
    .trigger(availableNow=True)
    .option("checkpointLocation", dataset_gold_checkpointh_path)
    .queryName("silvering_data")
    .start()
)

# COMMAND ----------

time.sleep(60)

# load the delta lake resulting from the silvering 
gold_df = spark.read.load(dataset_gold_path, format ="delta", versionAsOf = 1)

# let's have a look at it
gold_df.display()
