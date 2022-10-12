# Databricks notebook source
# Hide warnings
import warnings

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from sklearn import datasets
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Dense, Flatten, Reshape
from tensorflow.keras.models import Sequential

warnings.filterwarnings("ignore")
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# COMMAND ----------

# MAGIC %md
# MAGIC ### Helper Functions

# COMMAND ----------


def get_index_of_values(array, values):
    sorter = np.argsort(array)
    return sorter[np.searchsorted(array, values, sorter=sorter)]


def get_n_indices_of_value(array, value, n):
    return np.where(array == value)[0][0:n]


# COMMAND ----------

# MAGIC %md
# MAGIC ## Load mnist dataset from sklearn

# COMMAND ----------

from sklearn.datasets import fetch_openml

mnist = fetch_openml(name="mnist_784")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Reshape images to proper 28x28 format

# COMMAND ----------

nr_images = len(mnist.data.values)
all_images = mnist.data.values.reshape((nr_images, 28, 28))
all_labels = np.array(mnist.target.values)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Visualize digits from the dataset

# COMMAND ----------

images = all_images[0:4]
labels = np.array(mnist.target.iloc[0:4].values)

# COMMAND ----------

_, axes = plt.subplots(nrows=1, ncols=4, figsize=(10, 3))
for ax, image, label in zip(axes, images, labels):
    ax.set_axis_off()
    ax.imshow(image, cmap=plt.cm.gray)
    ax.set_title("Training: " + label)

# COMMAND ----------

# MAGIC %md
# MAGIC # Prepare Datasets

# COMMAND ----------

# MAGIC %md
# MAGIC ### Split data into training and tests sets, also scale input values to a value between 0 and 1

# COMMAND ----------

X_train, X_test, y_train, y_test = train_test_split(
    all_images, all_labels, test_size=0.2, shuffle=True
)

# highest value of any pixel is 255.0
X_train = X_train / 255.0
X_test = X_test / 255.0

# COMMAND ----------

# MAGIC %md
# MAGIC # Create Autoencoder

# COMMAND ----------

# MAGIC %md
# MAGIC ### Create the Encoder

# COMMAND ----------

encoder = Sequential(name="Encoder")

encoder.add(Flatten(input_shape=(28, 28)))
encoder.add(Dense(784, activation="relu"))
encoder.add(Dense(392, activation="relu"))
encoder.add(Dense(10, activation="relu"))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Create the Decoder

# COMMAND ----------

decoder = Sequential(name="Decoder")

decoder.add(Dense(392, activation="relu"))
decoder.add(Dense(784, activation="sigmoid"))
decoder.add(Reshape((28, 28)))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Combine the encoder and decoder

# COMMAND ----------

autoencoder = Sequential([encoder, decoder], name="Autoencoder")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Compile the model

# COMMAND ----------

autoencoder.compile(loss="mean_squared_error", optimizer="adam")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Train the model

# COMMAND ----------

history = autoencoder.fit(
    X_train, X_train, batch_size=512, epochs=100, verbose=0  # Samples  # Labels
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Visualize our results

# COMMAND ----------

# MAGIC %md
# MAGIC ### Fetch 10 images from the test set, one for each number

# COMMAND ----------

# Create list of all numbers between 0 -> 10
all_numbers = [str(i) for i in list(range(0, 10))]

# Get the index of one image for each value between 0 -> 10
index_of_numbers = get_index_of_values(y_test, all_numbers)

# Get 10 images, one for each number
test_images = X_test[index_of_numbers]

# COMMAND ----------

# MAGIC %md
# MAGIC ### Use the autoencoder on the 10 images

# COMMAND ----------

preds = autoencoder.predict(test_images)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Visualize the original images

# COMMAND ----------

_, axes = plt.subplots(nrows=1, ncols=10, figsize=(10, 3))
for ax, image in zip(axes, test_images):
    ax.set_axis_off()
    ax.imshow(image, cmap=plt.cm.gray)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Visualize the copies made by the autoencoder

# COMMAND ----------

_, axes = plt.subplots(nrows=1, ncols=10, figsize=(10, 3))
for ax, image in zip(axes, preds):
    ax.set_axis_off()
    ax.imshow(image, cmap=plt.cm.gray)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Visualize the internal representation of the numbers

# COMMAND ----------

# MAGIC %md
# MAGIC ### Extract encoder from autoencoder

# COMMAND ----------

encoder = autoencoder.layers[0]

# COMMAND ----------

# MAGIC %md
# MAGIC ### Get latent representations from test images

# COMMAND ----------

latent_representations = encoder.predict(test_images)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Reshape and visualize latent representations

# COMMAND ----------

latent_images = latent_representations.reshape((10, 5, 2))

_, axes = plt.subplots(nrows=1, ncols=10, figsize=(10, 3))
for ax, image in zip(axes, latent_images):
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    ax.imshow(image, cmap=plt.cm.gray)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Visualize internal rep. of the same number

# COMMAND ----------

# Get index of 4 images containing the number 4
indices = get_n_indices_of_value(y_test, "4", 10)

# COMMAND ----------

number_4_images = X_test[indices]

# COMMAND ----------

_, axes = plt.subplots(nrows=1, ncols=10, figsize=(10, 3))
for ax, image in zip(axes, number_4_images):
    ax.set_axis_off()
    ax.imshow(image, cmap=plt.cm.gray)

# COMMAND ----------

number_4_preds = autoencoder.predict(number_4_images)

# COMMAND ----------

_, axes = plt.subplots(nrows=1, ncols=10, figsize=(10, 3))
for ax, image in zip(axes, number_4_preds):
    ax.set_axis_off()
    ax.imshow(image, cmap=plt.cm.gray)

# COMMAND ----------

number_4_latent = encoder.predict(number_4_images)

# COMMAND ----------

latent_4_images = number_4_latent.reshape((10, 5, 2))

_, axes = plt.subplots(nrows=1, ncols=10, figsize=(10, 3))
for ax, image in zip(axes, latent_images):
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    ax.imshow(image, cmap=plt.cm.gray)
