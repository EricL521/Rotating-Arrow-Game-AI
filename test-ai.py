import os
import numpy as np
import yaml

os.environ["KERAS_BACKEND"] = "jax"
import keras_core as keras
from keras_core import ops

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
def custom_accuracy(y_true, y_pred):
	# round y_pred and calculate proportion of correct predictions
	return ops.equal(ops.round(y_pred), y_true).mean()
model = keras.models.load_model(os.path.join(MODEL_DIRECTORY, "model.keras"), custom_objects={"custom_accuracy": custom_accuracy})

# test ai
y_pred = model.predict(x_train)
# round y_pred and calculate proportion of correct predictions
accuracy = ops.equal(ops.round(y_pred), y_train).mean()
print("Accuracy: ", accuracy)
