# Databricks notebook source
# import required packages

import pyspark
import pyspark.sql.functions as F
from pyspark.sql import DataFrame
import time

# COMMAND ----------

#remove previously ingested silver stream
dbutils.fs.rm("/FileStore/silver",recurse= True)

# COMMAND ----------

# function for renaming columns of a dataset
def rename_columns(df: DataFrame, name_mapping: dict,) -> DataFrame:

    for name in name_mapping:

        df = df.withColumnRenamed(name, name_mapping[name])

    return df

# COMMAND ----------

# read and write directories

dataset_bronze_path = "/FileStore/bronze/data"
dataset_silver_path = "/FileStore/silver/data"
dataset_silver_checkpointh_path = "/FileStore/silver/checkpoint/data"

# COMMAND ----------

# function to be applied to each batch of the bronze stream

def make_silver_data(bronze_df: DataFrame, batchId: int) -> None:
    
    data_names_map = {
        "NAME": "name",
        "COUNTY": "county",
        "AREA": "area",
        "POPULATION": "population",
        "CABIN_CONSTRUCTION": "cabin_construction",
        "ECO_RIVER_WATER": "eco_river_water",
    }
    
    #rename columns 
    silver_df_stage_1 = rename_columns(bronze_df, data_names_map)
    
    # reduce number of partitions to one
    silver_df_stage_2 = silver_df_stage_1.coalesce(1)
    
     # save the silver dataset

    (
        silver_df_stage_2.write.mode("append")
        .option("mergeSchema", False)
        .format("delta")
        .save(dataset_silver_path)
    )

# COMMAND ----------

# read bronze stream

read_bronze_data = (
    spark.readStream.format("delta")
    .option("enforceSchema", False)
    .option("maxFilesPerTrigger", 1)
    .load(dataset_bronze_path)
)

# COMMAND ----------

# write silver stream

write_silver_data = (
    read_bronze_data.writeStream.foreachBatch(make_silver_data)
    .trigger(availableNow=True)
    .option("checkpointLocation", dataset_silver_checkpointh_path)
    .queryName("silvering_data")
    .start()
)

# COMMAND ----------

time.sleep(60)

# load the delta lake resulting from the silvering 
silver_df = spark.read.load(dataset_silver_path, format ="delta", versionAsOf = 0)

# let's have a look at it
silver_df.display()
