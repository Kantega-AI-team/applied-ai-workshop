# Databricks notebook source
# MAGIC %md ## Manglende data - Hva gjør vi da?
# MAGIC
# MAGIC Du er Data Scientist for bedriften *Grønnere enn Grønnest*, og har fått beskjed om å lage en maskinlæringsmodell for å predikere den økologiske tilstanden i elver og vann i norske kommuner.
# MAGIC
# MAGIC Modellen du skal bygge skal være basert på kommunestørrelse, populasjon og hyttebygging, i tillegg til en variabel du ikke helt har forstått hva er for noe, og som attpåtil mangler informasjon for noen kommuner.
# MAGIC
# MAGIC Et utdrag fra datasettet kan du se ved å kjøre kommandoen under:

# COMMAND ----------

from sklearn import linear_model
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

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
# MAGIC *Ditt svar her*

# COMMAND ----------

# MAGIC %md #### Oppgave 2: Hva tror du konsekvensene er ved taktikken du har valgt?

# COMMAND ----------

# MAGIC %md
# MAGIC **Svar**:
# MAGIC
# MAGIC *Ditt svar her*

# COMMAND ----------

# MAGIC %md Nå er det på tide å gå i gang med selve kodingen. Vi har allerede gjort oss klar til å trene en enkel maskinlæringsmodell, men først må vi altså rydde opp i dataene. Dette er din jobb!

# COMMAND ----------

pdf = df.toPandas()
pdf.drop(columns=["_c0", "unnamed_metric", "name", "county"], inplace=True)
target = "eco_river_water"
X, y = pdf[[col for col in pdf.columns if col not in [target, "name"]]], pdf[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
reg = linear_model.Ridge(alpha=0.5)
reg.fit(X_train, y_train)
plt.scatter(reg.predict(X_test), y_test)
