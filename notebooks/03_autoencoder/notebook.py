# Databricks notebook source
# MAGIC %md # Autoenkodere
# MAGIC
# MAGIC Dagens bonusoppgave handler om autoenkoderen. Vi jobber oss gjennom eksempelet til Magnus fra [denne bloggartikkelen](https://www.kantega.no/blogg/avanserte-maskinlaerekonsepter-autoenkoderen), og prøver til slutt å forbedre modellen som er satt opp.
# MAGIC
# MAGIC Vi begynner med litt boilerplate: Imports, hjelpefunksjoner og last av datasettet. Dette kan fint kjøres uten at man trenger å forstå alt.

# COMMAND ----------

# Skjule advarsler
import warnings

import matplotlib.pyplot as plt

# Imports
import numpy as np
import tensorflow as tf
from sklearn import datasets
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Dense, Flatten, Reshape
from tensorflow.keras.models import Sequential

warnings.filterwarnings("ignore")
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# Hjelpefunksjoner
def get_index_of_values(array: np.ndarray, values: np.ndarray):
    sorter = np.argsort(array)
    return sorter[np.searchsorted(array, values, sorter=sorter)]


def get_n_indices_of_value(array: np.ndarray, value: np.ndarray, n: int):
    return np.where(array == value)[0][0:n]


# Laste inn data
mnist = fetch_openml(name="mnist_784")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Inspisere datasettet

# COMMAND ----------

images = mnist.data.values.reshape((mnist.data.shape[0], 28, 28))
labels = np.array(mnist.target.values)

# Vi ser på et utvalg
image_subset = images[0:4]
label_subset = np.array(mnist.target.iloc[0:4].values)

_, axes = plt.subplots(nrows=1, ncols=4, figsize=(10, 3))
for ax, image, label in zip(axes, image_subset, label_subset):
    ax.set_axis_off()
    ax.imshow(image, cmap=plt.cm.gray)
    ax.set_title("Training: " + label)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Klargjøre datasettet for trening

# COMMAND ----------

# Vi splitter i trenings- og testsett, og skalerer inputverdiene til å være mellom 0 og 1
X_train, X_test, y_train, y_test = train_test_split(
    images, labels, test_size=0.2, shuffle=True
)

# Høyeste pikselverdi er 255
X_train = X_train / 255.0
X_test = X_test / 255.0

# COMMAND ----------

# MAGIC %md
# MAGIC ## Designe autoenkoderen
# MAGIC
# MAGIC Autoenkoderen vi skal sette opp ser slik ut
# MAGIC
# MAGIC
# MAGIC
# MAGIC ![arkitektur](https://cdn.sanity.io/images/syubz90f/kantegano-prod/9df82f22cfa79167a0a74d3b94c0c199f0d2cf6e-800x448.png?w=1200)

# COMMAND ----------

# MAGIC %md Sette opp enkoderen

# COMMAND ----------

encoder = Sequential(name="Encoder")

encoder.add(Flatten(input_shape=(28, 28)))
encoder.add(Dense(784, activation="relu"))
encoder.add(Dense(392, activation="relu"))
encoder.add(Dense(10, activation="relu"))

# COMMAND ----------

# MAGIC %md Sette opp dekoderen

# COMMAND ----------

decoder = Sequential(name="Decoder")

decoder.add(Dense(392, activation="relu"))
decoder.add(Dense(784, activation="sigmoid"))
decoder.add(Reshape((28, 28)))

# COMMAND ----------

# MAGIC %md Kombinere for å sette opp hele autoenkoderen

# COMMAND ----------

autoencoder = Sequential([encoder, decoder], name="Autoencoder")

# COMMAND ----------

# MAGIC %md ## Kompilere og trene modellen

# COMMAND ----------

# Kompilering
autoencoder.compile(loss="mean_squared_error", optimizer="adam")

# COMMAND ----------

history = autoencoder.fit(
    X_train, X_train, batch_size=512, epochs=100, verbose=0  # Samples  # Labels
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Inspisere resultater

# COMMAND ----------

# MAGIC %md Hente 10 eksempler fra testsettet, en for hvert siffer

# COMMAND ----------

# Create list of all numbers between 0 -> 10
all_numbers = [str(i) for i in list(range(0, 10))]

# Get the index of one image for each value between 0 -> 10
index_of_numbers = get_index_of_values(y_test, all_numbers)

# Get 10 images, one for each number
test_images = X_test[index_of_numbers]

# COMMAND ----------

# MAGIC %md Bruke autoenkoderen på disse 10 bildene

# COMMAND ----------

preds = autoencoder.predict(test_images)

# COMMAND ----------

# MAGIC %md Visualisere orginalbildene

# COMMAND ----------

_, axes = plt.subplots(nrows=1, ncols=10, figsize=(10, 3))
for ax, image in zip(axes, test_images):
    ax.set_axis_off()
    ax.imshow(image, cmap=plt.cm.gray)

# COMMAND ----------

# MAGIC %md Visualisere kopiene laget av autoenkoderen

# COMMAND ----------

_, axes = plt.subplots(nrows=1, ncols=10, figsize=(10, 3))
for ax, image in zip(axes, preds):
    ax.set_axis_off()
    ax.imshow(image, cmap=plt.cm.gray)

# COMMAND ----------

# MAGIC %md Ser dette bra ut?

# COMMAND ----------

# MAGIC %md
# MAGIC ## Oppgaver

# COMMAND ----------

# MAGIC %md Oppgave 1: Hvordan kan vi vurdere autoenkoderens performance?

# COMMAND ----------

# MAGIC %md
# MAGIC Oppgave 2: Kan du lage en modell som yter bedre enn modellen vi har trent?
# MAGIC >Tips: Se på [bloggartikkelen](https://www.kantega.no/blogg/avanserte-maskinlaerekonsepter-autoenkoderen) igjen
