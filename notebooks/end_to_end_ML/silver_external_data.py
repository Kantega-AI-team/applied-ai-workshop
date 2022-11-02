# Databricks notebook source
# import required packages

import pyspark
import pyspark.sql.functions as F
from pyspark.sql import DataFrame
import time

# COMMAND ----------

#remove previously ingested silver stream
dbutils.fs.rm("/FileStore/silver/external_data",recurse= True)
dbutils.fs.rm("/FileStore/silver/checkpoint/external_data",recurse= True)

# COMMAND ----------

# function for renaming columns of a dataset
def rename_columns(df: DataFrame, name_mapping: dict,) -> DataFrame:

    for name in name_mapping:

        df = df.withColumnRenamed(name, name_mapping[name])

    return df

# COMMAND ----------

# read and write directories

external_dataset_bronze_path = "/FileStore/bronze/external_data"
external_dataset_silver_path = "/FileStore/silver/external_data"
external_dataset_silver_checkpointh_path = "/FileStore/silver/checkpoint/external_data"

# COMMAND ----------

# function to be applied to each batch of the bronze stream

def make_silver_external_data(bronze_df: DataFrame, batchId: int) -> None:
    
    data_names_map = {
        "NAME": "name",
        "temp": "temperature",
    }
    
    #rename columns 
    silver_df_stage_1 = rename_columns(bronze_df, data_names_map)
    
    # add columns categorizing the temperature into "weather"
    
    silver_df_stage_2 = (
        silver_df_stage_1
        .withColumn("weather", 
                    F.when(F.col("temperature")<= 5, "very_cold")
                    .when( (F.col("temperature")> 5) & ((F.col("temperature")<= 11)), "cold")
                    .when( (F.col("temperature")> 11) & ((F.col("temperature")<= 22)), "mild")
                    .when( (F.col("temperature")> 22) & ((F.col("temperature")<= 30)), "warm")
                    .when( (F.col("temperature")> 30) , "hot")
                   )
    )

    
    
    # reduce number of partitions to one
    silver_df_stage_3 = silver_df_stage_2.coalesce(1)
    
     # save the silver dataset

    (
        silver_df_stage_3.write.mode("append")
        .option("mergeSchema", False)
        .format("delta")
        .save(external_dataset_silver_path)
    )

# COMMAND ----------

# read bronze stream

read_bronze_external_data = (
    spark.readStream.format("delta")
    .option("enforceSchema", False)
    .option("maxFilesPerTrigger", 1)
    .load(external_dataset_bronze_path)
)

# COMMAND ----------

# write silver stream

write_silver_external_data = (
    read_bronze_external_data.writeStream.foreachBatch(make_silver_external_data)
    .trigger(availableNow=True)
    .option("checkpointLocation", external_dataset_silver_checkpointh_path)
    .queryName("silvering_external_data")
    .start()
)

# COMMAND ----------

time.sleep(60)

# load the delta lake resulting from the silvering 
silver_df = spark.read.load(external_dataset_silver_path, format ="delta", versionAsOf = 4)

# let's have a look at it
silver_df.display()

# COMMAND ----------


