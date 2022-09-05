# Databricks notebook source
# MAGIC %md ## Low code ML
# MAGIC 
# MAGIC *Grønnere enn Grønnest* ber deg nå vurdere om det er noe som kan forklare endelig rangering i naturkampen, baserte på generelle kriterier som folketall, areal og hvilket parti som har ordføreren i kommunen. Din oppgave er å finne ut om noen av disse variablene forklarer mye av sluttrangeringen. Du velger å bygge mange modeller, raskt - ved bruk av et low code ML-verkøy.

# COMMAND ----------

""" Vi begynner med å importere et par nyttige klasser og funksjoner, 
for så å gjøre noen enkle transformasjoner på datasettet.
Som sist - Det er ikke så farlig om du ikke forstår hva som skjer her! """ 


from typing import List

import pandas as pd
from databricks import automl
from pyspark.sql.functions import col, regexp_replace, trim
from sklearn.compose import ColumnTransformer
from pyspark.sql import DataFrame
from sklearn.preprocessing import OneHotEncoder
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", False)

def custom_data_preparation(
    table_name: str, categorical_features: List[str], numeric_features: List[str]
) -> DataFrame:
    """
    Not strictly necassary, just makes it easier to view and understand
    how categorical encoding works
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

display(df.sample(0.1))

# COMMAND ----------



# COMMAND ----------

""" Her trener du modellene """

summary = automl.regress(
    dataset=df,
    target_col="rank",
    exclude_cols=["name"],
    primary_metric="mae",
    timeout_minutes=5,
)

# COMMAND ----------

# MAGIC %md #### Oppgave 1: Kan du gjøre en prediksjon med en av modellene?
# MAGIC 
# MAGIC Hvordan tolker du prediksjonen?
# MAGIC 
# MAGIC **TIPS**: Se på eksperimentnotebooken som har laget modellen

# COMMAND ----------

# MAGIC %md #### Oppgave 2: Kan du forklare modellen du brukte for prediksjon?
# MAGIC 
# MAGIC Hvilke inputvariabler kan forklare mest av naturkampen-plasseringen?
# MAGIC 
# MAGIC **TIPS**: Se på eksperimentnotebooken
