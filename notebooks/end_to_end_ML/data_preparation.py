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
import time

# COMMAND ----------

#read original dataset 
original_dataset = pd.read_csv("/dbfs/FileStore/raw_data/naturkampen_original.csv",delimiter=",", header=0)

# display data
original_dataset.display()

# COMMAND ----------

# check for null values
original_dataset[original_dataset.isna().any(axis=1)].display()

# COMMAND ----------

# the column "UNNAMED_METRIC" has 231 Null over a total of 356 rows. Delete the column
original_dataset = original_dataset.drop(["UNNAMED_METRIC"], axis = 1)

original_dataset.display()

# COMMAND ----------

# split the original dataset in 5 unique samples (each 20% of the original dataset - 71 observations)

# sample dataset_1
dataset_1 = original_dataset.sample(frac=0.2,random_state=200)

# remove dataset_1 from dataset_original 
original_dataset_left_1 = original_dataset.drop(dataset_1.index)

# sample dataset_2
dataset_2 = original_dataset_left_1.sample(frac= 71/len(original_dataset_left_1),random_state=201)

# remove dataset_2 from dataset_original_left_1
original_dataset_left_2 = original_dataset_left_1.drop(dataset_2.index)

# sample dataset_3
dataset_3 = original_dataset_left_2.sample(frac=71/len(original_dataset_left_2),random_state=202)

# remove dataset_3 from dataset_original_left_2
original_dataset_left_3 = original_dataset_left_2.drop(dataset_3.index)

# sample dataset_4
dataset_4 = original_dataset_left_3.sample(frac=71/len(original_dataset_left_3),random_state=203)

# remove dataset_4 from dataset_original_left_3
original_dataset_left_4 = original_dataset_left_3.drop(dataset_4.index)

# sample dataset_5
dataset_5 = original_dataset_left_4.sample(frac=71/len(original_dataset_left_4),random_state=204)


# COMMAND ----------

# store the generated datasets as csv files - 10 seconds btw each storing operation (needed for streaming purposes later on)

dataset_1.to_csv("/dbfs/FileStore/raw_data/dataset_1.csv", sep = ";", index = False)
time.sleep(10)

dataset_2.to_csv("/dbfs/FileStore/raw_data/dataset_2.csv", sep = ";", index = False)
time.sleep(10)

dataset_3.to_csv("/dbfs/FileStore/raw_data/dataset_3.csv", sep = ";", index = False)
time.sleep(10)

dataset_4.to_csv("/dbfs/FileStore/raw_data/dataset_4.csv", sep = ";", index = False)
time.sleep(10)

dataset_5.to_csv("/dbfs/FileStore/raw_data/dataset_5.csv", sep = ";", index = False)
time.sleep(10)
