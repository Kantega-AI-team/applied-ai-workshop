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
import numpy as np
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

# two towns are called "Våler", call one of them Våler_v
original_dataset.loc[(original_dataset["NAME"] == "Våler") &  (original_dataset["COUNTY"] == "VIKEN"), "NAME" ] = "Våler_v"

# two towns are called "Herøy", call one of them Herøy_n
original_dataset.loc[(original_dataset["NAME"] == "Herøy") &  (original_dataset["COUNTY"] == "NORDLAND"), "NAME" ] = "Herøy_n"

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

# COMMAND ----------

## generate another table with a correlated column with "CABIN_CONSTRUCTION "

# select "NAME" and "CABIN_CONSTRUCTION"

external_dataset = original_dataset[["NAME", "CABIN_CONSTRUCTION"]]

external_dataset.display()

# COMMAND ----------

# generate a new featues "temperature" highly correlated with the with "CABIN_CONSTRUCTION" and add it to the dataset  "external_dataset"

def fun_ex(x):
    y = -1 + 0.0015 * x  +  np.random.normal(0,1,1)[0]
    
    return y


out = pd.Series(map(fun_ex,external_dataset.CABIN_CONSTRUCTION))

external_dataset = external_dataset.assign(temp = round(out,2)) 

# COMMAND ----------

# split the external_dataset in 5 datasets having each the same towns as in the naturkampen datasets

#external_dataset_1
external_dataset_1 = pd.merge(external_dataset, dataset_1.NAME, on = "NAME", how = "right" )

#external_dataset_2
external_dataset_2 = pd.merge(external_dataset, dataset_2.NAME, on = "NAME", how = "right" )

#external_dataset_3
external_dataset_3 = pd.merge(external_dataset, dataset_3.NAME, on = "NAME", how = "right" )

#external_dataset_4
external_dataset_4 = pd.merge(external_dataset, dataset_4.NAME, on = "NAME", how = "right" )

#external_dataset_5
external_dataset_5 = pd.merge(external_dataset, dataset_5.NAME, on = "NAME", how = "right" )

# COMMAND ----------

external_dataset_5.display()

# COMMAND ----------

# store the 5 externa_datasets

external_dataset_1.to_csv("/dbfs/FileStore/raw_data/external_dataset_1.csv", sep = ";", index = False)
time.sleep(10)

external_dataset_2.to_csv("/dbfs/FileStore/raw_data/external_dataset_2.csv", sep = ";", index = False)
time.sleep(10)

external_dataset_3.to_csv("/dbfs/FileStore/raw_data/external_dataset_3.csv", sep = ";", index = False)
time.sleep(10)

external_dataset_4.to_csv("/dbfs/FileStore/raw_data/external_dataset_4.csv", sep = ";", index = False)
time.sleep(10)

external_dataset_5.to_csv("/dbfs/FileStore/raw_data/external_dataset_5.csv", sep = ";", index = False)
time.sleep(10)
