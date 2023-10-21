import os
import numpy as np
import yaml

os.environ["KERAS_BACKEND"] = "jax"
import keras_core as keras

# load data config
DATA_DIRECTORY = "data"
config = yaml.load(open( os.path.join(DATA_DIRECTORY, "config.yaml") , "r"), Loader=yaml.Loader)

FILENAME_X = config["file_name_x"]
FILENAME_Y = config["file_name_y"]

# load data
print("Loading data")
x_train = np.load(os.path.join(DATA_DIRECTORY, FILENAME_X))
y_train = np.load(os.path.join(DATA_DIRECTORY, FILENAME_Y))

# load ai
MODEL_DIRECTORY = "model"
model = keras.models.load_model(os.path.join(MODEL_DIRECTORY, "model.keras"))

# test ai
print(y_train)
print(model.predict(x_train))