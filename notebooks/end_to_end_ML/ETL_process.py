# Databricks notebook source
# import required modules

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
import os

# COMMAND ----------

# read the original dataset

original_dataset = spark.read.load("dbfs:/user/hive/warehouse/naturkampen_1", format = "delta")

# COMMAND ----------

# transform Spark DataFrame in Pandas
original_dataset_pd = original_dataset.toPandas()

# drop _c0 column
original_dataset_pd = original_dataset_pd.drop(["_c0"], axis = 1)

# store the pandas version of the original dataset in FileStore/raw_data
original_dataset_pd.to_csv("/dbfs/FileStore/raw_data/naturkampen_original.csv", index = False)

# COMMAND ----------

# split the original dataset in 5 unique samples

# COMMAND ----------

# split the original dataset in more datasets


# store the data as csv files with ordered tables 
