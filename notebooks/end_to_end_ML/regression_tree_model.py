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

spark.read.load(dataset_gold_path,format = "delta").display()

# COMMAND ----------

# define function that trains, track and logs each regression tree model

def train_model(x_train, y_train, x_test, y_test, params, data_version):
    
    with mlflow.start_run(run_name = "tune_decision_tree_model_dataset_1") as run:

            #define the model

            tree_model = DecisionTreeRegressor(criterion = params["criterion"],
                                               splitter = "best",
                                               max_depth = params["max_depth"],
                                               random_state = 112)



            # fit the model
            tree_model_fit = tree_model.fit(x_train, y_train)

            # get predicted value for training set
            y_train_pred = tree_model_fit.predict(x_train) 


            # get train MSE
            train_mse = metrics.mean_absolute_error(y_train,y_train_pred)


            # get predicted values for test set
            y_test_pred = tree_model_fit.predict(x_test)

            # get test MSE
            test_mse = metrics.mean_absolute_error(y_test,y_test_pred)

            #log the model parameters

            mlflow.log_param("criterion",params["criterion"])
            mlflow.log_param("max_depth",params["max_depth"])
            mlflow.log_param("data_version",data_version)
            mlflow.log_param("n_train_obs",x_train.shape[0])


            #log model metrics 

            mlflow.log_metric("test_mae", test_mse)
            mlflow.log_metric("train_mae", train_mse)

            return [y_train_pred,
                    y_test_pred,
                    y_train,
                    y_test]


# COMMAND ----------

# train a regression tree each time a new dataset is available

def train_regreesion_tree(dataset_gold_path):
    
    
    # create/activate an experiemtn workspace where all the model run will be stored
    mlflow.set_experiment("/Users/emanuele.gramuglia@kantega.no/tree_model")
    
    # loop through all the different versions of the dataset
    
    for j in range(0,5):
    
        #inpput paramter
        data_version = j 

        # load the gold data

        gold_data = spark.read.load(dataset_gold_path,format = "delta", versionAsOf = data_version)
        
        # transform gold_data in pandas data frame

        gold_data_pd = gold_data.toPandas()

        # transform categorical variables using one-hot-encoder
        
        gold_data_pd = pd.get_dummies(data = gold_data_pd, columns = ["county", "weather"])
        
        # split dataset in train and test set (70% train - 30% test)

        (train_df,test_df) = train_test_split(gold_data_pd, test_size = 0.2, random_state = 5291 ) 
        
        #split featureas and outcome for train and test

        x_train = train_df.drop(["cabin_construction"],axis=1)
        x_test = test_df.drop(["cabin_construction"],axis=1)
        y_train = train_df.cabin_construction
        y_test = test_df.cabin_construction

        #set hyper-parameter grid

        parameters = {'max_depth': [4,6,8,10,12,14,16],
                      'criterion': ['mae','poisson','friedman_mse']}
        parameters_grid = list(ParameterGrid(parameters))
        number_of_models = len(parameters_grid)

        # loop through all the paramters combination

        for i in range(0,number_of_models):

            output = train_model(x_train, y_train, x_test, y_test, parameters_grid[i], data_version)






# COMMAND ----------

train_regreesion_tree(dataset_gold_path)

# COMMAND ----------


