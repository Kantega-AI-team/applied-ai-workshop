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

#read original dataset 
original_dataset = pd.read_csv("/dbfs/FileStore/raw_data/naturkampen_original.csv",delimiter=",", header=0)


# COMMAND ----------

# split the original dataset in 5 unique samples

# COMMAND ----------

# split the original dataset in more datasets


# store the data as csv files with ordered tables 
