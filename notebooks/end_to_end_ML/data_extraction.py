# Databricks notebook source
# import required modules

import pyspark
import pyspark.sql.functions as F
from pyspark.sql import DataFrame
from pyspark.sql.types import (
    DoubleType,
    FloatType,
    IntegerType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)
import os
import pandas as pd

# COMMAND ----------

# read the original dataset

original_dataset = spark.read.load("dbfs:/user/hive/warehouse/naturkampen_1", format = "delta")

# COMMAND ----------

# transform Spark DataFrame in Pandas
original_dataset_pd = original_dataset.toPandas()

# drop _c0 column
original_dataset_pd = original_dataset_pd.drop(["_c0"], axis = 1)

# change column names from lower to upper case (so we can re-transform them in lower case during the silvering phase)
original_dataset_pd = original_dataset_pd.rename(columns = str.upper)

# store the pandas version of the original dataset in FileStore/raw_data
original_dataset_pd.to_csv("/dbfs/FileStore/raw_data/naturkampen_original.csv", index = False)
