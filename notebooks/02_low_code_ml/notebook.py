# Databricks notebook source
from typing import List

import pandas as pd
from databricks import automl
from pyspark.sql.functions import col, regexp_replace, trim
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", False)

# COMMAND ----------


def custom_data_preparation(
    table_name: str, categorical_features: List[str], numeric_features: List[str]
):
    """
    Not strictly necassary, just
    """
    df = spark.read.table(table_name).toPandas()

    new_numerical_columns = []
    for category in categorical_features:
        original_array = df[category].unique()
        dummies = pd.get_dummies(df[category], drop_first=True)
        new_numerical_columns = new_numerical_columns + list(dummies.columns)
        df = pd.concat([df, dummies], axis=1)
        df.drop(columns=[category], inplace=True)
        base = [item for item in original_array if item not in df.columns]

    sdf = spark.createDataFrame(df)
    for category in new_numerical_columns + numeric_features:
        metadata_dict = sdf.schema[category].metadata
        metadata_dict["spark.contentAnnotation.semanticType"] = "numeric"
        sdf = sdf.withMetadata(category, metadata_dict)
    return sdf


df = custom_data_preparation(
    "naturkampen_2",
    categorical_features=["county", "mayors_party"],
    numeric_features=["area", "population"],
)

automl.regress(
    dataset=sdf,
    target_col=target,
    exclude_columns=["name"],
    primary_metric="mae",
    timeout_minutes=5,
)

# COMMAND ----------

# MAGIC %md #### Oppgave 1: Kan du gjøre en prediksjon med en av modellene?
# MAGIC Hvordan tolker du prediksjonen?

# COMMAND ----------

# MAGIC %md #### Oppgave 2: Kan du forklare modellen du brukte for prediksjon? 
# MAGIC # Hvilke inputvariabler kan forklare mest av naturkampen-plasseringen?
# MAGIC # TIPS: Se på eksperimentnotebooken
