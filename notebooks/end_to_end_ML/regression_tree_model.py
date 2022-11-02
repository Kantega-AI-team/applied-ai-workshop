# Databricks notebook source
import matplotlib.pyplot as plt

import mlflow
import mlflow.sklearn
from sklearn import tree
from sklearn.tree import DecisionTreeRegressor
import numpy as np
import pyspark.pandas as ps
from sklearn import datasets
from sklearn.linear_model import ElasticNet, enet_path, lasso_path
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from pyspark.ml.feature import Bucketizer
import pyspark.sql.functions as F
import numpy
from sklearn.model_selection import GridSearchCV, train_test_split, cross_val_score, ParameterGrid
from sklearn import metrics
from sklearn import tree
from sklearn.preprocessing import OneHotEncoder
import pandas as pd

# COMMAND ----------

spark.conf.set("spark.sql.execution.arrow.enabled", "false")

# COMMAND ----------

# gold data directory
dataset_gold_path = "/FileStore/gold/data"

# COMMAND ----------

# train a regression tree each time a new dataset is available

def train_regreesion_tree(dataset_gold_path):
    
    
    # create/activate an experiemtn workspace where all the model run will be stored
    #mlflow.set_experiment("/Users/emanuele.gramuglia@kantega.no/tree_model")
    
    
    #inpput paramter
    data_version = 0 

    # load the gold data

    gold_data = spark.read.load(dataset_gold_path,format = "delta", versionAsOf = data_version)

    # split dataset in train and test set (70% train - 30% test)

    (train_df,test_df) = gold_data.randomSplit([0.7,0.3], seed=5291)

    #split featureas and outcome in both train and test - make them pandas on spark DFs

    x_train = train_df.drop(F.col("area")).toPandas()
    x_test = test_df.drop(F.col("area")).toPandas()
    y_train = train_df.select(F.col("area")).toPandas()
    y_test = test_df.select(F.col("area")).toPandas()

    x_train = pd.get_dummies(data = x_train, columns = ["county", "weather"])
    x_test = pd.get_dummies(data = x_test, columns = ["county", "weather"])
    

    #define the model
     
    tree_model = DecisionTreeRegressor(criterion = "squared_error",
                                      splitter = "best",
                                      max_depth = 4 )
    
    

    # fit the model
    tree_model_fit = tree_model.fit(x_train, y_train)
    
    # get predicted value for training set
    y_train_pred = tree_model_fit.predict(x_train) 
    
    
    # get train MSE
    train_mse = metrics.mean_squared_error(y_train,y_train_pred)
    
    
    # get predicted values for test set
    y_test_pred = tree_model_fit.predict(x_test)
    
    # get test MSE
    test_mse = metrics.mean_squared_error(y_test,y_test_pred)
        
        

# COMMAND ----------

#inpput paramter
data_version = 0 

# load the gold data

gold_data = spark.read.load(dataset_gold_path,format = "delta", versionAsOf = data_version)

# split dataset in train and test set (70% train - 30% test)

(train_df,test_df) = gold_data.randomSplit([0.7,0.3], seed=5291)

#split featureas and outcome in both train and test - make them pandas on spark DFs

x_train = train_df.drop(F.col("area")).toPandas()
x_test = test_df.drop(F.col("area")).toPandas()
y_train = train_df.select(F.col("area")).toPandas()
y_test = test_df.select(F.col("area")).toPandas()

x_train = pd.get_dummies(data = x_train, columns = ["county", "weather"])
x_test = pd.get_dummies(data = x_test, columns = ["county", "weather"])

# COMMAND ----------

tree_model = DecisionTreeRegressor(splitter = "best",
                                      max_depth = 4 )


#fit the model
tree_model_fit = tree_model.fit(x_train, y_train)

#get  train accuracy: (negative) mean squared error
train_accuracy =  metrics.mean_squared_error(x_train, y_train)

# COMMAND ----------

train_accuracy

# COMMAND ----------


