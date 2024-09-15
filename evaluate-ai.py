import os
from matplotlib import pyplot as plt
import numpy as np
import yaml

os.environ["KERAS_BACKEND"] = "jax"
import keras_core as keras
from keras_core import ops

# ===== load data config =====
DATA_DIRECTORY = "data"
config = yaml.load(open( os.path.join(DATA_DIRECTORY, "config.yaml") , "r"), Loader=yaml.Loader)

FILENAME_X = config["file_name_x"]
FILENAME_Y = config["file_name_y"]

# ===== load data =====
print("Loading data")
x_train = np.load(os.path.join(DATA_DIRECTORY, FILENAME_X))
y_train = np.load(os.path.join(DATA_DIRECTORY, FILENAME_Y))
print("x_train.shape:", x_train.shape)
print("y_train.shape:", y_train.shape)

# ===== load model =====
def custom_accuracy(y_true, y_pred):
	# round y_pred and calculate proportion of correct predictions
	return ops.equal(ops.round(y_pred), y_true).mean()

print("Loading model")
model = keras.models.load_model(
	os.path.join("", "best_model.keras"), 
	custom_objects={"custom_accuracy": custom_accuracy}
)
model.summary()

print("Evaluating model")
model.evaluate(x_train, y_train, verbose=2)
print("Percent correct: ")
print(100 * ops.mean(ops.equal(ops.round(model(x_train)), y_train)))