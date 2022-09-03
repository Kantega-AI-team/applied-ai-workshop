# Databricks notebook source
# MAGIC %md ## Manglende data - Hva gjør vi da?
# MAGIC
# MAGIC Du er Data Scientist for bedriften *Grønnere enn Grønnest*, og har fått beskjed om å lage en maskinlæringsmodell for å predikere den økologiske tilstanden i elver og vann i norske kommuner.
# MAGIC
# MAGIC Modellen du skal bygge skal være basert på kommunestørrelse, populasjon og hyttebygging, i tillegg til en variabel du ikke helt har forstått hva er for noe, og som attpåtil mangler informasjon for noen kommuner.
# MAGIC
# MAGIC Et utdrag fra datasettet kan du se ved å kjøre kommandoen under:

# COMMAND ----------

import matplotlib.pyplot as plt
import pandas as pd
from numpy import absolute, mean
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import HuberRegressor
from sklearn.model_selection import KFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# COMMAND ----------

df = spark.read.table("naturkampen_e1")

# COMMAND ----------

display(df.sample(0.2))

# COMMAND ----------

# MAGIC %md #### Oppgave 1: Hvordan vil du gå frem for å håndtere disse manglende dataene?
# MAGIC Har du flere forslag er det fritt fram å kommme med alle

# COMMAND ----------

# MAGIC %md
# MAGIC **Svar**:
# MAGIC
# MAGIC *Fyll inn ditt svar her*

# COMMAND ----------

# MAGIC %md #### Oppgave 2: Hva tror du konsekvensene er ved taktikken du har valgt?

# COMMAND ----------

# MAGIC %md
# MAGIC **Svar**:
# MAGIC
# MAGIC *Fyll inn ditt svar her*

# COMMAND ----------

# MAGIC %md Nå er det på tide å gå i gang med selve kodingen. Vi har allerede gjort oss klar til å trene en enkel maskinlæringsmodell, men først må vi altså rydde opp i dataene. Dette er din jobb!

# COMMAND ----------

pdf = df.toPandas()
pdf.head()

# COMMAND ----------

# Her må du behandle den manglende verdien!
pdf.drop(columns=["_c0", "unnamed_metric", "name"], inplace=True)

# COMMAND ----------

numeric_features = ["area", "population", "eco_river_water"]
numeric_transformer = Pipeline(
    steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]
)

categorical_features = ["county"]
categorical_transformer = OneHotEncoder(handle_unknown="ignore")
preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features),
    ]
)

pipeline = Pipeline(
    steps=[("preprocessor", preprocessor), ("classifier", HuberRegressor())]
)
target = "cabin_construction"
X, y = pdf[[col for col in pdf.columns if col not in [target, "name"]]], pdf[target]
model = TransformedTargetRegressor(regressor=clf, transformer=StandardScaler())
cv = KFold(n_splits=10, shuffle=True, random_state=1)
scores = cross_val_score(
    model, X, y, scoring="neg_mean_absolute_error", cv=cv, n_jobs=-1
)
scores = absolute(scores)


# Gjennomsnittlig absoluttfeil:
s_mean = mean(scores)
print("Mean MAE: %.3f" % (s_mean))